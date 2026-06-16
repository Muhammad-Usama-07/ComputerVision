# Eye Blink Detection using OpenCV and Dlib

A real-time eye blink detector that uses facial landmark detection to identify when a person blinks, based on the geometric ratio between the horizontal and vertical span of the eye.

## Overview

This script captures live video from a webcam, detects faces frame-by-frame, locates 68 facial landmarks per face, and calculates the ratio between the horizontal eye-corner distance and the vertical eyelid distance. When the eye closes, the vertical distance shrinks sharply, causing the ratio to spike — this spike is used as the blink signal.

## Features

- Real-time face detection from webcam feed
- Facial landmark detection (68-point model)
- Eye Aspect Ratio (EAR)-style blink detection using horizontal/vertical eye line ratio
- Visual overlays: face bounding box, eye reference lines, and a "blinking" text alert
- Simple, dependency-light implementation (no deep learning model required beyond dlib's landmark predictor)

## How It Works

1. **Face detection** — Each frame is converted to grayscale and passed to dlib's frontal face detector to locate face bounding boxes.
2. **Landmark detection** — For each detected face, dlib's 68-point shape predictor locates key facial features, including six points around each eye.
3. **Eye geometry** — For the left eye, two horizontal corner points (landmarks 36 and 39) and two midpoints of the upper/lower eyelid (landmarks 37, 38 and 41, 40) are used to draw a horizontal and a vertical line across the eye.
4. **Ratio calculation** — The Euclidean distance of the horizontal line is divided by the distance of the vertical line. A wide-open eye produces a low ratio; a closed eye produces a much higher ratio (since the vertical distance approaches zero).
5. **Blink decision** — If the ratio exceeds a threshold (`4` in this implementation), the frame is flagged as a blink and "blinking" is displayed on screen.

## Requirements

- Python 3.7+
- OpenCV (`opencv-python`)
- dlib
- A pretrained dlib facial landmark model: `shape_predictor_68_face_landmarks.dat`
- A working webcam

### Install dependencies

```bash
pip install opencv-python dlib
```

> **Note:** dlib installation on Windows may require CMake and a C++ build toolchain (Visual Studio Build Tools). Pre-built wheels are also available via `pip install dlib-binary` on some platforms if compilation fails.

### Download the landmark model

Download `shape_predictor_68_face_landmarks.dat` from the [dlib model repository](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2), extract it, and place it in your project directory.

## Setup

This script assumes `detector` and `predictor` are already initialized before the main loop, for example:

```python
import dlib
import cv2 as cv
from math import hypot

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
```

Add these lines (along with the necessary imports) above the `midpoint` function if they're not already present in your full script.

## Usage

```bash
python blink_detection.py
```

- A window will open showing your webcam feed.
- A green rectangle will track your face, and green lines will mark the horizontal and vertical span of your left eye.
- When you blink, the word **"blinking"** will appear on screen.
- Press **`q`** to quit the application.

## Code Structure

| Component | Purpose |
|---|---|
| `midpoint(p1, p2)` | Calculates the midpoint between two dlib landmark points |
| `font` | Font style used for on-screen text overlay |
| Main loop | Captures frames, detects faces/landmarks, computes the eye ratio, and renders overlays |

## Known Limitations

- Only the **left eye** (landmarks 36–41) is used for detection; the right eye is not currently checked.
- The threshold value of `4` is a fixed heuristic — it may need tuning depending on lighting, camera distance, and individual eye shape.
- No smoothing or frame-averaging is applied, so detection can be sensitive to single-frame noise or fast head movement.
- Designed for a single face at a time visually, though it will technically loop over all detected faces.
- Performance depends on dlib's HOG-based detector, which is CPU-bound and can be slow on low-power hardware.

## Possible Improvements

- Average the ratio across both eyes for more robust detection.
- Add temporal smoothing (e.g., require the ratio to stay above threshold for N consecutive frames) to reduce false positives.
- Add a blink counter and blink-rate (blinks per minute) display.
- Replace the fixed threshold with a calibration step that adapts to the user's resting eye-aspect ratio.
