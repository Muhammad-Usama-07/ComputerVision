import py_compile
import random
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

import math
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
 
detector = HandDetector(detectionCon=0.8, maxHands=1)
 
 
        
