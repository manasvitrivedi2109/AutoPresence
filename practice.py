import cv2
import numpy as np
from scipy.spatial.distance import euclidean

# Initialize the camera
camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    if not ret:
        break

    # Display the live feed
    cv2.imshow('Camera Feed', frame)

    # Capture the image when the user presses 'c'
    if cv2.waitKey(1) & 0xFF == ord('c'):
        cv2.imwrite("iris_image.jpg", frame)
        break

camera.release()
cv2.destroyAllWindows()

# Read the captured image
image = cv2.imread('iris_image.jpg')

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur to reduce noise
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Apply edge detection (Canny)
edges = cv2.Canny(blurred_image, 100, 200)

# Predefined feature (this would typically be extracted from a stored iris image)
stored_feature = np.array([0, 1, 1, 0, 0, 1, 1, 0])  # Example feature

# Flatten the edge-detected image (for simplicity, this is just a basic example)
captured_feature = edges.flatten()

# Calculate similarity (using Euclidean distance)
distance = euclidean(captured_feature, stored_feature)

# Set a threshold for recognition
if distance < 10000:
    print("Iris recognized!")
else:
    print("Iris not recognized.")
