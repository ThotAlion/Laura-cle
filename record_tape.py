#!/usr/bin/env python3

import json,queue,sys,time,keyboard,os
import sounddevice as sd
import vosk,pyttsx3
import numpy as np
from lauraTools import *

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

###################################
robotIP = "10.0.0.110:8080"
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
            os.system("py -3.8 .\play_chore.py")
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