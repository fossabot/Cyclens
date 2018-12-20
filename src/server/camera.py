# coding: utf-8

import cv2 as cv2
import numpy as np
import os

FILE_OUTPUT = 'output.avi'

if os.path.isfile(FILE_OUTPUT):
    os.remove(FILE_OUTPUT)


cap = cv2.VideoCapture(0)

currentFrame = 0

width = cap.set(cv2.CAP_PROP_FRAME_WIDTH, 630)
height = cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


fourcc = cv2.VideoWriter_fourcc(*'X264')
out = cv2.VideoWriter(FILE_OUTPUT, fourcc, 20.0, (int(width), int(height)))

kernel = np.ones((7, 7), np.uint8)


while(cap.isOpened()):
    ret, frame = cap.read()

    if ret == True:
        # Handles the mirroring of the current frame
        frame = cv2.flip(frame, 1)

        blur = cv2.blur(frame, (10, 10))
        blur2 = cv2.GaussianBlur(frame, (23, 23), 0)

        # Saves for video
        out.write(frame)

        # Display the resulting frame
        cv2.imshow('Pure', frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        fix = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)

        #fix2 = cv2.fastNlMeansDenoisingColored(frame, None, 5, 5, 3, 13)
        fix3 = cv2.equalizeHist(cv2.cvtColor(cv2.absdiff(blur2, blur), cv2.COLOR_BGR2GRAY))

        hist = cv2.equalizeHist(gray)
        edges = cv2.Canny(frame, 100, 200)

        vis = np.concatenate((edges, fix3), axis=1)

        merged = cv2.addWeighted(fix3, 0.7, edges, 1.3, 0)

        #cv2.imshow('HVS', hsv)
        cv2.imshow('HISTOGRAM EQUAL', hist)
        cv2.imshow('A', merged)


    else:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        out.release()
        break

    currentFrame += 1

cv2.destroyAllWindows()