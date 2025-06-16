import cv2

#cam_w = cv2.VideoCapture(4)  # /dev/video4
cam_r = cv2.VideoCapture(2)  # /dev/video2
cam_l = cv2.VideoCapture(0)  # /dev/video0



while(True):

    if False:
        ret_w, frame_w = cam_w.read()  # ret==True/False: read successfully or not; frame: image
        if not ret_w:
            print("Failed to read the image from wrist camera.")
            break
        # display image
        cv2.imshow('Video_from_wrist', frame_w)
        # press ESC key to exit
        key_w = cv2.waitKey(1)
        if key_w == 27:
            break

    if True:
        ret_r, frame_r = cam_r.read()  # ret==True/False: read successfully or not; frame: image
        if not ret_r:
            print("Failed to read the image from right camera.")
            break
        # display image
        cv2.imshow('Video_from_right', frame_r)
        # press ESC key to exit
        key_r = cv2.waitKey(1)
        if key_r == 27:
            break

    if True:
        ret_l, frame_l = cam_l.read()  # ret==True/False: read successfully or not; frame: image
        if not ret_l:
            print("Failed to read the image from left camera.")
            break
        # display image
        cv2.imshow('Video_from_left', frame_l)
        # press ESC key to exit
        key_l = cv2.waitKey(1)
        if key_l == 27:
            break



#cam_w.release()
cam_l.release()
cam_r.release()






#import cv2
#import threading
#
#def read_camera(cam, window_name):
#    while True:
#        ret, frame = cam.read()
#        if not ret:
#            print(f"Failed to read from {window_name}")
#            break
#        cv2.imshow(window_name, frame)
#        if cv2.waitKey(1) == 27:
#            break
#    cam.release()
#
##cam_w = cv2.VideoCapture(0)
#cam_r = cv2.VideoCapture(2)
#cam_l = cv2.VideoCapture(4)
#
#threads = []
##threads.append(threading.Thread(target=read_camera, args=(cam_w, 'Video_from_wrist')))
#threads.append(threading.Thread(target=read_camera, args=(cam_r, 'Video_from_right')))
#threads.append(threading.Thread(target=read_camera, args=(cam_l, 'Video_from_left')))
#
#for t in threads:
#    t.start()
#
#for t in threads:
#    t.join()
#
#cv2.destroyAllWindows()
