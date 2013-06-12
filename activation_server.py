import time
import urllib2
import argparse
import threading

import yaml
import serial
import RPi.GPIO as GPIO
from lib.wiegand import serial_to_wiegand

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--settings", help="Path to the settings file", default="conf/settings.yaml")
args = parser.parse_args()

settings = yaml.load(open(args.settings))

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)  # controls the relay for tool activation

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1.0)
resource_lock = threading.Lock()
seconds_left = 1


def activate_resource():
    global seconds_left, resource_lock
    seconds_left = settings['activation_seconds']
    if resource_lock.acquire(False):  # non-blocking lock acquisition
        GPIO.output(11, GPIO.HIGH)
        while seconds_left > 0:
            time.sleep(1)
            seconds_left = seconds_left - 1
            print "seconds left: %d" % seconds_left
        GPIO.output(11, GPIO.LOW)
        resource_lock.release()

while True:
    input = port.read(16)
    if len(input) > 0:
        wiegand_tag = serial_to_wiegand(input)
        try:
            response = urllib2.urlopen(
                '%s/auth/%s/%s' % (settings['auth_server_url'], settings['resource'], wiegand_tag)
            )
        except urllib2.HTTPError as response:
            if response.code != 401:
                raise
        else:
            if response.getcode() == 200:
                activate_thread = threading.Thread(target=activate_resource)
                activate_thread.start()

