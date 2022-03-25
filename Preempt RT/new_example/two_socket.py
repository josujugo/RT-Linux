import random
import sys
import socket
import os
import time
import struct
from ctypes import *
from signal import signal, SIGINT
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    sock_out.close()
    sock_in.close()
    time.sleep(0.5)
    os.unlink(server_addressS)
    sys.exit(0)

signal(SIGINT, handler)

broker="raspberrypi.local"
mqttc = mqtt.Client()
mqttc.connect(broker, 1883, 60)

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
ref=255
while True:
   try:
    ii=ii+1
    if ii%500==0:
        ref = (ref+255)%(255*2)
    #time.sleep(0.1)
    data = connection.recv(8)
    data0.value[0]= 0.01*(ref-struct.unpack('d',data)[0])
    mqttc.publish("sea/test",str(struct.unpack('d',data)[0]))
    #publish.single("sea/test", str(struct.unpack('d',data)[0]), hostname=HOSTNAME)
    #print(data0.value[0])
    sock_out.sendall(data0) #str(ii*0.1))
   except KeyboardInterrupt:
       pass
