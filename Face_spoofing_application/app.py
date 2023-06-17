import base64
import cv2
import face_recognition
from flask import Flask, jsonify, render_template, request
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np

app = Flask(__name__)

json_file = open('./antispoofing_models/model.json','r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load antispoofing model weights 
model.load_weights('./antispoofing_models/model_weights.h5')
print("Model loaded from disk")

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
    try: 
        face_locations = face_recognition.face_locations(image)
        print('face_locations: ', face_locations)
        if face_locations == []:
            print('Face not found----')
            return jsonify({'success': False, 'face_match': 'Face Not Found'})
        # Return the number of faces found
        else:
            print(face_locations)
            for (top, right, bottom, left) in face_locations:
                cropped_face = image[top:bottom, left:right]
                resized_face = cv2.resize(cropped_face,(160,160))
                resized_face = resized_face.astype("float") / 255.0
                resized_face = img_to_array(resized_face)
                resized_face = np.expand_dims(resized_face, axis=0)
                preds = model.predict(resized_face)[0]
                print(preds)
                if preds> 0.5:
                    label = 'spoof'
                    print(label)
                else:
                    label = 'real'
                    print(label)
            cv2.imwrite('cropped_face.png', cv2.cvtColor(cropped_face, cv2.COLOR_RGB2BGR))
            return jsonify({'success': True, 'face_match': label})
    except Exception as e:
        return jsonify({'success': False, 'error': e})

        

if __name__ == '__main__':
    app.run()