#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 21:22:08 2018

@author: jiang
"""
#
#import cv2
#import numpy as np
#img = cv2.imread('test_img_19.jpg')
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#edges = cv2.Canny(gray,50,150,apertureSize = 3)
#
#cv2.namedWindow('test_img_edge', cv2.WINDOW_NORMAL)
#cv2.imshow("test_img_edge",edges)
#
#lines = cv2.HoughLines(edges,1,np.pi/180,150)
#print("lines"," ","size:",len(lines))
#for line in lines:
#    for rho,theta in line:
#        a = np.cos(theta)
#        b = np.sin(theta)
#        x0 = a*rho
#        y0 = b*rho
#        x1 = int(x0 + 1000*(-b))
#        y1 = int(y0 + 1000*(a))
#        x2 = int(x0 - 1000*(-b))
#        y2 = int(y0 - 1000*(a))
#        print("x1:",x1," y1:",y1," x2:",x2," y2:",y2)
#        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
#cv2.imwrite('houghlines3.jpg',img)
#cv2.namedWindow('test_img', cv2.WINDOW_NORMAL)
#cv2.imshow("test_img",img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


import cv2
import numpy as np
img = cv2.imread('test_img_19.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
cv2.namedWindow('test_img', cv2.WINDOW_NORMAL)
cv2.imshow("test_img",edges)
cv2.waitKey(0)

minLineLength = 100
maxLineGap = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)
cv2.imwrite('houghlines5.jpg',img)
cv2.imshow("test_img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()