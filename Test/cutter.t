Setup

  $ cd "$TESTDIR/.."

Print help output

  $ icocutter -h
  usage: icocutter [-h] [-t TIME] filepath
  
  Split a HDF5 file into two parts
  
  positional arguments:
    filepath  \s*measurement data in HDF5 format (re)
  
  option.* (re)
    -h, --help\s*show this help message and exit (re)
    -t.*TIME  \s*the maximum timestamp in seconds that should still be.* (re)
               .*of the first HDF5 file (re)

Check that opening a non-existent file fails

  $ icocutter -t 10 does-not-exist.hdf5
  usage: icocutter [-h] [-t TIME] filepath
  icocutter: error: argument filepath: “does-not-exist.hdf5” does not exist
  [2]

Check if opening a file works

  $ icocutter examples/log-z.hdf5
