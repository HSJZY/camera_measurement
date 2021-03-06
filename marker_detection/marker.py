import cv2

from numpy import mean, binary_repr, zeros
from numpy.random import randint
from scipy.ndimage import zoom

MARKER_SIZE = 28


class Marker(object):
    def __init__(self, id, contours=None,position_3D=None):
        self.id = id
        self.contours = contours
        self.position_3D=position_3D

    def __repr__(self):
        return '<Marker id={} center={}> position_3D={}'.format(self.id, self.center,self.position_3D)

    @property
    def center(self):
        if self.contours is None:
            return None
        center_array = mean(self.contours, axis=0).flatten()
        return (int(center_array[0]), int(center_array[1]))
    @property
    def position(self):
        return self.position_3D
    @position.setter
    def position(self,pos_3D):
        self.position_3D=pos_3D
    @property
    def contour(self):
        return self.contours

    def set_position_3D(self,position):
        self.position_3D=position

    def draw_contour(self, img, color=(0, 255, 0), linewidth=5):
#        print("self.contours:",self.contours)
        cv2.drawContours(img, [self.contours], -1, color, linewidth)

    def highlite_marker(self, img, contour_color=(0, 255, 0), text_color=(255, 0, 0), linewidth=5):
        self.draw_contour(img, color=contour_color, linewidth=linewidth)
        cv2.putText(img, str(self.id), self.center, cv2.FONT_HERSHEY_SIMPLEX, 2, text_color)

    @property
    def id_as_binary(self):
        return binary_repr(self.id, width=12)
    
    


