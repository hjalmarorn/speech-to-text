import speech_recognition as sr
import os
import eng_to_ipa as ipa
from flask import Flask, render_template, request
import sqlite3
import threading
import sys

app = Flask(__name__)
word = ""


def rec(recognizer, audio):
	global word
	conn = sqlite3.connect('words.db', check_same_thread=False)
	try: 
		speech = recognizer.recognize_google(audio)
		text = ipa.convert(speech)
		print(text)
		if(text != word):
			word = text
			conn.execute("INSERT INTO words (word, ipa) VALUES(?,?)", (text, speech))
			conn.commit()
			conn.close()
		else:
			word = '?'
	except sr.UnknownValueError as e:
		print("Didn't catch that")
	except Exception as e:
		print(e.message)

@app.route('/newWord', methods=["GET"])
def get_new_word():
	global word
	newWord = word
	word = "?"
	return newWord

def get_all_words():
	conn = sqlite3.connect('words.db', check_same_thread=False)
	cur = conn.cursor()
	rows = cur.execute(''' SELECT word, ipa FROM words ORDER BY id DESC''')
	word_list = ["[" + str(item[0]) + "]" for item in rows]
	print(word_list)
	return word_list
	conn.close()

@app.route('/', methods=["GET", "POST"])
def index():
	word_list = get_all_words()
	return render_template("test.html", word_list=word_list)

def init():
	r = sr.Recognizer()

	m = sr.Microphone()


	with m as source:
		r.adjust_for_ambient_noise(source)

	r.dynamic_energy_threshold = False
	r.energy_threshold = 500
	stop_listening = r.listen_in_background(m, rec)
	conn = sqlite3.connect('words.db', check_same_thread=False)
	conn.execute('''CREATE TABLE IF NOT EXISTS words (id integer primary key, word string, ipa string)''')
	conn.close()


init()


