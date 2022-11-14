import random
import string
import psutil
import pyttsx3
import datetime
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import pyaudio
import wikipedia
import urllib.request
import os
import pyautogui
from time import sleep

engine = pyttsx3.init()
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[1].id)
newvoicerate = 190
engine.setProperty('rate',newvoicerate)
model = Model("D:\projects\AI assistant\model")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)


def get_input():
    print("Listening...")
    stream.start_stream()
    try:
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                print("Recognizing....")
                text = recognizer.Result()
                print(text[14:-3])
                return text[14:-3]

    except Exception as e:
        print(e)
        return "e"


def connect():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def time():
    Time = datetime.datetime.now().strftime("%I %M %p")
    print(Time)
    speak("the current time is" + Time)


def date():
    Date = datetime.datetime.now().strftime("%d %B %Y")
    print(Date)
    speak("the current date is" + Date)


def wishme():
    stream.stop_stream()
    speak("welcome back sir!")
    # hour = datetime.datetime.now().hour
    # print(hour)
    # if 6 <= hour < 12:
    #     speak("good morning sir !")
    # elif 12 <= hour < 18:
    #     speak("good afternoon sir !")
    # elif 18 <= hour < 24:
    #     speak("good evening sir!")
    # else:
    #     speak("good night sir!")
    speak("sub-zero at your service sir")
    sleep(0.1)
    speak("please tell me how can i help you ")


def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU is at' + usage)
    battery = psutil.sensors_battery().percent
    speak('battery is at' + str(usage))


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-uk')
        print(query)
    except Exception as e:
        print(e)
        # speak("Say that again please...")
        return "none"

    return query


def screenshot():
    img = pyautogui.screenshot()
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(10))
    img.save('screenShots\\' + result_str + '.png')


if __name__ == "__main__":
    wishme()
    while True:
        if connect():
            query = takeCommand().lower()
        else:
            query = get_input().lower()
            stream.stop_stream()

        if 'time' in query:
            time()
        elif 'date' in query:
            date()
        elif 'remember that' in query:
            speak("what should I remember?")
            if connect():
                data = takeCommand()
            else:
                data = get_input()
            speak("you said me to remember that" + data)
            remember = open('data.txt', 'w')
            remember.write(data)
            remember.close()
        elif 'do you know anything' in query:
            remember = open('data.txt', 'r')
            speak("you said me to remember that" + remember.read())
            remember.close()
        elif 'connection' in query or 'internet' in query:
            if connect():
                speak("sir you are on online mode")
            else:
                speak("sorry you are on offline mode")
        elif 'status' in query:
            cpu()
        elif 'screenshot' in query:
            speak("taking screen shot")
            screenshot()
            speak('mission success sir')
        elif 'search' in query:
            speak("what should i search ?")
            search = takeCommand().lower()
            result = wikipedia.summary(search)
            print(result)
            speak(result)
        elif 'sign out' in query:
            speak("sign out")
            os.system("shutdown -l")
        elif 'shutdown' in query:
            speak("close pc")
            os.system("shutdown /s /t 1")
        elif 'restart' in query:
            speak("restart pc")
            os.system("shutdown /r /t 1")
        elif 'turn off' in query:
            speak("good bye sir")
            quit()

        elif query != 'none':
            if connect():
                speak("sorry i cant understand")
            else:
                if len(query) > 0:
                    speak("sorry i cant understand")
