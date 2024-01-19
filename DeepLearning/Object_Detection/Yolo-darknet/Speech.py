import pyttsx3
# from gtts import gTTS
from io import BytesIO


# engine = pyttsx3.init()
# engine.runAndWait() # this is needed to initialize the engine and wait for it to finish initializing

class Speech():
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150) # setting up new voice rate, the speed of the voice
        self.engine.setProperty('volume', 1.0) # setting up volume level  between 0 and 1
        voices = self.engine.getProperty('voices') #getting details of current voice, get the voice property 
        self.engine.setProperty('English', voices[1].id)
    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

class TextToSpeech():
    def speak(self, text):
        tts = gTTS(text=text, lang="en")
        fp = BytesIO()
        tts.write_to_fp(fp)


def main():
    sp = Speech()
    # sp.say("Hello world!")
    # engine.runAndWait()
    tts = TextToSpeech()
    tts.speak("Hello world!")
    


if __name__ == "__main__":
    main()
