import pyttsx3
import speech_recognition as sr
import datetime
import wikipediaapi
import wikipedia
import webbrowser
import os
import smtplib



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good morning")
    elif hour>=12 and hour<18:
        speak("Good afternoon")

    else:
        speak("Good evening")

    speak("I am your assistant Jarvis. Please tell me, how may I help you")

def takeCommand():
    '''It takes microphone input from the user and returns string output'''

    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 2 #gap between speaking intervals
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='eng-in')
        print(f"User said: {query}\n")

    except Exception as e:
        #print(e)
        speak(
            "Say that again please...")
        return "None"
    return query

def sendEmail(to,content):
    server = smtplib.SMTP('smntp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('rithiklab@gmail.com', 'rithiklab1512')
    server.sendmail('rithiklab@gmail.com', 'contactanshul1@gmail.com', 'Hello papa and mummy. This is the first auto-sent email done by me, Jarvis, created as a part of Rithik first project.')
    server.close()
if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand().lower()

        #Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'open spotify' in query:
            webbrowser.open("https://open.spotify.com/")

        elif 'play music' in query:
            music_dir = 'C:\\Users\\Rithik\\Music'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Hey, the time is {strTime}")

        elif 'open compiler' in query.lower():
            codepath = '"D:\\Microsoft VS Code\\Code.exe"'
            os.startfile(codepath)
            print("Opening VS Code")

        elif 'email to Papa' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "contactanshul1@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("Sorry, Rithik. I was unable to send the email")
