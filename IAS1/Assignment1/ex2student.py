#import required libraries
import vrep
import numpy as np
import time
import math
# Command to run
# C:\Users\root\AppData\Local\Microsoft\WindowsApps\python.exe .\ex2student.py
# Robot Geometry
diameter         = 0.1                 # Diameter of the wheels in m
perimeter        = math.pi * diameter  # Perimeter of the wheels in m
wheelDistanceVer = 0.471               # Vertical distance between the wheels
wheelDistanceHor = 0.30046             # Horizontal distance between the wheels


def setWheelVelocityToZero(wheelJoints, clientID):
    for wheel in wheelJoints:
        vrep.simxSetJointTargetVelocity(clientID, wheel, 0, vrep.simx_opmode_oneshot)


def controlCommunication(clientID, pauseStatus):
    vrep.simxPauseCommunication(clientID, pauseStatus)


def moveForward(distance, speed, clientID, wheelJoints):
    correctionFactor = 1.045

    # set wheels velocity to 0
    setWheelVelocityToZero(wheelJoints, clientID)

    # calculate velocity for each wheel (hint: call wheelVel function and pause communication)
    wheel_speeds = wheelVel(speed, 0, 0)
    controlCommunication(clientID, True)

    # set wheel velocity to calculated values (hint: pause communication in the end)
    for i in range(4):
        vrep.simxSetJointTargetVelocity(clientID, wheelJoints[i], wheel_speeds[i], vrep.simx_opmode_oneshot)

    controlCommunication(clientID, False)  
    required_sleep_time = (distance/perimeter) * (2*math.pi/speed) * correctionFactor
    time.sleep(required_sleep_time)

    # set wheels velocity to 0
    setWheelVelocityToZero(wheelJoints, clientID)


def turnRight(degree, speed, clientID, wheelJoints):
    # set wheel velocity to 0
    setWheelVelocityToZero(wheelJoints, clientID) 
    
    # calculate velocity for each wheel
    wheel_speeds = wheelVel(0, 0, speed)
    controlCommunication(clientID, True)

    # set wheel velocity to calculated values
    for i in range(4):
        vrep.simxSetJointTargetVelocity(clientID, wheelJoints[i], wheel_speeds[i], vrep.simx_opmode_oneshot)

    controlCommunication(clientID, False)
    
    # keep the velocity for the required amount of time
    time_required = (wheelDistanceVer + wheelDistanceHor)/perimeter * math.pi * degree/abs(speed) * math.pi/180
    time.sleep(time_required)

    # set wheel velocity to 0
    setWheelVelocityToZero(wheelJoints, clientID)     


def wheelVel(forwBackVel , leftRightVel , rotVel):
    frontLeft = forwBackVel - leftRightVel - rotVel
    rearLeft = forwBackVel - leftRightVel - rotVel
    rearRight = forwBackVel + leftRightVel + rotVel
    frontRight = forwBackVel + leftRightVel + rotVel
    return np.array([frontLeft, rearLeft, rearRight, frontRight])


def main():
    # connect to coppeliasim
    print ('Program started')
    vrep.simxFinish(-1) 
    clientID=vrep.simxStart('127.0.0.1',19997,True,True, 2000,5)

    if clientID!=-1:
        print ('Connected to remote API server')
        emptyBuff = bytearray()

        # Start the simulation:
        vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)

        # initiaize robot
        # Retrieve wheel joint handles:
        wheelJoints = np.empty(4, dtype=int)
        wheelJoints.fill(-1)  # front left, rear left, rear right, front right
        joint_names = ['rollingJoint_fl', 'rollingJoint_rl', 'rollingJoint_rr', 'rollingJoint_fr']

        for i, joint_name in enumerate(joint_names):
            res, wheelJoints[i] = vrep.simxGetObjectHandle(clientID, joint_name, vrep.simx_opmode_oneshot_wait)

        armJointsHandle = [0] * 5
        
        #--------------------------------------------------arm------------------------------------------------------------------
        # Retrieve arm joint handles
        for i in range(0, 5):
            res,armJointsHandle[i] = vrep.simxGetObjectHandle(clientID, 'youBotArmJoint%d' % i, vrep.simx_opmode_oneshot_wait)
        
        # Move the third joint of the arm four times
        for i in range(0, 4):
            res = vrep.simxSetJointTargetPosition(clientID, armJointsHandle[2], i*math.pi/8, vrep.simx_opmode_oneshot)
            time.sleep(1)
        #-----------------------------------------------------------------------------------------------------------------------
        
        # set wheel velocity to 0
        setWheelVelocityToZero(wheelJoints, clientID)

        #INSERT YOUR CODE HERE (for the main loop to form a square)
        for _ in range(4):
            moveForward(1, 5, clientID, wheelJoints)
            turnRight(90, 5, clientID, wheelJoints)

     # Pause communication, Stop simulation, Close the connection to V-REP
	 # Ako ne uspije zatvaranje ispiši 'Failed connecting to remote API server'
	 # na samom kraju ispiši 'Program ended'

        controlCommunication(clientID, False)
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
        vrep.simxFinish(clientID)
    else:
        print("Connection to the remote API server failed! Re-open CoppeliaSim, load the movement.ttt and run this script again.")
    print("Program ended")

if __name__ == "__main__": main()
