#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 21:01:45 2018

@author: jiang
"""
"""
@parameter:
    contours: [[[2423  781]] [[2308  785]] [[2308  899]] [[2421  897]]]
"""
import cv2
import math
import numpy as np
from marker import  Marker
def simple_seprate_contour(markers):
    def calc_distance(point1,point2):
        return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
    def clac_area_triangle(point1,point2,point3):
        a=calc_distance(point1,point2)
        b=calc_distance(point2,point3)
        c=calc_distance(point3,point1)
        p=(a+b+c)/2
        return math.sqrt(p*(p-a)*(p-b)*(p-c))
    def calc_area_square(contour,point):
        area_1=clac_area_triangle(point,contour[0],contour[1])
        area_2=clac_area_triangle(contour[1],point,contour[2])
        area_3=clac_area_triangle(contour[3],contour[2],point)
        area_4=clac_area_triangle(contour[0],contour[3],point)
        return (area_1+area_2+area_3+area_4)
    def point_in_contour(point,contour):
        print("contour:",contour)
#        input()
        contour_center=np.mean(contour,axis=0)
        contour_area=calc_area_square(contour,contour_center)
        point_to_contour_area=calc_area_square(contour,point)
        epsilon=0.1
        if point_to_contour_area>contour_area+epsilon:
            return False
        else:
            return True

    markers_info=[]#tuple包含了四个组成部分:(id,center,contour,area)
    for marker in markers:
        if(marker.center==None):
            continue
        cur_contour=[]
        cur_contour.append(marker.contour[0][0])
        cur_contour.append(marker.contour[1][0])
        cur_contour.append(marker.contour[2][0])
        cur_contour.append(marker.contour[3][0])
        marker_info=(marker.id,marker.center,cur_contour,calc_area_square(cur_contour,marker.center))
        markers_info.append(marker_info)
    sorted(markers_info,key=lambda x:(x[3]),reverse=True)
    marker_list=[]
    for index,marker_info in enumerate(markers_info):
        if index+1<len(markers_info):
            marker_need_remove=False
            for i in range(index+1,len(markers_info)):
                if point_in_contour(marker_info[1],markers_info[i][2]):
                    marker_need_remove=True
                    break
            if marker_need_remove==False:
                marker_list.append(Marker(id=marker_info[0], contours=marker_info[2]))
        else:
            marker_list.append(Marker(id=marker_info[0], contours=marker_info[2]))
    return marker_list

test_marker1=Marker(id=1, contours=[[[2423,781]],[[2308,785]],[[2308,899]],[[2421,897]]])
test_marker2=Marker(id=1, contours=[[[2087,967]],[[2181,1021]],[[2185,1107]],[[2089,1054]]])
test_marker3=Marker(id=1, contours=[[[2086,967]],[[2090,1056]],[[2186,1107]],[[2181,1020]]])
marker_list=[test_marker1,test_marker2,test_marker3]
print(simple_seprate_contour(marker_list))
    
    
    
        
    # countours=[ [[2423  781],[2308  785],[2308  899],[2421  897]],
    #           [[2423  781],[2308  785],[2308  899],[2421  897]] ]
    #centers=[ (2135, 1037),(2135, 1037) ]
    
    
    