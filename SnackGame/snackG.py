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
 
 
class SnakeGameClass:
    def __init__(self,pathFood):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 500  # total allowed Length
        self.previousHead = 0, 0  # previous head point
        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()
        self.gameOver = False
    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)





game = SnakeGameClass("Donut.png")
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    
    
    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)

        cv2.circle(img, pointIndex, 15, (200, 0, 200), cv2.FILLED)
        cv2.imshow("Image", img)
        
        key = cv2.waitKey(1)
        
        if key == ord('r'):
            game.gameOver = False
    else:
        cv2.imshow("Image", img)
        
        key = cv2.waitKey(1)
        
        if key == ord('q'):
            break
        
