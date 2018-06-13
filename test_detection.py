import cv2
from marker_detection.detect import detect_markers,simple_seprate_contour

# if __name__ == '__main__':
frame = cv2.imread("test_img_5.jpg")
print(frame.shape)
markers=detect_markers(frame)
markers=simple_seprate_contour(markers)
print("markers:",markers)
for marker in markers:
    marker.highlite_marker(frame)
cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.imshow('image',frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
