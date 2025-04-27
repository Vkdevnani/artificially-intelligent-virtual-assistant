import os
import webbrowser
import sqlite3

import awake
import subprocess
import time
import sys
import mixer
import notification
from pygame import mixer
from plyer import notification
from gui import stop_gif,start_gif
sys.path.append('D:/Jarvis AI/pythonProject/modules')
import pyautogui
import pyttsx3
#import remember
import speech_recognition as sr
import datetime
import webbrowser
import os
import eel
import webbrowser

# Initialize the Eel library with the 'assets' directory
eel.init("assets")

# Start the Eel application in a separate thread



import pygame
import psutil
import random
import sys
from translator_module import translategl
import sys
import subprocess
from FocusMode import main as focus_mode_main


pygame.mixer.init()

from weather_new import ask_location, get_weather_info, get_temp_info

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate", 170)

# Global flags
video_playing = False
music_playing = False
app_opening = False
awake = False  # Flag to control whether Jarvis is awake

def speak(audio):
    if awake and not video_playing and not music_playing and not app_opening:
        engine.say(audio)
        engine.runAndWait()

for i in range(3):
    a = input("Enter Password to open Jarvis :- ")
    with open("password.txt", "r") as pw_file:
        pw = pw_file.read()
    if a == pw:
        print("WELCOME!! Please speak wake up to load me.")
        eel.start('index.html', mode='chrome', host='localhost', port=8000, block=False)
        # Open the web application in a default browser
        webbrowser.open("http://localhost:8000/index.html")
        # Keep the script running
        eel.sleep(1)  # Adjust the sleep time as needed
        break
    elif i == 2 and a != pw:
        print("Too many incorrect attempts. Exiting.")
        exit()
    else:
        print("Incorrect password, try again.")



def takeCommand():
    '''It takes microphone input from the user and returns string output'''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 2  # gap between speaking intervals
        r.energy_threshold = 300  # adjust energy threshold based on ambient noise
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=4)
        except sr.WaitTimeoutError:
            print("Listening timed out, trying again...")
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I did not catch that.")
        if awake and not video_playing and not music_playing and not app_opening:
            speak("Say that again please...")
        return "None"
    except sr.RequestError:
        print("Network issues, please check your connection.")
        if awake and not video_playing and not music_playing and not app_opening:
            speak("There seems to be a network issue.")
        return "None"
    except Exception as e:
        print(f"An error occurred: {e}")
        if awake and not video_playing and not music_playing and not app_opening:
            speak("Sorry, I couldn't recognize what you said.")
        return "None"

    return query

def speak(audio):
    if awake and not video_playing and not music_playing and not app_opening:
        engine.say(audio)
        engine.runAndWait()
# Assuming the 'speak' function is defined in use_jarvis.py
# from use_jarvis import speak

# Connection to the Jarvis database
connection = sqlite3.connect('jarvis.db')
cursor = connection.cursor()

# Assistant name should be the same as in use_jarvis.py
ASSISTANT_NAME = "jarvis"

def openCommand(query):
    # Clean up the query by removing assistant name and "open" keyword
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    app_name = query.lower().strip()

    if app_name != "":
        try:
            # Searching for local applications in sys_command table
            cursor.execute('SELECT path FROM sys_command WHERE name = ?', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                # If application path is found, open it
                speak(f"Opening {app_name}")
                os.startfile(results[0][0])

            else:
                # Searching for web URLs in web_command table
                cursor.execute('SELECT url FROM web_command WHERE name = ?', (app_name,))
                results = cursor.fetchall()

                if len(results) != 0:
                    # If URL is found, open it in the browser
                    speak(f"Opening {app_name}")
                    webbrowser.open(results[0][0])

                else:
                    # Attempt to open the app directly using os.system if no match found
                    speak(f"Attempting to open {app_name}")
                    try:
                        os.system('start ' + app_name)
                    except Exception as e:
                        speak(f"Could not open {app_name}, application not found.")
                        print(f"Error: {e}")
        except Exception as e:
            speak("Something went wrong.")
            print(f"Error: {e}")

# Make sure to close the connection to the database when you're done
def close_connection():
    cursor.close()
    connection.close()
