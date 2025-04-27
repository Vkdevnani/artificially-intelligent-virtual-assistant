import api
import pyttsx3
import speech_recognition as sr
import datetime
import wikipediaapi
import wikipedia
import webbrowser
import os
import smtplib
import pywhatkit
import requests
from bs4 import BeautifulSoup

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate",170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def takeCommand():
    '''It takes microphone input from the user and returns string output'''

    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("listening....")
        r.pause_threshold = 1.5 #gap between speaking intervals
        audio = r.listen(source,0,10)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='eng-in')
        print(f"You said: {query}\n")
    except Exception as e:
        #print(e)
        speak("Say that again please...")
        return "None"
    return query

query = takeCommand().lower()



def searchgoogle(query):
    if 'google' in query:
        import wikipedia as googleScrap
        query = query.replace("jarvis", "")
        query = query.replace("google search", "")
        speak("This is what I found on google")

        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query, 2)
            speak(result)
        except:
            speak("No speakable output available")

def searchYT(query):
    if "youtube" in query:
        speak("This is what I found for your search")
        query = query.replace("youtube search", "")
        query = query.replace("youtube", "")
        query = query.replace("jarvis", "")
        web = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done")


def searchwiki(query):
    if 'wikipedia' in query:
        speak("Searching from Wikipedia...")
        query = query.replace("wikipedia", "")
        query = query.replace("search wikipedia", "")
        query = query.replace("jarvis", "")

        # Strip leading and trailing whitespace
        query = query.strip()

        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find any results for your query on Wikipedia.")
        except wikipedia.exceptions.DisambiguationError as e:
            speak("The query is too ambiguous. Did you mean one of these?")
            speak(', '.join(e.options[:5]))  # List a few disambiguation options
        except Exception as e:
            speak("An error occurred while searching Wikipedia.")
            print(e)







