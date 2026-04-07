"""Split HDF5 measurement files into parts"""

# -- Imports ------------------------------------------------------------------

from argparse import ArgumentParser, Namespace
from datetime import timedelta
from logging import basicConfig, getLogger
from os import sep
from pathlib import Path
from platform import system
from sys import exit as sys_exit, stderr

from pandas import read_hdf
from tables import HDF5ExtError, open_file

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


def remove_second_part(filepath: Path, cutoff: timedelta) -> int:
    """Remove measurement data after a certain cutoff point

    Args:

        filepath:

            Path to the HDF file that should be cut

        cutoff:

            The duration after which measurement data should be removed

    Returns:

        The index of the first row that is not part of the modified
        measurement data

    """

    first_row_to_remove = 0

    with open_file(filepath, mode="r+") as copy:
        data = copy.get_node("/acceleration")
        cut_microseconds = cutoff.total_seconds() * 1_000_000
        # It might make more sense to use a faster algorithm (e.g. something
        # like binary search) for determining the cut-off.
        for row in data.iterrows():
            if row["timestamp"] > cut_microseconds:
                break
            first_row_to_remove += 1

        data.remove_rows(first_row_to_remove)

    return first_row_to_remove


def remove_first_part(filepath: Path, first_row: int) -> None:
    """Remove measurement before a certain cutoff point

    Args:

        filepath:

            Path to the HDF file that should be cut

        first_row:

            The index of the first row that should be included in the
            measurement data

    """

    with open_file(filepath, mode="r+") as copy:
        data = copy.get_node("/acceleration")

        data.remove_rows(start=0, stop=first_row)


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
            original.copy_file(first_part_filepath, overwrite=args.overwrite)
            original.copy_file(second_part_filepath, overwrite=args.overwrite)

        first_row_removed = remove_second_part(
            first_part_filepath, cut_timedelta
        )
        print(
            f"Stored first part of HDF data ({timedelta(seconds=0)} – "
            f"{cut_timedelta}) in “{first_part_filepath}”"
        )
        remove_first_part(second_part_filepath, first_row_removed)
        print(
            f"Stored second part of HDF data ({cut_timedelta} – "
            f"{measurement_timedelta}) in “{second_part_filepath}”"
        )
    except (HDF5ExtError, OSError) as error:
        exit_error(f"Unable to cut HDF5 file: {error}")


# -- Main ---------------------------------------------------------------------

if __name__ == "__main__":
    main()
