import pyttsx3
from gtts import gTTS
from io import BytesIO

engine = pyttsx3.init()
engine.setProperty('rate', 150) # setting up new voice rate, the speed of the voice
engine.setProperty('volume', 1.0) # setting up volume level  between 0 and 1
voices = engine.getProperty('voices') #getting details of current voice, get the voice property 
engine.setProperty('voice', voices[11].id)

def speak(text):

    engine.say(text)
    
    if engine._inLoop:
        engine.endLoop()
    else:
        engine.runAndWait()

class Speech():
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 100) # setting up new voice rate, the speed of the voice
        self.engine.setProperty('volume', 1.0) # setting up volume level  between 0 and 1
        voices = self.engine.getProperty('voices') #getting details of current voice, get the voice property 
        self.engine.setProperty('voice', 'mb-en1')

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

class TextToSpeech():
    def speak(self, text):
        tts = gTTS(text=text, lang="en")
        fp = BytesIO()
        tts.write_to_fp(fp)

