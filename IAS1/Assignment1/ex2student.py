#import required libraries
import vrep
import numpy as np
import time
import math

# Robot Geometry
diameter         = 0.1                 # Diameter of the wheels in m
perimeter        = math.pi * diameter  # Perimeter of the wheels in m
wheelDistanceVer = 0.471               # Vertical distance between the wheels
wheelDistanceHor = 0.30046             # Horizontal distance between the wheels


def moveForward(distance, speed, clientID, wheelJoints):
    correctionFactor = 1.045

    # set wheels velocity to 0
# INSERT YOUR CODE HERE

    # calculate velocity for each wheel
# INSERT YOUR CODE HERE (hint: call wheelVel function and pause communication)
    
    # set wheel velocity to calculated values
# INSERT YOUR CODE HERE (hint: pause communication in the end)

    # keep the velocity for the required amount of time
# INSERT YOUR CODE HERE

    # set wheels velocity to 0
# INSERT YOUR CODE HERE

def turnRight(degree, speed, clientID, wheelJoints):

    # set wheel velocity to 0
# INSERT YOUR CODE HERE
    
    # calculate velocity for each wheel
# INSERT YOUR CODE HERE
    
    # set wheel velocity to calculated values
# INSERT YOUR CODE HERE
    
    # keep the velocity for the required amount of time
# INSERT YOUR CODE HERE

    # set wheel velocity to 0
# INSERT YOUR CODE HERE

def wheelVel(forwBackVel, leftRightVel, rotVel):
    # set individual wheel velocities
# INSERT YOUR CODE HERE


def main():
    # connect to coppeliasim
    print ('Program started')
    vrep.simxFinish(-1) 
    clientID=vrep.simxStart('127.0.0.1',19997,True,True, 2000,5)
    if clientID!=-1:
        print ('Connected to remote API server')

        emptyBuff = bytearray()

        # Start the simulation:
#INSERT YOUR CODE HERE

        # initiaize robot
        # Retrieve wheel joint handles:
        wheelJoints=np.empty(4, dtype=int); wheelJoints.fill(-1) #front left, rear left, rear right, front right
#INSERT YOUR CODE HERE
        res,wheelJoints[0]=
        res,wheelJoints[1]=
        res,wheelJoints[2]=
        res,wheelJoints[3]=
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
#INSERT YOUR CODE HERE

#INSERT YOUR CODE HERE (for the main loop to form a square)

#INSERT YOUR CODE HERE
        # Pause communication, Stop simulation, Close the connection to V-REP
	# Ako ne uspije zatvaranje ispiši 'Failed connecting to remote API server'
	# na samom kraju ispiši 'Program ended'

if __name__ == "__main__": main()
