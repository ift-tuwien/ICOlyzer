"""Utility code for working with command line data"""

# -- Imports ------------------------------------------------------------------

from argparse import ArgumentTypeError
from pathlib import Path

# -- Functions ----------------------------------------------------------------


def file_exists(filepath: str) -> str:
    """Check if the given path points to an existing file

    Parameters
    ----------

    filepath:
        Path to the file

    Raises
    ------

    An argument type error in case the the filepath does not point to an
    existing file

    Returns
    -------

    The given filepath on success

    """

    if not Path(filepath).exists():
        raise ArgumentTypeError(f"“{filepath}” does not exist")

    if not Path(filepath).is_file():
        raise ArgumentTypeError(f"“{filepath}” does not point to a file")

    return filepath


def measurement_time(value: str) -> float:
    """Check if the given number is valid measurement time

    Returns:

        A float value representing the measurement time on success

    Raises:

        ArgumentTypeError:

             If the given text is not a valid measurement time value

    Examples:

        Parse correct measurement times


        >>> measurement_time("0.1")
        0.1

        >>> measurement_time("12.34")
        12.34

        0 is not a valid measurement time

        >>> measurement_time("0")
        Traceback (most recent call last):
           ...
        argparse.ArgumentTypeError: “0” is not a valid measurement time

        A measurement time has to be positive

        >>> measurement_time("-1")
        Traceback (most recent call last):
           ...
        argparse.ArgumentTypeError: “-1” is not a valid measurement time

        A measurement time has to be a number

        >>> measurement_time("something")
        Traceback (most recent call last):
           ...
        argparse.ArgumentTypeError: “something” is not a valid measurement time

    """

    try:
        number = float(value)
        if number <= 0:
            raise ValueError()
        return number
    except ValueError as error:
        raise ArgumentTypeError(
            f"“{value}” is not a valid measurement time"
        ) from error
