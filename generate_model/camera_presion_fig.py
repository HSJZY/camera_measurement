#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 19:34:36 2018

@author: jiang
"""
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

x_camera=[488.1,424.84,366.1,301.82,233.17,170.46,106.8,44.7,-19.8,-83.25,-143.5,-221.8,-272,-332.9,-403,-469.32,-528.4,-591,-665.3,-730.75]
y_camera=[407,338.47,281.13,219.18,156.43,90.66,34.04,-30.32,-93.71,-151.6,-215.94,-282.17,-345.3,-408.3,-474.8]

data=x_camera
data.reverse()
data=np.array(data)
data-=data[0]

data_interval=[data[i+1]-data[i] for i in range(len(data)-1)]
data-=data[0]
data_real=np.array([60 for i in range(len(data)-1)])
data_real_improve=[60*i for i in range(len(data))]

data_error=data_interval-data_real


fig_1=plt.figure(figsize=(8,8))

X_x=[i for i in range(len(data))]
plt.plot(X_x,data,color='blue',linewidth=2,label='X轴测量数据')
plt.scatter(X_x,data,c='blue',edgecolors='black',s=100)
plt.plot(X_x,data_real_improve,color='green',linewidth=2,label='X轴groundtruth')
plt.scatter(X_x,data_real_improve,c='green',edgecolors='black',s=100)
plt.xlabel('times')
plt.ylabel('measure distance')
plt.legend()
plt.grid(linestyle='--')
plt.show()

fig_e1=plt.figure(figsize=(8,4))
X_x=[i for i in range(len(data_error))]
plt.plot(X_x,data_error,color='black',linewidth=2,label='X轴')
plt.scatter(X_x,data_error,c='black',edgecolors='black',s=100)
plt.ylim((-20,30))
plt.legend()

plt.grid(linestyle='--')
plt.show()
