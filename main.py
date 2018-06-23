import cv2
from marker_detection.detect import detect_markers,simple_seprate_contour,calc_distance_to_marker
from marker_detection.markers_position import MarkersPosition
from marker_detection.udp_server import UDP_Server
from sklearn.externals import joblib

def test():
    frame = cv2.imread("./test_img/test_img_81.jpg")
    print(frame.shape)  
    markers=detect_markers(frame)
    markers=simple_seprate_contour(markers)
    print("markers:",markers)
    for marker in markers:
        try:
            marker.highlite_marker(frame)
        except:
            continue
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)   
    cv2.imshow('image',frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    cap=cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    cv2.namedWindow("image",cv2.WINDOW_NORMAL)
    j=81
    video_file_path="/home/jiang/Desktop/求毕业/python-ar-markers/digit_detection/camera_measurment/test_img/"
    file_name="video_test.avi"
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out_video = cv2.VideoWriter(video_file_path+file_name, fourcc, 20, (1920, 1080))
    
    addr=('192.168.1.104',5000)
    server=UDP_Server(addr)
    server.start_server();

    model = joblib.load("./marker_detection/neigh_model.m")
    
    while(1):
        ret,frame=cap.read()   
        markers=detect_markers(frame,model)

        ms_pos=MarkersPosition()
        ms_pos.markers_pos=markers
        
        print("markers_position:",ms_pos.markers_pos_string)
        
        for marker in markers:
            try:
                marker.highlite_marker(frame)
            except:
                continue
        cv2.imshow("image",frame)
        key=cv2.waitKey(100)
        print("key:",key)
        if key==27:
            break;
        out_video.write(frame)
    out_video.release()
    cap.release()
    cv2.destroyAllWindows()
if __name__=="__main__":
    main()