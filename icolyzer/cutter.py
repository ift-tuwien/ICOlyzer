"""Split HDF5 measurement files into parts"""

# -- Imports ------------------------------------------------------------------

from argparse import ArgumentParser, Namespace
from datetime import timedelta
from pathlib import Path
from sys import exit as sys_exit, stderr

from pandas import read_hdf

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


def main() -> None:
    """Split a HDF5 measurement file into two parts"""

    args = get_arguments()

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


# -- Main ---------------------------------------------------------------------

if __name__ == "__main__":
    main()
