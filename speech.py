import speech_recognition as sr
import os
import eng_to_ipa as ipa

r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
	r.adjust_for_ambient_noise(source)
	audio = r.listen(source)

speech = r.recognize_google(audio)
print(ipa.convert(speech))
os.system("say {}".format(speech))
