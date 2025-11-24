import tkinter as tk
import pyperclip
import speech_recognition as sr
import threading

def recording():
  global listening, stopper, rec_button

  if not listening:

    listening = True
    rec_button.config(text= "Aufnahme Beenden")

    mic = sr.Microphone()
    r = sr.Recognizer()
    r.pause_threshold = 20

    def callback(r, audio):
      global audio_data
      audio_data = audio
    
    stopper = r.listen_in_background(mic, callback)

    return

  if listening:

    listening = False
    rec_button.config(text = "Aufnahme Starten")

    if stopper:
      stopper()
      stopper = None

def main():

  global listening 
  listening = False
  global stopper
  stopper = None

  root = tk.Tk()
  root.title("Speech to Text")
  root.geometry("300x200")

  global rec_button
  rec_button = tk.Button(root, text = "Aufnahme Starten", command=lambda: recording())
  rec_button.pack(pady=10)
  conv_button = tk.Button(text = "Audio umwandeln")
  conv_button.pack(pady=10)
  copy_button = tk.Button(text = "Text kopieren")
  copy_button.pack(pady=10)


  root.mainloop()

if __name__ == "__main__":
   main()