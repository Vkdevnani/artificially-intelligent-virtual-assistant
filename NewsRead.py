import requests
import json
import pyttsx3

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


def latestnews():
    apidict = {
        "business": "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=5fd839e1ea8c4389af6050f600bed89a",
        "entertainment": "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=5fd839e1ea8c4389af6050f600bed89a",
        "health": "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=5fd839e1ea8c4389af6050f600bed89a",
        "science": "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=5fd839e1ea8c4389af6050f600bed89a",
        "sports": "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=5fd839e1ea8c4389af6050f600bed89a",
        "technology": "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=5fd839e1ea8c4389af6050f600bed89a"
    }

    speak("Which field's news do you wish to hear? [business], [health], [technology], [sports], [entertainment], or [science]")
    field = input("Type the field you want: ").lower()

    url = apidict.get(field)

    if url:
        print(f"Fetching news from: {url}")
    else:
        speak("Sorry, the field you entered is not available.")
        return

    try:
        news_response = requests.get(url).text
        news_data = json.loads(news_response)

        speak("Here is the first news.")

        arts = news_data.get("articles", [])

        for i, article in enumerate(arts[:5], 1):  # Limit to 5 news items
            title = article["title"]
            news_url = article["url"]

            print(f"{i}. {title}")
            speak(title)
            print(f"For more info visit: {news_url}")

            a = input("[Press 1 to continue] and [Press 2 to stop]: ")

            if a == "2":
                break

        speak("That's all for now.")
    except Exception as e:
        print(f"Error: {e}")
        speak("I couldn't fetch the news. Please try again later.")


# Set awake flag to True for testing
awake = True

# Test the latestnews function
latestnews()
