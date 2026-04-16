import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()
    engine.stop()

recognizer = sr.Recognizer()
while True:
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            if "hello" in text.lower():
                speak("Hello there!")

            elif "how are you" in text.lower():
                speak("I am doing great!")

            elif "bye" in text.lower():
                speak("Goodbye!")
                break
            else:
                speak("I did not understand that.")
            print("You said:", text)
        except:
            speak("Sorry, I could not hear you.")
