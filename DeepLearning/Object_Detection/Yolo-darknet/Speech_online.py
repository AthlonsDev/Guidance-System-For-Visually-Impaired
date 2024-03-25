from gtts import gTTS
import time
import os

# myText = "Hello, I am a text to speech program"
# output = gTTS(text=myText, lang='en', slow=False)
# output.save("output.mp3")
# os.system("mpg123 output.mp3")

def speak(text):
    time.sleep(1)
    output = gTTS(text=text, lang='en', slow=False)
    output.save("output.mp3")
    os.system("mpg123 output.mp3")