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
			mic = sr.Microphone()
			with mic as source:
				print("listening...")
				#r.adjust_for_ambient_noise(source)
				audio = r.listen(source)

			speech = r.recognize_google(audio)

			text = ipa.convert(speech)
			if(text != word):
				word = text
				conn.execute("INSERT INTO words VALUES(?,?)", (text, speech))
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
	word = ""
	print(newWord)
	return newWord


def get_all_words():
	conn = sqlite3.connect('words.db', check_same_thread=False)
	cur = conn.cursor()
	rows = cur.execute(''' SELECT * FROM words''')
	word_list = ""
	for row in rows:
		word_list += row[0] + " "
	return word_list

@app.route('/', methods=["GET", "POST"])
def index():
	word_list = get_all_words()
	return render_template("test.html", word_list=word_list)

def init():
	word_thread = threading.Thread(target=rec)
	word_thread.daemon = True
	word_thread.start()
	conn = sqlite3.connect('words.db', check_same_thread=False)
	conn.execute('''CREATE TABLE IF NOT EXISTS words (word string, ipa string)''')
	conn.execute(''' SELECT * FROM words''')
	conn.close()

init()