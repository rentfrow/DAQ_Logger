#!/usr/bin/env python3
""" Proposed usage: ./start <config file name> <logging interval> <test log file name>

"""
# TODO Create function to sync time (ntplib)
# TODO Output to a file
# TODO Make sure program can be run via command line arguments

import sys
import time
import handle_config_file
import parse_config_file as pcf
import DAQ_commands as DAQ_cmd
from pathlib import Path
config_path = "config/"
test_log_path = "logs/"

try:
    config_file_name = sys.argv[1]
    log_interval = sys.argv[2]
    test_log_file_name = sys.argv[3]
except IndexError:
    config_file_name = False
    log_interval = False
    test_log_file_name = False


def get_test_log_name(test_log_file_name, test_log_path):
    """Check if a passed test log file name already exists or if none was given.
        If it does already exist or none was given prompt for a new one
    """
    if test_log_file_name:
        test_log_file_name = Path(test_log_path + "/" + test_log_file_name)



    while not test_log_file_name:
        proposed_test_log_file = input("\nEnter test log file name or 'screen' to output only to screen: ")
        test_log_file_name = Path(test_log_path + "/" + proposed_test_log_file)
        if not test_log_file_name.is_file():
            print("It's good. File does not exist")

        else:
            print("Please use another file name file exists")
            test_log_file_name = False
    return test_log_file_name



def main():
    global config_file_name
    global log_interval
    global test_log_file_name
    global config_path
    global test_log_path

    if config_file_name:
        # TODO: Create a function here to open the config_file_name
        pass
    else:
        # TODO: Instead of returning a file handle this should return a
        #  file name and then a separate function to return a file handle
        config_file = handle_config_file.get_config_file(config_path)

    print(test_log_file_name)
    test_log_file_name = get_test_log_name(test_log_file_name, test_log_path)
    print(test_log_file_name)


    # Slurp file contents into a list of strings so we can close the file
    file_list = handle_config_file.file_to_list(config_file)

    # Parse the list of strings into two separate lists
    # configuration data and syntax errors in configuration file
    chan_list, error_list = pcf.parse_config_file(file_list)

    # Close config file after putting config file into a list
    handle_config_file.close_config_file(config_file)

    # Print a list of errors if found
    # TODO: Prompt the user to see if they want to continue with the error
    if error_list:
        pcf.list_errors(error_list, config_file.name)

    # Fetch the DAQ IP form the sensor list
    for items in range(0, (len(chan_list))):
        ip_addr = chan_list[items].found_ip()
        ip_port = chan_list[items].found_port()
        if ip_addr:
            print("Found: %s %s" % (ip_addr, ip_port))
            break

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
        print("DAQ reset")
    else:
        print("Problem resetting DAQ")


    # Channel configuration list
    sensors_in_a_list = pcf.sensors_to_list(chan_list)

    # Configuring DAQ channels
    chan_numbers = DAQ_cmd.configure_daq_channels(tel_conn, sensors_in_a_list)
    print("######### channels configured ##########")
    print(chan_numbers)

    # Configure the daq to scan the channels (sensors)
    DAQ_cmd.configure_daq(tel_conn, chan_numbers)



    collection_interval = 10
    # Now collect and display sensor data
    while True:
        try:
            # Read from DAQ one set of sensor data and return it as a raw string
            sensor_line = DAQ_cmd.collect_sensor_line(tel_conn, daq_prompt)

            # Get a datestamp
            datestamp = sensor_line[2] + "/" + sensor_line[3] + "/" + sensor_line[1] + " " + sensor_line[4] + ":" + \
                        sensor_line[5] + ":" + sensor_line[6][0:2]

            print("%s, " % datestamp, end="")
            for i in range(0, len(sensor_line), 8):
                print("%s, " % pcf.e_notation_to_dec(sensor_line[i]), end="")
            print("")




            try:
                time.sleep(collection_interval)
            except (KeyboardInterrupt, SystemExit):
                # TODO: Clean up things here before exiting
                sys.exit()

        except (KeyboardInterrupt, SystemExit):
            # TODO: Clean up things here before exiting
            sys.exit()




    DAQ_cmd.put_in_local_mode(tel_conn, daq_prompt)
    # Reset the DAQ to factory defaults before closing connection
    #if DAQ_cmd.reset_daq_factory_cfg(tel_conn, daq_prompt):
    #    print("TODO: Put a choice here to choose between reset or just disconnect remote.")
        #put_in_local_mode(tel_conn, daq_prompt)
    #    print("DAQ Reset")
    #else:
    #    print("Problem resetting DAQ")
    tel_conn.write(b"\x04")


if __name__ == "__main__":
    main()
