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
#daq_ip_address = "10.193.64.232"

# Agilent Technologies 34972A
# TODO: Need to pass the IP address from the configuration file
# daq_ip_address = "10.193.70.133"
daq_ip_address = "172.28.94.64"

daq_port_address = "5024"

# TODO: channel number for 34972A only works with 3 digits while the 34980A only works with 4 digits
# Channel Config
# Number, Name, Function, Range, Resolution, MORE?, Scale, Gain(M), Offset(B), Units
# Functions Supported: Temp(T,J,etc), Volt_DC, Frequency, Current_DC
#             Num, Name,            Function,    Range, Resolution, Scale,   Gain(M),   Offset(B),   Units
chan_list = [[101, "Front Ambient", "TCouple-T", "1",   "C",       "FALSE",  "1",       "0",         "C"],
             [102, "Fan Voltage",   "Volt_DC",   "DEF", "DEF",     "FALSE",  "1",       "0",         "Vdc"],
             [103, "Shunt Current", "Volt_DC",   "DEF", "DEF",     "TRUE",   "500",     "0",         "Amp"],
             [104, "Fan RPM 1",     "Frequency", "10",  "4.5",     "TRUE",   "1000",    "0",         "RPM"],
             [104, "Fan RPM 2",     "Frequency", "10",  "4.5",     "TRUE",   "1000",    "0",         "RPM"],
             [106, "REAR Amb",      "TCouple-T", "1",   "C",       "FALSE",  "1",       "0",         "C"]
            ]

def connect_daq(ip, port, timeout_num):
    """Connect to DAQ and return the connection and telnet terminal prompt
    """
    try:
        telnet_conn = telnetlib.Telnet(ip, port, timeout=timeout_num)
        telnet_conn.write(b"\n")
    except:
        print("Telnet to %s %s timed out."% (daq_ip_address, daq_port_address))
        return False

    return telnet_conn


def welcome_daq(daq_conn):
    """Collect logon response of DAQ and return the prompt after first connection
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
        print("Issue resetting the DAQ")
        return False


def put_in_local_mode(daq_conn, daq_prompt):
    """Put DAQ into remote mode
    """
    #daq_prompt = b"34980A> "
    prompt = daq_prompt.encode()
    daq_conn.write(b"SYSTem:LOCal\n")
    time.sleep(1)
    result = daq_conn.read_until(prompt, 5)
    if result:
        return True
    else:
        print("Issue putting DAQ into local mode")
        return False


def get_idn(daq_conn):
    """Fetch the IDN from the DAQ
    Agilent Technologies,34980A,MY53151561,2.51-2.43-2.07-1.05
    [\w\s]*,[\w\s]*,[\w\s]*,[\w\s.-]*
    """

    idn_regex=[re.compile(b"[\w\s]*,[\w]*,[\w]*,[\d.-]*\r\n")]

    # daq_conn.write(b"*IDN?\n")
    daq_conn.write(b"*IDN?\n")
    time.sleep(0.1)
    m_index, obj_returned, bytes_matched = daq_conn.expect(idn_regex, 10)
    # m_index, obj_returned, bytes_matched = daq_conn.expect([b"[\w\s]*,[\w\s]*,[\w\s]*,[\w\s.-]*"], 5)

    line = bytes_matched.decode('ascii').split(",")
    manu_line = line[0].split("> ")
    manufacturer = manu_line[1]
    daq_model = line[1]
    daq_serial_number = line[2]
    daq_firmware_version = line[3].strip()

    return (manufacturer, daq_model, daq_serial_number, daq_firmware_version)


def configure_dc_voltage(daq_conn, chan_num):
    """Configure a DC Voltage channel
    CONFigure[:VOLTage][:DC] [{<range>|AUTO|MIN|MAX|DEF} [,{<resolution>|MIN|MAX|DEF}] , ] [(@<ch_list>)]
    Auto Range -> [SENSe:]VOLTage:AC:RANGe:AUTO <state>[,(@<ch_list>)]
                    VOLT:AC:RANG:AUTO ON,(@103,113)
    Range -> [SENSe:]VOLTage:AC:RANGe {<range>|MIN|MAX}[,(@<ch_list>)]
                    VOLT:DC:RANG 10,(@103,113)
    """
    sleep_time = 0.1
    chan_num = "@" + str(chan_num)
    execute_daq_cmd(daq_conn, ":CONFigure:VOLTage :DC DEF ,DEF,(" + chan_num + ")", sleep_time)
    execute_daq_cmd(daq_conn, ":SENSe:VOLTage:DC:NPLCycles 10,(" + chan_num + ")", sleep_time)
    return True


def configure_dc_current(daq_conn, chan_num):
    """Configure a DC Current channel
    This only works on 34901A 20 Channel Multiplexer (2/4-wire) Module (channels 21 and 22 only) at 250V 1A
    CONFigure:CURRent:DC [{<range>|AUTO|MIN|MAX|DEF}[,{<resolution>|MIN|MAX|DEF}],] (@<scan_list>)
    [SENSe:]CURRent:DC:NPLC {<PLCs>|MIN|MAX}[,(@<ch_list>)]
    """
    sleep_time = 0.1
    chan_num = "@" + str(chan_num)
    execute_daq_cmd(daq_conn, ":CONFigure:CURRent :DC DEF ,DEF,(" + chan_num + ")", sleep_time)
    execute_daq_cmd(daq_conn, ":SENSe:CURRent:DC:NPLCycles 10,(" + chan_num + ")", sleep_time)
    return True


def configure_shunt(daq_conn, chan_num):
    """Configure a shunt to measure an ampere >1A
    also can be used for lower amperes <1A but the 34901A on channel 21 & 22 will measure amps below 1A
    CALCulate:SCALe:GAIN <gain>[,(@<ch_list>)]
    CALCulate:SCALe:GAIN? [(@<ch_list>)]
    CALCulate:SCALe:OFFSet <offset>[,(@<ch_list>)]
    CALCulate:SCALe:OFFSet? [(@<ch_list>)]
    CALCulate:SCALe:STATe <state>[,(@<ch_list>)]
    Shunt - Lab 25-50, 25A, 50MV, 0.002 Ohms
    """

    # This is specifically for the EM-PRO Lab 25-50 (25Amp, MV 50, .002 OHMs)
    gain = "500" # This is equal to (1.0 / 0.002)
    sleep_time = 0.1
    chan_num = "@" + str(chan_num)
    execute_daq_cmd(daq_conn, ":CONFigure:VOLTage :DC MAX,1,(" + chan_num + ")", sleep_time)
    execute_daq_cmd(daq_conn, "CALCulate:SCALe:STATe ON,(" + chan_num + ")", sleep_time)
    execute_daq_cmd(daq_conn, ":SENSe:VOLTage:DC:NPLCycles 10,(" + chan_num + ")", sleep_time)
    execute_daq_cmd(daq_conn, "CALCulate:SCALe:GAIN " + gain + ",(" + chan_num + ")", sleep_time)


def configure_frequency(daq_conn, chan_num):
    """Configure frequency such as RPM
    """
    gain = "1000"
    volt_range = "10"
    resolution = "4.5"  # 4.5, 5.5, 6.5
    sleep_time = 0.1
    chan_num = "@" + str(chan_num)
    execute_daq_cmd(daq_conn, "CONFigure:FREQuency ," + volt_range + "," + resolution + ",(" + chan_num + ")", sleep_time)
    execute_daq_cmd(daq_conn, "CALCulate:SCALe:GAIN " + gain + ",(" + chan_num + ")", sleep_time)
    execute_daq_cmd(daq_conn, "CALCulate:SCALe:STATe ON,(" + chan_num + ")", sleep_time)


def configure_thermocouple_chan(daq_conn, chan_num):
    """Configure a thermocouple channel
    Stuff to worry about:
    set the temp unit C or F
    Just always use internal reference T junction
    Number of Power Line Cycles - NPLC - This effects the resolution and accuracy of reading
        need to experiment with it, default is 1 - range {0.02|0.2|1|2|10|20|100|200} MIN = 0.02 PLC, MAX = 200 PLC
    """
    chan_num = "@" + str(chan_num)
    sleep_time = 0.1
    execute_daq_cmd(daq_conn, ":CONFigure:TEMPerature TCouple,T,(" + chan_num + ")", sleep_time)
    execute_daq_cmd(daq_conn, ":UNIT:TEMPerature C,(" + chan_num + ")", sleep_time)
    execute_daq_cmd(daq_conn,
                    ":SENSe:TEMPerature:TRANsducer:TCouple:RJUNction:TYPE INTernal,(" + chan_num + ")", sleep_time)
    execute_daq_cmd(daq_conn, ":SENSe:TEMPerature:NPLCycles 10,(" + chan_num + ")", sleep_time)
    return True


def execute_daq_cmd(daq_conn, daq_cmd, interval_between_cmds):
    """Execute the DAQ command on the DAQ
    """
    daq_conn.write(daq_cmd.encode())
    time.sleep(interval_between_cmds)
    daq_conn.write(b"\n\n")
    return True


def configure_daq(daq_conn, chan_list):
    """Set up DAQ for logging not individual channels
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

    cmd = ":ROUTe:SCAN (" + chan_list + ")"
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
    return round(m*10**e, 6)
    #return e_nota


def collect_sensor_line(tel_conn, daq_prompt):
    """Read from DAQ and return a raw list of sensor values, date, time, and channel number
    """
    tel_conn.write(b":READ?\n")
    response = tel_conn.read_until(b"\n", 5)
    # Time between log events
    time.sleep(1)
    # Put the read_until into a list
    response = response.strip()
    response = response.decode('ascii')
    response = response.split(",")
    response[0] = response[0].strip(daq_prompt)
    # prints the entire matched list
    # print("Matched line: %s"%(response))

    return response


def return_sensor_value(raw_sensor_line, chan_config_list):
    """Finds the sensor channel number, datestamp and value in the matched list and returns it as a list
    """
    sensor_re = r"[+-]\d\.\d{8}E[+-]\d{2}"
    sen_line = re.compile(sensor_re)
    sensor_line = []
    for i in range(len(raw_sensor_line)):
        # Find an sensor value
        sen_line_match = sen_line.match(raw_sensor_line[i])
        if sen_line_match:
            sensor_value = e_notation_to_dec(raw_sensor_line[i])
            year    = raw_sensor_line[i+1]
            month   = raw_sensor_line[i+2]
            day     = raw_sensor_line[i+3]
            hour    = raw_sensor_line[i+4]
            minutes = raw_sensor_line[i+5]
            seconds = raw_sensor_line[i+6]
            seconds = seconds.split(".")
            seconds = seconds[0]
            datestamp = month + "/" + day + "/" + year + " " + hour + ":" + minutes + ":" + seconds
            channel = raw_sensor_line[i+7]
            chan_description = find_channel_description(channel, chan_config_list)
            # print("%s, %s, %s, %f"% (channel, chan_description, datestamp, sensor_value))
            sensor_line.append(datestamp)
            sensor_line.append(channel)
            sensor_line.append(chan_description)
            sensor_line.append(sensor_value)
    return sensor_line


def find_channel_description(channel, chan_config_list):
    """Find the channel description from the channel config file
    """
    for i in range(0,len(chan_config_list)):
        if str(channel) == str(chan_config_list[i][0]):
            return chan_config_list[i][1]
    return False


def welcome_get_idn(daq_conn):
    """Check if we got the welcome connection and return the idn
    Need to run these two commands in sequence welcome -> idn
    """
    welcome = welcome_daq(daq_conn)
    if welcome:
        daq_prompt = welcome[1]
        print(daq_prompt)
    else:
        print("Issues getting login message.")

    # Identify the DAQ
    daq_identity = get_idn(daq_conn)
    if daq_identity:
        print("DAQ Manufacturer:  %s"% daq_identity[0])
        print("DAQ Model:         %s"% daq_identity[1])
        print("DAQ Serial Number: %s"% daq_identity[2])
        print("DAQ Firmware:      %s"% daq_identity[3])
    else:
        print("Cannot get DAQ identity")

    return daq_prompt, daq_identity


def configure_daq_channels(daq_conn, chan_list):
    """Takes processed channel list and configures the channels on the DAQ
    """
    #[1005, "my volts", "VOLT", "DC", "AUTO", "DEF"]
    chan_numbers = "@"
    for i in range(len(chan_list)):
        print(chan_list[i][2].upper())
        chan_type = chan_list[i][2].upper()
        if chan_type == "TEMP":
            print("Configuring channel: %s"% (chan_list[i][0]))
            configure_thermocouple_chan(daq_conn, chan_list[i][0])
            chan_numbers = chan_numbers + str(chan_list[i][0])
            if not i >= len(chan_list)-1:
                chan_numbers = chan_numbers + ","

        elif chan_type == "VOLT":
            print("Configuring channel: %s"% (chan_list[i][0]))
            configure_dc_voltage(daq_conn, chan_list[i][0])
            chan_numbers = chan_numbers + str(chan_list[i][0])
            if not i >= len(chan_list)-1:
                chan_numbers = chan_numbers + ","

        elif chan_type == "SHUNT":
            print("Configuring channel: %s"% (chan_list[i][0]))
            configure_shunt(daq_conn, chan_list[i][0])
            chan_numbers = chan_numbers + str(chan_list[i][0])
            if not i >= len(chan_list)-1:
                chan_numbers = chan_numbers + ","

        elif chan_type == "FREQ":
            print("Configuring channel: %s"% (chan_list[i][0]))
            configure_frequency(daq_conn, chan_list[i][0])
            chan_numbers = chan_numbers + str(chan_list[i][0])
            if not i >= len(chan_list)-1:
                chan_numbers = chan_numbers + ","

    return chan_numbers


def main():
    # Connect to DAQ
    tel_conn = connect_daq(daq_ip_address, daq_port_address, 10)
    if not tel_conn:
        print("Can't reach IP address: %s %s"%(daq_ip_address, daq_port_address))
        exit()

    daq_prompt, daq_identity = welcome_get_idn(tel_conn)

    # Reset the DAQ before configuring
    reset_daq_factory_cfg(tel_conn, daq_prompt)

    # Configuring DAQ channels
    chan_numbers = configure_daq_channels(tel_conn, chan_list)

    # Configure the daq to scan the channels (sensors)
    configure_daq(tel_conn, chan_numbers)

    # Now collect and display sensor data
    for i in range(0,3):
        # Read from DAQ one set of sensor data and return it as a raw string
        raw_sensor_line = collect_sensor_line(tel_conn, daq_prompt)
        # Convert raw sensor line string and print the results
        #TODO return this as a list that can be manipulated
        sensor_line = return_sensor_value(raw_sensor_line, chan_list)
        print(sensor_line)
        time.sleep(3)


    # Reset the DAQ before closing to release it back to locol control
    # reset_daq_factory_cfg(tel_conn, daq_prompt)
    # Put DAQ into local mode and exit
    put_in_local_mode(tel_conn, daq_prompt)
    tel_conn.write(b"\x04")


if __name__ == "__main__":
    main()