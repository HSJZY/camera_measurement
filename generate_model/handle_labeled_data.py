#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 11:05:20 2018

@author: jiang
"""
import numpy as np

def shuffle_data(data):
    index=[i for i in range(len(data[0]))]
    np.random.shuffle(index)
    print("index:",index)
    res_imgs=[]
    res_labels=[]
    for i in range(len(index)):
        res_imgs.append(data[0][index[i]])
        res_labels.append(data[1][index[i]])
        print("i_label:",data[1][index[i]])
    return [res_imgs,np.array(res_labels)]

labeled_data=np.load("labeled_data_after.npy")
handled_data=[]
handled_labels=[]
imgs_data=labeled_data[0]
labels=labeled_data[1]
for i in range(len(labels)):
    if labels[i]!=0 and  labels[i]!=1 and labels[i]!=2 and labels[i]!=3 and labels[i]!=4 and labels[i]!=5:
        continue
    if len(imgs_data[i])!=784:
        print(imgs_data[i])
        input()
    
    handled_data.append(np.array(imgs_data[i],dtype=float).tolist())
    handled_labels.append(labels[i])
#print("before labels:",handled_labels)
handled_data=[handled_data,handled_labels]
handled_data=shuffle_data(handled_data)
np.save("labeled_data_0_5",handled_data)
np.save("data_0_5",handled_data[0])
np.save("labels_0_5",handled_data[1])
print("labels:",handled_data[1])
print("end generate labeled 1-5")
