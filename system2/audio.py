#System packages
import speech_recognition as sr
import pyttsx

#User Defined Packages

#Global definitions
speech_engine = pyttsx.init()
speech_engine.setProperty('rate', 180)
re = sr.Recognizer()

#Classes
def speak(text):
	speech_engine.say(text)
	speech_engine.runAndWait()

def listen():
	with sr.Microphone() as source:
		re.adjust_for_ambient_noise(source)
		audio = re.listen(source)
		try:
			value=re.recognize_google(audio, language="en")
			print 'audio.py value:',value
			return value
		except sr.UnknownValueError as e:
			speak("Could not understand audio")
			pass
		except sr.RequestError as e:
			speak("Recog Error; {0}".format(e))
			pass