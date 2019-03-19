import speech_recognition as sr
import os
import eng_to_ipa as ipa
from flask import Flask, render_template, request
import sqlite3





app = Flask(__name__)

def rec():
	r = sr.Recognizer()
	mic = sr.Microphone()

	with mic as source:
		print("listening...")
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)

	speech = r.recognize_google(audio)

	text = ipa.convert(speech)
	return text

@app.route('/newWord', methods=["GET"])
def get_new_word():
	text = rec()
	return text


@app.route('/', methods=["GET", "POST"])
def index():
	if(request.method == "POST"):
		text = rec()
		return render_template("test.html", text=text)
	else:
		return render_template("test.html")

