#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 10:55:08 2018

@author: jiang
"""
import numpy as np
import socket
try:
    from marker_detection.markers_position import MarkersPosition
    from marker_detection.marker import Marker
except:
    from marker import Marker
    from markers_position import MarkersPosition
import threading
import time

class UDP_Server(object):
    _stop_server=False
    def stop_server(self):
        UDP_Server._stop_server=True
    def __init__(self,address=('192.168.43.95',5000)):
        self.address=address
    def _tcp_link(self,sock,addr):
        print('Accept new connection from %s:%s...' % addr)
        while True:
            data=sock.recv(1024)
            time.sleep(0.1)
            if data=='exit':
                break
            markers_pos=MarkersPosition()
            reply_data=markers_pos.markers_pos_string
            
            sock.send(reply_data.encode('utf_8'))
        sock.close()
        print('Connection from %s:%s closed.' % addr)
    def _start_server_thread(self):
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("address:",self.address)
        sock.bind(self.address)
        sock.listen(5)        
        print("Server Started")
        while True:
            
            if UDP_Server._stop_server==True:
                break
            sock_t,sock_addr=sock.accept()
            print('got connected from',sock_addr)
            thread_t=threading.Thread(target=self._tcp_link, args=(sock_t, sock_addr))
            thread_t.start()
        sock.close()
        print("sertver stopped")
    def start_server(self):
        udp_server_thread=threading.Thread(target=self._start_server_thread)
        udp_server_thread.start()
def test():
    f2=MarkersPosition()
    marker1=Marker(1,position_3D=(400,2,400))
    marker2=Marker(2,position_3D=(800,5,700))
    marker3=Marker(3,position_3D=(1200,2,400))
    marker4=Marker(4,position_3D=(1600,5,700))
    marker5=Marker(5,position_3D=(0,5,0))
    marker6=Marker(5,position_3D=(3000,3,0))
#    marker7=Marker(5,position_3D=(2,5,7))
#    marker8=Marker(5,position_3D=(1,3,6))
    
    markers=[marker1,marker2,marker3,marker4,marker5,marker6]
    f2.markers_pos=markers
    
    print("starting")
    test_case=UDP_Server()#('192.168.1.103',5000)
    test_case.start_server()
    print("ending")
if __name__=="__main__":
    test()
    
        
