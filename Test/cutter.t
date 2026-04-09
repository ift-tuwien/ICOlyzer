Setup

  $ cd "$TESTDIR/.."

Print help output

  $ icocutter -h
  usage: icocutter [-h] [-l {debug,info,warning,error,critical}] [-o] -t TIME
                   filepath
  
  Split a HDF5 file into two parts
  
  positional arguments:
    filepath  \s*measurement data in HDF5 format (re)
  
  option.* (re)
    -h, --help\s*show this help message and exit (re)
    -l.*--log \s*{debug,info,warning,error,critical} (re)
              \s*minimum log level (re)
    -o, --overwrite\s*overwrite output files (re)
    -t.*TIME  \s*the maximum timestamp in seconds that should still be.* (re)
               .*of the first HDF5 file (re)

Check that opening a non-existent file fails

  $ icocutter -t 10 does-not-exist.hdf5
  usage: icocutter [-h] [-l {debug,info,warning,error,critical}] [-o] -t TIME
                   filepath
  icocutter: error: argument filepath: “does-not-exist.hdf5” does not exist
  [2]

Check that using an incorrect time argument fails

  $ icocutter --time hello examples/log-z.hdf5
  usage: icocutter [-h] [-l {debug,info,warning,error,critical}] [-o] -t TIME
                   filepath
  icocutter: error: argument -t/--time: “hello” is not a valid measurement time
  [2]

Check that not providing a time to cut fails

  $ icocutter examples/log-z.hdf5
  usage: icocutter [-h] [-l {debug,info,warning,error,critical}] [-o] -t TIME
                   filepath
  icocutter: error: the following arguments are required: -t/--time
  [2]

Check that using a cutting time is too large fails

  $ icocutter --time 30 examples/log-z.hdf5
  Time to cut of “0:00:30” .* than measurement time of “0:00:29.991154” (re)
  [1]

Check that opening an existing file works with a valid cutting time works

  $ icocutter --time 10 examples/log-z.hdf5
  Stored first .* \(0:00:00 – 0:00:10\) in “examples/log-z-part-1.hdf5” (re)
  Stored second.*\(0:00:10 – 0:00:29\.\d+\) in “examples/log-z-part-2.hdf5” (re)

  $ ls examples/log-z-part*.hdf5 | wc -l | sed -E 's/^[[:space:]]+//'
  2

Check that overwriting output data works

  $ icocutter --time 9.999958 -o examples/log-z.hdf5 >/dev/null

Check that the number of measurement values

  $ h5dump -a acceleration/NROWS examples/log-z-part-1.hdf5 | 
  > grep '(0)' |
  > sed -E 's/.*: ([[:digit:]]+)$/\1/'
  94449

  $ h5dump -a acceleration/NROWS examples/log-z-part-2.hdf5 | 
  > grep '(0)' |
  > sed -E 's/.*: ([[:digit:]]+)$/\1/'
  189231

  $ h5dump -a acceleration/NROWS examples/log-z.hdf5 | 
  > grep '(0)' |
  > sed -E 's/.*: ([[:digit:]]+)$/\1/'
  283680

Cleanup

  $ rm examples/log-z-part-1.hdf5
  $ rm examples/log-z-part-2.hdf5
