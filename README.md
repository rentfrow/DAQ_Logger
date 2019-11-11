# read_DAQ_config
Description: This script takes a file name as an argument,
open and reads the file, filters the contents for DAX
configurations, and returns the configuration as an array.

Usage:

Notes:
The 34972A DAQ uses channel numbering of 3 digits for each of the 3 modules (34901A) 20 channels per module (34901A)
101, 102, 103, ... 120 and 201, 202, 203, ... 220 and 301, 302, 303, ... 320

The 34980A DAQ uses channel numbering of 4 digits for each of its 8 modules
