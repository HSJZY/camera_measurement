import cv2

from numpy import mean, binary_repr, zeros
from numpy.random import randint
from scipy.ndimage import zoom



MARKER_SIZE = 28


class Marker(object):
    def __init__(self, id, contours=None):
        self.id = id
        self.contours = contours

    def __repr__(self):
        return '<Marker id={} center={}>'.format(self.id, self.center)

    @property
    def center(self):
        if self.contours is None:
            return None
        center_array = mean(self.contours, axis=0).flatten()
        return (int(center_array[0]), int(center_array[1]))
    
    @property
    def contour(self):
        return self.contours

    def draw_contour(self, img, color=(0, 255, 0), linewidth=5):
        cv2.drawContours(img, [self.contours], -1, color, linewidth)

    def highlite_marker(self, img, contour_color=(0, 255, 0), text_color=(255, 0, 0), linewidth=5):
        self.draw_contour(img, color=contour_color, linewidth=linewidth)
        cv2.putText(img, str(self.id), self.center, cv2.FONT_HERSHEY_SIMPLEX, 2, text_color)

    @property
    def id_as_binary(self):
        return binary_repr(self.id, width=12)


