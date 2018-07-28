#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 11:08:36 2018

@author: jiang
"""
try:
    from marker_detection.marker import Marker
except:
    from marker import Marker

class MarkersPosition(object):
    _marker1_pos=None
    _marker2_pos=None
    _marker3_pos=None
    _marker4_pos=None
    _marker5_pos=None
    _markers_pos=None
    _hung_index=None
    def __init__(self):
        pass
#        MarkersPosition._markers_pos=[MarkersPosition._marker1_pos,MarkersPosition._marker2_pos,MarkersPosition._marker3_pos,MarkersPosition._marker4_pos,MarkersPosition._marker5_pos]
    
    def __repr__(self):
        return '<Marker position={}>'.format(self.markers_pos_string)
    """
    @parameter position: [[],[],...]
    """
    @property
    def hungarian_index(self):
        return self._hung_index
    @hungarian_index.setter
    def hungarian_index(self,index):
        MarkersPosition._hung_index=index
    @property
    def markers_pos(self):
        return self._markers_pos
    @markers_pos.setter
    def markers_pos(self,markers):
        marker5=[]
        marker5_changed=False
        for marker in markers:
            marker_id=marker.id
            
            if marker.position==None:
                continue
            
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
                marker5_changed=True
            else:
                continue
        if marker5_changed:
            MarkersPosition._marker5_pos=marker5
        MarkersPosition._markers_pos=[self._marker1_pos,self._marker2_pos,self._marker3_pos,self._marker4_pos,self._marker5_pos]
    def get_marker_i_pos(self,marker_id):
        if marker_id==1:
            return MarkersPosition._marker1_pos
        elif marker_id==2:
            return MarkersPosition._marker2_pos
        elif marker_id==3:
            return MarkersPosition._marker3_pos
        elif marker_id==4:
            return MarkersPosition._marker4_pos
        elif marker_id==5:
            return MarkersPosition._marker5_pos
    '''
    return str_markers_pos format: marker1_pos:(1,2,3).marker2_pos:(4,5,6).marker3_pos:None.marker4_pos:(4,5,6).marker5_pos:(4,5,6).(1,3,6).
    '''
    @property
    def markers_pos_string(self):
        str_markers_pos=""
        for i in range(5):
            if i<4:
                str_markers_pos+="marker"+str(i+1)+"_pos:"
                if self._markers_pos[i]==None:
                    str_markers_pos+="None|"
                else:
                    str_markers_pos+="("+str(self._markers_pos[i][0])+","+str(self._markers_pos[i][1])+","+str(self._markers_pos[i][2])+")|"
            else:
                str_markers_pos+="marker"+str(i+1)+"_pos:"
                if self._markers_pos[i]==None:
                    str_markers_pos+="None|"
                    continue
                for j in range(len(self._markers_pos[i])):
                    if self._markers_pos[i][j]==None:
                        continue
                    append_str=";"
                    str_markers_pos+="("+str(self._markers_pos[i][j][0])+","+str(self._markers_pos[i][j][1])+","+str(self._markers_pos[i][j][2])+")"+(append_str if j<len(self._markers_pos[i])-1 else "")
                str_markers_pos+="|"
        return str_markers_pos
    @property
    def hungarian_index_string(self):
        str_hung_index="hungarian_index:["
        if self._hung_index==None:
            return str_hung_index+"None]"
        
        for i,index in enumerate(self._hung_index):
            str_hung_index+=str(index)
            if i==len(self._hung_index)-1:
                break
            else:
                str_hung_index+=","
        str_hung_index+="]"
        return str_hung_index

def test():
    f1=MarkersPosition()
    
    marker1=Marker(1,position_3D=(1,2,3))
    
    marker2=Marker(2,position_3D=(4,5,6))
#    marker6=Marker(5,position_3D=(1,3,6))
    marker3=Marker(3,position_3D=(1,2,3))
    marker4=Marker(4,position_3D=(4,5,6))
    marker5=Marker(5,position_3D=(4,5,6))
    marker6=Marker(5,position_3D=(4,5,6))

    
    markers=[marker1,marker2,marker3,marker4,marker5,marker6]
    f1.markers_pos=markers
    f1.hungarian_index=[1,2,3,4]
    
    
    
    print(f1._marker1_pos)
    print(f1._marker2_pos)
    print(f1.markers_pos_string)
    f2=MarkersPosition()
    marker_append=Marker(5)
    f2.markers_pos=[marker_append]
    print(f1.hungarian_index_string)
    print("f1.hungarian_index_string",f1.hungarian_index_string)
if __name__=="__main__":
    test()
        