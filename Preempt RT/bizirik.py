#!/usr/bin/python3
import datetime  # Importing the datetime library
import telepot   # Importing the telepot library
import subprocess
from telepot.loop import MessageLoop    # Library function to communicate with telegram bot
import RPi.GPIO as GPIO     # Importing the GPIO library to use the GPIO pins of Raspberry pi
from time import sleep      # Importing the time library to provide the delays in program

red_led_pin = 21                # Initializing GPIO 21 for red led
green_led_pin = 20                # Initializing GPIO 20 for green led

GPIO.setmode(GPIO.BCM)      # Use Board pin numbering
GPIO.setup(red_led_pin, GPIO.OUT) # Declaring the GPIO 21 as output pin
GPIO.setup(green_led_pin, GPIO.OUT) # Declaring the GPIO 20 as output pin

now = datetime.datetime.now() # Getting date and time

def handle(msg):
    chat_id = msg['chat']['id'] # Receiving the message from telegram
    command = msg['text']   # Getting text from the message

    print ('Received:')
    print(command)

    # Comparing the incoming message to send a reply according to it
    if command == '/hi':
        bot.sendMessage (chat_id, str("Hi! MakerPro"))
    elif command == '/time':
        bot.sendMessage(chat_id, str("Time: ") + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second))
    elif command == '/date':
        bot.sendMessage(chat_id, str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))
    elif command == '/red_1':
        bot.sendMessage(chat_id, str("Red led is ON"))
        GPIO.output(red_led_pin, True)
    elif command == '/red_0':
        bot.sendMessage(chat_id, str("Red led is OFF"))
        GPIO.output(red_led_pin, False)
    elif command == '/green_1':
        bot.sendMessage(chat_id, str("Green led is ON"))
        GPIO.output(green_led_pin, True)
    elif command == '/green_0':
        bot.sendMessage(chat_id, str("Green led is OFF"))
        GPIO.output(green_led_pin, False)

    elif command == '/ifconfig':
        bot.sendMessage(chat_id, str("Received ifconfig"))
        result = subprocess.run(['/usr/sbin/ifconfig'], stdout=subprocess.PIPE)
        bot.sendMessage(chat_id, str("Received ifconfig")+str(result.stdout))
        print(result.stdout.decode('utf-8'))
        bot.sendMessage(chat_id, result.stdout.decode('utf-8'))
# Insert your telegram token below
sleep(10) 
bot = telepot.Bot('1889144993:AAESpnY0TJuKugVvMUhpW85HgXg4ywNuoro')
print (bot.getMe())

# Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
MessageLoop(bot, handle).run_as_thread()
print ('Listening....')

while 1:
    sleep(10)
