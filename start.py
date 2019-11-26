#!/usr/bin/env python3

import handle_config_file
import parse_config_file as pcf
import DAQ_commands as DAQ_cmd
config_path = "config/"


def main():
    # Prompt for config file:
    config_file = handle_config_file.get_config_file(config_path)

    # Slurp file contents into a list of strings so we can close the file
    file_list = handle_config_file.file_to_list(config_file)
    handle_config_file.close_config_file(config_file)

    # Parse the list of strings into two separate lists
    # configuration data and syntax errors in configuration file
    chan_list, error_list = pcf.parse_config_file(file_list)

    # Print a list of errors if found
    # TODO: Prompt the user to see if they want to continue with the error
    if error_list: pcf.list_errors(error_list)

    # Fetch the DAQ IP form the sensor list
    for items in range(0, (len(chan_list))):
        ip_addr = chan_list[items].found_ip()
        ip_port = chan_list[items].found_port()
        if ip_addr:
            print("Found: %s %s" % (ip_addr, ip_port))

    # Telnet to DAQ and configure then read the sensors
    # Connect to DAQ
    tel_conn = DAQ_cmd.connect_daq(ip_addr, ip_port, 10)
    if not tel_conn:
        print("Can't reach IP address: %s %s" % (ip_addr, ip_port))
        exit()

    # Check if we get a welcome connection and get the DAQ prompt
    welcome = DAQ_cmd.welcome_daq(tel_conn)
    if welcome:
        daq_prompt = welcome[1]
        print(daq_prompt)
    else:
        print("Issues getting login message.")

    # Identify the DAQ
    daq_identity = DAQ_cmd.get_idn(tel_conn)
    if daq_identity:
        print("DAQ Manufacturer:  %s"% daq_identity[0])
        print("DAQ Model:         %s"% daq_identity[1])
        print("DAQ Serial Number: %s"% daq_identity[2])
        print("DAQ Firmware:      %s"% daq_identity[3])
    else:
        print("Cannot get DAQ identity")


    # Reset the DAQ before configuring
    if DAQ_cmd.reset_daq_factory_cfg(tel_conn, daq_prompt):
        print("Reset DAQ")
    else:
        print("Problem resetting DAQ")






    # Reset the DAQ to factory defaults before closing connection
    if DAQ_cmd.reset_daq_factory_cfg(tel_conn, daq_prompt):
        print("Reset DAQ")
    else:
        print("Problem resetting DAQ")
    tel_conn.write(b"\x04")


if __name__ == "__main__":
    main()
