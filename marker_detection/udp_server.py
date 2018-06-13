#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 10:55:08 2018

@author: jiang
"""
import numpy as np
import socket
from markers_position import MarkersPosition
import threading
import time

class UDP_Server(object):
    _stop_server=False
    @property
    def stop_server(self):
        UDP_Server._stop_server=True
    def __init__(self,address=('127.0.0.1',5000)):
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
    print("starting")
    test_case=UDP_Server()#('192.168.1.103',5000)
    test_case.start_server()
    print("ending")
if __name__=="__main__":
    test()
    
        
