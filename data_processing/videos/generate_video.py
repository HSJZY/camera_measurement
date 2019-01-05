#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 03:02:34 2018

@author: jiang
"""

import cv2
import numpy as np
from pylab import *

def cut_video(cap,start,end,file_name):
    file_path='./cut_video/'+file_name+'.avi'
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out_video = cv2.VideoWriter(file_path, fourcc, 5.0, (960, 540))
    
    for i in range(end):
        ret,frame=cap.read()
        if ret==False:
            print('video end!!!')
            break
        if i<start:
            continue
        elif i>end:
            break
        else:
            print('i=',i)
            frame=cv2.resize(frame,(960,540))
            out_video.write(frame)
            cv2.imshow("image",frame)
            cv2.waitKey(10)
    out_video.release()
    cv2.destroyAllWindows()
def test_cut_video():
    cap_H=cv2.VideoCapture('./video_test_Line.avi')
    cut_video(cap_H,0,156,'cap_Line_cut') #obstacle(50,360);H(0,200);I(0,180);T(0,500);Line(0,156)


def combine(): 
    cap_line=cv2.VideoCapture('./cut_video/cap_Line_cut.avi')
    cap_H=cv2.VideoCapture('./cut_video/cap_H_cut.avi')
    cap_I=cv2.VideoCapture('./cut_video/cap_I_cut.avi')
    cap_T=cv2.VideoCapture('./cut_video/cap_T_cut.avi')
    cap_obs=cv2.VideoCapture('./cut_video/cap_obs_cut.avi')
    cap=[cap_line,cap_H,cap_I,cap_T,cap_obs]
    cap_name=['video1.png','video2.png','video3.png']
    
    file_path='./combine.avi'
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out_video = cv2.VideoWriter(file_path, fourcc, 22.0, (960, 540))
    
    for i in range(len(cap)):
        cap_i=cap[i]
        if i==0 or i==1 or i==4:
            cur_cap_name=""
            if i==0 or i==1:
                cur_cap_name=cap_name[i]
            else:
                cur_cap_name=cap_name[-1]
            frame=cv2.imread('./'+cur_cap_name)
            for j in range(15):
                out_video.write(frame)

        while(1):
            ret,frame=cap_i.read()
            if ret==False:
                break
            out_video.write(frame)
    out_video.release()
    cv2.destroyAllWindows()
if __name__=="__main__":
#    test_cut_video()
    combine()
