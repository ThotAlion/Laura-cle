#!/usr/bin/env python3

import json,queue,sys,time
import sounddevice as sd
import vosk,openai,pyttsx3

fkey = open('key.txt','r')

openai.api_key = fkey.readline()
print(openai.api_key)

synthesizer = pyttsx3.init()

voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_FR-FR_JULIE_11.0'
synthesizer.setProperty('voice', voice_id)
synthesizer.setProperty('rate', 210)

nom = "Laura"
conv = nom+" est très heureuse. Elle est spécialiste en expressions idiomatiques françaises.\n"

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

try:
    print("Chargement du modèle :")
    # model = vosk.Model(model_name="vosk-model-fr-0.22")
    model = vosk.Model(model_name="vosk-model-small-fr-0.22")

    with sd.RawInputStream(samplerate=44100, blocksize = 8000, device=1, dtype='int16',channels=1, callback=callback):
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
    f = open("conversations/"+str(int(time.time()))+'.txt','w',encoding='utf-8')
    f.write(conv)
    f.close()
    print('\nDone')
except Exception as e:
    print(str(e))