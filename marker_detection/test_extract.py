#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 10:13:30 2018

@author: jiang
"""
import cv2
import numpy as np
#def extract_info_from_img(img):
#    info_sub_img = []
#    square_sub_img = []
#    x_sub_img = []
#    grayImage=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#    _img_blur = cv2.blur(grayImage, (5, 5)) 
#    _, _img_thre = cv2.threshold(_img_blur, 50, 255, cv2.THRESH_BINARY_INV)
#    cv2.namedWindow('sub', cv2.WINDOW_NORMAL)
#    cv2.imshow("sub",_img_thre)
#    cv2.waitKey(0)
#    _img_cont, cont, hier = cv2.findContours(_img_thre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#    print("cont:",cont)
#    for j in range(len(cont)):
#        rect = cv2.minAreaRect(cont[j])
#        center = list(rect[0])
#        size = list(rect[1])
#        for k in range(len(center)):
#            center[k] = int(center[k])
#            size[k] = int(size[k]*1.4+1)
#        sub_img = cv2.getRectSubPix(_img_thre, tuple(size), tuple(center))
#        sub_resize_img = cv2.resize(sub_img, (28, 28))
#        sub_resize_img = np.resize(sub_resize_img, (28, 28, 1))
#        info_sub_img.append(sub_resize_img)
#        square_sub_img.append((size[0])*(size[1])) # avoid the o length
#        x_sub_img.append(center[0])
#    return info_sub_img, square_sub_img, x_sub_img

def extract_rectbox_from_contour(contour):
    bbox=cv2.minAreaRect(contour)
    pts=cv2.boxPoints(bbox)
    res_pts=[]
    for pt in pts:
        pt=[int(i) for i in pt]
        res_pts.append([pt])
    return np.array(res_pts)
#    print("point",point,"edge_length:",edge_length,"rotate_angle:",rotate_angle)
    

_img=cv2.imread("test_img.png",0)

# Otsu's thresholding
ret2,_img = cv2.threshold(_img,200,255,cv2.THRESH_BINARY)
kernel=np.ones((5,5),np.uint8)
_img = cv2.morphologyEx(_img, cv2.MORPH_CLOSE, kernel)
#    gray = cv2.equalizeHist(gray)
edge=cv2.Canny(_img, 20, 200)


cv2.imshow("sub",edge)
cv2.waitKey(0)
cv2.destroyAllWindows()

contours, hierarchy = cv2.findContours(edge.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
for contour in contours:
    pts=extract_rectbox_from_contour(contour)
    print(pts)
    x1=pts[0][0][0]
    y1=pts[0][0][1]
    x2=pts[1][0][0]
    y2=pts[1][0][1]
    x3=pts[2][0][0]
    y3=pts[2][0][1]
    x4=pts[3][0][0]
    y4=pts[3][0][1]

    cv2.line(_img,(x1,y1),(x2,y2),255,2)
    cv2.line(_img,(x3,y3),(x2,y2),255,2)
    cv2.line(_img,(x3,y3),(x4,y4),255,2)
    cv2.line(_img,(x1,y1),(x4,y4),255,2)
#    cv2.line(_img,(pts[0][1][0],pts[0]),(pts[0][2]),255,2)
#    cv2.line(_img,(pts[0][2]),(pts[0][3]),255,2)
#    cv2.line(_img,(pts[0][3]),(pts[0][0]),255,2)
cv2.imshow("after:",_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
#    for pt in pts:
#        print(pt)
#        cv2.line(_img,tuple(pt),tuple(_img),255,2)