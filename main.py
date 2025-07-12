import os
import threading
import tkinter as tk
from gtts import gTTS
from tkinter import ttk
import speech_recognition as sr
from playsound import playsound
from deep_translator import GoogleTranslator
from indic_transliteration.sanscript import transliterate
from indic_transliteration.sanscript import DEVANAGARI, ITRANS
import webbrowser

# Create an instance of Tkinter frame or window
win = tk.Tk()
win.geometry("700x451")
win.title("Real-Time Voice🎙️ Translator🔊")

icon = tk.PhotoImage(file="icon.png")
win.iconphoto(False, icon)

# Labels and text boxes
input_label = tk.Label(win, text="Recognized Text ⮯")
input_label.pack()
input_text = tk.Text(win, height=5, width=50)
input_text.pack()

output_label = tk.Label(win, text="Translated Text ⮯")
output_label.pack()
output_text = tk.Text(win, height=5, width=50)
output_text.pack()

tk.Label(win, text="").pack()

# Language list
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Spanish": "es",
    "Chinese (Simplified)": "zh-CN",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "German": "de",
    "French": "fr",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Gujarati": "gu",
    "Punjabi": "pa"
}
language_names = list(language_codes.keys())

# Input language selection
tk.Label(win, text="Select Input Language:").pack()
input_lang = ttk.Combobox(win, values=language_names)
input_lang.set("Hindi")
input_lang.pack()

tk.Label(win, text="▼").pack()

# Output language selection
tk.Label(win, text="Select Output Language:").pack()
output_lang = ttk.Combobox(win, values=language_names)
output_lang.set("English")
output_lang.pack()

tk.Label(win, text="").pack()

keep_running = False

def update_translation():
    global keep_running

    if keep_running:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Speak Now!\n")
            audio = r.listen(source)
            
            try:
                speech_text = r.recognize_google(audio)

                if input_lang.get() == "Hindi":
                    speech_text_transliteration = transliterate(speech_text, DEVANAGARI, ITRANS)
                else:
                    speech_text_transliteration = speech_text

                input_text.insert(tk.END, f"{speech_text_transliteration}\n")

                if speech_text.lower() in {'exit', 'stop'}:
                    keep_running = False
                    return

                translated_text = GoogleTranslator(
                    source=language_codes.get(input_lang.get(), "auto"),
                    target=language_codes.get(output_lang.get(), "en")
                ).translate(text=speech_text_transliteration)

                voice = gTTS(translated_text, lang=language_codes.get(output_lang.get(), "en"))
                voice.save('voice.mp3')
                playsound('voice.mp3')
                os.remove('voice.mp3')

                output_text.insert(tk.END, translated_text + "\n")

            except sr.UnknownValueError:
                output_text.insert(tk.END, "Could not understand!\n")
            except sr.RequestError:
                output_text.insert(tk.END, "Could not request from Google!\n")

    win.after(100, update_translation)

def run_translator():
    global keep_running
    if not keep_running:
        keep_running = True
        threading.Thread(target=update_translation).start()

def kill_execution():
    global keep_running
    keep_running = False

def open_webpage(url):
    webbrowser.open(url)

def open_about_page():
    about_window = tk.Toplevel()
    about_window.title("About")
    about_window.iconphoto(False, icon)

    github_link = ttk.Label(
        about_window,
        text="github.com/SamirPaulb/real-time-voice-translator",
        underline=True,
        foreground="blue",
        cursor="hand2"
    )
    github_link.bind("<Button-1>", lambda e: open_webpage("https://github.com/SamirPaulb/real-time-voice-translator"))
    github_link.pack()

    about_text = tk.Text(about_window, height=10, width=50)
    about_text.insert("1.0", """
    A machine learning project that translates voice from one language to another in real time 
    while preserving the tone and emotion of the speaker, and outputs the result in MP3 format.
    """)
    about_text.pack()

    close_button = tk.Button(about_window, text="Close", command=about_window.destroy)
    close_button.pack()

# Buttons
tk.Button(win, text="Start Translation", command=run_translator).place(relx=0.25, rely=0.9, anchor="c")
tk.Button(win, text="Kill Execution", command=kill_execution).place(relx=0.5, rely=0.9, anchor="c")
tk.Button(win, text="About this project", command=open_about_page).place(relx=0.75, rely=0.9, anchor="c")

# Run the GUI
win.mainloop()
