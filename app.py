import speech_recognition as sr
import os
import eng_to_ipa as ipa
from flask import Flask, render_template



app = Flask(__name__)

r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
	r.adjust_for_ambient_noise(source)
	audio = r.listen(source)

speech = r.recognize_google(audio)

text = ipa.convert(speech)

@app.route('/', methods=["GET", "POST"])
def index():
	return render_template("test.html", text=text)