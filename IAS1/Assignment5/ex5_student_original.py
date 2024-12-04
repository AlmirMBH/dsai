import vrep
import numpy as np
import time
import math

import matplotlib.pyplot as plt

# Robot Geometry
diameter = 0.1  # Diameter of the wheels in m
perimeter = math.pi * diameter  # Perimeter of the wheels in m
wheelDistanceVer = 0.471  # Vertical distance between the wheels
wheelDistanceHor = 0.30046  # Horizontal distance between the wheels

# Robots global position
xPos = 0.0
yPos = 0.0
angle = 0.0

# Global variable that contains positions of all detected obstacles
Obstacles = []


def odometry(angleR, distanceR):
    """ Function for odometry calculation (based on current pose and desired difference in angle and distance, estimate
        the next pose)
        Input arguments:
            angleR - Difference in orientation applied on the robot
            distanceR - Difference in position applied on the robot """

    global xPos
    global yPos
    global angle

    # INSERT YOUR CODE HERE
    # Note: Function implemented in Exercise 4


def checkPose(clientID):
    """ Function used to get the global pose from the simulator
        Input arguments:
            clientID
        Output arguments:
            base_pos - Current position of the robot retrieved from the simulator
            base_orient - Current orientation of the robot retrieved from the simulator """

    global xPos
    global yPos
    global angle

    # INSERT YOUR CODE HERE
    # Note: Function implemented in Exercise 4


def wheelVel(forwBackVel, leftRightVel, rotVel):
    """ Function that sets velocity for individual wheels
        Input arguments:
            forwBackVel - Forward/backward velocity
            leftRightVel - Left/Right velocity
            rotVel - Angular velocity
        Output arguments:
            [frontLeft, rearLeft, rearRight, frontRight] - (numpy array) Calculated velocities for individual wheels """

    # INSERT YOUR CODE HERE
    # Note: Function implemented in Exercise 2


def moveForward(clientID, wheelJoints, distanceMeter, speed):
    """ Function for linear movement of the robot
        Input arguments:
            clientID
            wheelJoints - Handles for the wheel joints
            distanceMeter - Distance in meters """

    # INSERT YOUR CODE HERE
    # Note: Function implemented in Exercise 2


def rotateRobot(clientID, wheelJoints, angle, speed):
    """ Function that implements rotation of the robot
        Input arguments:
            angle - Desired angle for rotation of the robot (in radians)
            clientID
            wheelJoints - Wheel joints handles """

    # INSERT YOUR CODE HERE
    # Note: Function implemented in Exercise 2


def getDistance(auxD, n):
    """ Function returns distance measurement from the n-th laser beam
        Input parameters:
            auxD - All readings from the Hokuyo sensor
            n - Index of the desired laser beam
        Output parameters:
            Distance (sensor reading) from the n-th laser beam
        Note: Actual distance measurements are stored in the auxD[1] list """

    # INSERT YOUR CODE HERE
    # Hint: Distance measured from the n-th laser beam can be calculated using the following formula: auxD[1][4*n + 5]


def getLeftFrontRightDistances(auxD1, auxD2):
    """ Function calculates left, front and right distances from Hokuyo1 and hokuyo2 sensors
        Input arguments:
            auxD1 - Sensor readings from the right sensor (Hokuyo 1)
            auxD2 - Sensor readings from the left sensor (Hokuyo 2)
        Output arguments:
            leftDistance - Measured distance from the left side of the vehicle
            frontDistance - Measured distance from the front of the vehicle
            rightDistance - Measured distance from the right side of the vehicle """

    # INSERT YOUR CODE HERE
    # Hint: Front distance can be obtained by retrieveing measurement from the last index of Hokuyo 1 or..
    # .. from the first index of Hokuyo 2
    # Hint: Right distance can be obtained from Hokuyo 1 sensor on the index: (lastIndex * (30/120))
    # Hint: Left distance can be obtained from Hokuyo 2 sensor on the index: (lastIndex * (90/120))


def printDistances(leftDistance, frontDistance, rightDistance):
    """ Prints distances from the obstacles around the robot
        Input arguments:
            leftDistance - Measured distance from the left side of the vehicle
            frontDistance - Measured distance from the front of the vehicle
            rightDistance - Measured distance from the right side of the vehicle """

    print("Distance Left: " + str(leftDistance))
    print("Distance Front: " + str(frontDistance))
    print("Distance Right: " + str(rightDistance) + "\n")


def obstacleDetection(auxD1):
    """ Function used to define obstacles from the distance measurements
        Input arguments:
            auxD1 - Sensor readings from Hokuyo 1
        Output arguments:
            None
        Note: Function stores obstacle information into a global variable 'Obstacles' """

    global xPos
    global yPos
    global angle
    global Obstacles

    # INSERT YOUR CODE HERE
    # Hint: Use the front distance to detect obstacles
    # Hint: Store obstacles only if distance is less than 5 meters
    # Hint: Store (x, y) coordinates of the detected obstacle into global variable 'Obstacles'


def main():

    global Obstacles

    # Connect to coppeliasim
    print('\nProgram started\n')
    vrep.simxFinish(-1)
    clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 3000, 5)

    if clientID != -1:

        print('Connected to remote API server')

        emptyBuff = bytearray()

        # Start the simulation:
        vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)

        # Initiaize robot and retrieve wheel joint handles
        wheelJoints = np.empty(4, dtype=int);
        wheelJoints.fill(-1)  # front left, rear left, rear right, front right
        res, wheelJoints[0] = vrep.simxGetObjectHandle(clientID, 'rollingJoint_fl', vrep.simx_opmode_oneshot_wait)
        res, wheelJoints[1] = vrep.simxGetObjectHandle(clientID, 'rollingJoint_rl', vrep.simx_opmode_oneshot_wait)
        res, wheelJoints[2] = vrep.simxGetObjectHandle(clientID, 'rollingJoint_rr', vrep.simx_opmode_oneshot_wait)
        res, wheelJoints[3] = vrep.simxGetObjectHandle(clientID, 'rollingJoint_fr', vrep.simx_opmode_oneshot_wait)

        # Set wheel velocities to 0
        for i in range(0, 4):
            vrep.simxSetJointTargetVelocity(clientID, wheelJoints[i], 0, vrep.simx_opmode_oneshot)

        ################################################################################################################

        time.sleep(1)

        # Initialize Hokuyo sensors

        # INSERT YOUR CODE HERE
        # Note: Functions can be found in the materials for Exercise 5

        # Locates free space around the robot
        lastValue = int(len(auxD1[1]) / 4) - 1
        middleValue = int(lastValue // 2)

        left, front, right = getLeftFrontRightDistances(auxD1, auxD2)
        printDistances(left, front, right)

        pos, orient = checkPose(clientID)
        print(str(pos))
        print(str(orient))

        # Move backwards 1 meter
        moveForward(-1, 5, clientID, wheelJoints)
        odometry(0, -1)

        pos, orient = checkPose(clientID)
        print(str(pos))
        print(str(orient))

        print("\nRead sensors\n")
        res1, aux1, auxD1 = vrep.simxReadVisionSensor(clientID, hokuyo1, vrep.simx_opmode_buffer)
        res2, aux2, auxD2 = vrep.simxReadVisionSensor(clientID, hokuyo2, vrep.simx_opmode_buffer)
        time.sleep(1)

        left, front, right = getLeftFrontRightDistances(auxD1, auxD2)
        printDistances(left, front, right)

        # Rotate 3.6 deg 100 times and read data from sensor about the obstacle in front of the robot
        for i in range(0, 100):

            rotateRobot(3.6, 5, clientID, wheelJoints)
            odometry(0.01, 0)

            print("\nRead sensors\n")
            res1, aux1, auxD1 = vrep.simxReadVisionSensor(clientID, hokuyo1, vrep.simx_opmode_buffer)
            res2, aux2, auxD2 = vrep.simxReadVisionSensor(clientID, hokuyo2, vrep.simx_opmode_buffer)

            obstacleDetection(auxD1)
            left, front, right = getLeftFrontRightDistances(auxD1, auxD2)
            printDistances(left, front, right)

        pos, orient = checkPose(clientID)

        print(str(pos))
        print(str(orient))

        x = []
        y = []
        for obstacle_x, obstacle_y in Obstacles:
            x.append(obstacle_x)
            y.append(obstacle_y)

        print(Obstacles)

        # Plotting points on a graph
        plt.plot(x, y, 'ko')
        plt.plot(xPos, yPos, 'r*')
        plt.show()

        ################################################################################################################

        # Stop simulation:
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)

        # Close the connection to V-REP:
        vrep.simxFinish(clientID)

    else:
        print('Failed connecting to remote API server')

    print('Program ended')


if __name__ == "__main__": main()
