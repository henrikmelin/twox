import RPi.GPIO as GPIO
import time, sys, os, signal, urllib2, urllib
from subprocess import call

# Get some bash variables
server    = os.getenv('TWOX_LOG_SERVER')
location  = os.getenv('TWOX_LOG_DOOR_LOCATION')
home      = os.getenv('HOME')

# Log a change of door state to our log server
def log_door(state) :
    event = 'closed'
    if (state == True) : event = 'opened'
    try:
        args = {'location': location, 'event': event}
        response = urllib2.urlopen('http://' + server + '/log/?' + urllib.urlencode(args))
    except:
        print('Could not log!')

file = '/home/pi/401342__ckvoiceover__countdown.wav'
file = '/home/pi/213284__aderumoro__hello-2-female-friendly.wav'

# Init the door sensor
door_pin = 23
GPIO.setmode(GPIO.BCM) 
GPIO.setup(door_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP) 

isOpen = None
oldIsOpen = None 

while True: 
    oldIsOpen = isOpen 
    isOpen = GPIO.input(door_pin)
    if (isOpen and (isOpen != oldIsOpen)):  
        print("Closed")
        log_door(False)
        #call(["aplay", file])
    elif (isOpen != oldIsOpen):  
        print "OPEN!"  
        log_door(True)
        call(["aplay", file])
        #execfile( "led.py")

    time.sleep(0.1)
