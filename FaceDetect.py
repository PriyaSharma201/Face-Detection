import cv2
from deepface import DeepFace
import matplotlib.pyplot as plt
import numpy as np

# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start capturing video
cap = cv2.VideoCapture(0)

def handle_close(event):
    global running
    running = False

# Create a figure for matplotlib
fig = plt.figure()
fig.canvas.mpl_connect('close_event', handle_close)

running = True

while running:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert grayscale frame to RGB format
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Extract the face ROI (Region of Interest)
        face_roi = rgb_frame[y:y + h, x:x + w]

        # Perform emotion analysis on the face ROI
        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)

        # Determine the dominant emotion
        emotion = result[0]['dominant_emotion']

        # Draw rectangle around face and label with predicted emotion
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Convert frame to RGB for matplotlib
    rgb_display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the resulting frame using matplotlib
    plt.imshow(rgb_display_frame)
    plt.axis('off')
    plt.draw()
    plt.pause(0.001)
    plt.clf()

    # Check for 'q' key press to exit
    if plt.get_fignums():
        fig.canvas.flush_events()
    else:
        break

# Release the capture
cap.release()
plt.close()