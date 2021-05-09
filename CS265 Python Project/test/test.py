import speech_recognition as sr
for i in sr.Microphone.list_microphone_names():
    print(i)
