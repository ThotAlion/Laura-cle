import pyttsx3

synthesizer = pyttsx3.init()

voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_FR-FR_JULIE_11.0'

voices = synthesizer.getProperty('voices')
for voice in voices: 
    print("Voice:") 
    print("ID: %s" %voice.id) 
    print("Name: %s" %voice.name) 
    print("Age: %s" %voice.age) 
    print("Gender: %s" %voice.gender) 
    print("Languages Known: %s" %voice.languages)

synthesizer.setProperty('voice', voice_id)
rate = synthesizer.getProperty('rate')
print(rate)
synthesizer.setProperty('rate', 210)

synthesizer.say("Pouette pouette camembert.") 
synthesizer.runAndWait() 
synthesizer.stop()