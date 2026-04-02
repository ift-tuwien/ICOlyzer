Setup

  $ cd "$TESTDIR/.."

Print help output

  $ icocutter -h
  usage: icocutter [-h] [-t TIME] input
  
  Split a HDF5 file into two parts
  
  positional arguments:
    input       \s*measurement data in HDF5 format (re)
  
  option.* (re)
    -h, --help \s*show this help message and exit (re)
    -t.*TIME  \s*the maximum timestamp in seconds that should still be.* (re)
               .*of the first HDF5 file (re)
