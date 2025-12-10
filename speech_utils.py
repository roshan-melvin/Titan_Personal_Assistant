import pyttsx3
import speech_recognition as sr
import winsound

def speak(text):
    """Convert text to speech."""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

def play_buzzer():
    """Play a beep sound to indicate listening mode."""
    try:
        winsound.Beep(1000, 500)
    except Exception as e:
        print(f"Error playing buzzer: {e}")

def listen():
    """Listen to user's voice command and convert to text."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            play_buzzer()
            print("Titan: Listening...")
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio)
                return command.lower()
            except sr.UnknownValueError:
                speak("Sorry, I did not understand that.")
                return None
            except sr.RequestError:
                speak("Sorry, my speech service is down.")
                return None
    except Exception as e:
        print(f"Error accessing microphone: {e}")
        return None
