import pywhatkit
import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
from time import sleep
import os
from datetime import timedelta
from datetime import datetime
import random
from plyer import notification
import pyautogui
import wikipedia
import user_config
import openai_request as ai
import mtranslate

# Initialize the text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

def speak(audio):
    if audio:
        audio = mtranslate.translate(audio, to_language="en", from_language="en-in")
        print(audio)
        engine.say(audio)
        engine.runAndWait()
    else:
        print("No audio to speak.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)

    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception:
        print("Say that again")
        return "None"
    return query

# Get the current hour and the minute two minutes from now
strTime = int(datetime.now().strftime("%H"))
update = int((datetime.now() + timedelta(minutes=2)).strftime("%M"))

def sendMessage():
    speak("Who do you want to message?")
    a = int(input('ontact_name 1 - 1 Brother - 2 Brother - 3: '))
    if a == 1:
        speak("What's the message?")
        message = takeCommand()
        if message != "None":
            pywhatkit.sendwhatmsg("+91000000", message, time_hour=strTime, time_min=update, wait_time=20)
            speak("Message sent successfully to Sarkale Kartik.")
    elif a == 2:
        speak("What's the message for Brother?")
        message = takeCommand()
        if message != "None":
            pywhatkit.sendwhatmsg("+910000000", message, time_hour=strTime, time_min=update, wait_time=20)
            speak("Message sent successfully to Brother.")
    elif a == 3:
        speak("What's the message for Brother?")
        message = takeCommand()
        if message != "None":
            pywhatkit.sendwhatmsg("+9100000", message, time_hour=strTime, time_min=update, wait_time=20)
            speak("Message sent successfully to Brother.")       

def makeCall():
    speak("Who do you want to call?")
    a = int(input('ontact_name 1 - 1 ontact_name 2 - 2: '))
    if a == 1:
        contact_name = "contact_name 1"
        phone_number = "+910000000000"
    elif a == 2:
        contact_name = "contact_name 2r"
        phone_number = "+910000000000"
    else:
        speak("Invalid choice.")
        return

    speak(f"Opening WhatsApp Web and calling {contact_name}.")
    webbrowser.open(f"https://wa.me/{phone_number}")
    sleep(5)
    speak("Please initiate the call in WhatsApp Web.")

def main_process():
    jarvis_chat = []
    while True:
        request = takeCommand().lower()

        if "hello" in request:
            speak("Welcome, how can I help you.")

        elif "play music" in request:
            speak("Playing music")
            song = random.randint(1, 5)
            music_links = [
                "https://www.youtube.com/watch?v=HCWvgoTfUjg",
                "https://www.youtube.com/watch?v=UbgBidiaiZA",
                "https://www.youtube.com/watch?v=sZiETQzgAPc",
                "https://www.youtube.com/watch?v=6nQLoPwGsMM",
                "https://www.youtube.com/watch?v=5CSuwo_6gg"
            ]
            webbrowser.open(music_links[song - 1])

        elif "say time" in request:
            now_time = datetime.now().strftime("%H:%M")
            speak("Current time is " + now_time)

        elif "say date" in request:
            now_date = datetime.now().strftime("%d:%m")
            speak("Current date is " + now_date)

        elif "new task" in request:
            task = request.replace("new task", "").strip()
            if task:
                speak("Adding task: " + task)
                with open("todo.txt", "a") as file:
                    file.write(task + "\n")

        elif "speak task" in request:
            with open("todo.txt", "r") as file:
                tasks = file.read()
                speak("You have no tasks for today." if not tasks.strip() else "Tasks are: " + tasks)

        elif "show work" in request:
            with open("todo.txt", "r") as file:
                tasks = file.read()
            notification.notify(
                title="Today's work",
                message=tasks if tasks.strip() else "No tasks for today."
            )

        elif "open youtube" in request:
            webbrowser.open("https://www.youtube.com/")
            speak("Opening YouTube")

        elif "open whatsapp" in request:
            webbrowser.open("https://web.whatsapp.com/")
            speak("Opening WhatsApp")

        elif "open instagram" in request:
            webbrowser.open("https://www.instagram.com/")
            speak("Opening Instagram")

        elif "open facebook" in request:
            webbrowser.open("https://www.facebook.com/")
            speak("Opening Facebook")

        elif "open google" in request:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")

        elif "open vs code" in request:
            speak("Opening Visual Studio Code")
            os.system("code")

        elif "open" in request:
            query = request.replace("open", "").strip()
            pyautogui.press("win")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")

        elif "wikipedia" in request:
            query = request.replace("jarvis", "").replace("search wikipedia", "").strip()
            try:
                result = wikipedia.summary(query, sentences=3)
                print(result)
                speak(result)
            except Exception:
                speak("Sorry, I couldn't find any information on that topic.")

        elif "search google" in request:
            query = request.replace("jarvis", "").replace("search google", "").strip()
            webbrowser.open("https://www.google.com/search?q=" + query)
            speak("Searching Google for " + query)

        elif "search gemini" in request:
            query = request.replace("jarvis", "").replace("search gemini", "").strip()
            webbrowser.open("https://gemini.google.com/search?q=" + query)
            speak("Searching Gemini for " + query)

        elif "send whatsapp" in request:
            sendMessage()

        elif "call" in request:
            makeCall()

        elif "ask ai" in request:
            query = request.replace("jarvis", "").replace("ask ai", "").strip()
            jarvis_chat.append({"role": "user", "content": query})
            response = ai.send_request(jarvis_chat)
            print(response)
            speak(response if response else "I'm sorry, I couldn't generate a response to that.")

        else:
            query = request.replace("jarvis", "").strip()
            jarvis_chat.append({"role": "user", "content": query})
            print(jarvis_chat)
            response = ai.send_request2(jarvis_chat)
            jarvis_chat.append({"role": "assistant", "content": response})
            speak(response if response else "I'm sorry, I couldn't generate a response to that.")

if __name__ == "__main__":
    main_process()
