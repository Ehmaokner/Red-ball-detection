# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LIZOQ0_K_iPCnwepknxeAqSV0EslhULM
"""

import cv2 as cv
import imutils


def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


red_lo_1 = (155, 166, 80)
red_hi_1 = (175, 255, 245)


capture = cv.VideoCapture(0) # Set path for recorded video

while True:
    isTrue, frame = capture.read()

    if frame is None:
        break

    frame_resz = rescaleFrame(frame)
    blurred = cv.GaussianBlur(frame_resz, (3, 3), cv.BORDER_CONSTANT)
    col_hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
    #mask_1 = cv.inRange(col_hsv, red_lo_1, red_hi_1)
    mask_2 = cv.inRange(col_hsv, red_lo_2, red_hi_2)
    #mask = cv.addWeighted(mask_2, 1.0, mask_1, 1.0, 0.0)
    mask_2 = cv.erode(mask_2,(11,11), iterations=2)
    mask_2 = cv.dilate(mask_2, (11,11), iterations=2)

    contors = cv.findContours(mask_2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contors = imutils.grab_contours(contors)

    if len(contors) > 0:
        large = max(contors, key = cv.contourArea)
        ((x,y), radius) = cv.minEnclosingCircle(large)
        moms = cv.moments(large)
        flag = 1
        try:
            center = (int(moms['m10']/moms['m00']), int(moms['m01']/moms['m00']))
        except ZeroDivisionError:
            flag = 0

        if radius > 10 and flag:
            cv.circle(frame_resz, (int(x), int(y)), int(radius),(0, 255, 0), 2)


    cv.imshow("Video", frame_resz)

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()