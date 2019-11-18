#!/usr/bin/env python3
"""
Collects the sensor configuration file to be parsed and reads it into a list
"""
import sys
import os

config_path = "./config/"

def get_command_line_config_file():
    """Collects configuration file to be use by command line argument, prompting
    the user or by using the default test file. Returns config file to be
    opened.
    """
    try:
        configfile = sys.argv[1]
    except IndexError:
        print("You need to enter a config file name")
        return False
    return configfile


def open_file(file):
    """Opens a config file to be read in. Returns a file handle or False

    Args:
        file:
    """
    o_file = False
    file = "config/" + file
    try:
        o_file = open(file, 'r')

    except FileNotFoundError:
        print("Sorry I could not find the config file: \"%s\"" % file)
    except OSError:
        print("Did not understand '%s'. Try again."% (file))
    return o_file


def file_to_list(file_handle):
    """Takes a opened file handle and converts the content into a list then closes the file

    Args:
        file_handle:
    """
    file_list = []
    for line in file_handle:
        line = line.strip()
        file_list.append(line)
    file_handle.close()
    return file_list


def prompt_for_config_file():
    """ Request the DAQ configuration file from user
    :return:
    """
    # TODO add some input validation here
    # Only allow files from the local config directory
    # only alpha numeric, dash, underscore, period - "my-config_file.txt"
    return input("Enter the configuration file: ")


def get_config_file(config_path):
    """Collects the configuration file from a user prompt or from the command line.
    Then returns an opened file handle.
    """
    opened_config_file = False
    file = get_command_line_config_file()  # Fetch from the command line if possible
    # Loop over until we open a configuration file
    while not file:
        file_list_msg = "| Available configuration files in " + config_path + " |"
        msg_divider = ""
        for i in range(0, len(file_list_msg)):
            msg_divider = msg_divider + "-"
        print(msg_divider)
        print(file_list_msg)
        print(msg_divider)
        config_file_list = list_config_dir(config_path)
        for a_config_file in config_file_list:
            print("    - %s"%(a_config_file))
        print(msg_divider)

        file = prompt_for_config_file()
        # Check if it can be opened and open it if you can
        opened_config_file = open_file(file)
        if not opened_config_file:
            file = False
    return opened_config_file


def close_config_file(file):
    """Close the config file if it is still open
    """
    if file.closed:
        return True
    elif file.opened:
        print("file still opened closing file")
        file.close()
        return True
    else:
        print("Can't close file?")
        return False

def list_config_dir(config_path):
    """List the contents of the config directory
    """
    config_files = os.listdir(config_path)
    #for file in config_files:
    #    print(file)
    return config_files


def main():
    print("This script should be run from the start file.")
    print("As a test it can be ran alone and will return the contents of any file provided.")

    opened_config_file = get_config_file(config_path)
    # File contents to list so we can close the file now
    file_list = file_to_list(opened_config_file)

    close_config_file(opened_config_file)

    # list the contents of the file with line count
    count = 0
    for i in file_list:
        count = count + 1
        print(count, i)


if __name__ == "__main__":
    main()
