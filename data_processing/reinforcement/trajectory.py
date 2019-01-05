#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 15:41:36 2018

@author: jiang
"""

import numpy as np
import matplotlib.pyplot as plt
agents,obstacles=np.load('./data/config.npy')
trajectory=np.load('./data/agent_trajectory.npy')
fig_2=plt.figure(figsize=(8,8))

color_defined=['blue','green','orange','red']
for agent in agents:
    px,py,pgx,pgy=agent
    
    plt.scatter(px,py,c='blue',edgecolors='black',s=100)
    plt.text(px+5,py,'start', fontsize=14)
    plt.scatter(pgx,pgy,c='blue',edgecolors='red',s=100)
    plt.text(pgx-25,pgy,'end', fontsize=14)

for obstacle in obstacles:
    px,py,radius=obstacle
    print("radius:",radius)
    plt.scatter(px,py,c='black',edgecolors='black',s=2*radius*100)

for index,path in enumerate(trajectory):
    x=[path[i][0] for i in range(len(path))]
    y=[path[i][1] for i in range(len(path))]
    plt.plot(x,y,color=color_defined[index],linewidth=2,alpha=0.65,label='robot'+str(index+1))
plt.xlabel("X/mm",fontsize=15)
plt.ylabel("Y/mm",fontsize=15)
plt.grid(linestyle='--')
plt.legend()
plt.show()
    
