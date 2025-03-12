import cv2
import numpy as np
import psycopg2
import dlib

# Database Connection
DB_CONFIG = {
    "dbname": "iris_attendance",
    "user": "Manasvi Trivedi",
    "password": "Manasvi2006",
    "host": "localhost",
    "port": "5432"
}

def store_result(matched):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("INSERT INTO iris_verification (status) VALUES (%s)", (matched,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Database Error:", e)

def detect_iris(image):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    
    for face in faces:
        landmarks = predictor(gray, face)
        left_eye = (landmarks.part(36).x, landmarks.part(36).y)
        right_eye = (landmarks.part(45).x, landmarks.part(45).y)
        
        cv2.circle(image, left_eye, 5, (0, 255, 0), -1)
        cv2.circle(image, right_eye, 5, (0, 255, 0), -1)
    
    return image

def compare_iris(captured_image, ref_images):
    captured_gray = cv2.cvtColor(captured_image, cv2.COLOR_BGR2GRAY)
    
    for ref_path in ref_images:
        ref_image = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
        ref_image = cv2.resize(ref_image, captured_gray.shape[::-1])
        
        diff = np.sum(np.abs(captured_gray - ref_image))
        if diff < 500000:  # Threshold for match
            return "Matched"
    
    return "Not Matched"

def capture_and_recognize():
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        
        processed_frame = detect_iris(frame)
        cv2.imshow("Iris Detection", processed_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cam.release()
    cv2.destroyAllWindows()
    
    # Compare with saved eyes
    result = compare_iris(frame, ["cropped_eye_1.jpg", "cropped_eye_2.jpg"])
    print("Recognition Result:", result)
    store_result(result)

capture_and_recognize()
