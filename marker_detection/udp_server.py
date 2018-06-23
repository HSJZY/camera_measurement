#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 10:55:08 2018

@author: jiang
"""
import numpy as np
import socket
from marker_detection.markers_position import MarkersPosition
import threading
import time
from marker_detection.marker import Marker

class UDP_Server(object):
    _stop_server=False
    @property
    def stop_server(self):
        UDP_Server._stop_server=True
    def __init__(self,address=('192.168.1.104',5000)):
        self.address=address
    def _start_server_thread(self):
        sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("address:",self.address)
        sock.bind(self.address)
        markers_pos=MarkersPosition()
        
        print("Server Started")
        while True:
            data, addr = sock.recvfrom(1024)
            data=data.decode('utf-8')
            print("recieved message: " + str(addr))
            print("From Connected user: " + data)
            reply_data=markers_pos.markers_pos_string
#            data = data.upper()
            print("Sending: "+ reply_data)
            sock.sendto(reply_data.encode('utf-8'),addr)
        sock.close()
    def start_server(self):
        udp_server_thread=threading.Thread(target=self._start_server_thread)
        udp_server_thread.start()
def test():
    f2=MarkersPosition()
    marker1=Marker(1,position_3D=(0,2,0))
    marker2=Marker(2,position_3D=(400,5,400))
    marker3=Marker(3,position_3D=(800,2,0))
    marker4=Marker(4,position_3D=(1200,5,400))
    marker5=Marker(5,position_3D=(4,5,6))
    marker6=Marker(5,position_3D=(1,3,8))
    marker7=Marker(5,position_3D=(2,5,7))
    marker8=Marker(5,position_3D=(1,3,6))
    
    markers=[marker1,marker2,marker3,marker4,marker5,marker6,marker7,marker8]
    f2.markers_pos=markers
    
    print("starting")
    test_case=UDP_Server()#('192.168.1.103',5000)
    test_case.start_server()
    print("ending")
if __name__=="__main__":
    test()
    
        
