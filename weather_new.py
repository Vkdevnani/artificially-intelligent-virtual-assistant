# weather_utils.py
import requests
from bs4 import BeautifulSoup
import pyttsx3
import speech_recognition as sr

def speak(audio):
    """Function to make the assistant speak"""
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty("rate", 170)
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    """It takes microphone input from the user and returns string output"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 2 # Gap between speaking intervals
        audio = r.listen(source, 0, 4)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        speak("Say that again please...")
        return "None"
    return query

def get_temp_info(location):
    search = f"temperature in {location}"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp = data.find("div", class_="BNeawe").text
    return temp

def get_weather_info(location):
    searchweather = f"weather in {location}"
    url2 = f"https://www.google.com/search?q={searchweather}"
    r = requests.get(url2)
    data2 = BeautifulSoup(r.text, "html.parser")
    weather = data2.find_all("div", class_="BNeawe")[2].text  # This line fetches more detailed weather information
    return weather

def ask_location():
    speak("Please tell me the location.")
    location = takeCommand().lower()
    return location
