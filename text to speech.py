
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
import pyttsx3
import os

#create gui window
window = Tk()
window.title("Text to speech")
window.geometry("1000x700")
window.resizable(False, False)
window.configure(bg="whitesmoke")

# next window
def Next():
    window.destroy()

engine = pyttsx3.init()

def speaknow():
    text = text_area.get(1.0, END)
    gender = gender_combobox.get()
    speed = speed_combobox.get()
    voices = engine.getProperty('voices')

    def setvoice():
        if gender == 'Male':
            engine.setProperty('voice', voices[0].id)
            engine.say(text)
            engine.runAndWait()
        else:
            engine.setProperty('voice', voices[1].id)
            engine.say(text)
            engine.runAndWait()

    if text:
        if speed == "Fast":
            engine.setProperty('rate', 250)
            setvoice()
        elif speed == "Normal":
            engine.setProperty('rate', 150)
            setvoice()
        else:
            engine.setProperty('rate', 60)
            setvoice()

def download():
    text = text_area.get(1.0, END)
    gender = gender_combobox.get()
    speed = speed_combobox.get()
    voices = engine.getProperty('voices')

    def setvoice():
        if gender == 'Male':
            engine.setProperty('voice', voices[0].id)
        else:
            engine.setProperty('voice', voices[1].id)

    if text:
        setvoice()
        path = filedialog.askdirectory()
        if path:  # Check if a directory is selected
            os.chdir(path)
            engine.save_to_file(text, 'text.mp3')
            engine.runAndWait()

# top_frame
Top_frame = Frame(window, bg="dimgray", width=1000, height=100)
Top_frame.place(x=0, y=0)

Label(Top_frame, text="VocalizeMe", font=("arial 20 bold", 25, "bold"), bg="seashell", fg="slategrey").place(x=400, y=30)

text_area = Text(window, font="Roboto 20", bg="white", relief=GROOVE, wrap=WORD)
text_area.place(x=100, y=150, width=800, height=200)

Label(window, text="Sound Sculptor", font=("arial 15 bold", 20, "bold"), bg="dimgray", fg="snow").place(x=150, y=400)
Label(window, text="Rapid Rhythms", font=("arial 15 bold", 20, "bold"), bg="dimgray", fg="snow").place(x=550, y=400)

gender_combobox = Combobox(window, values=['Male', 'Female'], font="arial 14", state="readonly", width=12)
gender_combobox.place(x=190, y=450)
gender_combobox.set('Male')

speed_combobox = Combobox(window, values=['Fast', 'Normal', 'Slow'], font="arial 14 bold", state="readonly", width=12)
speed_combobox.place(x=600, y=450)
speed_combobox.set('Normal')

imageicon = PhotoImage(file="")
b1 = Button(window, text="Speak", width=10, bg="snow", font="arial 14 bold", command=speaknow)
b1.place(x=210, y=500)

imageicon2 = PhotoImage(file="")
save = Button(window, text="Save", width=10, bg="snow", font="arial 14 bold", command=download)
save.place(x=610, y=500)

b1 = Button(window, text="Exit", width=13, bg="mintcream", font="arial 14 bold", command=Next)
b1.place(x=400, y=600)

window.mainloop()
