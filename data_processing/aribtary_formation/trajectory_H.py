#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 11:11:56 2018

@author: jiang
"""


import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist
import math

formation_H=[[0,0],[800,0],[800,-800],[0,-800]]
formation_I=[[0,400],[0,0],[0,-400],[0,-800]]
formation_T=[[-400,0],[0,0],[0,800],[400,0]]

permutation_H=[3,1,2,0]

permutation=permutation_H

data=open('./H_2/log.txt').read().splitlines()
formation=np.array(formation_H)

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
start_pt=1
fig_1=plt.figure(figsize=(8,8))
for i in range(4):
    x=marker_all_pos[i][start_pt:,0]
    y=marker_all_pos[i][start_pt:,1]
    plt.plot(x,y,color=color_defined[i],linewidth=2,alpha=0.65,label='robot'+str(i+1))
    plt.scatter(marker_all_pos[i][start_pt,0],marker_all_pos[i][start_pt,1],c='',edgecolors='black',s=100)
    plt.text(marker_all_pos[i][start_pt,0]+25,marker_all_pos[i][start_pt,1],'start', fontsize=15)
    plt.scatter(marker_all_pos[i][-1,0],marker_all_pos[i][-1,1],c='',edgecolors='black',s=100)
    plt.text(marker_all_pos[i][-1,0],marker_all_pos[i][-1,1]+25,'end', fontsize=15)
plt.xlabel("X/mm",fontsize=14)
plt.ylabel("Y/mm",fontsize=14)
plt.grid(linestyle='--')
plt.legend()
plt.show()

fig_2=plt.figure(figsize=(8,4))
print("shape",marker_all_pos.shape)

for i in range(start_pt,len(marker_all_pos[0])):
    center_x=np.mean(marker_all_pos[:,i,0])
    center_y=np.mean(marker_all_pos[:,i,1])
    marker_all_pos[:,i,0]-=center_x
    marker_all_pos[:,i,1]-=center_y
    
formation_center=[np.mean(formation[:,0]),np.mean(formation[:,1])]
formation=np.array(formation)-formation_center


errors=[]
start_time=total_info[start_pt][0]
runtime=[x[0]-start_time for x in total_info[start_pt:]]

for i in range(4):
    marker_i=marker_all_pos[permutation[i]]
    marker_i_error=np.sqrt(np.sum(np.square(marker_i[start_pt:]-formation[i]),1))
    plt.plot(runtime,marker_i_error,color=color_defined[permutation[i]],linewidth=2,alpha=0.65,label='Error Robot'+str(i+1))
plt.xlabel("time/s",fontsize=15)
plt.ylabel("Distance Error/mm",fontsize=14)
plt.grid(linestyle='--')
plt.legend()
plt.show()
