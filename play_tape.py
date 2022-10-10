#!/usr/bin/env python3

import json,time,requests
import numpy as np

# init robot engine
robotIP = "10.0.0.105:8080"
def enableMotors(robotIP):
    for m in ["m1","m2","m3","m4","m5","m6"]:
        url = "http://"+robotIP+"/motors/"+m+"/registers/compliant/value.json"
        response = requests.post(url, data="false", headers={'Content-type': 'application/json'})
def disableMotors(robotIP):
    for m in ["m1","m2","m3","m4","m5","m6"]:
        url = "http://"+robotIP+"/motors/"+m+"/registers/compliant/value.json"
        response = requests.post(url, data="true", headers={'Content-type': 'application/json'})
def setPos(robotIP,listPositions):
    listMotors = ["m1","m2","m3","m4","m5","m6"]
    for im in range(len(listMotors)):
        url = "http://"+robotIP+"/motors/"+listMotors[im]+"/registers/goal_position/value.json"
        response = requests.post(url, data=str(listPositions[im]), headers={'Content-type': 'application/json'})
def setMaxSpeed(robotIP):
    listMotors = ["m1","m2","m3","m4","m5","m6"]
    for im in range(len(listMotors)):
        url = "http://"+robotIP+"/motors/"+listMotors[im]+"/registers/moving_speed/value.json"
        response = requests.post(url, data="0", headers={'Content-type': 'application/json'})
def setLED(robotIP,motorName,color):
    url = "http://"+robotIP+"/motors/"+motorName+"/registers/led/value.json"
    response = requests.post(url, data=color, headers={'Content-type': 'application/json'})

def getReg(robotIP,motorName,reg):
    url = "http://"+robotIP+"/motors/"+motorName+"/registers/"+reg+"/value.json"
    response = requests.get(url)

def motorGoto(robotIP,listPositions,duration):
    url = "http://"+robotIP+"/motors/goto.json"
    data = json.dumps({
        "motors": ["m1","m2","m3","m4","m5","m6"],
        "positions": listPositions,
        "duration": duration,
        "wait": "false",
    })
    h = {'Content-type': 'application/json'}
    response = requests.post(url, data=str(data), headers=h)
    return response.json()
def playTape(robotIP,tapeName):
    f = open("tapes/"+tapeName+".txt","r")
    lines = f.readlines()
    f.close()
    enableMotors(robotIP)
    pos_old = None
    pos = None
    for line in lines:
        a = line.split()
        if len(a)==7:
            t0 = time.time()
            dur = float(a[0])/10
            if pos is None:
                pos = np.array([float(a[1]),float(a[2]),float(a[3]),float(a[4]),float(a[5]),float(a[6])])
                dur = 0.1
                pos_old = pos.copy()
            else:
                pos = np.array([float(a[1]),float(a[2]),float(a[3]),float(a[4]),float(a[5]),float(a[6])])
                dur = float(a[0])/10
            while time.time()<t0+dur:
                b = (time.time()-t0)/dur
                setPos(robotIP,((b*pos)+(1-b)*pos_old).tolist())
            pos_old = pos.copy()

enableMotors(robotIP)
setMaxSpeed(robotIP)
playTape(robotIP,"candle2001")
disableMotors(robotIP)