from googletrans import Translator, LANGUAGES
from gtts import gTTS
import pygame
import os
import tempfile
import time
import speech_recognition as sr
import pyttsx3

# Initialize pyttsx3 engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)


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
        speak("Say that again please...")
        return "None"
    except sr.RequestError:
        print("Network issues, please check your connection.")
        speak("There seems to be a network issue.")
        return "None"
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, I couldn't recognize what you said.")
        return "None"

    return query


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def translategl(query):
    """This function translates the spoken text into the target language."""
    speak("Sure, what language do you want me to translate into?")

    # Take language input using voice
    language_input = takeCommand().lower()

    # Convert language name to language code if needed
    language_code = None
    for code, name in LANGUAGES.items():
        if name.lower() == language_input:
            language_code = code
            break

    if not language_code:
        print("Invalid language code.")
        speak("Sorry, I couldn't find the specified language.")
        return

    try:
        # Translate the captured query
        translator = Translator()
        text_to_translate = translator.translate(query, src="auto", dest=language_code)

        # Ensure translation is not None
        if text_to_translate and text_to_translate.text:
            translated_text = text_to_translate.text
            print(f"Translated Text: {translated_text}")

            # Convert translated text to speech using gTTS
            speakgl = gTTS(text=translated_text, lang=language_code, slow=False)

            # Use a temporary directory to avoid permission issues
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file_path = temp_file.name
                speakgl.save(temp_file_path)

            # Ensure the file exists before playing it
            if os.path.exists(temp_file_path):
                # Initialize pygame mixer for playback
                pygame.mixer.init()
                pygame.mixer.music.load(temp_file_path)
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():  # Wait for playback to finish
                    time.sleep(1)

                # Properly stop and uninitialize pygame mixer
                pygame.mixer.music.stop()
                pygame.mixer.quit()

                # Clean up the file after playback
                try:
                    os.remove(temp_file_path)
                except Exception as e:
                    print(f"Error deleting file {temp_file_path}: {e}")

            else:
                raise FileNotFoundError(f"File {temp_file_path} does not exist.")

        else:
            raise ValueError("Translation result is empty")

    except Exception as e:
        print(f"Unable to translate. Error: {e}")
        speak("Sorry, I couldn't translate the text.")
