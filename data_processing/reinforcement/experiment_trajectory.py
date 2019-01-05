#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 18:28:52 2018

@author: jiang
"""

import numpy as np
import matplotlib.pyplot as plt

data=open('./experiment/log.txt').read().splitlines()
total_info=[]
marker_1_trajectory=[]
obstacles_info=[]
for index,line_i in enumerate(data):
    i_info=[]
    runtime,pos_info=float(line_i.split(' ')[0]),line_i.split(' ')[1].split('|')[:-1]
#    print("pos_info:",pos_info[0].split(':'))
    marker_1_pos=[float(x) for x in (pos_info[0].split(':')[1][1:-1].split(',')[:-1])]
    marker_1_trajectory.append(marker_1_pos)
    
    if index==10:
        marker_2_pos=[float(x) for x in (pos_info[1].split(':')[1][1:-1].split(',')[:-1])]
        marker_5_pos=[[float(x) for x in str_info[1:-1].split(',')[:-1]] for str_info in pos_info[-1].split(':')[1].split(';')]
        obstacles_info=[marker_2_pos,marker_5_pos[0],marker_5_pos[1]]

obstacles_info=np.array(obstacles_info)
marker_1_trajectory=np.array(marker_1_trajectory)
obstacles_info[:,1]*=-1
marker_1_trajectory[:,1]*=-1

min_x=min(np.min(marker_1_trajectory[:,0]),np.min(obstacles_info[:,0]))

min_y=min(np.min(marker_1_trajectory[:,1]),np.min(obstacles_info[:,1]))
obstacles_info[:,0]+=abs(min_x)
obstacles_info[:,1]+=abs(min_y)
marker_1_trajectory[:,0]+=abs(min_x)
marker_1_trajectory[:,1]+=abs(min_y)

fig_2=plt.figure(figsize=(8,8))

plt.plot(marker_1_trajectory[:,0],marker_1_trajectory[:,1],color='red',linewidth=2,alpha=0.95,label='robot1')
plt.scatter(marker_1_trajectory[0,0],marker_1_trajectory[0,1],c='',edgecolors='black',s=100)
plt.scatter(marker_1_trajectory[-1,0],marker_1_trajectory[-1,1],c='',edgecolors='black',s=100)
plt.text(marker_1_trajectory[0,0],marker_1_trajectory[0,1]-65,'start', fontsize=14)
plt.text(marker_1_trajectory[-1,0]+25,marker_1_trajectory[-1,1],'end', fontsize=14)

for obstacle in obstacles_info:
    plt.scatter(obstacle[0],obstacle[1],c='black',edgecolors='black',s=5000)

plt.xlim((-50,1250))
plt.ylim((-50,1500))
plt.xlabel("X/mm",fontsize=14)
plt.ylabel("Y/mm",fontsize=14)
plt.grid(linestyle='--')
plt.legend()
plt.show()