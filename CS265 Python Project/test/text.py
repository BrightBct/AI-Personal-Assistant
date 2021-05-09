import speech_recognition as sr
import re
import time
import os
import logging
import pandas as pd
import random

from gtts import gTTS
from essential_generators import DocumentGenerator
from random_word import RandomWords
from playsound import playsound
from nltk.corpus import wordnet

logging.captureWarnings(True)
rw = RandomWords()
gen = DocumentGenerator()
r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

print("Start Practice\n")
df = pd.read_csv('../word/list_of_word.csv')
load_list = df['All_Word'].tolist()
while True:
    number_random = random.randint(0, len(load_list) - 1)
    generate_word = load_list[number_random]
    synset = wordnet.synsets(generate_word)
    try:
        synset[0].definition()
    except IndexError:
        continue
    my_obj = gTTS(text=generate_word, lang='en', slow=False)
    my_obj.save("audio/audio.mp3")
    speak_word = ''
    with mic as source:
        print("Say \""+generate_word+"\" (say \"turn off program\" to end program)")
        print("...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            speak_word = r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Please say something!")
            speak_word = "-999"
    if "turn off program" in speak_word:
        print("turn off program")
        break
    elif speak_word == "-999":
        continue
    elif generate_word == speak_word:
        print("Correct")
    elif generate_word != speak_word:
        print("Word is \"" + generate_word, end="\" ")
        print("but you said " + speak_word)
    print("Please Listen to AI")
    time.sleep(1)
    playsound('audio/audio.mp3')
    print("...")
    print('The meaning of the word : ' + synset[0].definition())
    print()
    time.sleep(1)
    os.remove('audio/audio.mp3')
