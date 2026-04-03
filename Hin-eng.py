import speech_recognition as sr
from deep_translator import GoogleTranslator
import pyautogui
import time
import threading
import tkinter as tk
from tkinter import scrolledtext, filedialog

is_listening = False

def process_voice(status_label, root, text_area):
    global is_listening
    recognizer = sr.Recognizer()
    status_label.config(text="Switch to your typing window! (5 sec)...", fg="#FF9F0A")
    root.update()
    time.sleep(5)
    with sr.Microphone() as source:
        status_label.config(text="Adjusting for background noise...", fg="#0A84FF")
        root.update()
        recognizer.adjust_for_ambient_noise(source, duration=1)
        while is_listening:
            status_label.config(text="Listening continuously... Speak now!", fg="#32D74B")
            root.update()
            try:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=15)
                if not is_listening:
                    break
                status_label.config(text="Processing and Translating...", fg="#0A84FF")
                root.update()
                hindi_text = recognizer.recognize_google(audio, language="hi-IN")
                english_text = GoogleTranslator(source='hi', target='en').translate(hindi_text)
                pyautogui.write(english_text + " ", interval=0.01)
                text_area.insert(tk.END, f"Hindi: {hindi_text}\nEnglish: {english_text}\n\n")
                text_area.see(tk.END)
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                status_label.config(text="Could not understand, keep speaking...", fg="#FF3B30")
                root.update()
            except sr.RequestError:
                status_label.config(text="Network Error! Reconnecting...", fg="#FF3B30")
                root.update()
            except Exception as e:
                print(f"Error: {e}")
    status_label.config(text="Stopped Listening.", fg="#FF3B30")

def start_listening():
    global is_listening
    if not is_listening:
        is_listening = True
        start_btn.config(state=tk.DISABLED)
        stop_btn.config(state=tk.NORMAL)
        threading.Thread(target=process_voice, args=(status_label, root, text_area), daemon=True).start()

def stop_listening():
    global is_listening
    is_listening = False
    start_btn.config(state=tk.NORMAL)
    stop_btn.config(state=tk.DISABLED)
    status_label.config(text="Stopping after current sentence...", fg="#FF9F0A")

def save_transcription():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        title="Save Transcription As",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_area.get(1.0, tk.END))
        status_label.config(text=f"File saved successfully!", fg="#32D74B")

root = tk.Tk()
root.title("Continuous AI Voice Typer")
root.geometry("600x520")
root.configure(bg="#1E1E1E")
root.resizable(False, False)
title_label = tk.Label(root, text="Voice Typer & Transcription", font=("Inter", 16, "bold"), bg="#1E1E1E", fg="white")
title_label.pack(pady=15)
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=65, height=12, font=("Inter", 10), bg="#2D2D30", fg="white", borderwidth=0)
text_area.pack(pady=5, padx=15)
status_label = tk.Label(root, text="Ready. Click Start to begin.", font=("Inter", 11), bg="#1E1E1E", fg="#D1D1D6")
status_label.pack(pady=10)
btn_frame = tk.Frame(root, bg="#1E1E1E")
btn_frame.pack(pady=10)
start_btn = tk.Button(btn_frame, text="Start Listening", font=("Inter", 10, "bold"), bg="#0A84FF", fg="white", width=15, borderwidth=0, cursor="hand2", command=start_listening)
start_btn.grid(row=0, column=0, padx=10)
stop_btn = tk.Button(btn_frame, text="Stop / Done", font=("Inter", 10, "bold"), bg="#FF3B30", fg="white", width=15, borderwidth=0, cursor="hand2", state=tk.DISABLED, command=stop_listening)
stop_btn.grid(row=0, column=1, padx=10)
save_btn = tk.Button(root, text="Save Transcription File", font=("Inter", 10, "bold"), bg="#32D74B", fg="black", width=25, height=2, borderwidth=0, cursor="hand2", command=save_transcription)
save_btn.pack(pady=15)
root.attributes('-topmost', True)
root.mainloop()
