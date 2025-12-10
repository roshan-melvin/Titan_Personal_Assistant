import dlib
import numpy as np
import cv2
import pickle
import os
import time

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES_DIR = os.path.join(SCRIPT_DIR, 'Modules')

# Load the shape predictor model
shape_predictor_path = os.path.join(MODULES_DIR, 'shape_predictor_68_face_landmarks.dat')
if not os.path.exists(shape_predictor_path):
    raise FileNotFoundError(f"Shape predictor model not found at: {shape_predictor_path}")
shape_predictor = dlib.shape_predictor(shape_predictor_path)

# Load the face recognition model
face_rec_model_path = os.path.join(MODULES_DIR, 'dlib_face_recognition_resnet_model_v1.dat')
if not os.path.exists(face_rec_model_path):
    raise FileNotFoundError(f"Face recognition model not found at: {face_rec_model_path}")
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)

def encode_face(image, face_location):
    """Generate face encoding from an image and face location."""
    try:
        shape = shape_predictor(image, face_location)
        face_encoding = np.array(face_rec_model.compute_face_descriptor(image, shape))
        return face_encoding
    except Exception as e:
        print(f"Error encoding face: {e}")
        return None

def find_closest_match(face_encoding, known_encodings, threshold=0.4):
    min_distance = float('inf')
    best_match_name = None
    for name, encoding in known_encodings.items():
        distance = np.linalg.norm(encoding - face_encoding)
        if distance < min_distance:
            min_distance = distance
            best_match_name = name
    if min_distance < threshold:
        return best_match_name
    return None

def recognize_face(known_encodings, timeout=15):
    """Recognize a face from webcam feed against known encodings."""
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not open webcam")
        return False, None
    
    face_found = False
    recognized_name = None
    face_detector = dlib.get_frontal_face_detector()
    start_time = time.time()
    
    while not face_found and (time.time() - start_time) < timeout:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_detector(rgb_frame)

        for face_location in face_locations:
            face_encoding = encode_face(rgb_frame, face_location)
            if face_encoding is not None:
                recognized_name = find_closest_match(face_encoding, known_encodings)

                if recognized_name:
                    face_found = True
                    break

        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return face_found, recognized_name

def save_face_encoding(name, face_encoding):
    """Save a face encoding with a name to the encodings file."""
    encodings_file = 'encodings.pkl'
    try:
        if os.path.exists(encodings_file):
            with open(encodings_file, 'rb') as file:
                known_encodings = pickle.load(file)
        else:
            known_encodings = {}

        known_encodings[name] = face_encoding
        with open(encodings_file, 'wb') as file:
            pickle.dump(known_encodings, file)
        return True
    except Exception as e:
        print(f"Error saving face encoding: {e}")
        return False

def load_known_encodings():
    """Load known face encodings from the encodings file."""
    encodings_file = 'encodings.pkl'
    try:
        if os.path.exists(encodings_file):
            with open(encodings_file, 'rb') as file:
                known_encodings = pickle.load(file)
            return known_encodings
        else:
            return {}
    except Exception as e:
        print(f"Error loading face encodings: {e}")
        return {}
