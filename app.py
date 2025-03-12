from flask import Flask, request, jsonify
import psycopg2
import numpy as np
import base64
import cv2
import requests
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# PostgreSQL Database Connection
DB_CONFIG = {
    'dbname': 'iris_attendance_db',
    'user': 'postgres',   # Change if using a different username
    'password': 'Manasvi2006',  # Change to your PostgreSQL password
    'host': 'localhost',
    'port': '5432'
}

def connect_db():
    return psycopg2.connect(**DB_CONFIG)

# Store iris template in the database
def insert_attendance(user_id, iris_template):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO iris_attendance (user_id, iris_template) 
        VALUES (%s, %s) RETURNING id;
    """, (user_id, psycopg2.Binary(iris_template)))
    conn.commit()
    cursor.close()
    conn.close()
    return True

@app.route('/store_iris', methods=['POST'])
def store_iris():
    data = request.get_json()
    user_id = data.get('user_id')
    iris_template = base64.b64decode(data.get('iris_template'))  # Decode image data
    
    if insert_attendance(user_id, iris_template):
        return jsonify({"message": "Attendance recorded successfully!"}), 201
    else:
        return jsonify({"error": "Failed to store iris data"}), 500

# Retrieve stored iris templates from the database
def get_stored_iris(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT iris_template FROM iris_attendance WHERE user_id = %s ORDER BY timestamp DESC LIMIT 1", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

# Function to compare iris images
def compare_iris(stored_iris, new_iris):
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(stored_iris, None)
    kp2, des2 = orb.detectAndCompute(new_iris, None)
    
    if des1 is None or des2 is None:
        return False
    
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    
    score = len(matches) / max(len(kp1), len(kp2))
    return score > 0.7  # Match threshold

@app.route('/recognize_iris', methods=['POST'])
def recognize_iris():
    data = request.get_json()
    user_id = data.get('user_id')
    new_iris_image = base64.b64decode(data.get('iris_template'))
    
    stored_iris = get_stored_iris(user_id)
    if not stored_iris:
        return jsonify({"error": "No stored iris data found"}), 404
    
    # Convert images from binary
    stored_iris_np = np.frombuffer(stored_iris, dtype=np.uint8)
    new_iris_np = np.frombuffer(new_iris_image, dtype=np.uint8)
    stored_iris_img = cv2.imdecode(stored_iris_np, cv2.IMREAD_GRAYSCALE)
    new_iris_img = cv2.imdecode(new_iris_np, cv2.IMREAD_GRAYSCALE)
    
    if compare_iris(stored_iris_img, new_iris_img):
        return jsonify({"message": "Iris Matched! Access Granted."}), 200
    else:
        return jsonify({"message": "Iris Not Recognized! Access Denied."}), 401

# Function to capture iris image and send for recognition
def capture_iris_and_recognize():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                eye_img = roi_color[ey:ey+eh, ex:ex+ew]
                cv2.imshow('Iris', eye_img)
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    cv2.imwrite('iris_image.jpg', eye_img)
                    print("Iris image saved as iris_image.jpg")
                    cap.release()
                    cv2.destroyAllWindows()
                    
                    # Convert image to base64 and send for recognition
                    with open('iris_image.jpg', 'rb') as img_file:
                        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                    
                    response = requests.post("http://127.0.0.1:5000/recognize_iris", json={
                        "user_id": 1,  # Change this dynamically as needed
                        "iris_template": img_base64
                    })
                    print("Server Response:", response.json())
                    return
        
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture_iris_and_recognize()  # Capture and recognize iris
    app.run(debug=True)
