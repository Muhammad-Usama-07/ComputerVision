"""
Face Anti-Spoofing Desktop App
--------------------------------
Real-time webcam face liveness detection (real vs spoof) using:
- OpenCV for webcam capture and image processing
- face_recognition (dlib) for face detection
- A pre-trained Keras CNN for real/spoof classification
- Tkinter for the desktop GUI

Run:
    python desktop_app.py

Requirements:
    pip install opencv-python face_recognition tensorflow numpy pillow
"""

import threading
import time

import cv2
import face_recognition
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.image import img_to_array

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
MODEL_JSON_PATH = "./antispoofing_models/model.json"
MODEL_WEIGHTS_PATH = "./antispoofing_models/model_weights.h5"
DETECT_EVERY_N_FRAMES = 5          # run detection/classification every Nth frame
DOWNSCALE_FOR_DETECTION = 0.5      # shrink frame before face detection for speed
SPOOF_THRESHOLD = 0.5
CAMERA_INDEX = 0


class AntiSpoofingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Anti-Spoofing Detector")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # --- Load model ---
        self.status_var = tk.StringVar(value="Loading model...")
        self._build_ui()
        self.model = self._load_model()
        self.status_var.set("Model loaded. Starting camera...")

        # --- Shared state between capture thread and UI thread ---
        self._lock = threading.Lock()
        self._latest_display_frame = None   # annotated frame (BGR) ready to show
        self._latest_label = "No face detected"
        self._running = True

        # --- Camera + worker thread ---
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        if not self.cap.isOpened():
            self.status_var.set("Error: could not open webcam.")
        else:
            self.worker_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.worker_thread.start()

        # Start UI refresh loop
        self._update_ui()

    # ------------------------------------------------------------------
    # Model loading
    # ------------------------------------------------------------------
    def _load_model(self):
        with open(MODEL_JSON_PATH, "r") as json_file:
            loaded_model_json = json_file.read()
        model = model_from_json(loaded_model_json)
        model.load_weights(MODEL_WEIGHTS_PATH)
        print("Model loaded from disk")
        return model

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_ui(self):
        self.video_label = tk.Label(self.root)
        self.video_label.pack(padx=10, pady=10)

        self.result_label = tk.Label(
            self.root, textvariable=self.status_var, font=("Segoe UI", 14, "bold")
        )
        self.result_label.pack(pady=(0, 10))

    # ------------------------------------------------------------------
    # Background thread: capture + detect + classify
    # ------------------------------------------------------------------
    def _capture_loop(self):
        frame_count = 0
        last_boxes_labels = []  # list of (top, right, bottom, left, label)

        while self._running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.05)
                continue

            frame_count += 1

            # Run detection/classification every N frames for performance
            if frame_count % DETECT_EVERY_N_FRAMES == 0:
                last_boxes_labels = self._detect_and_classify(frame)

            annotated = self._draw_annotations(frame, last_boxes_labels)
            overall_label = (
                ", ".join(lbl for *_, lbl in last_boxes_labels)
                if last_boxes_labels
                else "No face detected"
            )

            with self._lock:
                self._latest_display_frame = annotated
                self._latest_label = overall_label

        self.cap.release()

    def _detect_and_classify(self, frame):
        """Detect faces in `frame` and classify each as real/spoof.
        Returns list of (top, right, bottom, left, label) in original frame coords.
        """
        small_frame = cv2.resize(frame, (0, 0), fx=DOWNSCALE_FOR_DETECTION, fy=DOWNSCALE_FOR_DETECTION)
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small)
        results = []

        scale = 1 / DOWNSCALE_FOR_DETECTION
        for (top, right, bottom, left) in face_locations:
            # Scale coordinates back up to original frame size
            top, right, bottom, left = (
                int(top * scale),
                int(right * scale),
                int(bottom * scale),
                int(left * scale),
            )

            cropped_face = frame[max(top, 0):bottom, max(left, 0):right]
            if cropped_face.size == 0:
                continue

            try:
                resized_face = cv2.resize(cropped_face, (160, 160))
            except cv2.error:
                continue

            resized_face = cv2.cvtColor(resized_face, cv2.COLOR_BGR2RGB)
            resized_face = resized_face.astype("float") / 255.0
            resized_face = img_to_array(resized_face)
            resized_face = np.expand_dims(resized_face, axis=0)

            preds = self.model.predict(resized_face, verbose=0)[0]
            label = "spoof" if preds > SPOOF_THRESHOLD else "real"

            results.append((top, right, bottom, left, label))

        return results

    def _draw_annotations(self, frame, boxes_labels):
        annotated = frame.copy()
        for (top, right, bottom, left, label) in boxes_labels:
            color = (0, 0, 255) if label == "spoof" else (0, 200, 0)  # BGR
            cv2.rectangle(annotated, (left, top), (right, bottom), color, 2)
            cv2.putText(
                annotated,
                label.upper(),
                (left, max(top - 10, 0)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2,
            )
        return annotated

    # ------------------------------------------------------------------
    # UI thread: refresh video feed + status label
    # ------------------------------------------------------------------
    def _update_ui(self):
        with self._lock:
            frame = self._latest_display_frame
            label_text = self._latest_label

        if frame is not None:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_frame)
            photo = ImageTk.PhotoImage(image=image)
            self.video_label.configure(image=photo)
            self.video_label.image = photo  # keep reference to avoid garbage collection
            self.status_var.set(label_text)

        if self._running:
            self.root.after(15, self._update_ui)

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------
    def on_close(self):
        self._running = False
        time.sleep(0.2)  # give capture thread a moment to exit
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AntiSpoofingApp(root)
    root.mainloop()