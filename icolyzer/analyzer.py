"""
Created on Fri Mar 27 08:16:22 2020

@author: Clemens
"""

import argparse
from pathlib import Path
from sys import stderr

import pandas as pd
from rich import print as rprint
from tables import open_file


def get_arguments():
    """
    Returns the given Function Parameters off the script-call

    @return Returns the parameters
    """

    parser = argparse.ArgumentParser(
        description=(
            "Calculate packet loss, values outside of given range, and "
            "runtime for HDF5 input files"
        )
    )
    parser.add_argument(
        "-m",
        "--min",
        default=-1,
        type=float,
        help="minimum value for data range (default: -1)",
    )
    parser.add_argument(
        "-v",
        "--max",
        default=1,
        type=float,
        help="maximum value for data range (default: 1)",
    )
    parser.add_argument(
        "inputs",
        default=["log.hdf5"],
        nargs="*",
        help="measurement data in HDF5 format (default: log.hdf5)",
    )

    parser.add_argument(
        "-d",
        "--details",
        action="store_true",
        help="Show additional information about paket loss (default: false)",
    )

    parser.add_argument(
        "-s",
        "--sigma",
        action="store_true",
        help="Get average value and σ² of the measurement (default: false)",
    )
    args = parser.parse_args()

    return args.inputs, args.min, args.max, args.details, args.sigma


def print_error(text: str) -> None:
    """Print warning/error messages

    The text will be printed in bold red to the standard error output

    Arguments
    ---------

    text:
        The text that should be printed

    """

    rprint("[bold red]" + text + "[/bold red]", file=stderr)


# pylint: disable=too-many-locals, too-many-branches, too-many-statements


def main():
    """
    Main function of the ICOanalyzer.
    """

    filepaths, test_value_min, test_value_max, details_on, so = get_arguments()

    for filepath in filepaths:
        # Flush standard output to keep order with standard error output.
        # This means that the output about the current file and the warnings
        # about missing measurement data should be in the correct order. This
        # is helpful if we analyze multiple files at once (e.g. using
        # `find … -exec`)
        rprint(f"Input: {filepath}", flush=True)
        if not Path(filepath).exists():
            rprint(f"Skipping non-existent file “{filepath}”", file=stderr)
            continue

        data = pd.read_hdf(filepath, key="acceleration")

        last_counter = data["counter"][0]
        last_timestamp = data["timestamp"][0]
        packet_loss = 0
        packets = 0
        losses = 0
        for counter, timestamp in zip(data["counter"], data["timestamp"]):
            if counter == last_counter:
                continue  # Skip rows with same counter/timestamp value

            lost_packets = (int(counter) - int(last_counter)) % 256 - 1
            duration_last_packet_ms = (timestamp - last_timestamp) / 1000
            loss_timestamp_s = last_timestamp / 1_000_000

            if duration_last_packet_ms > 1000:
                duration_last_packet_s = duration_last_packet_ms / 1000
                print_error(
                    "No measurement data for "
                    f"{duration_last_packet_s:.3f} seconds after "
                    f"{loss_timestamp_s} seconds"
                )

            if lost_packets != 0 and details_on is True:
                losses += 1
                message = (
                    f"{lost_packets:3} Packets lost after "
                    f"{loss_timestamp_s:6.3f} seconds"
                )
                if duration_last_packet_ms > 0:
                    message += (
                        " - No values for "
                        f"{duration_last_packet_ms:3.1f} milliseconds"
                    )
                rprint(message)

            packet_loss += lost_packets
            packets += lost_packets + 1

            if timestamp < last_timestamp:
                print_error(
                    f"Latest data at {timestamp / 1_000_000:.6f} seconds is "
                    "older than data before at "
                    f"{last_timestamp / 1_000_000:.6f} seconds"
                )

            last_timestamp = timestamp
            last_counter = counter

        out_of_range = {"x": 0, "y": 0, "z": 0}
        if so is True:
            offset = {"x": 0, "y": 0, "z": 0}
            sigma = {"x": 0, "y": 0, "z": 0}
        for axis in "xyz":
            acceleration_values = data.get(axis)
            if acceleration_values is None:
                continue
            if so is True:
                data_sum = sum(acceleration_values)
                offset[axis] = data_sum / len(acceleration_values)
            for datapoint in acceleration_values:
                if datapoint > test_value_max or datapoint < test_value_min:
                    out_of_range[axis] += 1
                if so is True:
                    sigma[axis] += (datapoint - offset[axis]) ** 2
            if so is True:
                sigma[axis] = sigma[axis] / len(acceleration_values)

        if details_on is True:
            if losses != 0:
                losses = round((packet_loss / losses), 2)
            print(f"Average Packets Lost: {losses} Packets")
        packet_loss = round((packet_loss / packets) * 100, 2)
        rprint(f"Packet Loss: {packet_loss}%")

        rprint("Data Points:")
        for axis in "xyz":
            acceleration_values = data.get(axis)
            if acceleration_values is None:
                continue

            percent_overflow = round(
                (out_of_range[axis] / len(acceleration_values)) * 100, 2
            )
            indent = " " * 2
            rprint(
                f"{indent}{axis.upper()}-Axis: {len(data.get(axis))} Samples "
                f"- {out_of_range[axis]} Samples were over {test_value_max}g "
                f"or below {test_value_min}g ({percent_overflow}%)"
            )
            if so is True:
                rprint(
                    "The average value of the "
                    + axis
                    + " axis was: "
                    + str((round(offset[axis], 2)))
                    + "g"
                )
                rprint(
                    "The standard deviation(σ²) of the "
                    + axis
                    + " axis was: "
                    + str((round(sigma[axis], 7)))
                )

        with open_file(filepath, mode="r") as file:
            start_time = file.get_node("/acceleration").attrs["Start_Time"]

        rprint(f"Measurement Date: {start_time}")

        if len(data["timestamp"]) >= 2:
            runtime = data["timestamp"].iloc[-1] / 1_000_000
            rprint(f"Runtime: {runtime:.3f} seconds")


# pylint: enable=too-many-locals, too-many-branches, too-many-statements


if __name__ == "__main__":
    main()
