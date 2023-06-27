import cv2
import numpy as np
from flask import Flask, render_template, Response

# Initialize Flask application
app = Flask(__name__)

# Initialize OpenCV face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Capture video stream from webcam
video_capture = cv2.VideoCapture(0)

def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw bounding boxes around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


    return frame

def generate_frames():
    while True:
        # Read frames from the video stream
        ret, frame = video_capture.read()

        # Process frames (detect faces and draw bounding boxes)
        processed_frame = detect_faces(frame)

        # Convert processed frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()

        # Yield the frame bytes as an HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML page

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
