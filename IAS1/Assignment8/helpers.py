import vrep
import math
import cv2
import numpy as np
import time

orientationVector = [0.0, -1.0]

class Helpers:
    def setFloatSignal(clientID, signal):
        vrep.simxSetFloatSignal(clientID, signal, math.pi/2, vrep.simx_opmode_oneshot)


    def getObjectHandles(clientID, handleNames):
        handles = []
        for handleName in handleNames:
                res, handle = vrep.simxGetObjectHandle(clientID, handleName, vrep.simx_opmode_oneshot_wait)
                handles.append(handle)
        if (len(handles) > 1): return handles
        else: return handles[0]


    def setWheelVelocity(wheelJoints, clientID, wheelVelocities = None, pause = None):
        if wheelVelocities is None:
            wheelVelocities = [0, 0, 0, 0]

        for i, wheelJoint in enumerate(wheelJoints):
                vrep.simxSetJointTargetVelocity(clientID, wheelJoint, wheelVelocities[i], vrep.simx_opmode_oneshot)
                if pause:
                    time.sleep(pause)

    
    def getVisionSensorImage(clientID, sensorHandle, mode):
         if mode == 'buffering': mode = vrep.simx_opmode_buffer
         else: mode = vrep.simx_opmode_streaming
         ret, res, image  = vrep.simxGetVisionSensorImage(clientID, sensorHandle, 0, mode)
         return ret, res, image
    

    def redBlobExtract(imageBGR):
        lower = np.array([0, 0, 100], dtype=np.uint8)
        upper = np.array([120, 120, 255], dtype=np.uint8)
        return cv2.inRange(imageBGR, lower, upper)


    def blueBlobExtract(imageBGR):
        lower = np.array([100, 0, 0], dtype=np.uint8)
        upper = np.array([255, 120, 120], dtype=np.uint8)
        return cv2.inRange(imageBGR, lower, upper)
    

    def oriPhi():
        phi = 0
        global orientationVector
        if(orientationVector[1] >= 0):
            phi = math.pi
            if(orientationVector[0] >= 0):
                phi = math.asin(orientationVector[0])
            else:
                phi = math.pi / 2 + abs(math.asin(orientationVector[0]))
        else:
            phi = math.pi * 2
            if(orientationVector[0] >= 0):
                phi = math.pi * 2 - abs(math.asin(orientationVector[0]))
            else:
                phi = math.pi + abs(math.asin(orientationVector[0]))
        return phi
