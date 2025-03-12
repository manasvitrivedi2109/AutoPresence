import cv2
import numpy as np
import dlib
import face_recognition
from datetime import datetime

# Initialize face detector and recognition models
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_recognition_model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

# Initialize a dictionary for attendance tracking
attendance = {}

# Function to mark attendance
def mark_attendance(name):
    # Get current timestamp
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if name not in attendance:
        attendance[name] = current_time
        print(f"Attendance recorded for {name} at {current_time}")

# Function to detect and recognize the face
def recognize_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    face_locations = []
    for face in faces:
        landmarks = predictor(gray, face)
        (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())
        face_locations.append((x, y, w, h))
    return face_locations

# Function to recognize the iris (eye region) - simple detection based on eye regions
def recognize_iris(frame, face_locations):
    # Convert to grayscale for better processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    for (x, y, w, h) in face_locations:
        # Focus on the eye region
        eye_region = gray[y:y + h, x:x + w]
        
        # Detect eyes using Haar Cascade Classifier
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale(eye_region, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (ex, ey, ew, eh) in eyes:
            # Draw a rectangle around each detected eye
            cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)

    return frame

# Function to recognize face using face_recognition and record attendance
def process_frame(frame):
    # Convert to RGB (face_recognition library expects RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find faces in the frame using face_recognition
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Iterate through each detected face and recognize it
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            mark_attendance(name)

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Recognize iris (eyes)
    frame = recognize_iris(frame, face_locations)

    return frame

# Load known faces and their names
# In a real application, you would load your known faces from a database or files
known_face_names = ["Manasvi.jpg", "Aayushi.jpg"]
known_face_encodings = [
    face_recognition.face_encodings(face_recognition.load_image_file("Manasvi.jpg"))[0],  # Example of encoding for Person 1
    face_recognition.face_encodings(face_recognition.load_image_file("Aayushi.jpg"))[0],  # Example of encoding for Person 2
]

# Initialize webcam capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame for face and iris recognition
    frame = process_frame(frame)

    # Display the resulting frame
    cv2.imshow('Face and Iris Recognition', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Display recorded attendance after exiting
print("Attendance Record:")
for name, timestamp in attendance.items():
    print(f"{name} - {timestamp}")