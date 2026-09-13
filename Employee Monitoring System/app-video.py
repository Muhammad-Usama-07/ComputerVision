import pixellib
from pixellib.tune_bg import alter_bg
import cv2

segment_person = alter_bg()
segment_person.load_pascalvoc_model("mask_rcnn_coco.h5")

# Create a video capture object to read from the camera (change 0 to your video file path if using a file)
cap = cv2.VideoCapture('CCTV  Model Colony Karachi News_1080p.mp4')

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # Perform person segmentation
    result = segment_person.segmentFrame(frame, show_bboxes=True)

    # Retrieve the output image with the person segmentation
    image_output = result[1]

    # Display the output frame with person segmentation
    cv2.imshow("Person Detection", image_output)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the windows
cap.release()
cv2.destroyAllWindows()
