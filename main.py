import cv2
from marker_detection.detect import detect_markers,simple_seprate_contour,calc_distance_to_marker
from marker_detection.markers_position import MarkersPosition
from marker_detection.udp_server import UDP_Server
from marker_detection.marker import Marker
from sklearn.externals import joblib
import time
import numpy as np
from marker_detection.hungarian_assignment import TaskAssignment

formation_H=[[0,0],[1000,0],[1000,-1000],[0,-1000]]

marker_1=Marker(id=1)
marker_2=Marker(id=2)
marker_3=Marker(id=3)
marker_4=Marker(id=4)

def test():
    frame = cv2.imread("./test_img/test_img_113.jpg")
    print(frame.shape)
    model = joblib.load("./marker_detection/neigh_model.m")
    markers=detect_markers(frame,model)
#    markers=simple_seprate_contour(markers)
#    print("markers:",markers)
    for marker in markers:
        try:
            marker.highlite_marker(frame)
        except:
            continue
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)   
    cv2.imshow('image',frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def generate_marker_5_pos(markers):
    gen_markers=[]
    for marker in markers:
        if marker.id!=5:
            gen_markers.append(marker)
            continue
        marker_position=marker.position;
        pos_1=(marker_position[0],marker_position[1],marker_position[2]) #define the first point is left-buttom side with 500,200
        pos_2=(marker_position[0]+3000,marker_position[1],marker_position[2])
        pos_3=(marker_position[0]+3000,marker_position[1]-1600,marker_position[2])
        new_marker_1=Marker(id=5, contours=marker.contour,position_3D=pos_1)
        new_marker_2=Marker(id=5, contours=marker.contour,position_3D=pos_2)
        new_marker_3=Marker(id=5, contours=marker.contour,position_3D=pos_3)
        gen_markers.append(new_marker_1)
        gen_markers.append(new_marker_2)
        gen_markers.append(new_marker_3)
    return gen_markers
def for_adjust():
    f2=MarkersPosition()
    marker1=Marker(1,position_3D=(400,2,400))
    marker2=Marker(2,position_3D=(800,5,700))
    marker3=Marker(3,position_3D=(1200,2,400))
    marker4=Marker(4,position_3D=(1600,5,700))
    marker5=Marker(5,position_3D=(0,5,0))
    marker6=Marker(5,position_3D=(3000,3,0))

    
    markers=[marker1,marker2,marker3,marker4,marker5,marker6]
    f2.markers_pos=markers
    
def assignment_change(formation_setted):
    markers=[marker_1,marker_2,marker_3,marker_4]
    markers_position=[]
    for marker in markers:
        markers_position.append(marker.position)

    center_markers=np.sum(np.array(markers_position),0)/len(markers)
    markers_position=np.array(markers_position)-center_markers
    center_formation=np.sum(np.array(formation_setted),0)/len(markers)
    formation_setted_changed=formation_setted-center_formation
    munkres_matrix=np.zeros((len(markers_position),len(formation_setted_changed)))
    
    for i in range(len(munkres_matrix)):
        for j in range(len(munkres_matrix[i])):
            munkres_matrix[i][j]=(markers_position[i][0]-formation_setted_changed[j][0])**2+(markers_position[i][1]-formation_setted_changed[j][1])**2
    
    ass_by_Hun = TaskAssignment(munkres_matrix, 'Hungary')
    changed_index=ass_by_Hun.best_solution
#    print('best solution = ',changed_index )
    markers_position_exchanged=[]
    for index in changed_index:
        markers_position_exchanged.append(markers[index])
    return changed_index
    
def test_assignment():
    global marker_1
    global marker_2
    global marker_3
    global marker_4
    
    marker1=Marker(1,position_3D=(0,0,0))
    marker2=Marker(2,position_3D=(-400,0,0))
    marker3=Marker(3,position_3D=(-800,800,0))
    marker4=Marker(4,position_3D=(0,-800,0))
    marker5=Marker(5,position_3D=(0,5,0))
    markers=[marker1,marker2,marker3,marker4,marker5]
    
    for marker in markers:
        if marker.id==1:
            marker_1=marker
        elif marker.id==2:
            marker_2=marker
        elif marker.id==3:
            marker_3=marker
        elif marker.id==4:
            marker_4=marker
    markers_after=assignment_change(formation_H)
    print("markers:",markers,"\nmarkers_after:",markers_after)
    
def main():
    cap=cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    cv2.namedWindow("image",cv2.WINDOW_NORMAL)
    video_file_path="./test_img/"
    file_name="video_test.avi"
    file_name_orig="video_orig.avi"
    
    # Define the codec and create VideoWriter object
#    fourcc =cv2.VideoWriter_fourcc('M','J','P','G')
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out_video = cv2.VideoWriter(video_file_path+file_name, fourcc, 5.0, (1920, 1080))
    out_video_orig = cv2.VideoWriter(video_file_path+file_name_orig, fourcc, 5.0, (1920, 1080))
    for_adjust();
    addr=('192.168.43.95',5000)
    server=UDP_Server(addr)
    server.start_server()

    model = joblib.load("./marker_detection/neigh_model.m")
    
    log_file_path="./log.txt"
    log_file= open(log_file_path, "w")

    while(1):
        ret,frame=cap.read()
        before_markers=detect_markers(frame,model,118)
        markers=generate_marker_5_pos(before_markers)
        
        global marker_1
        global marker_2
        global marker_3
        global marker_4
        for marker in markers:
            if marker.id==1:
                marker_1=marker
            elif marker.id==2:
                marker_2=marker
            elif marker.id==3:
                marker_3=marker
            elif marker.id==4:
                marker_4=marker
        
        # ********这一句只能在任意拓扑编队中使用**********
        hung_index=assignment_change(formation_H)

        ms_pos=MarkersPosition()
        ms_pos.markers_pos=markers
#        print("*******************markers_position************************")
#        print(ms_pos.markers_pos_string)
#        for marker in markers:
#            print(marker)
#        print("***********************************************************")
        log_str=str(round(time.time(),2))+" "+ms_pos.markers_pos_string+"\n"
        log_file.write(log_str)
        out_video_orig.write(frame)        
        for marker in markers:
            try:
                marker.highlite_marker(frame)
            except:
                continue
            
#        frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("image",frame)
        out_video.write(frame)
        
        key=cv2.waitKey(10)
        if key==27:
            break;
        
    server.stop_server()
    log_file.close()
    out_video.release()
    out_video_orig.release()
    cap.release()
    cv2.destroyAllWindows()
if __name__=="__main__":
    test_assignment()