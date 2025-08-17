# Using Libraries
import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Displaying image
img = cv2.imread('images/RDJ1.jpg')

# Applying bounding box
face_casecade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converting to gray scale
faces = face_casecade.detectMultiScale(gray,1.2, 6)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

cv2.imshow('img',img)
# Not to close image automatically
cv2.waitKey(0)



