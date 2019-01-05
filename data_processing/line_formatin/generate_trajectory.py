#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 15:54:34 2018

@author: jiang
"""

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist
import math

data=open('./line_2/log.txt').read().splitlines()
total_info=[]
trajectory_info=[]
for line_i in data:
    i_info=[]
    runtime,pos_info=float(line_i.split(' ')[0]),line_i.split(' ')[1].split('|')[:-2]
    i_info.append(runtime)
    markers_pos=[[float(x_i) for x_i in x.split(':')[1][1:-1].split(',')[:-1]] for x in pos_info]
    #print(markers_pos)
    for i in range(len(markers_pos)):
        markers_pos[i][1]*=(-1)
    i_info.append(markers_pos)
    total_info.append(i_info)
    trajectory_info.append(markers_pos)
trajectory_info=np.array(trajectory_info)
marker_all_pos=[]
for j in range(4):
    marker_j_pos=np.array([trajectory_info[i][j] for i in range(len(trajectory_info))])
    marker_all_pos.append(marker_j_pos)
marker_all_pos=np.array(marker_all_pos)
#print("marker_all_pos:",np.array(marker_all_pos).shape)
min_x=np.min(marker_all_pos[:,:,0])
min_y=np.min(marker_all_pos[:,:,1])
marker_all_pos[:,:,0]+=abs(min_x)
marker_all_pos[:,:,1]+=abs(min_y)

color_defined=['blue','green','orange','red']
start_pt=13
fig_1=plt.figure(figsize=(8,5))
for i in range(4):
    x=marker_all_pos[i][start_pt:,0]
    y=marker_all_pos[i][start_pt:,1]
    plt.plot(x,y,color=color_defined[i],linewidth=2,alpha=0.65,label='robot'+str(i+1))
    plt.scatter(marker_all_pos[i][start_pt,0],marker_all_pos[i][start_pt,1],c='',edgecolors='black',s=100)
    plt.text(marker_all_pos[i][start_pt,0]+25,marker_all_pos[i][start_pt,1],'start', fontsize=15)
    plt.scatter(marker_all_pos[i][-1,0],marker_all_pos[i][-1,1],c='',edgecolors='black',s=100)
    plt.text(marker_all_pos[i][-1,0],marker_all_pos[i][-1,1]-65,'end', fontsize=15)
plt.xlabel("X/mm",fontsize=15)
plt.ylabel("Y/mm",fontsize=15)
plt.grid(linestyle='--')
plt.legend()
plt.show()

fig_2=plt.figure(figsize=(8,5))
permutation=[0,3,1,2]
start_time=total_info[start_pt][0]
runtime=[x[0]-start_time for x in total_info[start_pt:]]
angle_markers=[]
for i in range(1,4):
    marker_pre=marker_all_pos[permutation[i-1]][start_pt:]
    marker_cur=marker_all_pos[permutation[i]][start_pt:]
    sub_two_markers= marker_cur-marker_pre
    dist_two_markers=np.array([math.sqrt(x**2+y**2) for x,y in sub_two_markers])-600
    angle_two_markers=np.array([math.atan2(-y,x) for x,y in sub_two_markers])*180/math.pi
    angle_markers.append(angle_two_markers)
    plt.plot(runtime,dist_two_markers,color=color_defined[i],label='DistanceError'+str(permutation[i])+'-'+str(permutation[i-1]))
plt.grid(linestyle='--')
plt.xlabel("time/s",fontsize=15)
plt.ylabel("Distance Error/mm",fontsize=15)
plt.legend()
plt.show()

fig_3=plt.figure(figsize=(8,5))
for i in range(3):
    plt.plot(runtime,angle_markers[i],color=color_defined[i],label='AngleError'+str(permutation[i+1])+'-'+str(permutation[i]))
plt.grid(linestyle='--')
plt.xlabel("time/s",fontsize=15)
plt.ylabel("Angel Error/mm",fontsize=15)
plt.legend()
plt.show()