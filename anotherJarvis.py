import speech_recognition as sr
import datetime
import pyttsx3
import pywhatkit
import wikipedia
import requests
from bs4 import BeautifulSoup

# Initialize the TTS engine
machine = pyttsx3.init('sapi5')
voices = machine.getProperty('voices')
machine.setProperty('voice', voices[0].id)

NEWS_API_KEY = "5c9576e4865946b29140573260301e2a"
SEARCH_API_KEY = "AIzaSyAdUPzgn0vGjAEnwnmfWQ6JXYsq3UGMTFs"
CSE_ID = "voice-assistant--1717001887756"


def speak(text):
    machine.say(text)
    machine.runAndWait()


def greetings():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your voice assistant, Please tell me how may I help you")


def funcions_brief():
    speak("I can assist you to play a video on youtube, do Google Searches, browse Wikipedia, tell top NEWS Headlines & even tell you the time right now.")
    speak("Please tell me how may I help you!")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 150
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")
    except Exception:
        print("Sorry, I did not understand that. Say that again please...")
        return "None"
    return query


def wikipedia_Assistance(query):
    speak("Searching Wikipedia...")
    search_Results = wikipedia.summary(query, sentences=2)
    return search_Results


def search_google(query):
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={SEARCH_API_KEY}&cx={CSE_ID}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        search_results = response.json()
        results = []
        for item in search_results.get('items', []):
            title = item.get('title')
            snippet = item.get('snippet')
            results.append(f"{title} - {snippet}")
        return results
    except requests.RequestException as e:
        return [f"An error occurred: {e}"]


def fetch_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()
        headlines = [article['title'] for article in news_data['articles']]
        return headlines
    except requests.RequestException as e:
        return [f"An error occurred: {e}"]


if __name__ == "__main__":
    greetings()
    while True:
        query = takeCommand().lower().strip()

        if 'hi' in query or 'hello' in query:
            print("Hello! How may I assist you?")
            speak("Hello! How may I assist you?")
            query = takeCommand().lower().strip()

        elif 'wikipedia' in query:
            query = query.replace("wikipedia", "")
            results = wikipedia_Assistance(query)
            speak("According to Wikipedia")
            if results:
                print(results)
                speak(results)
            else:
                results = "No results found"
                print(results)
                speak(results)

        elif 'search for' in query or "on google" in query:

            query = query.replace('search for', "").replace("on google", "").strip()

            speak(f"Searching for {query} on Google...")

            results = search_google(query)

            if results:

                speak("Here are the top results:")

                for result in results[:5]:
                    speak(result)

            else:

                speak("No results found")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'on youtube' in query:
            query = query.replace("play", "").replace("on youtube", "").strip()
            speak(f"Playing {query} on YouTube")
            pywhatkit.playonyt(query)

        elif 'what can you do' in query:
            funcions_brief()

        elif 'news' in query or 'headlines' in query:
            speak("Fetching the latest news headlines...")
            headlines = fetch_news()
            if headlines:
                speak("Here are the top news headlines:")
                for headline in headlines[:5]:
                    speak(headline)
            else:
                speak("No news headlines found")

        elif 'exit' in query or 'stop' in query:
            speak('Have a nice day!')
            exit()

        else:
            continue
