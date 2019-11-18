#!/usr/bin/env python3

import handle_config_file
import parse_config_file as pcf
import DAQ_commands as daq
config_path = "config/"


def main():
    # Prompt for config file:
    config_file = handle_config_file.get_config_file(config_path)

    # File contents to list so we can close the file
    file_list = handle_config_file.file_to_list(config_file)
    handle_config_file.close_config_file(config_file)

    # Print a list of errors if found
    # TODO: Prompt the user to see if they want to continue with the error
    sensor_list, error_list = pcf.parse_config_file(file_list)

    # this is just a test that all the configurations are in a list and ready to go
    for items in range(0, (len(sensor_list))):
        sensor_list[items].display_sensor()

    #List line errors if found
    if error_list: pcf.list_errors(error_list)

    # Telnet to DAQ and configure then read the sensors


if __name__ == "__main__":
    main()
