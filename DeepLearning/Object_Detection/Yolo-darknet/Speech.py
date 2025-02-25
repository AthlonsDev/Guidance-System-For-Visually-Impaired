import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 100) # setting up new voice rate, the speed of the voice
engine.setProperty('volume', 1.0) # setting up volume level  between 0 and 1
voices = engine.getProperty('voices') #getting details of current voice, get the voice property 
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
        

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

