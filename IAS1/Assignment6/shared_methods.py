import numpy as np
import time
import vrep
import math


class CustomError(Exception):
    def __init__(self, message):
        self.message = message


class OnTarget(Exception):
    def __init__(self, message):
        self.message = message


class SharedMethods:
    mode_streaming = vrep.simx_opmode_streaming
    mode_buffering = vrep.simx_opmode_buffer

    def startSimulation():
        print("Program started")
        SharedMethods.closeServerCommunication(-1)
        clientID = vrep.simxStart("127.0.0.1", 19997, True, True, 3000, 5)
        if clientID != -1:
            print("Connected to remote API server")
            res = vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)
            if res != vrep.simx_return_ok:
                print("Failed to start simulation")
                return
            return clientID
        else: return False


    def closeServerCommunication(clientID):
        time.sleep(2)
        vrep.simxFinish(clientID)


    def getObjectHandles(clientID, handleNames):
        handles = []
        for handleName in handleNames:
                res, handle = vrep.simxGetObjectHandle(clientID, handleName, vrep.simx_opmode_oneshot_wait)
                handles.append(handle)
        if (len(handles) > 1): return handles
        else: return handles[0]

    
    def setIntegerSignal(clientID, signalName, signalValue):
         vrep.simxSetIntegerSignal(clientID, signalName, signalValue, vrep.simx_opmode_oneshot)


    def getVisionSensor(clientID, sensors, mode):
        auxD_sensors = []
        for sensor in sensors:
            res1, aux1, sensor_data = vrep.simxReadVisionSensor(clientID, sensor, mode)
            auxD_sensors.append(sensor_data)

        if len(auxD_sensors) > 1: return auxD_sensors[0], auxD_sensors[1]
        else: return auxD_sensors[0]


    def getObjectPosition(clientID, handle, mode):
        return vrep.simxGetObjectPosition(clientID, handle, -1, mode)
    

    def getObjectOrientation(clientID, handle, mode):
        return vrep.simxGetObjectOrientation(clientID, handle, -1, mode)
    

    def getObjectPositionAndOrientation(clientID, handle):
        res, handle = vrep.simxGetObjectHandle(clientID, "youBot_center", vrep.simx_opmode_oneshot_wait)
        res, base_pos = vrep.simxGetObjectPosition(clientID, handle, -1, SharedMethods.mode_streaming)
        res, base_orient = vrep.simxGetObjectOrientation(clientID, handle, -1, SharedMethods.mode_streaming)
        time.sleep(0.05)
        res, base_pos = vrep.simxGetObjectPosition(clientID, handle, -1, SharedMethods.mode_buffering)
        res, base_orient = vrep.simxGetObjectOrientation(clientID, handle, -1, SharedMethods.mode_buffering)
        base_pos = (res, base_pos)
        base_orient = (res, base_orient)
        return base_pos, base_orient


    def pauseCommunication(clientID, pauseStatus):
        vrep.simxPauseCommunication(clientID, pauseStatus)


    def calculateWheelVelocities(forwBackVel, leftRightVel, rotVel):
        frontLeft = forwBackVel - leftRightVel - rotVel
        rearLeft = forwBackVel + leftRightVel - rotVel
        rearRight = forwBackVel + leftRightVel + rotVel
        frontRight = forwBackVel - leftRightVel + rotVel
        return np.array([frontLeft, rearLeft, rearRight, frontRight])


    def setWheelVelocity(wheelJoints, clientID, wheelVelocities = None, pause = None):
        if wheelVelocities is None:
            wheelVelocities = [0, 0, 0, 0]
        for i, wheelJoint in enumerate(wheelJoints):
                vrep.simxSetJointTargetVelocity(clientID, wheelJoint, wheelVelocities[i], vrep.simx_opmode_oneshot)
                if pause:
                    time.sleep(pause)
    

    def rotateRobot(clientID, wheelJoints, speed):
        wheelVelocities = SharedMethods.calculateWheelVelocities(0, 0, -speed)
        SharedMethods.setWheelVelocity(wheelJoints, clientID, wheelVelocities)


    def moveForward(clientID, wheelJoints, speed):
        wheelVelocities = SharedMethods.calculateWheelVelocities(speed * 3, 0, 0)    
        SharedMethods.setWheelVelocity(wheelJoints, clientID, wheelVelocities)
    

    def adjustAngle(angle):
        if 0 <= angle < 3 * math.pi / 2: return angle - math.pi / 2
        if 3 * math.pi / 2 <= angle < 2 * math.pi: return angle - 5 * math.pi / 2
        angle = angle % (2 * math.pi)
        return SharedMethods.adjustAngle(angle)
    

    def transformAngle(theta):        
        if theta < -math.pi or theta > math.pi: raise CustomError("Input angle must be between -π and π!")
        if theta >= -math.pi and theta < -math.pi / 2: return (5*math.pi/2 + theta)
        elif theta >= -math.pi/2 and theta <= math.pi: return (math.pi / 2 + theta)


    def getDistance(auxD, n):
        return auxD[1][4*n + 5]
    

    def stopCoppelia(clientID, message = None):
        if message:
            print(message)

        SharedMethods.pauseCommunication(clientID, True)
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
        SharedMethods.pauseCommunication(clientID, False)
        SharedMethods.closeServerCommunication(clientID)
        print('Program ended')
