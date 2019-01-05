#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 09:27:52 2018

@author: jiang
"""

import cv2
import numpy as np

cap=cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) 

cv2.namedWindow("image",cv2.WINDOW_NORMAL)
j=1
file_path="../test_img/test_img_"
while(1):
    ret,frame=cap.read()
    cv2.imshow("image",frame)
    key=cv2.waitKey(100)
    print("key:",key)
    if key==32:
        cv2.imwrite(file_path+str(j)+".jpg",frame)
        j+=1
    elif key==27:
        break;
cap.release()
cv2.destroyAllWindows()
