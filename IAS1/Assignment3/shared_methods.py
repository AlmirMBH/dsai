import numpy as np
import time
import math
import vrep
import time


# Robot Geometry
diameter         = 0.1                 # Diameter of the wheels in m
perimeter        = math.pi * diameter  # Perimeter of the wheels in m
wheelDistanceVer = 0.471               # Vertical distance between the wheels
wheelDistanceHor = 0.30046             # Horizontal distance between the wheels
correctionFactor = 2


class SharedMethods:
    def startSimulation():
        print("Program started")
        SharedMethods.closeServerCommunication(-1)
        clientID = vrep.simxStart("127.0.0.1", 19997, True, True, 2000, 5)

        if clientID != -1:
            print("Connected to remote API server")
            res = vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)

            if res != vrep.simx_return_ok:
                print("Failed to start simulation")
                return
            
            return clientID
        else:
            print("Connection to the remote API server failed! Re-open CoppeliaSim, load the movement.ttt and run this script again.")


    def closeServerCommunication(clientID):
        vrep.simxFinish(clientID)


    def getObjectHandles(clientID, handles):
        wheelJoints = []

        for joint_name in handles:
                res, joint_handle = vrep.simxGetObjectHandle(clientID, joint_name, vrep.simx_opmode_oneshot_wait)
                wheelJoints.append(joint_handle)

        return wheelJoints


    def setWheelVelocity(wheelJoints, clientID, wheelVelocities = None, pause = None):
        if wheelVelocities is None:
            wheelVelocities = [0, 0, 0, 0]

        for i, wheelJoint in enumerate(wheelJoints):
                vrep.simxSetJointTargetVelocity(clientID, wheelJoint, wheelVelocities[i], vrep.simx_opmode_oneshot)
                if pause:
                    time.sleep(pause)


    def pauseCommunication(clientID, pauseStatus):
        vrep.simxPauseCommunication(clientID, pauseStatus)

    
    def moveForward(distance, speed, clientID, wheelJoints):
        SharedMethods.setWheelVelocity(wheelJoints, clientID)
        wheelVelocities = SharedMethods.wheelVel(speed, 0, 0)
        SharedMethods.pauseCommunication(clientID, True)
        SharedMethods.setWheelVelocity(wheelJoints, clientID, wheelVelocities)
        SharedMethods.pauseCommunication(clientID, False)
        required_sleep_time = (distance/perimeter) * (2*math.pi/speed) * correctionFactor
        time.sleep(required_sleep_time)
        SharedMethods.setWheelVelocity(wheelJoints, clientID)


    def turnRight(degree, speed, clientID, wheelJoints):
        SharedMethods.setWheelVelocity(wheelJoints, clientID)
        wheelVelocities = SharedMethods.wheelVel(0, 0, speed)
        SharedMethods.pauseCommunication(clientID, True)
        SharedMethods.setWheelVelocity(wheelJoints, clientID, wheelVelocities) 
        SharedMethods.pauseCommunication(clientID, False)
        time_required = (wheelDistanceVer + wheelDistanceHor)/perimeter * math.pi * degree/abs(speed) * math.pi/180
        time.sleep(time_required)
        SharedMethods.setWheelVelocity(wheelJoints, clientID)  


    def wheelVel(forwBackVel , leftRightVel , rotVel):
        frontLeft = forwBackVel - leftRightVel - rotVel
        rearLeft = forwBackVel - leftRightVel - rotVel
        rearRight = forwBackVel + leftRightVel + rotVel
        frontRight = forwBackVel + leftRightVel + rotVel
        return np.array([frontLeft, rearLeft, rearRight, frontRight])


    def changeSpeed(side, sideIndex, totalSides, angle, clientID, wheelJoints):
        speedMultiplier = 10
        midpoint = totalSides // 2
        
        if sideIndex <= midpoint:
            speed = speedMultiplier * (sideIndex / midpoint)
        else:
            speed = speedMultiplier * ((totalSides - sideIndex) / midpoint)
        speed = max(speed, 3)
        print("SPEED: " + str(speed))

        SharedMethods.moveForward(side, speed, clientID, wheelJoints)
        SharedMethods.turnRight(angle, 5, clientID, wheelJoints)