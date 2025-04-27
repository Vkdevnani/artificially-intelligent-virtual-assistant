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
        r.pause_threshold = 2  # Gap between speaking intervals
        audio = r.listen(source, 0, 4)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        speak("Say that again please...")
        return "None"
    return query


def get_temperature(location):
    search = f"temperature in {location}"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp = data.find("div", class_="BNeawe iBp4i AP7Wnd").text
    return f"The temperature in {location} is {temp}."


def get_weather(location):
    search = f"weather in {location}"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")

    # Extract temperature
    temp = data.find("div", class_="BNeawe iBp4i AP7Wnd").text

    # Extract weather condition
    condition = data.find("div", class_="BNeawe tAd8D AP7Wnd").text

    # Extract additional weather information if available
    try:
        additional_info = data.find_all("div", class_="BNeawe s3v9rd AP7Wnd")[1].text
        humidity, wind = additional_info.split('\n')[0], additional_info.split('\n')[1]
    except Exception as e:
        humidity, wind = "N/A", "N/A"

    return f"The weather in {location} is as follows: {condition}. Humidity: {humidity}. Wind: {wind}. The temperature is {temp}."


def ask_location():
    speak("Please tell me the location.")
    location = takeCommand().lower()
    return location


def main():
    speak("Do you want to know the temperature or the weather?")
    command = takeCommand().lower()

    if "temperature" in command:
        location = ask_location()
        temp_info = get_temperature(location)
        speak(temp_info)
    elif "weather" in command:
        location = ask_location()
        weather_info = get_weather(location)
        speak(weather_info)
    else:
        speak("I didn't understand. Please say either 'temperature' or 'weather'.")


if __name__ == "__main__":
    main()
