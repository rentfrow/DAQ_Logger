# read_DAQ_config
Description: 
I needed a way to read and collect sensor data from a Keysight (or Agilent Technologies) data aquisition unit (DAQ) in a local network
environment.

Requirements: 
- Must work on both Keysight DAQ models 34980A and 34972A
- Cannot use VXI-11 protocol as those port addresses have been blocked in the internal network. Internal telnet port addresses (5024) have
  not been block so those addresses will be used. 
- Must work on Linux and Windows console terminals. Going for lean and easy to use. 

Usage: <TBD>

Notes:
The 34972A DAQ uses channel numbering of 3 digits for each of the 3 modules (34901A) 20 channels per module (34901A)
101, 102, 103, ... 120 and 201, 202, 203, ... 220 and 301, 302, 303, ... 320

The 34980A DAQ uses channel numbering of 4 digits for each of its 8 modules
