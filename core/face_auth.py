import cv2
import face_recognition
import numpy as np
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'user_face.npy')

def load_saved_embedding():
    """Load the saved face embedding from file."""
    if not os.path.exists(DATA_PATH):
        print("No saved face embedding found.")
        return None
    return np.load(DATA_PATH)

def capture_face_embedding():
    """Capture face from webcam and return its embedding."""
    cap = cv2.VideoCapture(0)
    print("Capturing face... Please look at the camera.")

    face_encoding = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect face and get encoding
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if face_encodings:
            face_encoding = face_encodings[0]
            break

        cv2.imshow("Face Authentication - Press Q to cancel", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return face_encoding

def verify_user(tolerance=0.5):
    """Check if the live webcam face matches the saved embedding."""
    saved_embedding = load_saved_embedding()
    if saved_embedding is None:
        return False

    current_embedding = capture_face_embedding()
    if current_embedding is None:
        print("No face detected.")
        return False

    match = face_recognition.compare_faces([saved_embedding], current_embedding, tolerance=tolerance)[0]
    return match
