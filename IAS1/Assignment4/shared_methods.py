import numpy as np
import time
import vrep

class SharedMethods:
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
        else:
            return False


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


    def getObjectPosition(clientID, handle, mode):
        if mode == 'buffer': mode = vrep.simx_opmode_buffer
        else: mode = vrep.simx_opmode_streaming

        return vrep.simxGetObjectPosition(clientID, handle, -1, mode)


    def getObjectOrientation(clientID, handle, mode):
        if mode == 'buffer': mode = vrep.simx_opmode_buffer
        else: mode = vrep.simx_opmode_streaming

        return vrep.simxGetObjectOrientation(clientID, handle, -1, mode)

    def setWheelVelocity(wheelJoints, clientID, wheelVelocities = None, pause = None):
        if wheelVelocities is None:
            wheelVelocities = [0, 0, 0, 0]

        for i, wheelJoint in enumerate(wheelJoints):
                vrep.simxSetJointTargetVelocity(clientID, wheelJoint, wheelVelocities[i], vrep.simx_opmode_oneshot)
                if pause:
                    time.sleep(pause)


    def pauseCommunication(clientID, pauseStatus):
        vrep.simxPauseCommunication(clientID, pauseStatus)


    def calculateWheelVelocities(forwBackVel, leftRightVel, rotVel):
        frontLeft = forwBackVel - leftRightVel - rotVel
        rearLeft = forwBackVel - leftRightVel - rotVel
        rearRight = forwBackVel + leftRightVel + rotVel
        frontRight = forwBackVel + leftRightVel + rotVel
        return np.array([frontLeft, rearLeft, rearRight, frontRight])
    