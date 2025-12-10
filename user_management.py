import pickle
import os
from speech_utils import speak 
def list_users():
    """Return a list of registered user names."""
    encodings_file = 'encodings.pkl'
    if os.path.exists(encodings_file):
        with open(encodings_file, 'rb') as file:
            known_encodings = pickle.load(file)
        return list(known_encodings.keys())
    else:
        return []

def delete_user_face(name, passcode=None):
    """Delete a user's face encoding. Passcode verification is done in main.py."""
    encodings_file = 'encodings.pkl'
    if os.path.exists(encodings_file):
        with open(encodings_file, 'rb') as file:
            known_encodings = pickle.load(file)
        if name in known_encodings:
            del known_encodings[name]
            with open(encodings_file, 'wb') as file:
                pickle.dump(known_encodings, file)
            return True
        else:
            return False
    else:
        return False
