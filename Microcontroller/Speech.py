import pyttsx3
engine = pyttsx3.init()
engine.say("I will speak this text")
engine.runAndWait()

class Speech():
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('English', voices[0].id)

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()