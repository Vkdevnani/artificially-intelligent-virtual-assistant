import subprocess
import time
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pygame
import requests
from bs4 import BeautifulSoup

pygame.mixer.init()

from weather_new import ask_location, get_weather_info

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    '''It takes microphone input from the user and returns string output'''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 2  # gap between speaking intervals
        audio = r.listen(source, 0, 4)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        speak("Say that again please...")
        return "None"
    return query


def alarm(query):
    with open("Alarmtext.txt", "w") as timehere:
        timehere.write(query)

    # Start alarm script in a separate process
    subprocess.Popen(["python", "D:/Jarvis AI/pythonProject/alarm.py"])

    # Ensure the path to the alarm script is correct
    alarm_script_path = "D:/Jarvis AI/pythonProject/alarm.py"
    os.startfile(alarm_script_path)


if __name__ == '__main__':
    music_playing = False  # Initialize the music_playing flag
    while True:
        query = takeCommand().lower()
        if "wake up" in query:
            from greetme_new import greetme
            greetme()
            time.sleep(1)

            while True:
                query = takeCommand().lower()
                if "go to sleep" in query:
                    speak("Okay!, You can call me anytime again.")
                    break

                elif "hello" in query or "hey" in query:
                    speak("Hey, how are you doing today?")
                    time.sleep(3)

                elif "i am fine" in query or "I M fine" in query or "I'm fine" in query:
                    speak("That's great")

                elif "thank you" in query:
                    speak("You are welcome.")

                elif "open app" in query:
                    from dict_new import openappweb
                    openappweb(query)
                elif "close" in query:
                    from dict_new import closeappweb
                    closeappweb(query)

                elif 'play music' in query:
                    music_dir = 'C:\\Users\\Rithik\\Music'
                    songs = os.listdir(music_dir)
                    print(songs)
                    if songs:
                        pygame.mixer.music.load(os.path.join(music_dir, songs[0]))
                        pygame.mixer.music.play()
                        music_playing = True
                        speak("Music is playing.")
                    else:
                        speak("No music files found in the directory.")

                elif "stop music" in query:
                    if music_playing:
                        pygame.mixer.music.stop()
                        music_playing = False
                        speak("Music has been stopped.")
                    else:
                        speak("No music is playing.")

                elif "open" in query:
                    if "google" in query:
                        webbrowser.open("https://www.google.com")
                        speak("Google is open now.")
                    elif "youtube" in query:
                        webbrowser.open("https://www.youtube.com")
                        speak("YouTube is open now.")
                    elif "stackoverflow" in query:
                        webbrowser.open("https://stackoverflow.com")
                        speak("Stack Overflow is open now.")
                    elif "spotify" in query:
                        webbrowser.open("https://open.spotify.com")
                        speak("Spotify is open now.")
                    time.sleep(5)

                elif "google" in query:
                    from search_new import searchgoogle
                    searchgoogle(query)
                    time.sleep(10)

                elif "youtube" in query:
                    from search_new import searchYT
                    searchYT(query)
                    time.sleep(10)

                elif "wikipedia" in query:
                    from search_new import searchwiki
                    searchwiki(query)
                    time.sleep(10)

                elif "temperature" in query or "weather" in query:
                    location = ask_location()
                    temp = get_weather_info(location)
                    speak(f"Current temperature in {location} is {temp}")
                    time.sleep(5)

                elif 'the time' in query:
                    strTime = datetime.datetime.now().strftime("%H:%M")
                    speak(f"The time is {strTime}")

                elif "set an alarm" in query:
                    print("Input time example :- 10 and 10 and 10")
                    speak("Set the time")
                    a = input("Please tell the time :-")
                    alarm(a)
                    speak("Done")

                elif "shut down" in query or "shutdown" in query:
                    speak("Shutting down")
                    exit()
