fs_usage_stats.py
=================
Experimental Python script to calculate some statistics from macOS' fs_usage output

_Work in progress_

I'm analyzing an issue with high disk usage and general slowness on a family iMac.
macOS' Activity Monitor lacks real-time information about disk usage, and `iotop` can't be used without disabling SIP,
that's why I ended up running `fs_usage` for a while, dumping the output and analyzing it with this script.

Requirements
------------
A relatively recent Python 3 installation.

How to use
----------
1. Have a plain text file with output from `fs_usage` (note: all the columns need to be present, `-w` can be used to ensure this)
2. Run `fs_usage_stats.py -h` for usage information
