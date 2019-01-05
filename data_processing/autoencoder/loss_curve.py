#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 15:12:42 2018

@author: jiang
"""

import numpy as np
import matplotlib.pyplot as plt
data=np.load("saved_loss.npy")[0:8000]
x=[i+1 for i in range(len(data))]
plt.figure(figsize=(8,5))
plt.plot(x,data,color='blue',linewidth=0.5,alpha=0.35,label='original data')
moment=0.95
smooth_data=[data[0]]
for i in range(1,len(data)):
    smooth_data.append(smooth_data[i-1]*moment+(1-moment)*data[i])
plt.plot(x,smooth_data,color='black',linewidth=1,label='smooth data')
plt.grid(linestyle='--')
plt.xlabel("Iteration Times",fontsize=14)
plt.ylabel("Loss Value",fontsize=14)
plt.legend()
plt.show()
