"""Split HDF5 measurement files into parts"""

# -- Imports ------------------------------------------------------------------

from argparse import ArgumentParser, Namespace
from datetime import timedelta
from logging import basicConfig, getLogger
from pathlib import Path
from sys import exit as sys_exit, stderr

from pandas import read_hdf
from tables import open_file

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

        The index of the last row of the modified measurement data

    """

    last_row_to_include = 0

    with open_file(filepath, mode="r+") as copy:
        data = copy.get_node("/acceleration")
        cut_microseconds = cutoff.total_seconds() * 1_000_000
        # It might make more sense to use a faster algorithm (e.g. something
        # like binary search) for determining the cut-off.
        for row in data.iterrows():
            if row["timestamp"] > cut_microseconds:
                break
            last_row_to_include += 1

        data.remove_rows(last_row_to_include)
        print(
            f"Stored first part of HDF data ({timedelta(seconds=0)} – "
            f"{cutoff}) in “{filepath}”"
        )

    return last_row_to_include


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

    first_part_filepath = filepath.with_stem(f"{filepath.stem}-part-1")

    with open_file(filepath, mode="r") as original:
        original.copy_file(first_part_filepath, overwrite=args.overwrite)

    remove_second_part(first_part_filepath, cut_timedelta)


# -- Main ---------------------------------------------------------------------

if __name__ == "__main__":
    main()
