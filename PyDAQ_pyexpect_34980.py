#!/usr/bin/env python3
"""
Description:
    Connect to Keysight DAQ 34980A via telnet address port, configures
    channels and collect data to a csv file.

Usage:
    ./PyDAQ_telnet <address> <config file> <output file>


Todo:
    Almost everything, just barely works
    Fix regex so that it will scale with the channels
    Enable a config file
    Enable a output file
    Enable graceful exit
    Needs better error handling
    Enable other dataloggers and autodetect of those loggers
    Enable a gui with graphing
    Convert to OOP
"""

import pexpect
import time
import sys
import re

ip = "10.193.64.232"
daqPrompt = "34980A>"
connection = "'/usr/bin/telnet ", ip, " 5024'"
temp_channels = ["1001", "1002", "1003"]

logging_interval = 10

chan_count = len(temp_channels)
chan_list = "@"
chan_list_iter = 1
for chan_e in temp_channels:
    #print(chan_list_iter, " ", chan_count)
    if chan_list_iter < chan_count:
        chan_list = chan_list + chan_e + ","
    else:
        chan_list = chan_list + chan_e
    chan_list_iter = chan_list_iter + 1


# one_chan = '[\-\+][\d].[\d]+E[\-\+][\d]{2},\d{4}'
# chan_list_regex = '[\-\+][\d].[\d]+E[\-\+][\d]{2},\d{4},'
# for x in range(1, chan_count):
# chan_list_regex = chan_list_regex + one_chan + ","

# Cludge Fix for now!! Each time you add or remove a channel this needs to be edited for the number of channels
####    \+\d+\.\d{8}E\+\d{2},\d{4},  ####
# The key ^^^^^
chan_list_regex = "\+\d+\.\d{8}E\+\d{2},\d{4},\+\d+\.\d{8}E\+\d{2},\d{4},\+\d+\.\d{8}E\+\d{2},\d{4}"



def daqConnection():
    daqconn = pexpect.spawn('/usr/bin/telnet 10.193.64.232 5024')
    daqconn.expect(daqPrompt)
    daqconn.sendline('*RST\r')
    print("Waiting for reset ", daqPrompt)
    daqconn.expect(daqPrompt)
    return daqconn

def daqID(daqconn):
    daqconn.sendline('*IDN?\r')
    print("Checking for correct IDN\n")
    daqconn.expect('Agilent Technologies,34980A,*')
    check_this_id = daqconn.after
    check_this_id = check_this_id.decode('ASCII')
    print(check_this_id)

    re_daq_id = "Agilent Technologies,34980A,"
    daq_id = re.compile(re_daq_id)
    daq_id_match = daq_id.match(check_this_id)
    if daq_id_match:
        id = check_this_id.split(',')
        return id[1]
    else:
        print("wrong DAQ type")
        exit()


def configDAQ(daqconn, chan_list, daqPrompt):
    command = (":CONFigure:TEMPerature TCouple,T,1,MAX,("+chan_list+")")
    #print(command)
    # Need a try except here
    daqconn.sendline(command)
    daqconn.sendline('\r')
    daqconn.expect(daqPrompt)

    command = (":UNIT:TEMPerature C,("+chan_list+")")
    #print(command)
    # Need a try except here
    daqconn.sendline(command)
    daqconn.sendline('\r')
    daqconn.expect(daqPrompt)

    command = (":SENSe:TEMPerature:TRANsducer:TCouple:RJUNction:TYPE INTernal,("+chan_list+")")
    #print(command)
    daqconn.sendline(command)
    daqconn.sendline('\r')
    daqconn.expect(daqPrompt)

    command = (":SENSe:TEMPerature:NPLCycles 1,("+chan_list+")")
    #print(command)
    daqconn.sendline(command)
    daqconn.sendline('\r')
    daqconn.expect(daqPrompt)

    command = (":ROUTe:SCAN ("+chan_list+")")
    #print(command)
    daqconn.sendline(command)
    daqconn.sendline('\r')
    daqconn.expect(daqPrompt)

    daqconn.sendline(':TRIGger:SOURce IMMediate\r')
    daqconn.expect(daqPrompt)
    daqconn.sendline(':FORMat:READing:UNIT 0\r')
    daqconn.expect(daqPrompt)
    daqconn.sendline(':FORMat:READing:CHANnel 1\r')
    daqconn.expect(daqPrompt)
    daqconn.sendline(':FORMat:READing:TIME 0\r')
    daqconn.expect(daqPrompt)
    # Maybe return a configured flag
    return None

def flushdaq(daqconn):
    #cleandaq = ''
    #while not daqconn.expect(r'.+', timeout=5):
    #    cleandaq += daqconn.match.group(0)
    try:
        daqconn.expect("asfdeweadwaecs", timeout = 5)
    except pexpect.TIMEOUT:
        pass
    return None

def collectData(daqconn, chan_regex):
    daqconn.sendline(':READ?\r')
    daqconn.expect(chan_list_regex)
    #daqconn.expect('\+\d+\.\d{8}E\+\d{2}\D\d{4}')
    #print(daqconn.before)
    sensor_values = daqconn.after
    sensor_values = sensor_values.decode('ASCII')
    mylist = sensor_values.split(",")

    fixed_list = []
    for i, j in enumerate(mylist):
        if (i % 2 == 0):
            # print(j, "   ---  ", i)
            fixed_list.append(j)
    return fixed_list



def collectTime(daqconn):
    daqconn.sendline(':SYSTem:TIME:SCAN:STARt?\r')
    daqconn.expect('\d{4}\D\d{2}\D\d{2}\D\d{2}\D\d{2}\D\d{2}\.\d{3}')
    #print(daqconn.after)
    time_values = daqconn.after
    time_values = time_values.decode('ASCII')
    mytime = time_values.split(",")
    # year - 0
    # month - 1
    # day - 2
    # hour - 3
    # minures - 4
    # seconds/micro - 5
    # 08/15/2018 23:11:34.123
    mystring = mytime[1]+"/"+mytime[2]+"/"+mytime[0]+" "+mytime[3]+":"+mytime[4]+":"+mytime[5]
    return mystring


def headerPrint(header_list):
    print("Date/Time,",end='',flush=True)
    for i, entry in enumerate(header_list):
        if (i+1) < len(header_list):
            print("_" + entry + "_ ,",end='',flush=True)
        else:
            print("_" + entry + "_", end='\n',flush=True)


def daqPrint(sensor_line):
    for i, entry in enumerate(sensor_line):
        if (i+1) < len(sensor_line):
            print(entry + ",",end='',flush=True)
        else:
            print(entry,end='\n',flush=True)


def main():
    daqconn = daqConnection()
    print(daqID(daqconn))
    configDAQ(daqconn, chan_list, daqPrompt)
    flushdaq(daqconn)
    headerPrint(temp_channels)
    while True:
        sensor_values = collectData(daqconn, chan_list_regex)
        timestamp = collectTime(daqconn)
        sensor_values.insert(0, timestamp)
        daqPrint(sensor_values)
        time.sleep(logging_interval)

if __name__ == '__main__':
    main()