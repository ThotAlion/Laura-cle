#!/usr/bin/env python3

# library for Laura
import json,time,requests
import numpy as np

# doc : 
# https://docs.poppy-project.org/en/programming/rest.html

# robots api call
def enableMotors(robotIP):
    if type(robotIP) is str:
        robotIP = [robotIP]
    for robot in robotIP:
        if len(robot)>0:
            for m in ["m1","m2","m3","m4","m5","m6"]:
                url = "http://"+robot+"/motors/"+m+"/registers/compliant/value.json"
                response = requests.post(url, data="false", headers={'Content-type': 'application/json'})
def disableMotors(robotIP):
    if type(robotIP) is str:
        robotIP = [robotIP]
    for robot in robotIP:
        if len(robot)>0:
            for m in ["m1","m2","m3","m4","m5","m6"]:
                url = "http://"+robot+"/motors/"+m+"/registers/compliant/value.json"
                response = requests.post(url, data="true", headers={'Content-type': 'application/json'})
def setPos(robotIP,listPositions):
    if type(robotIP) is str:
        robotIP = [robotIP]
    for robot in robotIP:
        if len(robot)>0:
            listMotors = ["m1","m2","m3","m4","m5","m6"]
            for im in range(len(listMotors)):
                url = "http://"+robot+"/motors/"+listMotors[im]+"/registers/goal_position/value.json"
                response = requests.post(url, data=str(listPositions[im]), headers={'Content-type': 'application/json'})

def getPos(robotIP):
    listMotors = ["m1","m2","m3","m4","m5","m6"]
    listPos = []
    for im in range(len(listMotors)):
        url = "http://"+robotIP+"/motors/"+listMotors[im]+"/registers/present_position/value.json"
        response = requests.get(url, headers={'Content-type': 'application/json'})
        # print(response.text)
        a = json.loads(response.text)
        listPos.append(round(a["present_position"]))
    return listPos

def setMaxSpeed(robotIP):
    if type(robotIP) is str:
        robotIP = [robotIP]
    for robot in robotIP:
        if len(robot)>0:
            listMotors = ["m1","m2","m3","m4","m5","m6"]
            for im in range(len(listMotors)):
                url = "http://"+robot+"/motors/"+listMotors[im]+"/registers/moving_speed/value.json"
                response = requests.post(url, data="0", headers={'Content-type': 'application/json'})
def setLED(robotIP,motorName,color):
    if type(robotIP) is str:
        robotIP = [robotIP]
    for robot in robotIP:
        if len(robot)>0:
            url = "http://"+robot+"/motors/"+motorName+"/registers/led/value.json"
            # d = '{"led":"'+color+'"}'
            d='"'+color+'"'
            response = requests.post(url, data=d, headers={'Content-type': 'application/json'})

def getReg(robotIP,motorName,reg):
    if type(robotIP) is str:
        robotIP = [robotIP]
    for robot in robotIP:
        if len(robot)>0:
            url = "http://"+robot+"/motors/"+motorName+"/registers/"+reg+"/value.json"
            response = requests.get(url)
            print(response.text)

def motorGoto(robotIP,listPositions,duration):
    if type(robotIP) is str:
        robotIP = [robotIP]
    for robot in robotIP:
        if len(robot)>0:
            url = "http://"+robot+"/motors/goto.json"
            data = json.dumps({
                "motors": ["m1","m2","m3","m4","m5","m6"],
                "positions": listPositions,
                "duration": duration,
                "wait": "false",
            })
            h = {'Content-type': 'application/json'}
            response = requests.post(url, data=str(data), headers=h)
    
def playTape(robotIP,tapeName):
    if type(robotIP) is str:
        robotIP = [robotIP]
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