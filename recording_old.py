import speech_recognition as sr
from enum import Enum

import time

class Language(Enum):
  GERMAN = "de-DE"

class recording():

  #returns a dictionary of all audio devices:
  def show_mics():
    mics = {}
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
      mics[index] = name
    return mics

  #input: index des audio devices, maximale aufnahme länge, maximale pause
  #function: führt die aufnahme durch und gibt die audio datei zurück
  def choose_mic(index, max_recording, max_pause):
    r = sr.Recognizer()
    with sr.Microphone(device_index=index) as source:

      r.dynamic_energy_threshold = True

      r.pause_threshold = max_pause
      r.adjust_for_ambient_noise(source, duration=3)
      start = time.perf_counter()
      print("listening")
      audio = r.listen(source, timeout=10, phrase_time_limit=max_recording)
      print("gestoppt")
      end = time.perf_counter()
      print(end-start)
      
    return audio
  
  def convert(audio, language=Language.GERMAN):
    r = sr.Recognizer()
    try:
        text = r.recognize_google(audio, language=language.value)
    except:
      text = "versuche es erneut..."

    return text

#print(select_mic.show_mics())

