import pixellib
from pixellib.tune_bg import alter_bg
import cv2
segment_person = alter_bg()
segment_person.load_pascalvoc_model("mask_rcnn_coco.h5")
image = cv2.imread("image-asset.jpeg")
start_time = time.time()
result = segment_person.segmentImage(image)
end_time = time.time()
image_output = result[1]
cv2.imshow("Person Detection", image_output)
cv2.waitKey(0)
cv2.destroyAllWindows()

execution_time = end_time - start_time
print("Execution time:", execution_time, "seconds")
