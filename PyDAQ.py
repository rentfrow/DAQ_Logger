#!/usr/bin/env python3
"""
Description:
    Connect to Keysight DAQ 34980A via telnet address port, configures
    channels and collect data to a csv file.

Usage:
    ./PyDAQ_telnet <address> <config file> <output file>

During connection
Agilent Technologies,34980A,MY53151561,2.51-2.43-2.07-1.05
Use this to id the unit and the connection
"""

import telnetlib
import re
import time

# Agilent Technologies 34980A
daq_ip_address = "10.193.64.232"

# Agilent Technologies 34972A
#daq_ip_address = "10.193.70.133"

daq_port_address = "5024"

# TODO: channel number for 34972A only works with 3 digits while the 34980A only works with 4 digits
chan_list = [[1001, "This is a long sensor name up to 40 char", "Temp", "TC", "T", 1, "C", "DEF"],
             [1002, "#two+plus+signs", "Temp", "TC", "T", 1, "C", "DEF"],
             [1003, "three_3", "Temp", "TC", "T", 1, "C", "DEF"],
             [1004, "garbage", "Temp", "TC", "T", 1, "C", "DEF"]
            ]

def connect_daq(ip, port, timeout_num):
    try:
        telnet_conn = telnetlib.Telnet(daq_ip_address, daq_port_address, timeout=timeout_num)
        telnet_conn.write(b"\n")
    except:
        print("Telnet to %s %s timed out."% (daq_ip_address, daq_port_address))
        return False

    return telnet_conn


def welcome_daq(daq_conn):
    """Collect logon response of DAQ and return the prompt
    """
    output = False
    while not output:
        response = daq_conn.read_very_eager()
        response_str = response.decode('ascii')

        if response_str:
            output = response_str.split("\n")
            # print(output[1])  # prompt
    return output


def reset_daq_factory_cfg(daq_conn, daq_prompt):
    """Reset DAQ to factory config
    """
    #daq_prompt = b"34980A> "
    prompt = daq_prompt.encode()
    daq_conn.write(b"*RST\n")
    time.sleep(1)
    result = daq_conn.read_until(prompt, 5)
    if result:
        return True
    else:
        return False


def get_idn(daq_conn):
    """Fetch the IDN from the DAQ
    Agilent Technologies,34980A,MY53151561,2.51-2.43-2.07-1.05
    [\w\s]*,[\w\s]*,[\w\s]*,[\w\s.-]*
    """
    idn_regex=[re.compile(b"[\w\s]*,[\w]*,[\w]*,[\d.-]*\r\n")]

    # daq_conn.write(b"*IDN?\n")
    daq_conn.write(b"*IDN?\n")
    time.sleep(0.5)
    m_index, obj_returned, bytes_matched = daq_conn.expect(idn_regex, 10)
    # m_index, obj_returned, bytes_matched = daq_conn.expect([b"[\w\s]*,[\w\s]*,[\w\s]*,[\w\s.-]*"], 5)

    line = bytes_matched.decode('ascii').split(",")
    manu_line = line[0].split("> ")
    manufacturer = manu_line[1]
    daq_model = line[1]
    daq_serial_number = line[2]
    daq_firmware_version = line[3].strip()

    return (manufacturer, daq_model, daq_serial_number, daq_firmware_version)


def configure_thermocouple_chan(daq_conn, chan_num):
    """Configure a thermocouple channel
    Stuff to worry about:
    set the temp unit C or F
    Just always use internal reference T junction
    Number of Power Line Cycles - NPLC - This effects the resolution and accuracy of reading
        need to experiment with it, default is 1 - range {0.02|0.2|1|2|10|20|100|200} MIN = 0.02 PLC, MAX = 200 PLC
    """
    chan_num = "@" + str(chan_num)

    # print("Configuring %s"%(chan_num))
    st = 0.5

    cmd = ":CONFigure:TEMPerature TCouple,T,(" + chan_num + ")"
    daq_conn.write(cmd.encode())
    time.sleep(st)
    daq_conn.write(b"\n\n")

    cmd = ":UNIT:TEMPerature C,(" + chan_num + ")"
    daq_conn.write(cmd.encode())
    time.sleep(st)
    daq_conn.write(b"\n\n")

    cmd = ":SENSe:TEMPerature:TRANsducer:TCouple:RJUNction:TYPE INTernal,(" + chan_num + ")"
    daq_conn.write(cmd.encode())
    time.sleep(st)
    daq_conn.write(b"\n\n")

    cmd = ":SENSe:TEMPerature:NPLCycles 10,(" + chan_num + ")"
    daq_conn.write(cmd.encode())
    time.sleep(st)
    daq_conn.write(b"\n\n")


def configure_daq(daq_conn, chan_list):
    """Set up DAQ for logging
    """
    st = 0.1

    # Setup Trigger: The instrument will accept an immediate (continuous) trigger
    daq_conn.write(b":TRIGger:SOURce IMMediate\n")
    time.sleep(st)
    # Turn off unit display for reading. Stuff we have to strip off anyways
    daq_conn.write(b":FORMat:READing:UNIT 0\n")
    time.sleep(st)

    # Display the channel number with each reading
    daq_conn.write(b":FORMat:READing:CHANnel 1\n")
    time.sleep(st)

    # Enable the inclusion of a timestamp in each reading
    daq_conn.write(b":FORMat:READing:TIME 1\n")
    time.sleep(st)

    # Enable absolute time (Date and time) format for :FORM:READ:TIME
    daq_conn.write(b"FORMat:READing:TIME:TYPE ABS\n")
    time.sleep(st)

    print(chan_list)
    cmd = ":ROUTe:SCAN (" + chan_list + ")"
    #cmd = ":ROUTe:SCAN (@1001,1002,1003)"
    daq_conn.write(cmd.encode())
    time.sleep(st)
    daq_conn.write(b"\n\n")




def e_notation_to_dec(e_nota):
    """Agilent format of Engineering Notation (m * 10^n) to a decimal number
    +1.90380000E+01
    -1.00346000E+02
    """
    m = float(e_nota[0:11])
    e = float(e_nota[12:15])
    return round(m*10**e, 3)


def main():
    tel_conn = connect_daq(daq_ip_address, daq_port_address, 10)
    if not tel_conn:
        print("Can't reach IP address: %s %s"%(daq_ip_address, daq_port_address))
        exit()

    welcome = welcome_daq(tel_conn)
    if welcome:
        daq_prompt = welcome[1]
        print(daq_prompt)
    else:
        print("Issues getting login message.")

    daq_identity = get_idn(tel_conn)
    print("DAQ Manufacturer:  %s"% daq_identity[0])
    print("DAQ Model:         %s"% daq_identity[1])
    print("DAQ Serial Number: %s"% daq_identity[2])
    print("DAQ Firmware:      %s"% daq_identity[3])

    if reset_daq_factory_cfg(tel_conn, daq_prompt):
        print("Reset DAQ")
    else:
        print("Problem resetting DAQ")


    chan_numbers = "@"
    for i in range(len(chan_list)):
        print("Configuring channel %d"% (chan_list[i][0]))
        configure_thermocouple_chan(tel_conn, chan_list[i][0])
        chan_numbers = chan_numbers + str(chan_list[i][0])
        if not i >= len(chan_list)-1:
            chan_numbers = chan_numbers + ","

    configure_daq(tel_conn, chan_numbers)


    sensor_re = r"[+-]\d\.\d{8}E[+-]\d{2}"
    sen_line = re.compile(sensor_re)

    for i in range(1,5):
        tel_conn.write(b":READ?\n")
        response = tel_conn.read_until(b"\n", 5)
        # Time between log events
        time.sleep(5)

        # Put the read_until into a list
        response = response.strip()
        response = response.decode('ascii')
        response = response.split(",")
        response[0] = response[0].strip(daq_prompt)

        # prints the entire matched list
        print("Matched line: %s"%(response))

        # Finds the temperature sensor in the matched list, I think this will work for any sensor
        for i in range(len(response)):
            # Find an sensor value
            sen_line_match = sen_line.match(response[i])
            if sen_line_match:
                # print(sen_line_match)
                # print(response[i])
                print(e_notation_to_dec(response[i]))

    tel_conn.write(b"\x04")
    # tn.close()
    # print(tel_conn.read_all().decode('ascii'))


if __name__ == "__main__":
    main()