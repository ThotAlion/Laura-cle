#!/usr/bin/python3
import dlib,requests,json,time
import numpy as np

def enableMotors(robotIP):
    """
    This function enables the motors of the robot.
    """
    for m in ["m1","m2","m3","m4","m5","m6"]:
        url = "http://"+robotIP+"/motors/"+m+"/registers/compliant/value.json"
        data = "false"
        h = {'Content-type': 'application/json'}
        response = requests.post(url, data=data, headers=h)

def disableMotors(robotIP):
    """
    This function enables the motors of the robot.
    """
    for m in ["m1","m2","m3","m4","m5","m6"]:
        url = "http://"+robotIP+"/motors/"+m+"/registers/compliant/value.json"
        data = "true"
        h = {'Content-type': 'application/json'}
        response = requests.post(url, data=data, headers=h)

def motorGoto(robotIP,listPositions,duration):
    """
    This function sets the motor position of the robot.
    """
    url = "http://"+robotIP+"/motors/goto.json"

    data = json.dumps({
        "motors": ["m1","m2","m3","m4","m5","m6"],
        "positions": listPositions,
        "duration": duration,
        "wait": "false",
    })
    h = {'Content-type': 'application/json'}
    response = requests.post(url, data=str(data), headers=h)
    return response.json()

if __name__ == "__main__":
    robotIP = "10.0.0.112:8080"
    enableMotors(robotIP)
    motorGoto(robotIP,[0.0,-20.0,0.0,0.0,0.0,0.0],1.0)

    

    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor('shape_predictor_5_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
    xc=0.0
    yc=0.0
    cc=0.0
    tilt=0.0
    w=20.0
    while True:
        try:
            t0 = time.time()
            resp =requests.get('http://'+robotIP+'/sensors/camera/frame.png')
            imgFile = open('image.png','wb')
            imgFile.write(resp.content)
            imgFile.close()

            img = dlib.load_rgb_image('image.png')
            dets = detector(img, 1)
            if len(dets) > 0:
                # print(dets[0].center())
                img_shape = sp(img, dets[0])
                theta=img_shape.parts()[0].y-img_shape.parts()[2].y
                x = dets[0].center().x
                y = dets[0].center().y
                w = 1.0*np.abs(img_shape.parts()[0].x-img_shape.parts()[2].x)
                xc = xc+0.05*(x-320)
                cc = cc-0.07*xc
                yc = yc+0.02*(y-240)
                tilt = tilt+0.5*theta
            cc = np.clip(cc,-40,40)
            xc = np.clip(xc,-90,90)
            yc = np.clip(yc,-30,30)
            tilt = np.clip(tilt,-30,30)
            w = np.clip(w,-50,50)
            motorGoto(robotIP,[cc,w-20,-w+20+yc,tilt,xc,xc],0.1)
                # 
                # print(img_shape)
                # img_aligned = dlib.get_face_chip(img, img_shape)
            # print(i,time.time()-t0)
        except Exception as e:
            print(e)
            break
    disableMotors(robotIP)