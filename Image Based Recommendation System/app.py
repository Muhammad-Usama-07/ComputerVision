from flask import Flask, request, jsonify, send_file
from ultralytics import YOLOWorld
from PIL import Image
import io
import cv2
import math
import numpy as np

app = Flask(__name__)

# Load the pretrained YOLOv8s-worldv2 model
model = YOLOWorld("yolov8x-worldv2.pt")
classNames = ["hat", "collar belt", "leash", "harness", "collar", "bag", "shirt", "bed", "Scout", "scarf"]
model.set_classes(classNames)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    image_file = request.files['image']
    image = Image.open(io.BytesIO(image_file.read()))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Perform prediction
    results = model(img, stream=True)
    predictions = []
    # Process results and draw bounding boxes
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            conf = math.ceil((box.conf[0] * 100)) / 100
            print('confidence --- ', conf)
            
            cls = box.cls[0]
            name = classNames[int(cls)]
            # predictions.append({name: conf})
            predictions.append(name)

            print('name --- ', name)
            # Draw bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f'{name} {conf}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    predictions = list(set(predictions))
    print('prediction --- ', predictions)
    
    # Save the processed image
    response = {
        "prediction_result": predictions
    }

    return jsonify(response)

@app.route('/image/<filename>', methods=['GET'])
def get_image(filename):
    return send_file(filename, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2525)
