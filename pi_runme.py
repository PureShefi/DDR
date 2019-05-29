#!/usr/bin/python
import RPi.GPIO as GPIO
import socket
from time import time, sleep

server_ip = '192.168.0.2'
power = (22, 9, 11)
inputs = (23, 24, 25, 8)
pressed = [False, False, False, False]
count = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def configure_ports():
        for pin in power:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)

        for pin in inputs:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


configure_ports()
last_set = time()

while True:
    if time() - last_set > 10:
        configure_ports()
        last_set = time()

    for input_index, input in enumerate(inputs):
        input_status = GPIO.input(input)
        if input_status == 1:
            if not pressed[input_index]:
                pressed[input_index] = True
                sock.sendto(str(input_index), (server_ip, 1337))
                print "Pressed: ", input, count
                count +=1
        else:
            pressed[input_index] = False
    sleep(0.05)