#!/usr/bin/env python3

import json,queue,sys,time,keyboard,os,vlc,requests
import sounddevice as sd
import vosk,openai,pyttsx3
import numpy as np

# init speech synthesis
synthesizer = pyttsx3.init()
voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_FR-FR_JULIE_11.0'
synthesizer.setProperty('voice', voice_id)
synthesizer.setProperty('rate', 210)

def talk(text):
    global synthesizer,q
    print(text)
    synthesizer.say(text) 
    synthesizer.runAndWait() 
    synthesizer.stop()
    q.queue.clear()

# init robot engine

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
    listMotors = ["m1","m2","m3","m4","m5","m6"]
    for im in range(len(listMotors)):
        url = "http://"+robotIP+"/motors/"+listMotors[im]+"/registers/moving_speed/value.json"
        response = requests.post(url, data="0", headers={'Content-type': 'application/json'})
def setLED(robotIP,motorName,color):
    url = "http://"+robotIP+"/motors/"+motorName+"/registers/led/value.json"
    response = requests.post(url, data=color, headers={'Content-type': 'application/json'})
    # print(response.text)

def getReg(robotIP,motorName,reg):
    url = "http://"+robotIP+"/motors/"+motorName+"/registers/"+reg+"/value.json"
    response = requests.get(url)
    # print(response.text)

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
###################################
robotIP = "10.0.0.101:8080"
###################################
disableMotors(robotIP)
setMaxSpeed(robotIP)

# init state machine
state = 0
goon = True

# init vosk
q = queue.Queue()
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))
model = vosk.Model(model_name="vosk-model-small-fr-0.22")

pos= []
with sd.RawInputStream(samplerate=44100, blocksize = 8000, device=1, dtype='int16',channels=1, callback=callback):
    rec = vosk.KaldiRecognizer(model, 44100)
    while goon:
        ###################################################
        # HEARING STATE
        if state == 0:
            data = q.get()
            if rec.AcceptWaveform(data):
                a = json.loads(rec.Result())
                if "text" in a and len(a["text"])>0:
                    inputText = a["text"]
                    print(inputText)
                    if inputText=="nouveau":
                        state = 1
                    elif inputText=="top":
                        state = 2
                    elif inputText=="lancée":
                        state = 3
                    elif inputText=="désactiver":
                        state = 4
                    elif inputText=="quitter":
                        goon=False

        ###################################################
        # NOUVEAU FICHIER
        elif state == 1:
            f = open('tapes/chore.txt','w',encoding='utf-8')
            f.close()
            talk("Nouveau fichier.")
            state = 0
        
        ###################################################
        # ajouter pause
        elif state == 2:
            pos = getPos(robotIP)
            f = open('tapes/chore.txt','a',encoding='utf-8')
            line = '30 '+' '.join(str(x) for x in pos)+'\n'
            print(line)
            f.write(line)
            f.close()
            talk("OK.")
            state = 0

        ###################################################
        # jouer chore
        elif state == 3:
            talk("go.")
            enableMotors(robotIP)
            setMaxSpeed(robotIP)
            playTape(robotIP,"chore")
            disableMotors(robotIP)
            talk("fini.")
            state = 0

        ###################################################
        # desactiver
        elif state == 4:
            disableMotors(robotIP)
            talk("Robot désactivé.")
            state = 0

        


        ###################################################
        # ESCAPE
        if keyboard.is_pressed('q'):
            goon=False

        time.sleep(0.1)
        

disableMotors(robotIP)
talk("Bonne soirée.")