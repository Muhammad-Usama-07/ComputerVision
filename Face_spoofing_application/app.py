import base64
import cv2
import face_recognition
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save-image', methods=['POST'])
def save_image():
    data_url = request.json['dataURL']
    image_data = base64.b64decode(data_url.split(',')[1])
    with open('snapshot.png', 'wb') as f:
        f.write(image_data)

    # Load the saved image using face_recognition
    image = face_recognition.load_image_file('snapshot.png')
    # Find all the faces in the image
    face_locations = face_recognition.face_locations(image)
    # Return the number of faces found
    print(face_locations)
    for (top, right, bottom, left) in face_locations:
        cropped_face = image[top:bottom, left:right]
    cv2.imwrite('cropped_face.png', cv2.cvtColor(cropped_face, cv2.COLOR_RGB2BGR))
    return jsonify({'success': True, 'faces': len(face_locations)})

if __name__ == '__main__':
    app.run()