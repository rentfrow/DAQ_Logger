#!/usr/bin/env python3
"""
Description: This script takes a file name as an argument,
open and reads the file, filters the contents for DAX
configurations, and returns the configuration as an array.

Usage:

Notes:
The 34972A DAQ uses channel numbering of 3 digits for each of the 3 modules (34901A) 20 channels per module (34901A)
101, 102, 103, ... 120 and 201, 202, 203, ... 220 and 301, 302, 303, ... 320

The 34980A DAQ uses channel numbering of 4 digits for each of its 8 modules

scratch notes DELETE LATER
    1. Get configuration file name
    2. Open configuration file name and assign to file handle
        2.1 If configuration file name cannot be opened return to step 1
    3. Parse through the file and search for sensor configuration information
        3.1 If the line is blank - skip the line
        3.2 If the line is a comment (starts with a "#") - skip the line
        3.3 If the line matches a sensor configuration line - continue to process the line
        3.4 If the line matches nothing it is an error in the line - record the error and skip the line
    4. Split the matched line into a list and append to the sensor list of lists
    5. return the list of sensors


"""

import sys
import re

class Sensor:
    """A general DAQ sensor"""
    def __init__(self, channel, name, sen_type, sen_attr01, sen_attr02, sen_attr03, sen_attr04, sen_attr05):
        """
        Args:
            channel:
            name:
            sen_type:
            sen_attr01:
            sen_attr02:
            sen_attr03:
            sen_attr04:
            sen_attr05:
        """
        self.channel = channel
        self.name = name
        self.sen_type = sen_type
        self.sen_attr01 = sen_attr01
        self.sen_attr02 = sen_attr02
        self.sen_attr03 = sen_attr03
        self.sen_attr04 = sen_attr04
        self.sen_attr05 = sen_attr05

    def display_sensor(self):
        print("%s, \"%s\", %s, %s, %s, %s, %s, %s" %
              (self.channel, self.name, self.sen_type,
               self.sen_attr01, self.sen_attr02, self.sen_attr03,
               self.sen_attr04, self.sen_attr05)
              )


def add_sensor_line(cfg_line, sensor_list):
    """Add a sensor config line to the sensor list

    Args:
        cfg_line:
        sensor_list:
    """
    sensor_line = []
    for line_entry in (cfg_line.split(',')):
        sensor_line.append(line_entry.strip())

    pad = 9 - len(sensor_line)
    for i in range(1, pad):
        sensor_line.append("na")

    sensor_list.append(Sensor(sensor_line[0], sensor_line[1], sensor_line[2], sensor_line[3],
                              sensor_line[4], sensor_line[5], sensor_line[6], sensor_line[7],
                              ))
    return sensor_list


def parse_config_file(config_file):
    """Search line by line through an opened file handle for sensor
    configuration information. :param config_file: :param sensor_list: :param
    error_list: :return sensor_list, error_list:

    Args:
        config_file:
    """
    sensor_list = []
    error_list = []
    line_count = 0
    error_found_in_config = False

    for config_line in config_file:
        line_count += 1

#       TODO: pass the sensor line to this function instead and iterate outside of the function
        sensor_line = search_for_sensor(config_line)

        # If a comment line or blank line is found just skip
        if not_config_information(config_line):
            continue

        elif sensor_line:
            sensor_line_type = sensor_line[0]
            sensor_line = add_sensor_line(config_line, sensor_list)

        else:
            line_error = line_count, config_line
            error_list.append(line_error)
            error_found_in_config = True
            continue

    return sensor_list, error_list


def not_config_information(cfg_line):
    """Identifying a blank and commented out line with regex these lines will be
    skipped

    Returns: Boolean

    Args:
        cfg_line:
    """
    blankline = re.compile(r"^\s*$")
    blanklinematch = blankline.match(cfg_line)

    commentline = re.compile(r"^#")
    commentlinematch = commentline.match(cfg_line)

    if blanklinematch or commentlinematch:
        return True
    else:
        return False


def search_for_sensor(cfg_line):
    """Search for a sensor line with a iter of regex :param cfg_line: :return:
    boolean

    Args:
        cfg_line:
    """
    search_results = False
    sensor_search_keys = (
        ("thermocouple", r"\d{3,4},\s[0-9a-zA-Z\s\-\+_#]{3,40},\sTemp,\sTC,\s[J|K|T],\s\d,\s[C|F],\sDEF"),
        ("frequency",    r"\d{3,4},\s*[0-9a-zA-Z\s\-\+_]{3,40},\s*FREQ,\s*DEF,\s*DEF"),
        ("dc_voltage",   r"\d{3,4},\s*[0-9a-zA-Z\s\-\+_]{3,40},\s*VOLT,\s*DC,\s*AUTO,\s*DEF"),
        ("dc_current",   r"\d{3,4},\s*[0-9a-zA-Z\s\-\+_]{3,40},\s*CURR,\s*DC,\s*AUTO,\s*DEF")
    )

    for sensor_type in sensor_search_keys:
        sen_line = re.compile(sensor_type[1])
        sen_line_match = sen_line.match(cfg_line)
        if sen_line_match:
            search_results = [sensor_type[0], sensor_type[1]]

    return search_results


def get_config_file():
    """Collects configuration file to be use by command line argument, prompting
    the user or by using the default test file. Returns config file to be
    opened.
    """
    try:
        configfile = sys.argv[1]
    except IndexError:
        print("You need to enter a config file name")
        # exit()
        print("Will use test config file instead: myconfigfile.txt")
        configfile = "myconfigfile.txt"
        #configfile = "my_good_config_file.txt"
    return configfile


def open_file(file):
    """Opens a config file to be read in. Returns a file handle or False

    Args:
        file:
    """
    o_file = False
    try:
        o_file = open(file, 'r')

    except FileNotFoundError:
        print("Sorry I could not find the config file: \"%s\"" % file)
    return o_file


def main():
    # Prompt for config file:
    configfile = get_config_file()
    # Check if it can be opened and open it if you can
    opened_config_file = open_file(configfile)


    sensor_list, error_list = parse_config_file(opened_config_file)

    opened_config_file.close()

    for items in range(0, (len(sensor_list))):
        sensor_list[items].display_sensor()

    #List line errors if found
    if error_list:
        print("Errors found in config file!")
        for items in range(0, len(error_list)):
            line = error_list[items][0]
            #print("%s"%line)
            error = error_list[items][1]
            #print(error)
            print("Line: %s"%(line),(error))

if __name__ == "__main__":
    main()