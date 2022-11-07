#!/usr/bin/env python3

from lauraTools import *

#######################################
# robotIP = "10.0.0.101:8080"
robotIP = "10.0.0.110:8080"
# robotIP = ["10.0.0.105:8080","10.0.0.101:8080"]
#######################################

enableMotors(robotIP)
setMaxSpeed(robotIP)
playTape(robotIP,"chore")
disableMotors(robotIP)