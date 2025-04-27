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

def alarm(query):
    with open("Alarmtext.txt", "w") as timehere:
        timehere.write(query)

    # Start alarm script in a separate process
    subprocess.Popen(["python", "D:/Jarvis AI/pythonProject/alarm.py"])
import time

def word_to_number(word):
    number_dict = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
        "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
        "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
        "eighteen": 18, "nineteen": 19, "twenty": 20
    }
    return number_dict.get(word, None)  # Returns None if the word is not found

def start_focus_mode():
    try:
        user_input = input("Are you sure you want to enter focus mode? [1 for YES / 2 for NO]: ")
        if user_input == '1':
            speak("Entering focus mode....")
            # Prompt the user for the duration
            duration_input = input("For how long do you want to stay in focus mode? (in minutes): ")
            try:
                duration_minutes = int(duration_input)
                if duration_minutes <= 0:
                    speak("Please enter a positive number for the duration.")
                    return
            except ValueError:
                speak("Invalid duration input. Please enter a number.")
                return
            # Calculate the end time
            end_time = time.time() + (duration_minutes * 60)
            speak(f"Focus mode activated for {duration_minutes} minutes.")
            # Call the focus mode script
            subprocess.run(["python", "D:\\Jarvis AI\\pythonProject\\FocusMode.py"], check=True)
            # Wait for the duration to expire
            while time.time() < end_time:
                time.sleep(60)  # Check every minute
            # Notify the user that the focus mode duration has ended
            speak("Focus mode duration has ended. You can now exit focus mode.")
            print("Focus mode duration has ended. Exiting focus mode.")

        elif user_input == '2':
            speak("Focus mode activation cancelled.")
        else:
            speak("Invalid input. Please enter 1 or 2.")
    except Exception as e:
        speak(f"An error occurred: {e}")


import os
import pygame

# Global variables
current_song_index = 0
music_playing = False
songs_list = []

def initialize_music_list():
    global songs_list
    music_dir = 'C:\\Users\\Rithik\\Music'  # Adjust the path if needed
    if os.path.exists(music_dir):
        songs_list = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
        if not songs_list:
            speak("No music files found in the directory.")
    else:
        speak(f"Music directory {music_dir} does not exist.")

def play_music(song_name=None):
    global current_song_index, music_playing, songs_list

    if not songs_list:
        initialize_music_list()

    if not songs_list:
        return  # Exit if there are no songs

    music_dir = 'C:\\Users\\Rithik\\Music'  # Adjust the path if needed

    try:
        if song_name:
            song_path = next(
                (os.path.join(music_dir, song) for song in songs_list if song_name.lower() in song.lower()), None)
            if song_path:
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play()
                music_playing = True
                speak(f"Playing {song_name}.")
            else:
                speak(f"Could not find a song named {song_name}.")
        else:
            pygame.mixer.music.load(os.path.join(music_dir, songs_list[current_song_index]))
            pygame.mixer.music.play()
            music_playing = True
            speak(f"Playing {songs_list[current_song_index]}.")

    except pygame.error as e:
        print(f"Error playing music: {e}")
        speak("There was an error playing the music.")
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"Unexpected error: {e}")
        speak("There was an unexpected error playing the music.")
        pygame.mixer.music.stop()

def next_song():
    global current_song_index, music_playing, songs_list
    if not songs_list:
        initialize_music_list()
    if not songs_list:
        return  # Exit if there are no songs
    # Stop the current song
    if music_playing:
        pygame.mixer.music.stop()

    # Move to the next song
    current_song_index = (current_song_index + 1) % len(songs_list)
    play_music()  # Play the next song

def stop_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.stop()
        music_playing = False
        speak("Music stopped.")



def jarvis_main():
    global video_playing, music_playing, app_opening, awake, remember
    awake = True  # Set Jarvis to be awake
    music_playing = False  # music play flag
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




        elif "schedule my day" in query:
            tasks = []  # Empty list
            speak("Do you want to clear old tasks (Plz speak YES or NO)")
            query = takeCommand().lower()
            if "yes" in query:
                file = open("tasks.txt", "w")
                file.write(f"")
                file.close()
                no_tasks = int(input("Enter the no. of tasks :- "))
                i = 0
                for i in range(no_tasks):
                    tasks.append(input("Enter the task :- "))
                    file = open("tasks.txt", "a")
                    file.write(f"{i}. {tasks[i]}\n")
                    file.close()
            elif "no" in query:
                i = 0
                no_tasks = int(input("Enter the no. of tasks :- "))
                for i in range(no_tasks):
                    tasks.append(input("Enter the task :- "))
                    file = open("tasks.txt", "a")
                    file.write(f"{i}. {tasks[i]}\n")
                    file.close()

        elif "focus mode" in query:
            start_focus_mode()

        elif "show my focus" in query:
            from FocusGraph import focus_graph
            focus_graph()

        elif "show my schedule" in query:
            file = open("tasks.txt", "r")
            content = file.read()
            file.close()
            mixer.init()  # Initialize the mixer module
            mixer.music.load("notification.mp3")
            mixer.music.play()
            notification.notify(
                title="My schedule :-",
                message=content,
                timeout=15
            )

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

        elif "screenshot" in query:
            import pyautogui  # pip install pyautogui
            im = pyautogui.screenshot()
            im.save("ss.jpg")
            speak("Screenshot has been saved in the folder")

        elif "click my photo" in query:
            pyautogui.press("super")
            pyautogui.typewrite("camera")
            pyautogui.press("enter")
            pyautogui.sleep(2)
            speak("SMILE")
            pyautogui.press("enter")


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




        elif "skip" in query and music_playing:
            next_song()


        elif "play music" in query:
            song_name = query.replace("play music", "").strip()
            play_music(song_name)


        elif "stop music" in query:
            stop_music()

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
            from whatsapp import sendMessage
            sendMessage()

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

        elif "what is" in query or "who is" in query:
            from dict_new import search_wikipedia
            search_wikipedia(query)


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
