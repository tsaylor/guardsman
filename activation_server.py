import RPi.GPIO as GPIO
import time
import serial
import urllib2
from wiegand import serial_to_wiegand

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)  # controls the relay for tool activation

RESOURCE = 'doors'
ACTIVATION_SECONDS = 1
AUTH_SERVER_URL = 'http://10.100.200.100:3000'
AUTH_SERVER_URL = 'http://localhost:3000'

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)


def activate_resource():
    GPIO.output(11, GPIO.HIGH)
    time.sleep(ACTIVATION_SECONDS)
    GPIO.output(11, GPIO.LOW)

while True:
    input = port.read(16)
    if len(input) > 0:
        wiegand_tag = serial_to_wiegand(input)
        try:
            response = urllib2.urlopen(
                '%s/auth/%s/%s' % (AUTH_SERVER_URL, RESOURCE, wiegand_tag)
            )
        except urllib2.HTTPError as response:
            if response.code != 401:
                raise
        else:
            if response.getcode() == 200:
                activate_resource()