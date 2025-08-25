import speech_recognition as sr
from googletrans import Translator
import tkinter as tk
from tkinter import scrolledtext
import random
import time
import threading

# Function to capture speech input in Hindi
def capture_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening for Hindi speech...") 
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source) 

    try:
        # Recognize speech using Google's speech recognition
        hindi_text = recognizer.recognize_google(audio, language="hi-IN") 
        print(f"Recognized Hindi Text: {hindi_text}")  
        return hindi_text 
    except sr.UnknownValueError:  
        print("Could not understand the audio.")
        return ""
    except sr.RequestError: 
        print("Request error.")
        return ""

# Function to translate text from Hindi to English
def translate_text(hindi_text):
    translator = Translator() 
    translation = translator.translate(hindi_text, src='hi', dest='en')
    english_text = translation.text
    return english_text

# Function to capture speech and display it in the text editor
def run_speech_to_text():
    hindi_text = capture_speech()
    if hindi_text:
        # Insert the recognized Hindi text into the text editor
        text_editor.insert(tk.END, f"Hindi: {hindi_text}\n")

        # Translate the Hindi text to English
        english_text = translate_text(hindi_text)
        # Insert the translated English text into the text editor
        text_editor.insert(tk.END, f"English: {english_text}\n")

# Function to run continuous listening with random intervals
def continuous_listening():
    while True:
        run_speech_to_text()
        # Pause for a random duration between 5 and 10 seconds before listening again
        pause_duration = random.randint(5, 10)
        print(f"Pausing for {pause_duration} seconds...")
        time.sleep(pause_duration) 

# Function to start continuous listening in a separate thread
def start_listening():
    listening_thread = threading.Thread(target=continuous_listening)
    listening_thread.daemon = True  # Ensures the thread exits when the main program exits
    listening_thread.start()

# Create the GUI for a simple text editor
root = tk.Tk()
root.title("Speech to Text and Translation")

# Create a scrolled text widget
text_editor = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15, font=("Times New Roman", 15))
text_editor.pack(padx=10, pady=10)

# Add a button to start the continuous speech capture and translation
start_button = tk.Button(root, text="Start Listening", command=start_listening, font=("Arial", 12))
start_button.pack(pady=10)

root.mainloop()
