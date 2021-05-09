from JarvisAI import JarvisAI
import re
import pprint
import random

obj = JarvisAI.JarvisAssistant()
# obj.setup()


def t2s(text):
    obj.text2speech(text)


while True:
    res = obj.mic_input()
    if re.search('turn off', res):
        t2s("turn off")
        break

    if re.search('sum|some|s u m|summarization|sam', res):
        t2s("Summarization")
        t2s("1.Image Url Summarization")
        t2s("2.Url Summarization from wikipedia")
        t2s("3.Search on Wiki")
        t2s("4.Exit from Summarization")
        print("Summarization")
        print("1.Image Url Summarization")
        print("2.Url Summarization from wikipedia")
        print("3.Search on Wiki")
        print("4.Exit from Summarization")

        while True:
            t2s("What do you want to do?")
            try:
                num = str(obj.mic_sum_input())
                if '1' in num:
                    t2s("Enter image url in console.")
                    obj.summarization(1)
                    t2s("Now, summary is on console")
                elif '2' in num:
                    t2s("Enter url in console.")
                    obj.summarization(2)
                    t2s("Now, summary is on console")
                elif '3' in num:
                    t2s("Enter your input in console.")
                    obj.summarization(3)
                    t2s("Now, summary is on console")
                elif '4' or 'pho' in num:
                    t2s("Quit from Summarization")
                    break
                else:
                    t2s("Error input. Please try again.")
            except Exception as e:
                print(e)
                t2s("Try again")
                num = 0

    if re.search('weather|temperature', res):
        city = res.split(' ')[-1]
        weather_res = obj.weather(city=city)
        print(weather_res)
        t2s(weather_res)

    if re.search('news', res):
        news_res = obj.news()
        pprint.pprint(news_res)
        t2s(f"I have found {len(news_res)} news. You can read it. Let me tell you first 2 of them")
        t2s(news_res[0])
        t2s(news_res[1])

    if re.search('tell me about', res):
        topic = res.split(' ')[-1]
        wiki_res = obj.tell_me(topic)
        print(wiki_res)
        t2s(wiki_res)

    if re.search('date', res):
        date = obj.tell_me_date()
        print(date)
        print(t2s(date))

    if re.search('time', res):
        time = obj.tell_me_time()
        print(time)
        t2s(time)

    if re.search('open', res):
        domain = res.split(' ')[-1]
        open_result = obj.website_opener(domain)
        print(open_result)

    if re.search('launch', res):
        dict_app = {
            'chrome': 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            'epic games': 'C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe'
        }

        app = res.split(' ', 1)[1]
        path = dict_app.get(app)
        if path is None:
            t2s('Application path not found')
            print('Application path not found')
        else:
            t2s('Launching: ' + app)
            obj.launch_any_app(path_of_app=path)

    if re.search('hello', res):
        print('Hi')
        t2s('Hi')

    if re.search('how are you', res):
        li = ['good', 'fine', 'great']
        response = random.choice(li)
        print(f"I am {response}")
        t2s(f"I am {response}")

    if re.search('your name|who are you', res):
        print("My name is Jarvis, I am your personal assistant")
        t2s("My name is Jarvis, I am your personal assistant")

    if re.search('what can you do', res):
        li_commands = {
            "open websites": "Example: 'open youtube.com",
            "time": "Example: 'what time it is?'",
            "date": "Example: 'what date it is?'",
            "launch applications": "Example: 'launch chrome'",
            "tell me": "Example: 'tell me about India'",
            "weather": "Example: 'what weather/temperature in Mumbai?'",
            "news": "Example: 'news for today' ",
        }
        ans = """I can do lots of things, for example you can ask me time, date, weather in your city,
        I can open websites for you, launch application and more. See the list of commands-"""
        print(ans)
        pprint.pprint(li_commands)
        t2s(ans)
