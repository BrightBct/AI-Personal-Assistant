import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import time
import subprocess
import requests
import torch
import pyjokes
import nltk

from transformers import T5Tokenizer
from transformers import T5ForConditionalGeneration
from ecapture import ecapture as ec

from function import image_summarization
from function import url_summarization
from function import window
from function import practice_english
from function import dictionary
from function.word import generate_word

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')

print('Loading your AI personal assistant - Ramen')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty("rate", 178)
engine.setProperty('voice', 'voices[0].id')

model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')
device = torch.device('cpu')


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Hello, Good Morning")
        print("Hello, Good Morning")
    elif 12 <= hour < 18:
        speak("Hello, Good Afternoon")
        print("Hello, Good Afternoon")
    else:
        speak("Hello, Good Evening")
        print("Hello, Good Evening")


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said:{statement}\n")
        except Exception:
            # speak("Pardon me, please say that again")
            return "0"
        return statement


if __name__ == '__main__':
    print("Say \"Start\" to activate your AI personal assistant")
    while True:
        start = take_command().lower()
        if "Start".lower() in start:
            speak("Loading your AI personal assistant Ramen")
            wish_me()
            speak("Tell me how can I help you now?")
            count = 0
            while True:
                statement = take_command().lower()
                if statement == "0":
                    count += 1
                    if count == 10:
                        speak("Tell me how can I help you now?")
                        count = 0
                    continue

                if "good bye" in statement or "goodbye" in statement or "ok bye" in statement or "okay bye" in statement \
                        or "stop" in statement or "turn off" in statement:
                    speak('Your personal assistant Ramen is shutting down, Good bye')
                    print('Your personal assistant Ramen is shutting down, Good bye')
                    break

                if 'wikipedia' in statement:
                    speak('Searching Wikipedia...')
                    statement = statement.replace("wikipedia", "")
                    results = wikipedia.summary(statement, sentences=3)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)

                elif 'open youtube' in statement:
                    webbrowser.open_new_tab("https://www.youtube.com")
                    speak("youtube is open now")
                    time.sleep(5)

                elif 'open google' in statement:
                    webbrowser.open_new_tab("https://www.google.com")
                    speak("Google chrome is open now")
                    time.sleep(5)

                elif 'open gmail' in statement:
                    webbrowser.open_new_tab("gmail.com")
                    speak("Google Mail open now")
                    time.sleep(5)

                elif "weather" in statement:
                    api_key = "8ef61edcf1c576d65d836254e11ea420"
                    base_url = "https://api.openweathermap.org/data/2.5/weather?"
                    speak("whats the city name")
                    city_name = take_command()
                    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                    response = requests.get(complete_url)
                    x = response.json()
                    if x["cod"] != "404":
                        y = x["main"]
                        current_temperature = y["temp"]
                        current_humidiy = y["humidity"]
                        z = x["weather"]
                        weather_description = z[0]["description"]
                        speak(" Temperature in kelvin unit is " +
                              str(current_temperature) +
                              "\n humidity in percentage is " +
                              str(current_humidiy) +
                              "\n description  " +
                              str(weather_description))
                        print(" Temperature in kelvin unit = " +
                              str(current_temperature) +
                              "\n humidity (in percentage) = " +
                              str(current_humidiy) +
                              "\n description = " +
                              str(weather_description))

                    else:
                        speak(" City Not Found ")

                elif 'time' in statement:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    speak(f"the time is {strTime}")

                elif 'who are you' in statement or 'what can you do' in statement:
                    speak('I am Ramen your personal assistant. I am programmed to minor tasks like '
                          'opening youtube, google chrome, gmail and stackoverflow, predict time, take a photo, '
                          'search wikipedia, predict weather in different cities, '
                          'summarization, practice English word, and dictionary')

                elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
                    speak("I was built by Mirthula")
                    print("I was built by Mirthula")

                elif "open stackoverflow" in statement or "stackoverflow" in statement or "overflow" in statement:
                    webbrowser.open_new_tab("https://stackoverflow.com/")
                    speak("Here is stackoverflow")

                elif "camera" in statement or "take a photo" in statement:
                    ec.capture(1, "test", "img.jpg")

                elif 'search' in statement:
                    statement = statement.replace("search", "")
                    webbrowser.open_new_tab("https://www.google.com/search?q="+statement)
                    time.sleep(5)

                elif "log off" in statement or "sign out" in statement:
                    speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
                    subprocess.call(["shutdown", "/l"])

                elif "joke" in statement or "jokes" in statement:
                    word = pyjokes.get_joke(language='en', category='neutral')
                    print(word)
                    speak(word)
                    time.sleep(2)

                elif "some" in statement or "sum" in statement or "summarization" in statement:
                    word = "What do you want to summarization\n" \
                           "1.Image Url Summarization\n" \
                           "2.Url Summarization (Wiki Url)\n" \
                           "3.Search on Wiki\n" \
                           "4.Exit from Summarization\n"
                    print(word)
                    # speak(word)
                    while True:
                        speak("What do you want to summarization?")
                        receive = ''
                        receive = take_command()
                        if "1" in receive or "one" in receive:
                            speak("1.Image Url Summarization\n")
                            speak("Please put a link in console")
                            url = str(window.open_windows())
                            if url == "error":
                                speak("Can't use this url\n Please try again")
                            else:
                                image_summarization.image_sum(model, tokenizer, device, url)
                            time.sleep(6)
                        elif "2" in receive or "two" in receive or "too" in receive or "to" in receive:
                            speak("2.Url Summarization (Wiki Url)\n")
                            speak("Please put a link in console")
                            url = str(window.open_windows())
                            url_summarization.url_sum(model, tokenizer, device, url)
                            time.sleep(6)
                        elif "3" in receive or "three" in receive or "tree" in receive:
                            speak("3.Search on Wiki\n")
                            speak("Please use console to summarize")
                            url_summarization.search_wiki(model, tokenizer, device)
                            time.sleep(6)
                        elif "4" in receive or "four" in receive or "fall" in receive:
                            speak("4.Exit from Summarization")
                            break
                        else:
                            speak("Please say it again")
                    time.sleep(3)

                elif "practice" in statement or "english" in statement:
                    speak("Doing Practice")
                    practice_english.english_practice()
                    speak("Stop Practice")
                    time.sleep(6)

                elif "generate" in statement or "word" in statement:
                    speak("Please put a link in console")
                    url = str(window.open_windows())
                    generate_word.increase_word(url)
                    speak("Generate Word Success")
                    time.sleep(3)

                elif "dictionary" in statement:
                    menu = "What method do you want to use to find the meaning?\n" \
                          "1.write\n" \
                          "2.speak\n" \
                          "3.type"
                    print(menu)
                    speak(menu)
                    method = take_command()
                    if "1" in method or "one" in method:
                        speak("1.write")
                    elif "2" in method or "two" in method or "too" in method or "to" in method:
                        speak("2.speak")
                        time.sleep(1)
                        speak("What word do you want to find?")
                        while True:
                            word = take_command()
                            if word is not None:
                                break
                            else:
                                speak("Please say it again")
                        print(word)
                        time.sleep(1)
                        speak("Search"+word+"in dictionary")
                        dictionary.search_dictionary(word)
                        time.sleep(2)
                    elif "3" in method or "three" in method or "tree" in method:
                        speak("Please use console to find the meaning")
                        word = input("Word: ")
                        dictionary.search_dictionary(word)
                        time.sleep(2)
                    else:
                        speak("Did not hear anything\nExit from dictionary")
                        time.sleep(2)

                elif "sleep" in statement:
                    speak("Sleep 1 minute")
                    time.sleep(60)

                elif "love you" in statement:
                    speak("I love you too")
                    time.sleep(1.5)

                elif "thank you" in statement:
                    speak("you're welcome")
                    time.sleep(1.5)

        start = ""

time.sleep(3)
