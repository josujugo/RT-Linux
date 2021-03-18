#!/usr/bin/env python


# for debugging, requires: python configure.py  --trace ...
if False:
    import sip
    sip.settracemask(0x3f)

import random
import sys
import socket
import os
import time
import struct
from ctypes import *


""" This class defines a C-like struct """
class Payload(Structure):
    _fields_ = [("value", (c_double*1))]

data0=Payload()

# Create a UDS socket
sock_out = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)


server_addressS = '/tmp/bsock'
sock_in = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock_in.bind(server_addressS)
sock_in.listen(1)
sock_in.settimeout(1)


while True:
	try:
		connection, client_address = sock_in.accept()
		break
	except KeyboardInterrupt:
		sock_in.shutdown(1)
		sock_in.close()
		os.unlink(server_addressS)
		sys.exit(1)
	except socket.timeout:
		time.sleep(0.5)
		print("Trying again ...")

sys.stderr.write('connecting FROM '+str(server_addressS))

server_addressC = '/tmp/ssock'

tr=True

while tr:
	sys.stderr.write('connecting to '+str(server_addressC))
	try:
		sock_out.connect(server_addressC)
		tr=False 
	except socket.error as msg:
		sys.stderr.write(msg)
		time.sleep(2)

print("Connected!")
ii=0
while True:
   try:
    ii=ii+1
    #time.sleep(0.1)
    data = connection.recv(8)
    data0.value[0]= 5*struct.unpack('d',data)[0]
    #print(data0.value[0])
    sock_out.sendall(data0) #str(ii*0.1))
   except KeyboardInterrupt:
    time.sleep(1)
    #ret=connection.close()
    #ret=sock_in.close()
    #sock_out.close()
    os.unlink(server_addressS)
    sys.exit(0)


