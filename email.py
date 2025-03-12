import smtplib
import time
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

# Initialize Firebase
cred = credentials.Certificate("path/to/serviceAccountKey.json")  # Replace with your JSON key file
firebase_admin.initialize_app(cred)
db = firestore.client()

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-password"

def send_email(to_email, lecture_time):
    subject = "Lecture Reminder"
    body = f"Reminder: You have a lecture at {lecture_time}. Please be ready."
    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, message)
        print(f"Email sent to {to_email} for lecture at {lecture_time}")
    except Exception as e:
        print(f"Error sending email: {e}")

def check_and_send_reminders():
    now = datetime.now()
    reminder_time = (now + timedelta(minutes=10)).strftime("%H:%M")  # 10 minutes ahead

    lectures = db.collection("lectures").stream()
    
    for lecture in lectures:
        data = lecture.to_dict()
        if data.get("lectureTime") == reminder_time:
            send_email(data["email"], data["lectureTime"])

# Run the function every minute
while True:
    check_and_send_reminders()
    time.sleep(60)  # Wait for a minute before running again
