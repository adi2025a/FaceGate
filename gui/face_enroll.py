import cv2
import face_recognition
import numpy as np
import os

def capture_and_save_face(save_path="data/user_face.npy"):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return False

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb)

    if len(face_locations) != 1:
        return False  # Only proceed if exactly one face

    face_encoding = face_recognition.face_encodings(rgb, face_locations)[0]

    os.makedirs("data", exist_ok=True)
    np.save(save_path, face_encoding)
    return True
