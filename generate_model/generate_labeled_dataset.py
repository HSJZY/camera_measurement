#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 20:12:08 2018

@author: jiang
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy import rot90


def show_binary(test_img):
    fig = plt.figure()    
    plt.imshow(test_img,cmap = 'binary')#黑白显示    
    plt.show() 

def rotate_90_img(img,row_size):
    img_matrix=np.array(img).reshape(row_size,row_size).tolist()
    rotated_img=rot90(img_matrix).reshape(-1,row_size*row_size)[0]
    return rotated_img

def generate_labeled_dataset(path):
    if not os.path.exists(path):
        return -1
    imgs_path=[]
    labels=[]
    imgs=[]
    imgs_labels=[]
    for root,dirs,names in os.walk(path):
        for filename in names:
            try:
                com_path=os.path.join(root,filename)
                labels.append(int(filename.split("_")[-1].split(".")[0]))
                imgs_path.append(com_path)
            except:
                continue
    for index,img_name in enumerate(imgs_path):
        img=cv2.imread(img_name,0)
#        img[img>=0.2]=1
#        img[img<0.2]=0
#        show_binary(img)
        for i in range(28):
            for j in range(28):
                if i==0 or i==27 or j==0 or j==27 or i==1 or i==26 or j==1 or j==26:
                    img[i][j]=0
#        show_binary(img)
#        print("label",labels[index])
#        cv2.waitKey(0)
        img_binary=np.array(img.reshape((-1,28*28)))
#        if labels[index]!=0:
        rot_img=img_binary
        for i in range(4):
            rot_img=rotate_90_img(rot_img,28)
#                print("train_images[i]",rot_img)
            imgs.append(rot_img.tolist())
            imgs_labels.append(labels[index])
#        else:
##            print("img_binary.tolist()",img_binary.tolist()[0])
#            imgs.append(img_binary.tolist()[0])
#            imgs_labels.append(labels[index])
    dataset=(imgs,imgs_labels)
    return dataset
if __name__=="__main__":
    path="/home/jiang/Desktop/求毕业/python-ar-markers/digit_detection/camera_measurement/img_dataset/new_img_dataset/"
    dataset=generate_labeled_dataset(path)
    np.save("labeled_data_after",dataset)
    print(len(dataset),len(dataset[0][0]),len(dataset[1]))
    
    