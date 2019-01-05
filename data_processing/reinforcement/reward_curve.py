#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 22:28:41 2018

@author: jiang
"""
import numpy as np
import matplotlib.pyplot as plt
reward=np.load("./data/reward_eps.npy")
#x_r=[i for i in range(len(reward))]
x=[i for i in range(len(reward))]
moment=0.95
smooth_reward=[reward[0]]
fig=plt.figure(figsize=(8,5))

for i in range(1,len(reward)):
    smooth_reward.append(smooth_reward[i-1]*moment+(1-moment)*reward[i])
plt.plot(x,reward,color='blue',linewidth=0.5,alpha=0.35,label='original data')
plt.plot(x,smooth_reward,color='black',linewidth=1,label='smooth data')
plt.xlabel("iteration times",fontsize=15)
plt.ylabel("rewards",fontsize=15)
plt.grid(linestyle='--')
plt.legend()
plt.show()