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
import handle_config_file as hcf

class Sensor:
    """A general DAQ sensor
    Num, Name, Function, Type, Range, Resolution, Scale, Gain(M), Offset(B), Units
    """
    def __init__(self,  channel, name, sen_func, sen_type, sen_range,
                 sen_resolution, sen_scale, sen_gain, sen_offset, sen_units):
        """
        Args:
            channel:
            name:
            sen_func:
            sen_type:
            sen_range:
            sen_resolution:
            sen_scale:
            sen_gain:
            sen_units:
        """
        self.channel = channel
        self.name = name
        self.sen_func = sen_func
        self.sen_type = sen_type
        self.sen_range = sen_range
        self.sen_resolution = sen_resolution
        self.sen_scale = sen_scale
        self.sen_gain = sen_gain
        self.sen_offset = sen_offset
        self.sen_units = sen_units

    def display_sensor(self):
        print("%s, %s, %s, %s, %s, %s, %s, %s %s %s" %
              (self.channel, self.name, self.sen_func, self.sen_type, self.sen_range, self.sen_resolution,
               self.sen_scale, self.sen_gain, self.sen_offset, self.sen_units)
              )

    def return_sensor_list(self):
        """Changes the Sensor object into a normal list
         chan_list = [[101, "Front Ambient", "TCouple",   "T",  "1",   "4.5",      "FALSE", "1",     "0",       "C"],
        :return:
        """
        list_line = [self.channel, self.name, self.sen_func, self.sen_type, self.sen_range, self.sen_resolution,
         self.sen_scale, self.sen_gain, self.sen_offset, self.sen_units]
        return list_line

    def found_ip(self):
        """Search for and return ip or host address from configuration file
        """
        if "DAQ_IP" in self.channel:
            return self.name
        else:
            return False

    def found_port(self):
        """Search for and return port address from configuration file
        """
        if "DAQ_IP" in self.channel:
            return self.sen_func
        else:
            return False



def list_errors(error_list, config_file):
    """
    :param error_list:
    :return:
    """
    msg = "# Errors found in config file: " + config_file + "! #"
    for i in range(0, len(msg)):
        print("#", end="")
    print("\n%s"%msg)
    for i in range(0, len(msg)):
        print("#", end="")
    print("")
    for items in range(0, len(error_list)):
        line = error_list[items][0]
        error = error_list[items][1]
        print("Error in configuration at line: %s - \n\"%s\""%(line, error))
    print("\nDo you wish to exit and correct the errors in \"%s?\""% config_file)
    response = input("Press 'X' to exit or any other key to continue: ")
    if "X" in response.upper():
        print("Exiting")
        sys.exit()
    return True


def add_ip_line(cfg_line):
    """Add the DAQ IP address to the DAQ sensor list
    Args:
        cfg_line:
        sensor_list:

    Sample line:
    Address: 172.28.94.64 5024
    """
    ip_line = ["DAQ_IP"]  # Create a list with DAQ_IP as first item
    cfg_line = cfg_line.split(':')
    # "DAQ_IP", "192.0.0.3", "5024"
    line = cfg_line[1].split(' ')
    ip_line.append(line[1].strip())
    ip_line.append(line[2].strip())
    pad = 11 - len(ip_line)
    for i in range(1, pad):
        ip_line.append("na")
    return ip_line


def add_sensor_line(cfg_line, sensor_list, sensor_type):
    """Add a sensor config line to the sensor list
    Args:
        cfg_line:
        sensor_list:
        sensor_type:
    """
    if 'ip_address' in sensor_type:
        ip_line = add_ip_line(cfg_line)
        sensor_list.append(Sensor(ip_line[0], ip_line[1], ip_line[2], ip_line[3], ip_line[4],
                                  ip_line[5], ip_line[6], ip_line[7], ip_line[8], ip_line[9]))
    else:
        sensor_line = []
        for line_entry in (cfg_line.split(',')):
            sensor_line.append(line_entry.strip())

        pad = 10 - len(sensor_line)
        for i in range(1, pad):
            sensor_line.append("na")
        try:
            sensor_list.append(Sensor(sensor_line[0], sensor_line[1], sensor_line[2], sensor_line[3], sensor_line[4],
                                      sensor_line[5], sensor_line[6], sensor_line[7], sensor_line[8], sensor_line[9]))
        except IndexError:
            print("Error in config file on line number %s."% i)
            print("Wrong number of fields entered. Review config file.")
            sys.exit()
            # TODO: should we close the config file here???
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

        # Found a config line add it to the list
        elif sensor_line:
            sensor_type = sensor_line[0]
            sensor_list = add_sensor_line(config_line, sensor_list, sensor_type)

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
    # TODO current is not working need to test on actual system
    sensor_search_keys = (
        ("ip_address",
                        r"Address:\s(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.)"
                        r"{3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\s\d+"),
        ("thermocouple",
                        r"\d{3,4},\s*[0-9a-zA-Z\s\-\+_#\"]{1,40},\s*TCouple,\s*[BEJKNRST],"
                        r"\s*[DEF1]+,\s*[DEF\d\.]+,\s*[FALSETRU]+,\s*[\d\.]+,\s*[\d\.]+,\s*[FC]"),
        ("frequency", r"\d{3,4},\s*[0-9a-zA-Z\s\-\+_\"]{3,40},\s*Freq,\s*,\s*[DEF\d]+,"
                        r"\s*[DEF\d\.]+,\s*[FALSETRU]+,\s*\d+,\s*\d+,\s*\w{,3}"),
        ("dc_voltage", r"\d{3,4},\s*[0-9a-zA-Z\s\-\+_\"]{3,40},\s*Volt,\s*[ACD]{2},\s*[\d\.AUTOMINXDEF]*,"
                       r"\s*[\d\.AUTOMINXDEF]*,\s*[FALSETRU]+,\s*[\d+\.]+,\s*[\d\.]+,\s*\w+"),
        ("dc_current",
                        r"\d{3,4},\s*[0-9a-zA-Z\s\-\+_]{3,40},\s*CURR,\s*DC,\s*AUTO,\s*DEF")
    )

    for sensor_type in sensor_search_keys:
        sen_line = re.compile(sensor_type[1])
        sen_line_match = sen_line.match(cfg_line)
        if sen_line_match:
            search_results = [sensor_type[0], sensor_type[1]]

    return search_results


def sensors_to_list(sensor_list):
    """
    :param sensor_list:
    :return:
    """
    a_list = []
    for items in range(0, (len(sensor_list))):
        a_list.append(sensor_list[items].return_sensor_list())
    return a_list


def e_notation_to_dec(e_nota):
    """Agilent format of Engineering Notation (m * 10^n) to a decimal number
    +1.90380000E+01
    -1.00346000E+02
    """
    m = float(e_nota[0:11])
    e = float(e_nota[12:15])
    return round(m*10**e, 6)
    #return e_nota


def main():
    """Parse the config file into a list and return it
    """
    ###########
    # Get the config file to parse, use handle_config_file.py
    ###########
    config_path = "config/"
    # Prompt for config file:
    opened_config_file = hcf.get_config_file(config_path)


    ###########
    # Parse the config file and return some lists
    # sensor_list, error_list, server_IP_list(will be in sensor_list)
    ###########
    sensor_list, error_list = parse_config_file(opened_config_file)

    print(sensors_to_list(sensor_list))
    print(error_list)


    opened_config_file.close()

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