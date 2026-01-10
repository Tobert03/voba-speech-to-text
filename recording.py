import tkinter as tk
import pyaudio, sys, tiktoken, wave
from pathlib import Path

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 5

AUDIO_FILE = 'recording.wav'
FILE_PATH = Path(AUDIO_FILE)

def recording():

  #recording_mode = 'ab' if FILE_PATH.exists() else 'wb'

  # if the recording file already existst we safe the old frames, so we can write them into the new file as well
  if FILE_PATH.exists():
     with wave.open(AUDIO_FILE, "rb") as r:
      params = r.getparams()
      old_frames = r.readframes(r.getnframes())

  # we open the .wav file in wb= write binary mode (there is no append mode for wave), we first write the old_frames to the file and then record new audio
  with wave.open(AUDIO_FILE, 'wb') as wf:
      p = pyaudio.PyAudio()
      wf.setnchannels(CHANNELS)
      wf.setsampwidth(p.get_sample_size(FORMAT))
      wf.setframerate(RATE)
      wf.writeframes(old_frames)

      stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

      # recording audio
      for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
        wf.writeframes(stream.read(CHUNK))


      '''
      print('Recording...')
      for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
          wf.writeframes(stream.read(CHUNK))
      print('Done')
      '''
      
      stream.close()
      p.terminate()

def main():

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