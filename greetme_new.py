import pyttsx3
import datetime


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate",170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greetme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 4 and hour < 12:
        speak("Good morning")
    elif hour >= 12 and hour < 16:
        speak("Good afternoon")

    else:
        speak("Good evening")

    speak("This is your assistant Jarvis. How may I help you?")