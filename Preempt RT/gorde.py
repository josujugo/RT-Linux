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


server_addressC = '/tmp/ssock'

sock_out.connect(server_addressC)
data0.value[0]=5
sock_out.sendall(data0) #str(ii*0.1))
