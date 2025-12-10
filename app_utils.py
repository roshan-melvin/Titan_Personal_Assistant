import subprocess
import webbrowser

def open_application(app_name):
    """Open an application based on the app name."""
    try:
        app_name_lower = app_name.lower().strip()
        if app_name_lower == "notepad":
            subprocess.Popen(["notepad.exe"])
            return True
        elif app_name_lower == "calculator":
            subprocess.Popen(["calc.exe"])
            return True
        else:
            print(f"Application '{app_name}' is not recognized.")
            return False
    except Exception as e:
        print(f"Error opening application: {e}")
        return False

def close_application(app_name):
    """Close an application based on the app name."""
    try:
        app_name_lower = app_name.lower().strip()
        if app_name_lower == "notepad":
            subprocess.call(["taskkill", "/F", "/IM", "notepad.exe"])
            return True
        elif app_name_lower == "calculator":
            subprocess.call(["taskkill", "/F", "/IM", "calc.exe"])
            return True
        else:
            print(f"Application '{app_name}' is not recognized.")
            return False
    except Exception as e:
        print(f"Error closing application: {e}")
        return False

def open_youtube(search_query):
    """Open YouTube with a specific search query."""
    url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
    webbrowser.open(url)

def open_browser(search_query):
    """Open the default web browser with a search query."""
    url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
    webbrowser.open(url)

def open_spotify(search_query):
    """Open Spotify with a specific search query."""
    url = f"https://open.spotify.com/search/{search_query.replace(' ', '%20')}"
    webbrowser.open(url)

# Additional functions can be added as needed.
