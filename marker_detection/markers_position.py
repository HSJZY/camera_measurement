#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 11:08:36 2018

@author: jiang
"""
from marker import Marker

class MarkersPosition(object):
    _marker1_pos=None
    _marker2_pos=None
    _marker3_pos=None
    _marker4_pos=None
    _marker5_pos=None
    """
    @parameter position: [[],[],...]
    """
    @property
    def markers_pos(self):
        marker_pos=[self._marker1_pos,self._marker2_pos,self._marker3_pos,self._marker4_pos,self._marker5_pos]
        return marker_pos
    @markers_pos.setter
    def markers_pos(self,markers):
        marker5=[]
        print("hello",markers)
        for marker in markers:
            marker_id=marker.id
            if marker_id==1:
                MarkersPosition._marker1_pos=marker.position
            elif marker_id==2:
                MarkersPosition._marker2_pos=marker.position
            elif marker_id==3:
                MarkersPosition._marker3_pos=marker.position
            elif marker_id==4:
                MarkersPosition._marker4_pos=marker.position
            elif marker_id==5:
                marker5.append(marker.position)
            else:
                continue
        MarkersPosition.marker5_pos=marker5
def test():
    f1=MarkersPosition()
    f2=MarkersPosition()
    marker1=Marker(1,position_3D=(1,2,3))
    marker2=Marker(2,position_3D=(4,5,6))
    markers=[marker1,marker2]
    f1.markers_pos=markers
    print(f2._marker1_pos)
    print(f2._marker2_pos)
if __name__=="__main__":
    test()
        