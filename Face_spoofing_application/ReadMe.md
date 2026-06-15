# Face Spoofing Detection (Anti-Spoofing) Web App

A Flask web application that captures a snapshot from the user's webcam, detects faces using the `face_recognition` library, and classifies each detected face as **real** or **spoof** using a pre-trained Keras CNN model. This kind of liveness check is commonly used as a guard step before facial authentication to block presentation attacks (printed photos, screen replays, masks, etc.).

## Features

- Capture a webcam image directly from the browser and send it to the backend as a base64 data URL
- Face detection via `face_recognition` (dlib-based)
- Automatic cropping, resizing (160x160), and normalization of detected faces
- Binary anti-spoofing classification using a pre-trained Keras model
- JSON API response indicating whether the face is real or spoofed

## Tech Stack

- **Python / Flask** – web server and API
- **TensorFlow / Keras** – loads model architecture (`model.json`) and weights (`model_weights.h5`)
- **OpenCV (`cv2`)** – image resizing and color conversion
- **face_recognition (dlib)** – face detection
- **NumPy** – array manipulation

## Project Structure

```
project/
├── app.py
├── antispoofing_models/
│   ├── model.json
│   └── model_weights.h5
├── templates/
│   └── index.html
├── snapshot.png        # generated at runtime (latest webcam capture)
├── cropped_face.png     # generated at runtime (latest cropped face)
└── README.md
```

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd project
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install flask opencv-python face_recognition tensorflow numpy
   ```

   > **Note:** `face_recognition` depends on `dlib`, which needs CMake and a C++ build toolchain. On Windows, installing pre-built wheels (or using `conda install -c conda-forge dlib`) is often easier than building from source.

4. **Add the model files**
   Place your trained `model.json` and `model_weights.h5` inside `antispoofing_models/`.

5. **Run the app**
   ```bash
   python app.py
   ```

6. Open your browser at `http://127.0.0.1:5000`

## Usage

1. Open the web app and grant camera permission.
2. Capture a frame from your webcam through the page UI.
3. The frame is sent to the backend, where the app:
   - Detects any faces in the image
   - Crops and resizes each face to 160x160
   - Runs the anti-spoofing model on the cropped face
4. The result (`real` or `spoof`, or "Face Not Found") is returned to the page.

## How It Works (Backend Flow)

1. **`POST /save-image`** receives `{ "dataURL": "data:image/png;base64,..." }`
2. The base64 payload is decoded and saved as `snapshot.png`
3. `face_recognition.face_locations()` finds all face bounding boxes in the image
4. For each detected face:
   - Crop the region from the image
   - Resize to `160x160`
   - Normalize pixel values to `[0, 1]`
   - Expand dimensions to match the model's expected input shape
   - Run `model.predict()` to get a probability score
   - If `score > 0.5` → label = `"spoof"`, otherwise `"real"`
5. The cropped face is saved as `cropped_face.png`
6. The result is returned as JSON

## API Reference

### `POST /save-image`

**Request body (JSON):**
```json
{
  "dataURL": "data:image/png;base64,<encoded-image>"
}
```

**Responses:**

| Scenario | Response |
|---|---|
| Face detected | `{"success": true, "face_match": "real"}` or `{"success": true, "face_match": "spoof"}` |
| No face detected | `{"success": false, "face_match": "Face Not Found"}` |
| Error during processing | `{"success": false, "error": "<error message>"}` |

## Model Details

- The model architecture is stored separately (`model.json`) from its weights (`model_weights.h5`) and reassembled at startup with `model_from_json` + `load_weights`.
- **Input:** 160x160x3 RGB face crop, scaled to `[0, 1]`
- **Output:** A single sigmoid probability; values above `0.5` are classified as `spoof`

## Known Issues / Things to Review

A few details in the current implementation are worth keeping in mind, especially before moving to production:

- **Multiple faces:** if more than one face is found, `label` and `cropped_face` are overwritten on each loop iteration, so only the *last* face's result is returned and saved. Consider returning a list of results, one per face.
- **Error serialization:** the exception handler returns `jsonify({'success': False, 'error': e})`, but `e` (an `Exception` object) isn't directly JSON-serializable in all cases — convert it with `str(e)`.
- **Disk writes on every request:** `snapshot.png` and `cropped_face.png` are written to disk on each call, which can become a storage/privacy concern in production. Consider processing images in memory or using temporary files.
- **`debug=True`:** fine for development, but should be disabled (and a production WSGI server used) for any real deployment.
- **No input validation:** the `dataURL` format/size isn't validated before decoding.

## Possible Future Improvements

- Return per-face results when multiple faces are detected
- Add confidence thresholds/calibration and configurable decision thresholds
- Process images in memory instead of writing to disk
- Add request validation and rate limiting
- Containerize with Docker for easier deployment
- Add unit tests for the detection and classification pipeline
