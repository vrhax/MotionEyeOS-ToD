#!/usr/local/bin/python

# modified python script by Murray @ https://blog.ligos.net/2016-04-18/Day-Night-Cycle-For-MotionEye.html
# modified python script by Pi up My Life @ https://pimylifeup.com/raspberry-pi-light-sensor/
# EDITOR=nano crontab -e
# 02,07,12,17,22,27,32,37,42,47,52,57 * * * * /usr/bin/python /data/ToD.py >> /var/log/daynight.log

import RPi.GPIO as GPIO
import time
import os
import os.path
import shutil

__author__ = 'Gus (Adapted from Adafruit)'
__license__ = "GPL"
__maintainer__ = "pimylifeup.com"

GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit
pin_to_circuit = 7
threshold = 7500

#Current state of day / night is stored in this file
dayAndNightStateFile = '/data/ToD/dayornight'

def copyConfigFiles(suffix):
        print "Updating config files ..."
        if os.path.isfile("/data/etc/motion.conf." + suffix):
                shutil.copyfile("/data/etc/motion.conf." + suffix, "/data/etc/motion.conf")
        if os.path.isfile("/data/etc/motioneye.conf." + suffix):
                shutil.copyfile("/data/etc/motioneye.conf." + suffix, "/data/etc/motioneye.conf")
        if os.path.isfile("/data/etc/raspimjpeg.conf." + suffix):
                shutil.copyfile("/data/etc/raspimjpeg.conf." + suffix, "/data/etc/raspimjpeg.conf")
        if os.path.isfile("/data/etc/streameye.conf." + suffix):
                shutil.copyfile("/data/etc/streameye.conf." + suffix, "/data/etc/streameye.conf")
        if os.path.isfile("/data/etc/smb.conf." + suffix):
                shutil.copyfile("/data/etc/smb.conf." + suffix, "/data/etc/smb.conf")
        if os.path.isfile("/data/etc/thread-1.conf." + suffix):
                shutil.copyfile("/data/etc/thread-1.conf." + suffix, "/data/etc/thread-1.conf")
        if os.path.isfile("/data/etc/watch.conf." + suffix):
                shutil.copyfile("/data/etc/watch.conf." + suffix, "/data/etc/watch.conf")
        if os.path.isfile("/data/etc/watch.conf." + suffix):
                shutil.copyfile("/data/etc/watch.conf." + suffix, "/data/etc/watch.conf")

def restartMotionEye():
        print "Restarting MotionEye ..."
        os.system("/etc/init.d/S84streameye restart")
        os.system("/etc/init.d/S85motioneye restart")

def readLineOfFile(path):
        print "Fetching Day/Night state ..."
        if not os.path.isfile(path): return ""
        f = open(path, "r")
        result = f.readline()
        f.close()
        return result

def updateContentsOfFile(path, data):
        print "Updating Day/Night state ..."
        f = open(path, "w")
        f.write(data)
        f.close()

def rc_time (pin_to_circuit):
        print "Probing GPIO light sensor ..."
        count = 0
        #Output on the pin for
        GPIO.setup(pin_to_circuit, GPIO.OUT)
        GPIO.output(pin_to_circuit, GPIO.LOW)
        #5 minutes = 1000 (milliseconds) * 60 (seconds) * 1 (minute)
        time.sleep(0.1)

        #Change the pin back to input
        GPIO.setup(pin_to_circuit, GPIO.IN)

        #Count until the pin goes high
        while (GPIO.input(pin_to_circuit) == GPIO.LOW):
                count += 1
        return count

#Catch when script is interupted, cleanup correctly
try:
        # Main loop
        print "Checking ..."
        rvalue = rc_time(pin_to_circuit)
        fileDayOrNight = readLineOfFile(dayAndNightStateFile)
        if rvalue > threshold:
                currentDayOrNight = "night"
        else:
                currentDayOrNight = "day"
        if fileDayOrNight != currentDayOrNight:
                copyConfigFiles(currentDayOrNight)
                restartMotionEye()
                updateContentsOfFile(dayAndNightStateFile, currentDayOrNight)
        else:
                print "No change necessary ... "

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
