import speech_recognition as sr
import pyttsx3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
        except Exception as e:
            print("Say that again please...")
            return "None"
        return query

def sendEmail(to, content):
    from_email = "your_email@gmail.com"
    from_password = "your_password"

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to
    message['Subject'] = 'Subject of the Email'

    message.attach(MIMEText(content, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)
    text = message.as_string()
    server.sendmail(from_email, to, text)
    server.quit()

if __name__ == "__main__":
    query = takeCommand().lower()

    if 'email to papa' in query:
        try:
            speak("What should I say?")
            content = takeCommand()
            to = "contactanshul1@gmail.com"
            sendEmail(to, content)
            speak("Email has been sent")
        except Exception as e:
            print(e)
            speak("Sorry, Rithik. I was unable to send the email")
