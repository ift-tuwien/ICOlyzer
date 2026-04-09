"""Split HDF5 measurement files into parts"""

# -- Imports ------------------------------------------------------------------

from argparse import ArgumentParser, Namespace
from datetime import timedelta
from logging import basicConfig, getLogger
from math import ceil
from os import sep
from pathlib import Path
from platform import system
from sys import exit as sys_exit, stderr
from tempfile import TemporaryDirectory

from pandas import read_hdf
from tables import HDF5ExtError, open_file, Table

from icolyzer.cli import file_exists, measurement_time

# -- Functions ----------------------------------------------------------------


def get_arguments() -> Namespace:
    """Parse command line arguments

    Returns:

        An object that contains the given command line arguments

    """

    parser = ArgumentParser(description="Split a HDF5 file into two parts")
    parser.add_argument(
        "filepath",
        type=file_exists,
        help="measurement data in HDF5 format",
    )

    parser.add_argument(
        "-l",
        "--log",
        choices=("debug", "info", "warning", "error", "critical"),
        default="warning",
        required=False,
        help="minimum log level",
    )

    parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        default=False,
        help="overwrite output files",
    )

    parser.add_argument(
        "-t",
        "--time",
        type=measurement_time,
        required=True,
        help=(
            "the maximum timestamp in seconds that should still be part of "
            "the first HDF5 file"
        ),
    )

    return parser.parse_args()


def get_maximum_filename_length(directory: Path) -> int:
    """Determine the maximum filename length for a given directory

    Args:

        directory:

            The filepath of the directory where the maximum filename length
            should be determined

    Returns:

        The maximum filename length for a new file in the given directory

    """

    if system() != "Windows":
        # pylint: disable=import-outside-toplevel, no-name-in-module

        from os import pathconf  # type: ignore[attr-defined]

        # pylint: enable=import-outside-toplevel, no-name-in-module

        return pathconf(directory, "PC_NAME_MAX")

    # https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation
    max_path_length_windows = 260
    return max_path_length_windows - len(str(directory) + sep)


def exit_error(message: str) -> None:
    """Exit program with the given error message"""

    print(message, file=stderr)

    sys_exit(1)


def search_first_row_larger_timestamp(
    data: Table, cut_microseconds: int
) -> int:
    """Search a table containing acceleration data for a cutoff index

    Args:

        data:

            A table containing acceleration data

        cut_microseconds:

            The maximum timestamp value that should still be contained in the
            data specified by the index returned by this function

    Returns:

        The first row index in ``data`` that contains a timestamp that is
        larger than ``cut_microseconds``

    """

    logger = getLogger(__file__)
    logger.debug("Cutoff point in us: %s", cut_microseconds)

    # Use binary search to get the approximate location of the cutoff point
    start = 0
    end = len(data) - 1
    while start != end:
        middle = start + ceil((end - start) / 2)
        if data[middle]["timestamp"] > cut_microseconds:
            end = middle - 1
        else:
            start = middle

    # - If we found the next lowest or exact timestamp we only need to
    #   search timestamps after the current one
    # - If we found the next highest timestamp, we need to check the
    #   timestamp before the current one
    first_row_larger_timestamp = max(0, start - 1)
    while data[first_row_larger_timestamp]["timestamp"] <= cut_microseconds:
        first_row_larger_timestamp += 1
    return first_row_larger_timestamp


def copy_first_part(
    original: Path, modified: Path, overwrite: bool, cutoff: timedelta
) -> int:
    """Copy a file and remove measurement data after a certain cutoff point

    Args:

        original:

            Path to the original HDF file

        modified:

            Path to the file that should not contain data after the cutoff
            point

        overwrite:

            Specifies if the file at ``modified`` should be overwritten, if
            it already exists

        cutoff:

            The duration after which measurement data should be removed

    Returns:

        The index of the first row that is not part of the modified
        measurement data

    """

    with TemporaryDirectory() as temporary_directory:
        temporary_filepath = Path(temporary_directory) / "temp.hdf5"
        with open_file(original, mode="r") as opened_file:
            opened_file.copy_file(temporary_filepath)

        with open_file(temporary_filepath, mode="r+") as temporary_copy:
            data = temporary_copy.get_node("/acceleration")
            cut_microseconds = cutoff.total_seconds() * 1_000_000
            first_row_to_remove = search_first_row_larger_timestamp(
                data, int(cut_microseconds)
            )
            data.remove_rows(first_row_to_remove)

        # Removing rows from the table does not make the file smaller
        # This is why we copy a temporary file again to make the resulting
        # file smaller
        with open_file(temporary_filepath, mode="r") as temporary_copy:
            temporary_copy.copy_file(modified, overwrite=overwrite)

        return first_row_to_remove


def copy_second_part(
    original: Path, modified: Path, overwrite: bool, first_row: int
) -> None:
    """Copy a file and remove measurement data before a certain cutoff point

    Args:

        original:

            Path to the original HDF file

        modified:

            Path to the file that should not contain data after the cutoff
            point

        overwrite:

            Specifies if the file at ``modified`` should be overwritten, if
            it already exists

        first_row:

            The index of the first row that should be included in the
            modified measurement data

    """

    with TemporaryDirectory() as temporary_directory:
        temporary_filepath = Path(temporary_directory) / "temp.hdf5"
        with open_file(original, mode="r") as opened_file:
            opened_file.copy_file(temporary_filepath)

        with open_file(temporary_filepath, mode="r+") as temporary_copy:
            data = temporary_copy.get_node("/acceleration")
            data.remove_rows(start=0, stop=first_row)

        # Removing rows from the table does not make the file smaller
        # This is why we copy a temporary file again to make the resulting
        # file smaller
        with open_file(temporary_filepath, mode="r") as temporary_copy:
            temporary_copy.copy_file(modified, overwrite=overwrite)


def main() -> None:
    """Split a HDF5 measurement file into two parts"""

    args = get_arguments()

    basicConfig(
        level=args.log.upper(),
        style="{",
        format="{asctime} {levelname:7} {message}",
    )
    logger = getLogger(__name__)
    logger.info("CLI arguments %s", args)

    filepath = Path(args.filepath)
    data = read_hdf(filepath, key="acceleration")

    measurement_timedelta = timedelta(
        microseconds=int(data.timestamp.iloc[-1])
    )
    cut_timedelta = timedelta(seconds=args.time)
    if cut_timedelta >= measurement_timedelta:
        exit_error(
            f"Time to cut of “{cut_timedelta}” is equal or larger than "
            f"measurement time of “{measurement_timedelta}”",
        )

    max_filename_length = get_maximum_filename_length(filepath.parent)

    basename = filepath.stem[0 : max_filename_length - len("-part-_")]
    first_part_filepath = filepath.with_stem(f"{basename}-part-1")
    second_part_filepath = filepath.with_stem(f"{basename}-part-2")

    try:
        with open_file(filepath, mode="r") as original:
            original.copy_file(second_part_filepath, overwrite=args.overwrite)

        first_row_removed = copy_first_part(
            original=filepath,
            modified=first_part_filepath,
            overwrite=args.overwrite,
            cutoff=cut_timedelta,
        )
        print(
            f"Stored first part of HDF data ({timedelta(seconds=0)} – "
            f"{cut_timedelta}) in “{first_part_filepath}”"
        )
        copy_second_part(
            original=filepath,
            modified=second_part_filepath,
            overwrite=args.overwrite,
            first_row=first_row_removed,
        )
        print(
            f"Stored second part of HDF data ({cut_timedelta} – "
            f"{measurement_timedelta}) in “{second_part_filepath}”"
        )
    except (HDF5ExtError, OSError) as error:
        exit_error(f"Unable to cut HDF5 file: {error}")


# -- Main ---------------------------------------------------------------------

if __name__ == "__main__":
    main()
