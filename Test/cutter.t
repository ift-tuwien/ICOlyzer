Setup

  $ cd "$TESTDIR/.."

Print help output

  $ icocutter -h
  usage: icocutter [-h] -t TIME filepath
  
  Split a HDF5 file into two parts
  
  positional arguments:
    filepath  \s*measurement data in HDF5 format (re)
  
  option.* (re)
    -h, --help\s*show this help message and exit (re)
    -t.*TIME  \s*the maximum timestamp in seconds that should still be.* (re)
               .*of the first HDF5 file (re)

Check that opening a non-existent file fails

  $ icocutter -t 10 does-not-exist.hdf5
  usage: icocutter [-h] -t TIME filepath
  icocutter: error: argument filepath: “does-not-exist.hdf5” does not exist
  [2]

Check that using an incorrect time argument fails

  $ icocutter --time hello examples/log-z.hdf5
  usage: icocutter [-h] -t TIME filepath
  icocutter: error: argument -t/--time: “hello” is not a valid measurement time
  [2]

Check that not providing a time to cut fails

  $ icocutter examples/log-z.hdf5
  usage: icocutter [-h] -t TIME filepath
  icocutter: error: the following arguments are required: -t/--time
  [2]

Check that using a cutting time is too large fails

  $ icocutter --time 30 examples/log-z.hdf5
  Time to cut of “0:00:30” is equal or larger than measurement time of “0:00:29.991154”
  [1]

Check that opening an existing file works with a valid cutting time works

  $ icocutter --time 10 examples/log-z.hdf5
