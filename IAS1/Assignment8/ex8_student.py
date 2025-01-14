import vrep
import time
import os
import math as m
import numpy as np
import cv2
import array
from PIL import Image
from helpers import Helpers
import random

orientationVector = [0.0, -1.0]
startPos = [0.0, 0.0]
startOri = 0.0
clientID = -1
wheels = [-1] * 4
imaging=None
buffering = "buffering"
streaming = "streaming"


def initimg(clientID):
    # change to setFloatSignal
    # Helpers.setFloatSignal(clientID, "rgbd_sensor_scan_angle")
    # Helpers.setFloatSignal(clientID, "handle_rgb_sensor")
    # handle = Helpers.getObjectHandles(clientID, "rgbSensor")
    # ret, res, image = Helpers.getVisionSensorImage(clientID, handle, streaming)
    # time.sleep(1)
    # ret, res, image = Helpers.getVisionSensorImage(clientID, handle, buffering)
    # cv2.namedWindow("display")
    # return handle
    vrep.simxSetFloatSignal(clientID, 'rgbd_sensor_scan_angle', m.pi/2, vrep.simx_opmode_oneshot)
    vrep.simxSetIntegerSignal(clientID, 'handle_rgb_sensor', 2, vrep.simx_opmode_oneshot)
    res, sensorHandle = vrep.simxGetObjectHandle(clientID, "rgbSensor", vrep.simx_opmode_oneshot_wait)
    ret, res, image = vrep.simxGetVisionSensorImage(clientID, sensorHandle, 0, vrep.simx_opmode_streaming)
    time.sleep(1)
    ret, res, image = vrep.simxGetVisionSensorImage(clientID, sensorHandle, 0, vrep.simx_opmode_buffer)
    cv2.namedWindow("display")
    return sensorHandle
    

def updateImage(img):
    cv2.imshow("display", img)
    cv2.waitKey(25)


def getImage(clientID, youBotCam):
    start = time.time()
    err, res, image = vrep.simxGetVisionSensorImage(clientID, youBotCam, 0, vrep.simx_opmode_buffer)
    if err == vrep.simx_return_ok:
        data1 = array.array('b', image)
        image_buffer = Image.frombytes("RGB", (res[0],res[1]), bytes(data1), "raw", "RGB", 0, 1)
        img = np.asarray(image_buffer)
        rimg = cv2.cvtColor(cv2.flip(img, 0), cv2.COLOR_BGR2RGB)
        return rimg
    return None


def extractBlobsOfColor(imageBGR, detector, color, KeypointColor):
    if color == "r":
        img = Helpers.redBlobExtract(imageBGR)
    elif color == "b":
        img = Helpers.blueBlobExtract(imageBGR)
    else:
        return None
    keypoints = detector.detect(img)
    for i in range(0, len(keypoints)):
        KeypointColor[keypoints[i].pt] = color
    return img


def imagingSetup():
    global clientID
    global imaging
    imaging = initimg(clientID)
    if (imaging is None):
        print("Could not get cam handle, try again!")
        return
    test = getImage(clientID, imaging)
    updateImage(test)
    params = cv2.SimpleBlobDetector_Params()
    params.minDistBetweenBlobs = 1
    params.filterByColor = True
    params.blobColor = 255
    params.filterByArea = True
    params.minArea = 1
    params.maxArea = 50000
    params.filterByCircularity = False
    params.filterByConvexity = False
    params.filterByInertia = True
    params.minInertiaRatio = 0.01
    params.maxInertiaRatio = 1
    detector = cv2.SimpleBlobDetector_create(params)
    keypointColor = {}
    image = extractBlobsOfColor(test, detector, "r", keypointColor)
    detector2 = cv2.SimpleBlobDetector_create(params)
    image2 = extractBlobsOfColor(test, detector2, "b", keypointColor)
    cv2.imshow("red", image)
    cv2.imshow("blue", image2)
    cv2.waitKey(0)
    return detector, detector2


def sim():
    global startPos
    global startOri
    global clientID
    ori = getObjectOrientation("youBot")
    startPos = getObjectPosition("youBot")
    startOri = Helpers.oriPhi()
    detector, detector2 = imagingSetup()


def getObjectPosition(oname, fromname = None):
    global clientID
    res, t = vrep.simxGetObjectHandle(clientID, oname, vrep.simx_opmode_oneshot_wait)
    res, pos = vrep.simxGetObjectPosition(clientID, t, -1, vrep.simx_opmode_oneshot_wait)
    if (fromname):
        res, f = vrep.simxGetObjectHandle(clientID, fromname, vrep.simx_opmode_oneshot_wait)
        res, posf = vrep.simxGetObjectPosition(clientID, f, -1, vrep.simx_opmode_oneshot_wait)
        pos = [pos[0] - posf[0], pos[1] - posf[1], pos[2] - posf[2]]
    return pos


def getObjectOrientation(oname, fromname = None):
    global clientID
    res, t = vrep.simxGetObjectHandle(clientID, oname, vrep.simx_opmode_oneshot_wait)
    res, ori = vrep.simxGetObjectOrientation(clientID, t, -1, vrep.simx_opmode_oneshot_wait)
    if (fromname):
        res, f = vrep.simxGetObjectHandle(clientID, fromname, vrep.simx_opmode_oneshot_wait)
        res, orif = vrep.simxGetObjectOrientation(clientID, f, -1, vrep.simx_opmode_oneshot_wait)
        ori = [ori[0] - orif[0], ori[1] - orif[1], ori[2] - orif[2]]
    return ori


def start():
    global clientID
    global wheels
    vrep.simxReadStringStream(clientID, "test", vrep.simx_opmode_streaming)
    print("Waiting for response, please be patient ...")
    res, state = vrep.simxGetInMessageInfo(clientID, 17)
    while (res == -1):
        res, state = vrep.simxGetInMessageInfo(clientID, 17)
    if (state == 5 or state == 7):
        print("simulation is already running. stopping simulation ...")
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
        time.sleep(5.5)
    print("starting simulation ...")
    vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)
    time.sleep(1)
    wheelJoints = Helpers.getObjectHandles(clientID, ['rollingJoint_fl', 'rollingJoint_rl', 'rollingJoint_rr', 'rollingJoint_fr'])
    Helpers.setWheelVelocity(wheelJoints, clientID)
    time.sleep(1)


def quit():
    global clientID
    global wheels   
    for i in range(0, 3):
        vrep.simxSetJointTargetVelocity(clientID, wheels[i], 0, vrep.simx_opmode_oneshot)
    vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)


def main():
    global clientID
    print('Program started')
    vrep.simxFinish(-1)
    clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 2000, 5)
    if clientID != -1:
        print('The connection to the remote API server successful!')
        start()
        sim()
        quit()
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_blocking)
        vrep.simxFinish(clientID)
    else:
        print('The connection to the remote API server failed!')
    print('Program ended')

if __name__ == "__main__": main()
