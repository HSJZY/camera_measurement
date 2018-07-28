#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 19:30:47 2018

@author: jiang
"""

import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt


IMSIZE=28

def show_binary(test_img):
    fig = plt.figure()    
    plt.imshow(test_img,cmap = 'binary')#黑白显示    
    plt.show() 
def gen_dataset(file_name,images,labels):
    frame=cv2.imread(file_name,0)
    height,width=frame.shape
    print("height,width:",height,width)
    cv2.imshow("frame",frame)
    cv2.waitKey(0)

    for i in range(800):
        rand_size=max(10,int(np.random.rand()*min(height,width)*0.25))
        start_pos=[np.random.randint(0,height-1-rand_size),np.random.randint(0,width-1-rand_size)]
        roi_img=frame[start_pos[0]:start_pos[0]+rand_size-1,start_pos[1]:start_pos[1]+rand_size-1]
        roi_img_resized=cv2.resize(roi_img,(IMSIZE,IMSIZE),interpolation=cv2.INTER_CUBIC)/255.0
        roi_img_binary=np.array(roi_img_resized.reshape((IMSIZE*IMSIZE,-1)))
        roi_img_binary[roi_img_binary<0.45]=int(0)
        roi_img_binary[roi_img_binary>0.45]=int(1)
        images.append(roi_img_binary.tolist())
        labels.append(0)

if __name__=="__main__":
    images=[]
    labels=[]
    
    dataset=np.load("negative_samples.npy")
    images=np.array(dataset[0])
    labels=np.array(dataset[1])
    
    x=1192
    print("image[x]:",images[x])
    show_binary(images[x].reshape((28,28)))
    print(images[x].reshape((28,28)))
#    
#    
#    for i in range(7):
#        file_name="./image/timg_"+str(i)+".jpeg"
#        gen_dataset(file_name,images,labels)
#    dataset=[images,labels]
#    
#    np.save("negative_samples",dataset)
##    
    
    
    
    
    
    
    
        #cv2.imshow("frame",roi_img_resized)
        #cv2.imshow("roi_img_resized_reversed",roi_img_binary)
        #cv2.waitKey(0)
    #roi_img = frame[300:400, 50:300]
#    
#    cv2.imshow("frame",roi_img)
#    cv2.waitKey(0)

