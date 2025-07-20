import face_recognition
import cv2

# Load images and encode faces
image_of_person1 = face_recognition.load_image_file("David Warne.jpg")
image_of_person2 = face_recognition.load_image_file("steve.jpg")

person1_face_encoding = face_recognition.face_encodings(image_of_person1)[0]
person2_face_encoding = face_recognition.face_encodings(image_of_person2)[0]

known_face_encodings = [person1_face_encoding, person2_face_encoding]
known_face_names = ["David Warne", "steve"]

# Load the image in which you want to perform face recognition
unknown_image = face_recognition.load_image_file("Steve-Smith-David-Warner.jpg")

# Find all face locations and face encodings in the unknown image
face_locations = face_recognition.face_locations(unknown_image)
face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

# Create a window to display the image
window_name = "Face Recognition"
cv2.namedWindow(window_name)

# Loop through each face found in the unknown image
for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    # Check if the face matches any known faces
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    name = "Unknown"  # Default to "Unknown" if no match is found

    # If a match is found, use the name of the known person
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]

    # Draw a rectangle around the face and display the name
    cv2.rectangle(unknown_image, (left, top), (right, bottom), (0, 255, 0), 2)
    font = cv2.FONT_HERSHEY_DUPLEX
    font_size = 1.3
    # cv2.putText(unknown_image, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
    text_width, text_height = cv2.getTextSize(name, font, font_size, 1)[0]

    cv2.putText(unknown_image, name, (left + (right - left - text_width) // 2, top - 10),
                font, font_size, (0, 0, 255), 5)

# Display the image with bounding boxes and recognized names
result_img = cv2.cvtColor(unknown_image, cv2.COLOR_RGB2BGR)
cv2.imwrite('result1.jpg', result_img)
# cv2.imshow(window_name, unknown_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
