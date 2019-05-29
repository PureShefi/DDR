import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def GpioCallback(param):
    print param, "PIN UP"


def TurnOn(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)


def TurnOff(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)


def GetInput(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    return GPIO.input(pin)


def AddCallback(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING)
    GPIO.add_event_callback(pin, GpioCallback)


print "Adding callbacks & turning on"
AddCallback(17)
TurnOn(18)

while True:
    try:
        time.sleep(1)
        print GetInput(17)
    except:
        GPIO.reset()
        print "Exiting"
