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

Check if opening a file works

  $ icocutter examples/log-z.hdf5
