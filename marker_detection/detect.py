import cv2

from numpy import array, rot90
from marker_detection.marker import  Marker
from sklearn.externals import joblib
import math
import numpy as np
MARKER_SIZE=28

def calc_distance_to_marker(marker,length_marker_edge):
    def order_marker_contour(contour):
        # sort this contour to the form as follow
        #   1....2
        #   .    .
        #   4....3
        contour=sorted(contour,key=lambda x:(x[0]),reverse=False)
        point_1_2=contour[:2]
        point_3_4=contour[2:]
        print("point1_2:",point_1_2)
        print("point3_4",point_3_4)
        points=[]
        if point_1_2[0][1]<point_1_2[1][1]:
            points.append((point_1_2[0][0],point_1_2[0][1]))
            points.append((point_1_2[1][0],point_1_2[1][1]))
        else:
            points.append((point_1_2[1][0],point_1_2[1][1]))
            points.append((point_1_2[0][0],point_1_2[0][1]))
        if point_3_4[0][1]>point_3_4[1][1]:
            points.append((point_3_4[0][0],point_3_4[0][1]))
            points.append((point_3_4[1][0],point_3_4[1][1]))
        else:
            points.append((point_3_4[1][0],point_3_4[1][1]))
            points.append((point_3_4[0][0],point_3_4[0][1]))
        return np.array(points,dtype = "double")
    
    camera_matrix = np.array(
            [[853.2785, 0,307.2291],
             [0, 852.4253, 227.778],
             [0, 0, 1]], dtype = "double"
             )
    dist_coeffs=np.array([0.1792,-0.2934,-0.0012,0.0026,0],dtype = "double")
    _contour=marker.contour
    image_points=order_marker_contour(_contour)
    half_edge_length=length_marker_edge/2.0
    model_points = np.array([
            (-half_edge_length, half_edge_length, 0.0),             # Nose tip
            (half_edge_length, half_edge_length, 0),        # Chin
            (half_edge_length, -half_edge_length, 0),     # Left eye left corner
            (-half_edge_length, -half_edge_length, 0),      # Right eye right corne                        
            ],dtype = "double")
    print("model_points:",model_points,"image_points",image_points,"camera_matrix:",camera_matrix)
    success, rotation_vector, translation_vector= cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
    return translation_vector


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
#        print("contour:",contour)
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
                marker_list.append(Marker(id=marker_info[0], contours=np.array(marker_info[2])))
        else:
            marker_list.append(Marker(id=marker_info[0], contours=np.array(marker_info[2])))
    return marker_list


def detect_markers(img):
    def validate_digit_marker(detector,marker):
        rows,cols=marker.shape
        res_4=[]
        for i in range(4):
            M=cv2.getRotationMatrix2D((int(MARKER_SIZE/2),int(MARKER_SIZE/2)),90*i,1)
            rotated_img=cv2.warpAffine(marker,M,(0,0))
    #        cv2.imshow("frame:",rotated_img)
    #        cv2.waitKey(0)
            rotated_img_reshaped=rotated_img.reshape(-1,MARKER_SIZE*MARKER_SIZE)
            pred_res=detector.predict(rotated_img_reshaped)[0]
            res_4.append(pred_res)
        counts = np.bincount(res_4)
        res=int(np.argmax(counts))
        #返回众数  
        return res
    width, height, _= img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,gray = cv2.threshold(gray,100,255,0)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',gray)
    cv2.waitKey(0)
    
    svc = joblib.load("/home/jiang/Desktop/求毕业/python-ar-markers/ar_markers/hamming/svc_model.m")

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
#        print("shape:",warped_bin.shape)
        warped_bin=cv2.resize(warped_bin,(MARKER_SIZE,MARKER_SIZE))
        marker = warped_bin.reshape(
            [MARKER_SIZE, int(warped_size / MARKER_SIZE), MARKER_SIZE, int(warped_size / MARKER_SIZE)]
        )
#        print("marker:",marker.shape)
        marker = marker.mean(axis=3).mean(axis=1)
        marker[marker < 127] = 0
        marker[marker >= 127] = 1
        try:
            print("validating...")
            marker_id=validate_digit_marker(svc,marker)
            print("marker_id:",marker_id)
            if marker_id==0:
                continue
            markers_list.append(Marker(id=marker_id, contours=approx_curve))
#            print(mar)
        except ValueError:
            continue
    print("markers_list:",markers_list)
    return markers_list


