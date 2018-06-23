import cv2

from numpy import array, rot90
from marker_detection.marker import  Marker
import math
import numpy as np
import random
MARKER_SIZE=28

def calc_distance_to_marker(marker,length_marker_edge):
    def order_marker_contour(contour):
        # sort this contour to the form as follow
        #   1....2
        #   .    .
        #   4....3
        if not isinstance(contour,list):
            contour=contour.tolist()
        contour=sorted(contour,key=lambda x:(x[0]),reverse=False)
        for index,corner_points in enumerate(contour):
            if len(corner_points)==1:
                contour[index]=corner_points[0]
        
        point_1_2=contour[:2]
        point_3_4=contour[2:]
        
        print("point1_2",point_1_2)
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
            [[1381.2, 0,973.237],
             [0, 1382.7, 552.4756],
             [0, 0, 1]], dtype = "double"
             )
    dist_coeffs=np.array([0.1166,-0.2475,0.0023,0.000803,0.1074],dtype = "double")
    _contour=marker.contour
    
    image_points=order_marker_contour(_contour)
    print("_contour:",image_points)
    half_edge_length=length_marker_edge/2.0
    model_points = np.array([
            (-half_edge_length, half_edge_length, 0.0),             # Nose tip
            (half_edge_length, half_edge_length, 0),        # Chin
            (half_edge_length, -half_edge_length, 0),     # Left eye left corner
            (-half_edge_length, -half_edge_length, 0),      # Right eye right corne                        
            ],dtype = "double")
#    print("model_points:",model_points,"image_points",image_points,"camera_matrix:",camera_matrix)
    success, rotation_vector, translation_vector= cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
    trans_res=(translation_vector[0][0],translation_vector[1][0],translation_vector[2][0])
    print("trans_res:",trans_res)
    return trans_res


def simple_seprate_contour(markers):
    def calc_distance(point1,point2):
        return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
    def clac_area_triangle(point1,point2,point3):
        a=calc_distance(point1,point2)
        b=calc_distance(point2,point3)
        c=calc_distance(point3,point1)
        p=(a+b+c)/2
#        print("a:",a,"b:",b,"c:",c,"p:",p)
        return math.sqrt(abs(p*(p-a)*(p-b)*(p-c)))
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
    print("markers:",markers)
#    input()
    for marker in markers:
        print("marker__:",marker.contour)
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


def detect_markers(img,model,edge_length=120):
    def validate_digit_marker(detector,marker):
        rows,cols=marker.shape
        res_4=[]
#        cv2.imshow("frame_marker:",marker)
#        print("marker",marker)
#        cv2.waitKey(0)
#        _label=input()
#        cv2.imwrite("./img_dataset/img"+str(random.randint(1,3000))+"_"+str(_label)+".png",marker)
#        cv2.destroyAllWindows()
        
        for i in range(4):
            M=cv2.getRotationMatrix2D((int(MARKER_SIZE/2),int(MARKER_SIZE/2)),90*i,1)
            rotated_img=cv2.warpAffine(marker,M,(0,0))
#            cv2.imshow("frame:",rotated_img)
#            cv2.waitKey(0)
            rotated_img_reshaped=rotated_img.reshape(-1,MARKER_SIZE*MARKER_SIZE)
            pred_res=detector.predict(rotated_img_reshaped)[0]
            res_4.append(pred_res)
        print("res_4:",res_4)
        counts = np.bincount(res_4)
        res=int(np.argmax(counts))
        #返回众数  
        return res
    width, height, _= img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
#    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
#    cv2.imshow('image',gray)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
    
    gray = cv2.medianBlur(gray,5)
    
    # Otsu's thresholding
    ret2,gray_edge = cv2.threshold(gray.copy(),190,255,cv2.THRESH_BINARY)#+cv2.THRESH_OTSU
#    gray_close = cv2.medianBlur(gray_edge,5)
#    cv2.namedWindow('image_close', cv2.WINDOW_NORMAL)
#    cv2.imshow("image_close", gray_edge)
#    cv2.waitKey(0)
  
#    _img_cont, cont, hier = cv2.findContours(gray_edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#    _img = cv2.drawContours(gray, cont, -1, 0, 3)
    
#    gray = cv2.equalizeHist(gray)

    edges = cv2.Canny(gray_edge, 20, 200)
    
#    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
#    cv2.imshow('image',_img)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
    
#    minLineLength = 10
#    maxLineGap = 10
#    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
#    for line in lines:
#        for x1,y1,x2,y2 in line:
#            cv2.line(edges,(x1,y1),(x2,y2),255,2)
    
#    kernel = np.ones((3,3),np.uint8)
#    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
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
#    print("len(contours):",len(contours))
    for contour in contours:
        approx_curve = cv2.approxPolyDP(contour, len(contour) * 0.01, True)
        if not(cv2.isContourConvex(approx_curve) and len(approx_curve)==4):
            continue
        
        sorted_curve = array(cv2.convexHull(approx_curve, clockwise=False),dtype='float32')
#        print("sorted_curve:",sorted_curve)
        persp_transf = cv2.getPerspectiveTransform(sorted_curve, canonical_marker_coords)
        warped_img = cv2.warpPerspective(img, persp_transf, (warped_size, warped_size))
        warped_gray = cv2.cvtColor(warped_img, cv2.COLOR_BGR2GRAY)
        warped_gray=255-warped_gray
       

#        _, warped_bin = cv2.threshold(warped_gray, 210, 255, cv2.THRESH_BINARY)
#        cv2.imshow('image_gry',warped_bin)
#        cv2.waitKey(0)
#        print("shape:",warped_bin.shape)
        warped_bin=cv2.resize(warped_gray,(MARKER_SIZE,MARKER_SIZE))
        marker = warped_bin.reshape(
            [MARKER_SIZE, int(warped_size / MARKER_SIZE), MARKER_SIZE, int(warped_size / MARKER_SIZE)]
        )
#        print("marker:",marker.shape)
        marker = marker.mean(axis=3).mean(axis=1)
        marker=marker/255.0
        marker[marker<0.2]=0
        marker[marker>=0.2]=1
        try:
            print("############ validating ##################")
            marker_id=validate_digit_marker(model,marker)
            _marker=Marker(id=marker_id, contours=approx_curve)
            print("_marker:",_marker)
            if marker_id==0:
                continue
            markers_list.append(_marker)
#            print(mar)
        except ValueError:
            continue
        
    marker_list=simple_seprate_contour(markers_list)
    for marker in marker_list:
        position_3D=calc_distance_to_marker(_marker,edge_length)
        _marker.position=position_3D
    return markers_list


