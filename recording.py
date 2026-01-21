import tkinter as tk
import pyaudio, sys, tiktoken, wave, threading, pyperclip
from pathlib import Path
from faster_whisper import WhisperModel

#die Audio Aufnahme muss in einem extra thread laufen, damit Start/Stop funktionen entkoppelt voneinander Implementiert werden können
stop_event = threading.Event()
recording_thread = None

#standard einstellungen für das recording übernommen, Sekunden auf 1 gestellt, da die Aufnahme in einer loop läuft
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 0.5

#Vaiablen global erstellen, damit man aus verschiedenen Funktionen auf sie zugreifen kann:
AUDIO_FILE = 'recording.wav'
FILE_PATH = Path(AUDIO_FILE)

copy_button = None
transcribed_text = ""

def recording():

  append_old_frames = False

  # if the recording file already existst we safe the old frames, so we can write them into the new file as well
  if FILE_PATH.exists():
     with wave.open(AUDIO_FILE, "rb") as r:
      params = r.getparams()
      old_frames = r.readframes(r.getnframes())
      append_old_frames = True

  # we open the .wav file in wb= write binary mode (there is no append mode for wave), we first write the old_frames to the file and then record new audio
  with wave.open(AUDIO_FILE, 'wb') as wf:
      p = pyaudio.PyAudio()
      wf.setnchannels(CHANNELS)
      wf.setsampwidth(p.get_sample_size(FORMAT))
      wf.setframerate(RATE)
      if append_old_frames:
        wf.writeframes(old_frames)

      stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

      # Aufnahme loop, läuft solange bis der Thread das stop_event erhält
      while not stop_event.is_set():
        for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
          wf.writeframes(stream.read(CHUNK))

      stream.close()
      p.terminate()

#seperater Thread wird erstellt um die Aufnahme im hintergrund und entkoppelt von der record funktion durchzuführen
def start_recording():
  global recording_thread
  stop_event.clear()

  recording_thread = threading.Thread(target=recording)
  recording_thread.start()

#Aufnahme Thread erhält das stop_event
def stop_recording():
  stop_event.set()
  recording_thread.join()

def transcription(copy_button):

  global transcribed_text

  if not FILE_PATH.exists():
    return

  #transcriping speech to text and saving it in segments
  segments, info = transcription_model.transcribe(AUDIO_FILE, language="de", beam_size=1, word_timestamps=False, vad_filter=False)
  print('transribtion done')

  #joinging text from segments and saving it to a variable
  transcribed_text = "".join(seg.text for seg in segments)

  copy_button.config(bg="green")

#triggering the transcription thead
def trigger_transcription(copy_button):
  threading.Thread(target=transcription(copy_button), daemon=True).start()

#kopiert den text in die Zwischenablage
def copy_transcription():
    global transcribed_text

    pyperclip.copy(str(transcribed_text))

def main():

  root = tk.Tk()
  root.title("Speech to Text")
  root.geometry("300x200")

  global copy_button

  rec_button = tk.Button(root, text = "Aufnahme Starten", command=lambda: start_recording())
  rec_button.pack(pady=10)
  rec_button = tk.Button(root, text = "Aufnahme pausieren", command=lambda: stop_recording())
  rec_button.pack(pady=10)
  conv_button = tk.Button(text = "Audio umwandeln", command=lambda: trigger_transcription(copy_button))
  conv_button.pack(pady=10)
  copy_button = tk.Button(text = "Text kopieren", command=lambda: copy_transcription())
  copy_button.pack(pady=10)


  root.mainloop()

if __name__ == "__main__":
   transcription_model = WhisperModel("medium", device="cpu", compute_type="float32", cpu_threads=8)
   main()

#runtime bottleneck = looping through segments and getting the text out of it line 79