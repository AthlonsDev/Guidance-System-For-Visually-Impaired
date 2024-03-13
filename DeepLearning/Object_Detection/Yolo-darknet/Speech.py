# from dimits import Dimits
# import time
# dt = Dimits("voice-en-us-amy-low")

# def say(text):
#     # Initialize Dimits with the desired voice model

#     # Convert text to audio and play it using the aplay engine
#     dt.text_2_speech(text, engine="aplay")

    


# if "__main__" == __name__:
#     say("hello, world")

import piper as pi

model_path = "/home/athlons/piper/piper/models/piper-tts-1.0.0.onnx"
config_path = "/home/athlons/piper/piper/configs/piper-tts-1.0.0.yaml"
use_cuda = False

def say(text):
    voice = pi.PiperVoice(self, model_path, config_path, use_cuda)
    voice.synthesize_stream_raw(text, speaker_id=0, length_scale=1.0, noise_scale=0.0, noise_w=0.0, sentence_silence=0.0)

if "__main__" == __name__:
    say("hello, world")