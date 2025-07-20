# import face_recognition
# import cv2

# # Load images and encode faces
# image_of_person1 = face_recognition.load_image_file("usama.jpg")
# image_of_person2 = face_recognition.load_image_file("imran.jpg")

# person1_face_encoding = face_recognition.face_encodings(image_of_person1)[0]
# person2_face_encoding = face_recognition.face_encodings(image_of_person2)[0]

# known_face_encodings = [person1_face_encoding, person2_face_encoding]
# known_face_names = ["usama", "imran"]

# # Open the webcam
# video_capture = cv2.VideoCapture('http://192.168.100.126:8080//video')
# video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# window_name = "Face Recognition"
# cv2.namedWindow(window_name)

# while True:
#     # Capture each frame from the webcam
#     ret, frame = video_capture.read()

#     # Find all face locations and face encodings in the current frame
#     face_locations = face_recognition.face_locations(frame)
#     face_encodings = face_recognition.face_encodings(frame, face_locations)

#     # Loop through each face found in the frame
#     for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#         # Check if the face matches any known faces
#         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

#         name = "Unknown"  # Default to "Unknown" if no match is found

#         # If a match is found, use the name of the known person
#         if True in matches:
#             first_match_index = matches.index(True)
#             name = known_face_names[first_match_index]

#         # Draw a rectangle around the face and display the name
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#         font = cv2.FONT_HERSHEY_DUPLEX
#         cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

#     # Display the frame with bounding boxes and recognized names
#     cv2.imshow(window_name, frame)

#     # Exit the loop if 'q' key is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the webcam and close the OpenCV window
# video_capture.release()
# cv2.destroyAllWindows()


import face_recognition
import cv2
import threading

# Load images and encode faces
image_of_person1 = face_recognition.load_image_file("usama.jpg")
image_of_person2 = face_recognition.load_image_file("imran.jpg")

person1_face_encoding = face_recognition.face_encodings(image_of_person1)[0]
person2_face_encoding = face_recognition.face_encodings(image_of_person2)[0]

known_face_encodings = [person1_face_encoding, person2_face_encoding]
known_face_names = ["usama", "imran"]

# Open the webcam
video_capture = cv2.VideoCapture('http://192.168.100.126:8080//video')
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

window_name = "Face Recognition"
cv2.namedWindow(window_name)

# Function to perform face recognition
def recognize_faces(frame):
    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through each face found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the face matches any known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"  # Default to "Unknown" if no match is found

        # If a match is found, use the name of the known person
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Draw a rectangle around the face and display the name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the frame with bounding boxes and recognized names
    cv2.imshow(window_name, frame)

# Function to continuously capture frames and perform face recognition
def capture_frames():
    while True:
        ret, frame = video_capture.read()

        if ret:
            threading.Thread(target=recognize_faces, args=(frame.copy(),)).start()

            # Exit the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Start the capture_frames thread
capture_thread = threading.Thread(target=capture_frames)
capture_thread.start()

# Wait for the threads to finish
capture_thread.join()

# Release the webcam and close the OpenCV window
video_capture.release()
cv2.destroyAllWindows()
