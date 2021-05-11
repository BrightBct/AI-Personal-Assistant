import speech_recognition as sr
import time
import os
import logging
import numpy as np
import pandas as pd
import random

from gtts import gTTS
from playsound import playsound
from nltk.corpus import wordnet


def english_practice():

    logging.captureWarnings(True)
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=1)

    print("Start Practice\n")
    df = pd.read_csv('all_function/word/list_of_word.csv')
    load_list = df['All_Word'].tolist()
    df = pd.read_csv('all_function/result/correct.csv')
    correct = df['All_Word_Correct'].tolist()
    df = pd.read_csv('all_function/result/incorrect.csv')
    incorrect = df['All_Word_Incorrect'].tolist()

    while True:

        number_random = random.randint(0, len(load_list) - 1)
        generate_word = load_list[number_random]
        synset = wordnet.synsets(generate_word)

        try:
            synset[0].definition()
        except IndexError:
            continue

        my_obj = gTTS(text=generate_word, lang='en', slow=False)
        my_obj.save("all_function/audio.mp3")

        with mic as source:

            print("Say \""+generate_word+"\" (say \"turn off \" to end program)")
            print("...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

            try:
                speak_word = r.recognize_google(audio)
            except sr.UnknownValueError:
                print("Please say something!")
                speak_word = "-999"

        speak_word = speak_word.lower()
        if "turn off" in speak_word:
            print("Turn off program\n")
            break
        elif speak_word == "-999":
            continue
        elif generate_word == speak_word:
            print("Correct")
            correct.append(generate_word)
        elif generate_word != speak_word:
            print("Word is \""+generate_word, end="\" ")
            print("but you said "+speak_word)
            incorrect.append(generate_word)

        print("Please Listen to AI")
        time.sleep(1)
        playsound('all_function/audio.mp3')
        print("...")
        print('The meaning of the word : ' + synset[0].definition())
        print()
        time.sleep(1)

        os.remove('all_function/audio.mp3')
    correct = np.array(correct)
    incorrect = np.array(incorrect)
    correct = pd.DataFrame(data=correct)
    incorrect = pd.DataFrame(data=incorrect)
    correct.columns = ['All_Word_Correct']
    incorrect.columns = ['All_Word_Incorrect']
    correct.to_csv('all_function/result/correct.csv', index=False)
    incorrect.to_csv('all_function/result/incorrect.csv', index=False)
