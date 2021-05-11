import pyttsx3

from nltk.corpus import wordnet
from PyDictionary import PyDictionary

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[0].id')


def speak(text):
    engine.say(text)
    engine.runAndWait()


def search_dictionary(word):
    status = True
    dictionary = PyDictionary()
    synset = wordnet.synsets(word)
    try:
        synset[0].definition()
    except IndexError:
        print("Can't find "+word+" in dictionary")
        speak("Can't find "+word+" in dictionary")
        status = False
    if status:
        mean = dictionary.meaning(word)
        if 'Noun' in mean:
            print("Noun\n"+mean['Noun'][0]+"\n")
            speak("Noun\n"+mean['Noun'][0]+"\n")
        if 'Verb' in mean:
            print("Verb\n"+mean['Verb'][0]+"\n")
            speak("Verb\n"+mean['Verb'][0]+"\n")
        if 'Pronoun' in mean:
            print("Pronoun\n"+mean['Pronoun'][0]+"\n")
            speak("Pronoun\n"+mean['Pronoun'][0]+"\n")
        if 'Adjective' in mean:
            print("Adjective\n"+mean['Adjective'][0]+"\n")
            speak("Adjective\n"+mean['Adjective'][0]+"\n")
        if 'Adverb' in mean:
            print("Adverb\n"+mean['Adverb'][0]+"\n")
            speak("Adverb\n"+mean['Adverb'][0]+"\n")
        if 'Preposition' in mean:
            print("Preposition\n"+mean['Preposition'][0]+"\n")
            speak("Preposition\n"+mean['Preposition'][0]+"\n")
        if 'Conjunction' in mean:
            print("Conjunction\n"+mean['Conjunction'][0]+"\n")
            speak("Conjunction\n"+mean['Conjunction'][0]+"\n")
        if 'Interjection' in mean:
            print("Interjection\n"+mean['Interjection'][0]+"\n")
            speak("Interjection\n"+mean['Interjection'][0]+"\n")
