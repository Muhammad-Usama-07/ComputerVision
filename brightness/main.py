# Python
import cv2 
import mediapipe as mp
from math import hypot
import screen_brightness_control as sbc
import numpy as np 

cap = cv2.VideoCapture(0)
success,img = cap.read()

cv2.imshow('Image',img)


