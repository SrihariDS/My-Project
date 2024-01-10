
import pyttsx3
import speech_recognition as sr
import datetime
import os
import webbrowser
import subprocess
import random
import operator

engine=pyttsx3.init('sapi5')
voice=engine.getProperty('voices')
engine.setProperty('voice',voice[1].id)
recognizer=sr.Recognizer()

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def wishMe():
    hour=int(datetime.datetime.now().hour)
    print(hour)
    if hour>=0 and hour<12:
        speak("Good Morning sir !")
    elif hour>=12 and hour<18:
        speak("Good Afternoon sir !")
    else:
        speak("Good Evening sir !")
    assname =("Peter the Eagle")    
    speak("I am personal Assistant")
    speak(assname)

def username():
    
    speak("what is Your Name sir?")
    name = takeCommand()
    speak("welcome "+name)
    speak("How can i help you, Sir")
          
    
def takeCommand():
    
    r=sr.Recognizer()
    
    with sr.Microphone() as source:
        
        print("listening...")
        r.pause_threshold=1
        audio = r.listen(source)

        
        try:
            audio=r.listen(source,timeout=30,phrase_time_limit=10)
            print("compiling your voice please wait...")
            text=r.recognize_google(audio,language="en-in")
            print("text")
            
        except Exception as e:
            print(e)
            speak('Unable to recognize your voice')
            return "None"
        return text

    
if __name__=='__main__':
    clear = lambda:os.system('cls')

    wishMe()
    username()

    while True:
        text = takeCommand().lower()
        if 'how are you' in text:
            speak('I am fine. Thank you.')
            speak('How are you, sir?')
        elif 'fine' in text or 'good' in text:
            speak('It is good to know that you are fine.')
        elif 'i hate you' in text or 'love you' in text:
            speak('Oh my god, thank you.')
        elif 'open youtube' in text:
            speak("Here you go to Youtube.")
            webbrowser.open("https://www.youtube.com")
        elif 'open google' in text:
            speak("Here you go to Google.")
            webbrowser.open("https://www.google.com")
        elif 'bye' in text:
            speak('Goodbye, sir. See you again.')
            exit()
        else:
            speak('I can\'t understand. Please speak again.')

       


