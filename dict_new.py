import os
import pyautogui
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import smtplib
from time import sleep

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Dictionary mapping application names to their commands
dictapp = {
    "commandprompt": "cmd",
    "paint": "mspaint",
    "word": "winword",
    "excel": "excel",
    "chrome": "chrome",
    "vscode": "code",
    "powerpoint": "powerpnt"
}

def openappweb(query):
    speak("Launching the app")
    if ".com" in query or ".co.in" in query or ".org" in query:
        query = query.replace("open", "").replace("jarvis", "").replace("launch", "").replace(" ", "")
        webbrowser.open(f"https://www.{query}")
    else:
        keys = list(dictapp.keys())
        for app in keys:
            if app in query:
                os.system(f"start {dictapp[app]}")

def closeappweb(query):
    speak("Closing...")
    if "tab" in query:
        # Extract the number from the command
        try:
            num_tabs = [int(s) for s in query.split() if s.isdigit()]
            num_tabs = num_tabs[0] if num_tabs else 1  # Default to 1 if no number is found
            num_tabs = min(num_tabs, 5)  # Limit to closing up to 5 tabs
            for _ in range(num_tabs):
                pyautogui.hotkey("ctrl", "w")
                sleep(0.5)  # Allow time for each tab to close
            speak(f"{num_tabs} tab{'s' if num_tabs > 1 else ''} closed.")
        except ValueError:
            speak("Invalid number of tabs specified.")
    else:
        keys = list(dictapp.keys())
        for app in keys:
            if app in query:
                os.system(f"taskkill /f /im {dictapp[app]}.exe")
                speak(f"{app.capitalize()} closed.")

