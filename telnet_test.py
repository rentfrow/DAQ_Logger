#!/usr/bin/env python3

import telnetlib

HOST = "10.193.64.232"
PORT = "5024"
prompt = "34980A> "
# user = raw_input("Enter your remote account: ")
# password = getpass.getpass()

tn = telnetlib.Telnet(HOST, PORT)

(i, obj, res) = tn.expect([b"34980A>", "incorrect"], 5)
print(res.decode('ascii'))

tn.read_until(b"34980A> ")
tn.write(b"\n")
tn.write(b"*IDN?\n")
#if password:
#    tn.read_until("Password: ")
#    tn.write(password + "\n")
#
#tn.write("ls\n")


tn.read_until(b"34980A> ")
# print("read: %s"% mytext.decode('ascii'))

tn.write(b"\x04")
tn.close()


print(tn.read_all().decode('ascii'))