import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Retina image processing function
def process_retina(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    if image is None:
        print("Error: Unable to load the retina image.")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_image = clahe.apply(gray)

    # Detect blood vessels using Canny edge detection
    edges = cv2.Canny(enhanced_image, threshold1=50, threshold2=150)

    # Display retina results
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 3, 1)
    plt.title("Original Retina Image")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    plt.subplot(1, 3, 2)
    plt.title("Enhanced Retina Image")
    plt.imshow(enhanced_image, cmap="gray")

    plt.subplot(1, 3, 3)
    plt.title("Canny Edge Detection (Retina)")
    plt.imshow(edges, cmap="gray")
    plt.tight_layout()
    plt.show()

# Face detection function
def detect_faces(image_path):
    image = cv2.imread(image_path)
    
    if image is None:
        print("Error: Unable to load the face image.")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display face detection results
    plt.figure(figsize=(8, 6))
    plt.title("Face Detection")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

# Provide paths to retina and face images
retina_image_path = "retina image.jpeg"  # Replace with your retina image path
face_image_path = "Mani.jpg"      # Replace with your face image path

# Call the processing functions
print("Processing Retina Image...")
process_retina(retina_image_path)

print("Detecting Faces...")
detect_faces(face_image_path)