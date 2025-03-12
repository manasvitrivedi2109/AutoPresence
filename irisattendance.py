import traceback
import datetime
import firebase_admin
import numpy as np
import cv2
import base64
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify

with open("sample_iris.jpg", "rb") as image_file:
    base64_string = base64.b64encode(image_file.read()).decode('utf-8')
print(base64_string)

app = Flask(__name__)

# Initialize Firebase
try:
    cred = credentials.Certificate("firebase_credentials.json")  # Ensure this file exists!
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase initialized successfully!")
except Exception as e:
    print("❌ Firebase initialization failed:", str(e))
    exit(1)  # Stop execution if Firebase fails
def recognize_iris(image_data):
    print("🔍 Running Iris Recognition...")
    return "John Doe"  # Always return a valid user for testing
# Function to recognize iris (Dummy example, replace with real logic)
def recognize_iris(image_data):
    try:
        print("📷 Decoding image...")
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            print("⚠️ Image decoding failed!")
            return None

        print("🔍 Running Iris Recognition...")
        # Replace the following with actual recognition logic
        registered_users = ["Manasvi Trivedi"]  # Example database of users
        recognized_name = np.random.choice(registered_users)  # Dummy recognition
        return recognized_name

    except Exception as e:
        print("❌ Error in recognize_iris:", str(e))
        return None

# Flask Route: Process Iris Recognition
@app.route('/process_iris', methods=['POST'])
def process_iris():
    print("🚀 Request received at /process_iris")

    try:
        data = request.json
        print("📩 Received Data:", data)

        if 'image' not in data:
            print("⚠️ No image data found in request")
            return jsonify({"success": False, "message": "No image data provided!"}), 400

        user_name = recognize_iris(data['image'])
        print("👁️ Recognized User:", user_name)

        if user_name:
            timestamp = datetime.datetime.now().isoformat()
            db.collection("attendance").document(user_name).set({
                "name": user_name,
                "time": timestamp
            }, merge=True)

            print(f"✅ Attendance Marked for {user_name} at {timestamp}")
            return jsonify({"success": True, "user": user_name, "timestamp": timestamp})

        else:
            print("❌ Iris not recognized!")
            return jsonify({"success": False, "message": "Iris not recognized!"}), 401

    except Exception as e:
        print("🔥 Full Error Traceback:")
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True, port=5000)
