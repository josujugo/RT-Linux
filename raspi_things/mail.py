#!/usr/bin/python3
import socket
import smtplib
import os
import sys

# or uncomment the following lines and set secret values here
sender_address = 'josujugo.test@gmail.com'
sender_password = 'thisis_test1'
sender_server = 'smtp.gmail.com'
sender_port = 587
recipient_address = "josujugo@gmail.com"

def get_device_ip_address():

    try: 
        if os.name == "nt":
            # On Windows
            result = "Running on Windows"
            hostname = socket.gethostname()
            result += "\nHostname:  " + hostname
            host = socket.gethostbyname(hostname)
            result += "\nHost-IP-Address:" + host
            return result

        elif os.name == "posix":
            """
            gw = os.popen("ip -4 route show default").read().split()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((gw[2], 0))
            ipaddr = s.getsockname()[0]
            gateway = gw[2]
            host = socket.gethostname()
            result = "OS:\t\tRaspbian\nIP:\t\t" + ipaddr + "\nGateway:\t" + gateway + "\nHost:\t\t" + host
            """
            result="158.227.6.57 "
            return result
        
        else:
            result = os.name + " not supported yet."
            return result
    except:
        return "Could not detect ip address"

def send_email(text):
    try:
        message = "From: " + sender_address + "\nTo: " + recipient_address + "\nSubject: Device Information\n\n" + text 

        server = smtplib.SMTP(sender_server, sender_port)
        server.ehlo()
        server.set_debuglevel(True)
        server.starttls()
        server.login(sender_address, sender_password)
        server.sendmail(sender_address, recipient_address, message)
        server.close()
        print("Message sent:\n", message)

    except:
        print("failed to send email")

message = get_device_ip_address()
print(message)
print("Sending email, can take a while.")
send_email(message)
print("Done.")

sys.exit()
