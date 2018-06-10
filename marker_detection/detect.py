import cv2

from numpy import array, rot90
from marker_detection.marker import  Marker
from sklearn.externals import joblib
MARKER_SIZE=28

def validate_digit_marker(detector,marker):
    rows,cols=marker.shape
    res=[]
    for i in range(4):
        M=cv2.getRotationMatrix2D((int(MARKER_SIZE/2),int(MARKER_SIZE/2)),90*i,1)
        rotated_img=cv2.warpAffine(marker,M,(0,0))
#        cv2.imshow("frame:",rotated_img)
#        cv2.waitKey(0)
        rotated_img_reshaped=rotated_img.reshape(-1,MARKER_SIZE*MARKER_SIZE)
        pred_res=detector.predict(rotated_img_reshaped)
        res.append(pred_res)
    print("res:",res)
    return max(res)

def detect_markers(img):
    width, height, _= img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,gray = cv2.threshold(gray,100,255,0)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',gray)
    cv2.waitKey(0)
    
    svc = joblib.load("./marker_detection/svc_model.m")

    edges = cv2.Canny(gray, 10, 100)
    
    cv2.imshow('image',edges)
    cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

    # We only keep the long enough contours
    min_contour_length = min(width, height) / 80
    contours = [contour for contour in contours if len(contour) > min_contour_length]
    warped_size = 49
    canonical_marker_coords = array(((0, 0),
                                     (warped_size - 1, 0),
                                     (warped_size - 1, warped_size - 1),
                                     (0, warped_size - 1)),
                                    dtype='float32')
#    print("canonical_marker_coords:",canonical_marker_coords)

    markers_list = []
    for contour in contours:
        approx_curve = cv2.approxPolyDP(contour, len(contour) * 0.01, True)
        if not (len(approx_curve) == 4 and cv2.isContourConvex(approx_curve)):
            continue

        sorted_curve = array(cv2.convexHull(approx_curve, clockwise=False),dtype='float32')
        persp_transf = cv2.getPerspectiveTransform(sorted_curve, canonical_marker_coords)
        warped_img = cv2.warpPerspective(img, persp_transf, (warped_size, warped_size))
        warped_gray = cv2.cvtColor(warped_img, cv2.COLOR_BGR2GRAY)

        _, warped_bin = cv2.threshold(warped_gray, 127, 255, cv2.THRESH_BINARY)
        cv2.imshow('image_gry',warped_bin)
#        print("warped_gray:",warped_bin/255.0)
        cv2.waitKey(0)
        print("shape:",warped_bin.shape)
        warped_bin=cv2.resize(warped_bin,(MARKER_SIZE,MARKER_SIZE))
        marker = warped_bin.reshape(
            [MARKER_SIZE, int(warped_size / MARKER_SIZE), MARKER_SIZE, int(warped_size / MARKER_SIZE)]
        )
#        print("marker:",marker.shape)
        marker = marker.mean(axis=3).mean(axis=1)
        marker[marker < 127] = 0
        marker[marker >= 127] = 1
        
#        print('marker',marker.shape)

        try:
            print("validating...")
            marker_id=validate_digit_marker(svc,marker)
            if marker_id==0:
                continue
            markers_list.append(Marker(id=marker_id, contours=approx_curve))
#            print(mar)
        except ValueError:
            continue
    print("markers_list:",markers_list)
    return markers_list


