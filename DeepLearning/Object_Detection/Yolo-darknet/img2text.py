import Speech_online as sp
from transformers import pipeline

def img_to_text(pic_path):
    captioner = pipeline("image-to-text",model="Salesforce/blip-image-captioning-base")
    caption = captioner(pic_path)
    ## [{'generated_text': 'two birds are standing next to each other '}]

    result = caption[0]['generated_text']
    print(result)
    sp.speak(result)

