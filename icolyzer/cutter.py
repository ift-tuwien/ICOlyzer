"""Split HDF5 measurement files into parts"""

# -- Imports ------------------------------------------------------------------

from argparse import ArgumentParser, Namespace
from pathlib import Path
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
        help=(
            "the maximum timestamp in seconds that should still be part of "
            "the first HDF5 file"
        ),
    )

    return parser.parse_args()


def main() -> None:
    """Split a HDF5 measurement file into two parts"""

    args = get_arguments()

    filepath = Path(args.filepath)
    read_hdf(filepath, key="acceleration")


# -- Main ---------------------------------------------------------------------

if __name__ == "__main__":
    main()
