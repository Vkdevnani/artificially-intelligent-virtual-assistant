import subprocess
import time
import sys
from gui import stop_gif,start_gif
sys.path.append('D:/Jarvis AI/pythonProject/modules')
import pyautogui
import pyttsx3
#import remember
import speech_recognition as sr
import datetime
import webbrowser
import os
import pygame
import psutil
import random
import sys
from translator_module import translategl


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

for i in range(3):
    a = input("Enter Password to open Jarvis :- ")
    with open("password.txt", "r") as pw_file:
        pw = pw_file.read()
    if a == pw:
        print("WELCOME SIR! PLEASE SPEAK [WAKE UP] TO LOAD ME UP")
        start_gif()
        break
    elif i == 2 and a != pw:
        print("Too many incorrect attempts. Exiting.")
        exit()
    else:
        print("Incorrect password, try again.")

def speak(audio):
    if awake and not video_playing and not music_playing and not app_opening:
        engine.say(audio)
        engine.runAndWait()

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

def alarm(query):
    with open("Alarmtext.txt", "w") as timehere:
        timehere.write(query)

    # Start alarm script in a separate process
    subprocess.Popen(["python", "D:/Jarvis AI/pythonProject/alarm.py"])

def jarvis_main():
    global video_playing, music_playing, app_opening, awake, remember
    awake = True  # Set Jarvis to be awake
    music_playing = False  # Initialize the music_playing flag
    video_playing = False  # Initialize the video_playing flag
    app_opening = False  # Initialize the app_opening flag

    from greetme_new import greetme
    greetme()
    time.sleep(1)



    while awake:
        query = takeCommand().lower()

        if query == "none":
            continue

        if "go to sleep" in query:
            speak("Okay!, You can call me anytime again.")
            awake = False
            break

        elif "hello" in query or "hey" in query:
            speak("Hey, how are you doing today?")
            time.sleep(1)

        elif "i am fine" in query or "i m fine" in query or "i'm fine" in query:
            speak("That's great, what may I do for you?")

        elif "thank you" in query or "thanks" in query:
            speak("You are welcome.")

        elif "remember that" in query:
            rememberMessage = query.replace("Remember that", "")
            rememberMessage = query.replace("jarvis", "")
            speak("You told me to remember that " + rememberMessage)
            with open("Remember.txt", "w") as remember_file:
                remember_file.write(rememberMessage)
        elif "what do you remember" in query:
            with open("Remember.txt", "r") as remember_file:
                speak("You told me that " + remember_file.read())

        elif "open app" in query:
            from dict_new import openappweb
            openappweb(query)

        elif "translate" in query:
            # Clean up the query to get the text to translate
            query = query.replace("jarvis", "").replace("translate", "").strip()
            if query:
                translategl(query)
            else:
                print("No text to translate.")
                speak("Please provide text for translation.")

        elif "close" in query:
            from dict_new import closeappweb
            closeappweb(query)


        elif "pause" in query and video_playing:
            speak("Pausing the video.")
            time.sleep(1)  # Add delay to ensure the command has focus.txt
            pyautogui.press("k")
            speak("Video paused")

        elif "play" in query and video_playing:
            speak("Playing the video.")
            time.sleep(1)  # Add delay to ensure the command has focus.txt
            pyautogui.press("k")
            speak("Video playing")

        elif "mute" in query and video_playing:
            speak("Muting the video.")
            time.sleep(1)  # Add delay to ensure the command has focus.txt
            pyautogui.press("m")  # 'm' key is typically used to mute/unmute in YouTube
            speak("Video muted")

        elif "volume up" in query and video_playing:
            speak("Turning up the volume.")
            time.sleep(1)  # Add delay to ensure the command has focus.txt
            from keyboard import volumeup
            volumeup()
            speak("Volume increased.")


        elif "volume down" in query and video_playing:
            speak("Turning down the volume.")
            time.sleep(1)  # Add delay to ensure the command has focus.txt
            from keyboard import volumedown
            volumedown()
            speak("Volume decreased.")


        elif "open " in query:
            app_opening = True
            if "google" in query:
                webbrowser.open("https://www.google.com")
                speak("Google is open now.")
            elif "youtube" in query:
                webbrowser.open("https://www.youtube.com")
                speak("YouTube is open now.")
                video_playing = True  # Set the video_playing flag to True
            elif "stackoverflow" in query:
                webbrowser.open("https://stackoverflow.com")
                speak("Stack Overflow is open now.")
            elif "spotify" in query:
                webbrowser.open("https://open.spotify.com")
                speak("Spotify is open now.")
            app_opening = False
            time.sleep(5)


        elif "play music" in query:
            music_dir = 'C:\\Users\\Rithik\\Music'
            try:
                if not os.path.exists(music_dir):
                    speak(f"Music directory {music_dir} does not exist.")
                    continue
                songs = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
                if songs:
                    pygame.mixer.music.load(os.path.join(music_dir, songs[0]))
                    pygame.mixer.music.play()
                    music_playing = True
                    speak("Music is playing.")
                else:
                    speak("No music files found in the directory.")
            except Exception as e:
                print(f"Error playing music: {e}")
                speak("There was an error playing the music.")

        elif "stop music" in query:
            if music_playing:
                pygame.mixer.music.stop()
                music_playing = False
                speak("Music has been stopped.")
            else:
                speak("No music is playing.")

        elif "google" in query:
            app_opening = True
            from search_new import searchgoogle
            searchgoogle(query)
            app_opening = False
            time.sleep(10)

        elif "youtube" in query:
            app_opening = True
            from search_new import searchYT
            searchYT(query)
            video_playing = True  # Set the video_playing flag to True after searching on YouTube
            app_opening = False
            time.sleep(10)

        elif "wikipedia" in query:
            app_opening = True
            from search_new import searchwiki
            searchwiki(query)
            app_opening = False
            time.sleep(10)

        elif "news" in query:
            from NewsRead import latestnews
            latestnews()

        elif "temperature" in query:
            try:
                location = ask_location()
                print(f"Location received: {location}")  # Debug print
                temp = get_temp_info(location)
                if temp:
                    speak(f"Current temperature in {location} is {temp}")
                else:
                    speak("Sorry, I couldn't retrieve the weather information.")
            except Exception as e:
                speak("Sorry, there was an error getting the weather information.")
                print(f"Error: {e}")  # Debug print
            time.sleep(3)

        elif "whatsapp" in query:
            from whatsapp import sendmessage
            sendmessage(query)

        elif "weather" in query:
            try:
                location = ask_location()
                print(f"Location received: {location}")  # Debug print
                weather = get_weather_info(location)
                if weather:
                    speak(f"Current weather of {location} as of {weather}")
                else:
                    speak("Sorry, I couldn't retrieve the weather information.")
            except Exception as e:
                speak("Sorry, there was an error getting the weather information.")
                print(f"Error: {e}")  # Debug print
            time.sleep(3)

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {strTime}")


        elif "set an alarm" in query:
            print("input time example:- 10 and 10 and 10")
            speak("Set the time")
            a = input("Please tell the time :- ")
            alarm(a)
            speak("Done, the alarm has been set")

        elif "shut down" in query or "shutdown" in query:
            speak("Shutting down")
            stop_gif()
            exit()

if __name__ == '__main__':
    while True:
        command = takeCommand().lower()
        if command == "none":
            continue
        if "wake up" in command:
            jarvis_main()
