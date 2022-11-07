#!/usr/bin/env python3

import json,queue,sys,time,keyboard,os,vlc,requests
import sounddevice as sd
import vosk,openai,pyttsx3
import numpy as np
from lauraTools import *

# init openai GPT-3
openai_connected = True
fkey = open('key.txt','r')
openai.api_key = fkey.readline()
nom = "Laura"
conv = nom+" est très heureuse. Elle est spécialiste en expressions idiomatiques françaises.\n"

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

# init vlc
vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()
player.toggle_fullscreen()

def play_jingle():
    global vlc_instance
    media = vlc_instance.media_new("jingle.wav")
    player.set_media(media)
    player.play()
    time.sleep(4.0)

# init robots engine
##################################################
if True:
    robotFaceIP = "10.0.0.112:8080"
    robotColzaIP = "10.0.0.110:8080"
    robotCandleA =  "10.0.0.101:8080"
    robotCandleB =  "10.0.0.105:8080"
else:
    robotFaceIP = ""
    robotCandleA =  ""
    robotCandleB =  ""
visage = False

##################################################
disableMotors(robotCandleA)
enableMotors(robotFaceIP)
setMaxSpeed(robotFaceIP)

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
# model = vosk.Model(model_name="vosk-model-fr-0.22")
talk("Initialisation du système.")
with sd.RawInputStream(samplerate=44100, blocksize = 8000, device=1, dtype='int16',channels=1, callback=callback):
    rec = vosk.KaldiRecognizer(model, 44100)
    getReg(robotFaceIP,"m2","led")
    
    while goon:
        ###################################################
        # IDLE STATE
        if state == 0:
            time.sleep(0.1)
            # media = vlc_instance.media_new("images/logo_idiomatique.jpg")
            # player.set_media(media)
            # player.play()
            # playTape(robotFaceIP,"listen")
            if keyboard.is_pressed('t'):
                if visage:
                    playTape(robotFaceIP,"listen2speak")
                print("En écoute")
                setLED(robotFaceIP,"m2","blue")
                q.queue.clear()
                state = 1
            
        ###################################################
        # HEARING STATE
        elif state == 1:
            if player.is_playing():
                player.stop()
            data = q.get()
            if rec.AcceptWaveform(data):
                a = json.loads(rec.Result())
                if "text" in a and len(a["text"])>0:
                    inputText = a["text"]
                    print(inputText)
                    if inputText.find("top")>=0:
                        state = 2
                    elif inputText.find("séquence un")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 3
                    elif inputText.find("séquence de")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 4
                    elif inputText.find("séquence trois")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 5
                    elif inputText.find("séquence quatre")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 6
                    elif inputText.find("séquence cinq")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 7
                    elif inputText.find("séquence six")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 8
                    elif inputText.find("séquence sept")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 9
                    elif inputText.find("séquence huit")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 10
                    elif inputText.find("séquence neuf")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 11
                    elif inputText == "séquence dix":
                        setLED(robotFaceIP,"m2","off")
                        state = 12
                    elif inputText.find("séquence onze")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 13
                    elif inputText.find("séquence douze")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 14
                    elif inputText.find("séquence treize")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 15
                    elif inputText.find("séquence quatorze")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 16
                    elif inputText.find("séquence quinze")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 17
                    elif inputText.find("séquence seize")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 18
                    elif inputText.find("séquence dix-sept")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 19
                    elif inputText.find("séquence dix-huit")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 20
                    elif inputText.find("séquence dix-neuf")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 21
                    elif inputText=="séquence vingt":
                        setLED(robotFaceIP,"m2","off")
                        state = 22
                    elif inputText.find("séquence vingt et un")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 23
                    elif inputText.find("séquence vingt-deux")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 24
                    elif inputText.find("séquence vingt-trois")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 25
                    elif inputText.find("séquence vingt-quatre")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 26
                    elif inputText.find("séquence vingt-cinq")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 27
                    elif inputText.find("séquence vingt-six")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 28
                    elif inputText.find("séquence vingt-sept")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 29
                    elif inputText.find("séquence vingt-huit")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 30
                    elif inputText.find("séquence vingt-neuf")>=0:
                        setLED(robotFaceIP,"m2","off")
                        state = 31
                    elif inputText=="séquence trente":
                        setLED(robotFaceIP,"m2","off")
                        state = 32
                    elif inputText=="quitter":
                        setLED(robotFaceIP,"m2","off")
                        goon = False
                    else:
                        setLED(robotFaceIP,"m2","off")
                        if openai_connected:
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
                            talk(response.choices[0].text)
                            setLED(robotFaceIP,"m2","blue")
        ###################################################
        # DEPART
        elif state == 2:
            talk("c'est parti")
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 1 : le putois
        elif state == 3:
            talk("On est parti pour le jeu numéro 1 !")
            play_jingle()
            talk("Essayez de deviner l'expression de la langue française que je vais mi mai.")
            time.sleep(1.0)
            media = vlc_instance.media_new("putois.wav")
            player.set_media(media)
            player.play()
            enableMotors(robotColzaIP)
            playTape(robotColzaIP,"putois")
            disableMotors(robotColzaIP)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 2 : poser
        elif state == 4:
            talk("C'est parti pour le jeu numéro 2 !")
            play_jingle()
            talk("Vous allez voir une vidéo d'un robot réalisant une expression française avec une boîte mystère. Le but est de devinez ce qu'il y a dans la boîte.")
            time.sleep(1.0)
            media = vlc_instance.media_new("poser.mp4")
            player.set_media(media)
            player.play()
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 3 : lever
        elif state == 5:
            talk("Voici l'enigme numéro 3 !")
            play_jingle()
            talk("Vous allez voir une vidéo d'un robot réalisant une expression française avec une boîte mystère. Le but est de devinez ce qu'il y a dans la boîte.")
            time.sleep(1.0)
            media = vlc_instance.media_new("lever.mp4")
            player.set_media(media)
            player.play()
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 4 : prendre un rateau
        elif state == 6:
            talk("Voici l'énigme numéro 4 !")
            play_jingle()
            talk("Vous allez voir une vidéo d'un robot réalisant une expression de la langue française. Devinez la.")
            time.sleep(1.0)
            media = vlc_instance.media_new("rateau.mp4")
            player.set_media(media)
            player.play()
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 5 : décrocher le cocotier
        elif state == 7:
            talk("C'est parti pour l'épreuve numéro 5")
            play_jingle()
            talk("Vous allez voir une vidéo d'un robot réalisant une expression de la langue française. Devinez la.")
            time.sleep(1.0)
            media = vlc_instance.media_new("cocotier.mp4")
            player.set_media(media)
            player.play()
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 6 : lacher un caisse
        elif state == 8:
            talk("Attention... énigme numéro 6!")
            play_jingle()
            talk("Vous allez voir une vidéo d'un robot réalisant plusieurs expressions de la langue française. Devinez les toutes !")
            time.sleep(1.0)
            media = vlc_instance.media_new("caisse.mp4")
            player.set_media(media)
            player.play()
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 7 : raconter des salades
        elif state == 9:
            talk("énigme spéciale : la numéro 7.")
            play_jingle()
            talk("Je vais mi mai une expression de la langue française. Essayer de la trouver !")
            time.sleep(1.0)
            if openai_connected:
                response = openai.Completion.create(
                    model="text-davinci-002",
                    prompt="Voici un conte court qui met en scène des salades :",
                    temperature=0.5,
                    max_tokens=200,
                    top_p=0.3,
                    frequency_penalty=0.5,
                    presence_penalty=0.0
                )
                talk(response.choices[0].text)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0

        ###################################################
        # Jeu 8 : donner des noms d'oiseaux
        elif state == 10:
            talk("énigme chaud chaud : la numéro 8.")
            play_jingle()
            talk("Je vais mi mai une expression de la langue française. Essayer de la trouver !")
            time.sleep(1.0)
            if openai_connected:
                response = openai.Completion.create(
                    model="text-davinci-002",
                    prompt="Voici une liste de 10 noms d'oiseaux exotiques :",
                    temperature=0.5,
                    max_tokens=200,
                    top_p=0.3,
                    frequency_penalty=0.5,
                    presence_penalty=0.0
                )
                talk(response.choices[0].text)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0

        ###################################################
        # Jeu 9 : faire revenir des petits légumes
        elif state == 11:
            talk("énigme difficile cette fois-ci : la numéro 9.")
            play_jingle()
            talk("Je vais mi mai une expression de la langue française. Essayer de la trouver !")
            time.sleep(1.0)
            if openai_connected:
                response = openai.Completion.create(
                    model="text-davinci-002",
                    prompt="Laura essaye de convaincre des haricots, des carottes, des choux et des patates qu'il faut qu'ils reviennent. Elle leur dit :",
                    temperature=0.9,
                    max_tokens=200,
                    top_p=0.3,
                    frequency_penalty=0.5,
                    presence_penalty=0.0
                )
                talk(response.choices[0].text)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0

        ###################################################
        # Jeu 10 : un robot qui mange son chapeau
        elif state == 12:
            talk("énigme image : la numéro 10.")
            play_jingle()
            talk("J'ai illustré une expression de la langue française. Essayez de deviner cette expression.")
            time.sleep(1.0)
            media = vlc_instance.media_new("images/manger chapeau.png")
            player.set_media(media)
            player.play()
            time.sleep(10.0)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 11 : un robot a côté de la plaque
        elif state == 13:
            talk("énigme image : la numéro 11.")
            play_jingle()
            talk("J'ai illustré une expression de la langue française. Essayez de deviner cette expression.")
            time.sleep(1.0)
            media = vlc_instance.media_new("images/a cote de la plaque.png")
            player.set_media(media)
            player.play()
            time.sleep(10.0)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 12 : un robot au pied du mur
        elif state == 14:
            talk("énigme image : la numéro 12.")
            play_jingle()
            talk("J'ai illustré une expression de la langue française. Essayez de deviner cette expression.")
            time.sleep(1.0)
            media = vlc_instance.media_new("images/au pied du mur.png")
            player.set_media(media)
            player.play()
            time.sleep(10.0)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 13 : un robot qui a le bras long
        elif state == 15:
            talk("énigme image : la numéro 13.")
            play_jingle()
            talk("J'ai illustré une expression de la langue française. Essayez de deviner cette expression.")
            time.sleep(1.0)
            media = vlc_instance.media_new("images/bras long.png")
            player.set_media(media)
            player.play()
            time.sleep(10.0)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 14 : un robot canon
        elif state == 16:
            talk("énigme image : la numéro 14.")
            play_jingle()
            talk("J'ai illustré une expression de la langue française. Essayez de deviner cette expression.")
            time.sleep(1.0)
            media = vlc_instance.media_new("images/canon.png")
            player.set_media(media)
            player.play()
            time.sleep(10.0)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 15 : un robot beau comme un camion
        elif state == 17:
            talk("énigme image : la numéro 15.")
            play_jingle()
            talk("J'ai illustré une expression de la langue française. Essayez de deviner cette expression.")
            time.sleep(1.0)
            media = vlc_instance.media_new("images/comme un camion.png")
            player.set_media(media)
            player.play()
            time.sleep(10.0)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 16 : un robot dans la lune
        elif state == 18:
            talk("énigme image : la numéro 16.")
            play_jingle()
            talk("J'ai illustré une expression de la langue française. Essayez de deviner cette expression.")
            time.sleep(1.0)
            media = vlc_instance.media_new("images/dans la lune.png")
            player.set_media(media)
            player.play()
            time.sleep(10.0)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 17 : un robot dans les pommes
        elif state == 19:
            talk("énigme image : la numéro 17.")
            play_jingle()
            talk("J'ai illustré une expression de la langue française. Essayez de deviner cette expression.")
            time.sleep(1.0)
            media = vlc_instance.media_new("images/dans les pommes.png")
            player.set_media(media)
            player.play()
            time.sleep(10.0)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 18 : un robot sur le carreau
        elif state == 20:
            talk("énigme image : la numéro 18.")
            play_jingle()
            talk("J'ai illustré une expression de la langue française. Essayez de deviner cette expression.")
            time.sleep(1.0)
            media = vlc_instance.media_new("images/sur le carreau.png")
            player.set_media(media)
            player.play()
            time.sleep(10.0)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 19 : un robot sur le fil du rasoir
        elif state == 21:
            talk("énigme image : la numéro 19.")
            play_jingle()
            talk("J'ai illustré une expression de la langue française. Essayez de deviner cette expression.")
            time.sleep(1.0)
            media = vlc_instance.media_new("images/sur le fil du rasoir.png")
            player.set_media(media)
            player.play()
            time.sleep(10.0)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 20 : un robot au bout du rouleau
        elif state == 22:
            talk("énigme image : la numéro 20.")
            play_jingle()
            talk("J'ai illustré une expression de la langue française. Essayez de deviner cette expression.")
            time.sleep(1.0)
            media = vlc_instance.media_new("images/au bout du rouleau.png")
            player.set_media(media)
            player.play()
            time.sleep(10.0)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 21 : un robot qui a un chat dans la gorge
        elif state == 23:
            talk("énigme image : la numéro 21.")
            play_jingle()
            talk("J'ai illustré une expression de la langue française. Essayez de deviner cette expression.")
            time.sleep(1.0)
            media = vlc_instance.media_new("images/chat dans la gorge.png")
            player.set_media(media)
            player.play()
            time.sleep(10.0)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 22 : un robot qui donne sa langue au chat
        elif state == 24:
            talk("énigme image : la numéro 22.")
            play_jingle()
            talk("J'ai illustré une expression de la langue française. Essayez de deviner cette expression.")
            time.sleep(1.0)
            media = vlc_instance.media_new("images/chat.png")
            player.set_media(media)
            player.play()
            time.sleep(10.0)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 23 : un robot qui court sur le haricot
        elif state == 25:
            talk("énigme image : la numéro 23.")
            play_jingle()
            talk("J'ai illustré une expression de la langue française. Essayez de deviner cette expression.")
            time.sleep(1.0)
            media = vlc_instance.media_new("images/court sur le haricot.png")
            player.set_media(media)
            player.play()
            time.sleep(10.0)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 24 : un robot qui fait rien
        elif state == 26:
            talk("Enigme mi mai : la numéro 24.")
            play_jingle()
            talk("Je vais mi mai une expression de de la langue française. Plusieurs réponses sont possibles.")
            time.sleep(10.0)
            talk("Voilà.")
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 25 : raconter des histoires à dormir debout
        elif state == 27:
            talk("énigme difficile cette fois-ci : la numéro 25.")
            play_jingle()
            talk("Je vais mi mai une expression de la langue française. Essayer de la trouver !")
            time.sleep(1.0)
            if openai_connected:
                response = openai.Completion.create(
                    model="text-davinci-002",
                    prompt="Voici un petit conte de fée qui parle de lits verticaux :",
                    temperature=0.9,
                    max_tokens=200,
                    top_p=0.3,
                    frequency_penalty=0.5,
                    presence_penalty=0.0
                )
                talk(response.choices[0].text)
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0

        ###################################################
        # Jeu 26 : tenir la chandelle
        elif state == 28:
            talk("On est parti pour le jeu numéro 26 !")
            play_jingle()
            talk("Essayez de deviner l'expression de la langue française que je vais mi mai.")
            time.sleep(1.0)
            media = vlc_instance.media_new("ext_2001.mp3")
            player.set_media(media)
            player.play()
            enableMotors([robotCandleA,robotCandleB])
            setMaxSpeed([robotCandleA,robotCandleB])
            playTape([robotCandleA,robotCandleB],"candle2001")
            disableMotors([robotCandleA,robotCandleB])
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0

        ###################################################
        # Jeu 27 : voir 36 chandelle
        elif state == 29:
            talk("On est parti pour le jeu numéro 27 !")
            play_jingle()
            talk("Essayez de deviner l'expression de la langue française que je vais mi mai.")
            time.sleep(1.0)
            media = vlc_instance.media_new("36chand.mp4")
            player.set_media(media)
            player.play()
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0

        ###################################################
        # Jeu 28 : passer l'arme à gauche
        elif state == 30:
            talk("On est parti pour le jeu numéro 28 !")
            play_jingle()
            talk("Vous allez voir une vidéo d'un robot réalisant une expression de la langue française. Devinez la !")
            time.sleep(1.0)
            media = vlc_instance.media_new("arme.mp4")
            player.set_media(media)
            player.play()
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0
        ###################################################
        # Jeu 29 : tremper le biscuit
        elif state == 31:
            talk("On est parti pour le jeu numéro 29 !")
            play_jingle()
            talk("Vous allez voir une vidéo d'un robot réalisant une expression de la langue française. Devinez la !")
            time.sleep(1.0)
            media = vlc_instance.media_new("biscuit.mp4")
            player.set_media(media)
            player.play()
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0    

        ###################################################
        # Jeu 30 : mettre son grain de sel
        elif state == 32:
            talk("On est parti pour le jeu numéro 30 !")
            play_jingle()
            talk("Vous allez voir une vidéo d'un robot réalisant une expression de la langue française. Devinez la !")
            time.sleep(1.0)
            media = vlc_instance.media_new("sel.mp4")
            player.set_media(media)
            player.play()
            if visage:
                playTape(robotFaceIP,"speak2listen")
            print("En idle")
            state = 0    

        else:
            goon=False
        ###################################################
        # ESCAPE
        if keyboard.is_pressed('q'):
            goon=False
        
if visage:
    disableMotors(robotFaceIP)
f = open("conversations/"+str(int(time.time()))+'.txt','w',encoding='utf-8')
f.write(conv)
f.close()
talk("Bonne soirée.")