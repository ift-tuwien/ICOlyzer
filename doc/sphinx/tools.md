# Tools

(tools:section:icoanalyzer)=

## ICOanalyzer

- Measures packet-loss of the recorded signal
- Print number of sample points/channel
- Measures how many datapoints are outside of a given minimum and maximum value
- Prints warnings about long durations (more than 1 second) between consecutive timestamps

### Usage

The ICOanalyzer script looks for the file `log.hdf5` in the current working directory (usually this will be the root of this repository) by default. After you use the command:

```sh
icoanalyzer
```

the script will run and analyze `log.hdf5`. The script will then list the packet loss and values outside of the given range (default is -1g and 1g):

```
Input: log.hdf5
Packet Loss: 0.61%
Data Points:
  X-Axis: 282021 Samples - 127772 Samples were over 1g or below -1g (45.31%)
Measurement Date: 2021-12-20T11:00:21.489537
Runtime: 29.996 seconds
```

If you want to change the file the script analyzes or the minimum and maximum values you have to provide some extra parameters. Using multiple parameters is also possible.

#### Parameters

##### `-h`, `--help`

This argument calls the help menu of the script instead of running the script.

##### Filepath

With the `input` positional parameter:

```sh
icoanalyzer examples/log-xz.hdf5
```

you can change the file the script analyzes:

```
Input: examples/log-xz.hdf5
Packet Loss: 24.67%
Data Points:
  X-Axis: 106992 Samples - 106992 Samples were over 1g or below -1g (100.0%)
  Z-Axis: 106992 Samples - 106992 Samples were over 1g or below -1g (100.0%)
Measurement Date: 2022-01-03T07:52:29.573573
Runtime: 29.993 seconds
```

The tool also supports multiple input files. For example, if you want to analyze all `.hdf5` files in the current directory, then you can use the following command:

```sh
icoanalyzer *.hdf5
```

##### `-d`, `--details`

With `-d`:

```sh
icoanalyzer -d
```

you can activate a more detailed information about the packet loss:

```
Input: log.hdf5
 64 Packets lost after  2.979 seconds - No values for 0.3 milliseconds
 64 Packets lost after  3.274 seconds - No values for 0.3 milliseconds
 64 Packets lost after  7.089 seconds - No values for 0.3 milliseconds
 64 Packets lost after 11.192 seconds - No values for 0.3 milliseconds
 64 Packets lost after 16.931 seconds - No values for 0.3 milliseconds
 64 Packets lost after 22.149 seconds - No values for 0.3 milliseconds
 64 Packets lost after 22.782 seconds - No values for 0.2 milliseconds
 64 Packets lost after 25.781 seconds - No values for 0.3 milliseconds
 64 Packets lost after 29.623 seconds - No values for 0.2 milliseconds
Packet Loss: 0.61%
Data Points:
  X-Axis: 282021 Samples - 127772 Samples were over 1g or below -1g (45.31%)
Measurement Date: 2021-12-20T11:00:21.489537
Runtime: 29.996 seconds
```

Not only will it show the percentage of data loss for the file, it will now also show how many packets were lost in each packet loss event.

##### `-m`, `--min`

With "-m VALUE" you can change the minimal value for datapoints to be checked. All values below this parameter will be counted as out of the borders.

##### `-v`, `--max`

With "-v VALUE":

```sh
icoanalyzer -m -0.42 -v 2.55
```

you can change the maximum value for datapoints to be checked. All values above this parameter will be counted as out of the borders.

```
Input: log-x.hdf5
Packet Loss: 0.61%
Data Points:
  X-Axis: 282021 Samples - 269420 Samples were over 2.55g or below -0.42g (95.53%)
Measurement Date: 2021-12-20T11:00:21.489537
Runtime: 29.996 seconds
```

(tools:section:icoconverter)=

## ICOconverter

- Converts HDF5 measurement files (`.hdf5`) into `.csv` (Comma-Separated Values) or `.xlsx` (Excel) files

### Usage

The ICOconverter script looks for the file `log.hdf5` in the current working directory by default. After you use the command:

```
icoconverter
```

the script will run and analyze `log.hdf5`. The script will then convert the .hdf5 file and create `log.csv` and save it into the same directory. Attention: When there is already an file with the name of the converted .csv it will be overwritten.

```
> icoconverter
Starting the conversion process
Converting “log.hdf5” to “log.csv”
Finished the conversion process
```

If you want to change the file the script converts or the format it should convert to you have to provide some extra parameters. Using multiple parameters is also possible.

#### Parameters

##### `-h`, `--help`

This argument calls the help menu of the script instead of running the script.

##### Filepath

With the `inputs` positional parameter you can change the file the script converts.

```
icoconverter ~/Downloads/log.hdf5
Starting the conversion process
Converting “/Users/rene/Downloads/log.hdf5” to “/Users/rene/Downloads/log.csv”
Finished the conversion process
```

This path can be given as a relative or an absolute path. If the given path is a folder the script will convert ALL .hdf5 files inside the given folder.

```
icoconverter ~/Downloads/TEST-LOGS-HDF5
Starting the conversion process
Converting “/Users/rene/Downloads/TEST-LOGS-HDF5/log-z.hdf5” to “/Users/rene/Downloads/TEST-LOGS-HDF5/log-z.csv”
Converting “/Users/rene/Downloads/TEST-LOGS-HDF5/log-xy.hdf5” to “/Users/rene/Downloads/TEST-LOGS-HDF5/log-xy.csv”
Converting “/Users/rene/Downloads/TEST-LOGS-HDF5/log-xyz.hdf5” to “/Users/rene/Downloads/TEST-LOGS-HDF5/log-xyz.csv”
Converting “/Users/rene/Downloads/TEST-LOGS-HDF5/log-xz.hdf5” to “/Users/rene/Downloads/TEST-LOGS-HDF5/log-xz.csv”
Converting “/Users/rene/Downloads/TEST-LOGS-HDF5/log-x.hdf5” to “/Users/rene/Downloads/TEST-LOGS-HDF5/log-x.csv”
Converting “/Users/rene/Downloads/TEST-LOGS-HDF5/log-yz.hdf5” to “/Users/rene/Downloads/TEST-LOGS-HDF5/log-yz.csv”
Converting “/Users/rene/Downloads/TEST-LOGS-HDF5/log-y.hdf5” to “/Users/rene/Downloads/TEST-LOGS-HDF5/log-y.csv”
Finished the conversion process
```

##### `-e`, `--excel`

With "-e" you can change the format the script converts to to excel sheets. Instead of .csv it now creates .xlsx files.

```
icoconverter ~/Downloads/*.hdf5 -e
Starting the conversion process
Starting the conversion of: /Users/rene/Downloads/log.hdf5
Starting the conversion of: /Users/rene/Downloads/Measurement_2022-03-31_10-20-16.hdf5
Finished the conversion process
```

(tools:section:icocutter)=

## ICOcutter

- Splits a HDF5 file into two separate files based on a certain cutting time

### Usage

To split a HDF5 file into two segments you need to:

- specify the filepath as positional argument and
- the cutting point in number of second after the option `-t/--time`.

For example, if we want to split the file **`log-x.hdf5`** into:

- one file that contains all data up to the **first 5 seconds** and
- and another file that contains the remaining data, we can use the following command:

```sh
icocutter -o --time 5 examples/log-x.hdf5
```

The command will use the same name as the input file with the additional postfix `-part-1` and `-part-2` added before the extension:

```
Stored first part of HDF data (0:00:00 – 0:00:05) in “examples/log-x-part-1.hdf5”
Stored second part of HDF data (0:00:05 – 0:00:29.995849) in “examples/log-x-part-2.hdf5”
```

#### Parameters

##### `-o`, `--overwrite`

Use the option `-o`/`--overwrite` to overwrite output files, if they already exist.

(tools:section:icoplotter)=

## ICOplotter

- Measures signal to noise ratio (SNR) value of a measurement
- Opens a plotter window visualizing the recorded signal
- Plots the power spectral density graph for the recorded signal
- Prints the IFT value of the signal
- Adds optional red lines for time periods containing missing data values

### Usage

The ICOplotter script looks for a `log.hdf5` file in the current working directory by default. After using the command:

```sh
icoplotter
```

the script will load this file and open the graph of the recording:

![Plotter window](assets/plotter.webp)

The calculated SNR will be written to the standard output.

```
SNR:
  X: -106.50 dB @ 9.40 kHz
```

With closing the plotter the script will finish and the command line will be ready for a new command. For running the script with another input-file use one of the parameters described below.

#### Positional Parameters

##### Filepath

To change the HDF filepath from `log.hdf5` in the current working directory, please specify the filepath as positional argument.

Example:

```sh
icoplotter HDF5/log-x.hdf5
```

#### Optional Parameters

##### `-h`, `--help`

Prints the help menu of the command

##### `-l`, `--loss`

Highlight periods containing lost data using red lines:

![Data plot containing red lines that highlight periods with data loss](assets/Plotter-Data-Loss.webp)

##### `-p`, `--print`

Store the plotter output as PDF file instead of displaying it on the screen. The output is stored in the same location as the the input file with the extension `.pdf`.

##### `-s`, `--scatter`

Use a scatter plot (instead of a line plot) to visualize the measurement data

<a name="readme:section:icoconverter"></a>
