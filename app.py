import speech_recognition as sr
import os
import eng_to_ipa as ipa
from flask import Flask, render_template, request
import sqlite3
import threading

word = ""
app = Flask(__name__)

word_list = []

def rec():
	global word
	global word_list


	while(True):
		try:
			conn = sqlite3.connect('words.db', check_same_thread=False)
			r = sr.Recognizer()
			r.energy_threshold = 3000
			mic = sr.Microphone(device_index=0)
			with mic as source:
				print("listening...")
				r.adjust_for_ambient_noise(source)
				audio = r.listen(source)

			speech = r.recognize_google(audio)

			text = ipa.convert(speech)
			if(text != word):
				word = text
				conn.execute("INSERT INTO words (word, ipa) VALUES(?,?)", (text, speech))
				conn.commit()
				conn.close()
			else:
				word = '?'
		except sr.UnknownValueError:
			word = '?'
		

@app.route('/newWord', methods=["GET"])
def get_new_word():
	global word
	newWord = word
	word = "?"
	print(newWord)
	return newWord

def get_all_words():
	conn = sqlite3.connect('words.db', check_same_thread=False)
	cur = conn.cursor()
	rows = cur.execute(''' SELECT word, ipa FROM words ORDER BY id DESC''')
	word_list = ["[" + item[0] + "]" for item in rows]
	print(word_list)
	return word_list

def clear_db():
	conn = sqlite3.connect('words.db', check_same_thread=False)
	cur = conn.cursor()
	cur.execute('''DROP TABLE IF EXISTS words''')
	conn.close()

@app.route('/', methods=["GET", "POST"])
def index():
	word_list = get_all_words()
	return render_template("test.html", word_list=word_list)

def init():
	word_thread = threading.Thread(target=rec)
	word_thread.daemon = True
	word_thread.start()
	conn = sqlite3.connect('words.db', check_same_thread=False)
	conn.execute('''CREATE TABLE IF NOT EXISTS words (id integer primary key, word string, ipa string)''')
	conn.close()

init()
#clear_db()
