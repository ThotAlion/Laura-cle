#!/usr/bin/env python3

import argparse
import os,json
import queue
import sounddevice as sd
import vosk
import sys

import openai
import pyttsx3

openai.api_key = "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"

synthesizer = pyttsx3.init()

voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_FR-FR_JULIE_11.0'
synthesizer.setProperty('voice', voice_id)
synthesizer.setProperty('rate', 210)

nom = "Laura"
conv = nom+" est une voyante très sûre d'elle et peut prédire l'avenir sur tout les sujets.\n"

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

try:
    print("Chargement du modèle :")
    # model = vosk.Model(model_name="vosk-model-fr-0.22")
    model = vosk.Model(model_name="vosk-model-small-fr-0.22")

    with sd.RawInputStream(samplerate=44100, blocksize = 8000, device=None, dtype='int16',channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 44100)
        print("Début de l'écoute")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                a = json.loads(rec.Result())
                if "text" in a and len(a["text"])>0:
                    inputText = a["text"]
                    print(inputText)
                    conv+="Vous: "+inputText+"\n"
                    response = openai.Completion.create(
                        model="text-davinci-002",
                        prompt=conv+nom+": ",
                        temperature=0.5,
                        max_tokens=200,
                        top_p=0.3,
                        frequency_penalty=0.5,
                        presence_penalty=0.0
                    )
                    conv+=nom+": "+response.choices[0].text+"\n"
                    print(response.choices[0].text)
                    synthesizer.say(response.choices[0].text) 
                    synthesizer.runAndWait() 
                    synthesizer.stop()
                    q.queue.clear()



except KeyboardInterrupt:
    print('\nDone')
except Exception as e:
    print(str(e))