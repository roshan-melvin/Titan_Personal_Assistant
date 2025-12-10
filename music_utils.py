import os
import pygame
import time
from urllib.parse import quote
from speech_utils import speak 
import webbrowser

# Initialize pygame mixer
pygame.mixer.init()

def open_browser(query):
    """Open a browser with a search query."""
    search_url = f"https://www.google.com/search?q={quote(query)}"
    webbrowser.open(search_url)

def play_music(song_name=None):
    """Play music from the local folder or search online."""
    if not song_name:
        speak("Please specify a song name.")
        return
    
    music_folder = os.path.expanduser('~/Music')
    song_path = os.path.join(music_folder, song_name)

    if not os.path.exists(song_path):
        speak("Sorry, the song was not found in the default music folder. Searching online.")
        search_online(song_name)
        return

    try:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        speak(f"Playing {song_name}")
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    except Exception as e:
        speak(f"Error playing music: {e}")
        print(f"Error: {e}")

def search_online(query):
    """Search for a song online."""
    speak("Searching for the song online.")
    open_browser(query)
