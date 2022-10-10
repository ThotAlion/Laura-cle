#!/usr/bin/env python3

import rospy
# from sensor_msgs.msg import JointState
import dlib,json,time,os
import numpy as np
import cv2

from tools.lib_qbo_pyarduqbo import qbo_control_client
from qbo_face_msgs.msg import FacePosAndDist

def findEuclideanDistance(source_representation, test_representation):
    euclidean_distance = source_representation - test_representation
    euclidean_distance = np.sum(np.multiply(euclidean_distance, euclidean_distance))
    euclidean_distance = np.sqrt(euclidean_distance)
    return euclidean_distance

def loadFaces(faces_dir):
    files = os.listdir(faces_dir)
    faces_dict = {}
    for file in files:
        if os.path.isfile(os.path.join(faces_dir, file)):
            f = open(os.path.join(faces_dir, file),'r')
            faces_dict[file]=np.array(json.loads(f.readline()))
            f.close()
    return faces_dict

def saveFaces(faces_dir,faces_dict):
    for kface, face in faces_dict.items() :
        f = open(os.path.join(faces_dir, kface),'w')
        f.write(json.dumps(face.tolist()))
        f.close()

class FaceVision(qbo_control_client):

    def __init__(self):

        qbo_control_client.__init__(self)

        rospy.init_node('qbo_vision', anonymous=False)

        # cmd_joints_pub=rospy.Publisher('/cmd_joints', JointState, queue_size=1)

        detector = dlib.get_frontal_face_detector()
        sp = dlib.shape_predictor('/home/jarvis/qbo_ws/src/qbo_vision/config/shape_predictor_5_face_landmarks.dat')
        facerec = dlib.face_recognition_model_v1('/home/jarvis/qbo_ws/src/qbo_vision/config/dlib_face_recognition_resnet_model_v1.dat')
        FacePosAndDist_pub = rospy.Publisher("/FacePosAndDist", FacePosAndDist, queue_size=10)
        faces_dir = "/home/jarvis/qbo_ws/src/qbo_vision/faces"
        threshold = 0.6 #distance threshold declared in dlib docs for 99.38% confidence score on LFW data set

        face_dict=loadFaces(faces_dir)
        print(face_dict)
        waiting_list_face = {}
        yaw_c = 0.0
        pitch_c = 0.0
        yaw_target = 0.0
        pitch_target = 0.0
        cap = cv2.VideoCapture(0)
        
        msg = FacePosAndDist()
        # msg.header = rospy.Time.now()
        msg.u = 0.0
        msg.v = 0.0
        msg.distance_to_head = 0.0
        msg.image_width = 640
        msg.image_height = 480
        msg.face_detected = False
        msg.type_of_tracking = "get_frontal_face_detector"
        

        while not rospy.is_shutdown():
            
            t0 = time.time()
            yaw_m = self.Servo1Pos # positif regarde vers la gauche (entre -100 et 100) 0 au milieu
            pitch_m = self.Servo2Pos # positif regarde vers le bas (entre 1 et 47) 36 = horizontal
            # print(yaw_m,pitch_m)
            
            if cap.isOpened():
                # img = dlib.load_rgb_image('image.jpg')
                flag, img = cap.read()
                dets = detector(img, 1)
                if len(dets) > 0:
                    msg.face_detected = True
                    yaw_target = yaw_m -(dets[0].center().x-341)*18.4/240
                    pitch_target = (pitch_m-36.0) +(dets[0].center().y-292)*18.4/240
                    img_shape = sp(img, dets[0])
                    img_aligned = dlib.get_face_chip(img, img_shape)
                    img_representation = facerec.compute_face_descriptor(img_aligned)
                    img_representation = np.array(img_representation)
                    # print(img_representation)
                    person = ""
                    for kface, face in face_dict.items() :
                        distance = findEuclideanDistance(img_representation, face)
                        print(distance)
                        if distance < threshold :
                           person = kface
                           print(person)
                           break

                    if len(person)==0 :
                        
                        face_dict[str(rospy.Time.now())]=img_representation
                        saveFaces(faces_dir,face_dict)

                    msg.header.stamp = rospy.Time.now()
                    msg.u = dets[0].center().x
                    msg.v = dets[0].center().y
                    # print(yaw_target,pitch_target)
                    # print(dets[0].center())
                    # img_shape = sp(img, dets[0])
                    # w = 1.0*np.abs(img_shape.parts()[0].x-img_shape.parts()[2].x)
                    # x = dets[0].center().x
                    # y = dets[0].center().y
                    # yaw_c = yaw_c-0.0002*(x-320)
                    # pitch_c = pitch_c+0.0002*(y-280)
                    # print(yaw_c)
                    # w = 1.0*np.abs(img_shape.parts()[0].x-img_shape.parts()[2].x)
                    # # print(w)
                    # xc = xc+0.05*(x-320)
                    # cc = cc-0.07*xc
                    # yc = yc+0.02*(y-240)
                    # tilt = tilt+0.3*theta
                else:
                    # msg.header = rospy.Time.now()
                    msg.u = 0.0
                    msg.v = 0.0
                    msg.face_detected = False
                #     yaw = 0
                #     pitch = 0

                # envoyer position aux moteurs
                yaw_c=yaw_target
                pitch_c=pitch_target+36.0
                self.moveHead(yaw_c,pitch_c)
            
                # print(time.time()-t0)
                FacePosAndDist_pub.publish(msg)
            # except Exception as e:
            #     self.moveHead(0,0)
            #     print(e)
            #     break



if __name__ == '__main__':
  try:
    node = FaceVision()  
  except rospy.ROSInterruptException:
    print("interrupted  !")