#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 19:16:14 2018

@author: jiang
"""

import cv2

cap=cv2.VideoCapture('collision_avoidance.mp4')
out=cv2.VideoWriter('collision_avoidance.avi',cv2.VideoWriter_fourcc('M','J','P','G'),10,(398,398))
i=0
while(cap.isOpened()):
    ret,frame=cap.read()
#    print(frame.shape)
    if ret==True:
        i+=1
        cv2.imshow('frame',frame)
        if cv2.waitKey(25) & 0xFF==ord('q'):
            break
#        print('i:',i)
        if i>204:
            out.write(frame)
        
    else:
        break
cap.release()
out.release()
cv2.destroyAllWindows()
