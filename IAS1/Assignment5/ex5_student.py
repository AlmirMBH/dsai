import vrep
import numpy as np
import time
import math
import matplotlib.pyplot as plt
from shared_methods import SharedMethods

# Robot Geometry
diameter = 0.1  # Diameter of the wheels in m
perimeter = math.pi * diameter  # Perimeter of the wheels in m
wheelDistanceVer = 0.471  # Vertical distance between the wheels
wheelDistanceHor = 0.30046  # Horizontal distance between the wheels
Obstacles = [] # Global variable that contains positions of all detected obstacles
# Robots global position
xPos = 0.0
yPos = 0.0
angle = 0.0
streaming = "straming"
buffering = "buffering"
obstacle_distance = 5 # 5 meters
laser_341 = 341


def odometry(angleR, distanceR):
    global xPos
    global yPos
    global angle
    angle += angleR
    angle = (angle + math.pi) % (2 * math.pi) - math.pi
    if angleR < 0:
        xPos += distanceR * math.cos(angle)
        yPos += distanceR * math.sin(angle)
    elif angleR > 0:
        xPos -= distanceR * math.cos(angle)
        yPos -= distanceR * math.sin(angle)
    else:
        xPos += distanceR * math.cos(angle)
        yPos += distanceR * -math.sin(angle)


def checkPose(clientID):
    handle = SharedMethods.getObjectHandles(clientID, ['youBot_center'])
    res, base_position = SharedMethods.getObjectPosition(clientID, handle, streaming)
    res, base_orientation = SharedMethods.getObjectOrientation(clientID, handle, streaming)
    time.sleep(0.1)
    res, base_position = SharedMethods.getObjectPosition(clientID, handle, buffering)
    res, base_orientation = SharedMethods.getObjectOrientation(clientID, handle, buffering)
    base_position = (res, base_position)
    base_orientation = (res, base_orientation)
    return base_position, base_orientation


def moveForward(distance, speed, clientID, wheelJoints):
    correctionFactor = 1.045    
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    wheel_velocities = SharedMethods.calculateWheelVelocities(speed, 0, 0)
    SharedMethods.pauseCommunication(clientID, True)
    SharedMethods.setWheelVelocity(wheelJoints, clientID, wheel_velocities)
    SharedMethods.pauseCommunication(clientID, False)
    required_pause = (distance/perimeter) * ((2 * math.pi)/speed) * correctionFactor
    time.sleep(abs(required_pause))
    SharedMethods.setWheelVelocity(wheelJoints, clientID)


def rotateRobot(angle, speed, clientID, wheelJoints):
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    wheel_velocities = SharedMethods.calculateWheelVelocities(0, 0, speed)
    SharedMethods.pauseCommunication(clientID, True)
    SharedMethods.setWheelVelocity(wheelJoints, clientID, wheel_velocities)
    SharedMethods.pauseCommunication(clientID, False)
    required_pause = (wheelDistanceVer + wheelDistanceHor)/perimeter * math.pi * angle/abs(speed) * math.pi/180
    time.sleep(required_pause)
    SharedMethods.setWheelVelocity(wheelJoints, clientID)


def getDistance(auxD, n):
    return auxD[4*n + 5]


def getLeftFrontRightDistances(auxD1, auxD2):
    """ Function calculates left, front and right distances from Hokuyo1 and hokuyo2 sensors
        Input arguments:
            auxD1 - Sensor readings from the right sensor (Hokuyo 1)
            auxD2 - Sensor readings from the left sensor (Hokuyo 2)
        Output arguments:
            leftDistance - Measured distance from the left side of the vehicle
            frontDistance - Measured distance from the front of the vehicle
            rightDistance - Measured distance from the right side of the vehicle 
        Front distance: can be obtained by retrieveing measurement from the last index of Hokuyo 1 or
        from the first index of Hokuyo 2
        Right distance: can be obtained from Hokuyo 1 sensor on the index: (lastIndex * (30/120))
        Left distance: can be obtained from Hokuyo 2 sensor on the index: (lastIndex * (90/120))"""
    left = getDistance(auxD2[1], laser_341) * (90/120)
    front = getDistance(auxD1[1], laser_341)
    right = getDistance(auxD1[1], laser_341) * (30/120)
    return left, front, right
    

def printDistances(leftDistance, frontDistance, rightDistance):
    print("Distance Left: " + str(leftDistance))
    print("Distance Front: " + str(frontDistance))
    print("Distance Right: " + str(rightDistance) + "\n")


def obstacleDetection(auxD1):
    """ Function used to define obstacles from the distance measurements
        Input arguments: auxD1 - Sensor readings from Hokuyo 1
        Output arguments: None
        Note: Function stores obstacle information into a global variable 'Obstacles'
        Use the front distance to detect obstacles
        Store obstacles only if distance is less than 5 meters
        Store (x, y) coordinates of the detected obstacle into global variable 'Obstacles'"""
    global xPos
    global yPos
    global angle
    global Obstacles
    if getDistance(auxD1[1], laser_341) < obstacle_distance:
        distance = getDistance(auxD1[1], laser_341)
        Obstacles.append((distance * math.cos(angle), distance * math.sin(angle)))


# Rotate 3.6 deg 100 times and read data from sensor about the obstacle in front of the robot
def readSensors(clientID, hokuyo1, hokuyo2, wheelJoints):
        for i in range(0, 100):
            rotation_radians = 3.6 * (math.pi / 180)  # Convert 3.6 degrees to radians
            rotateRobot(3.6, 5, clientID, wheelJoints)
            odometry(rotation_radians, 0)
            print("\nRead sensors\n")
            auxD1, auxD2 = SharedMethods.getVisionSensor(clientID, [hokuyo1, hokuyo2], buffering)
            obstacleDetection(auxD1)
            left, front, right = getLeftFrontRightDistances(auxD1, auxD2)
            printDistances(left, front, right)


def main():
    global Obstacles
    clientID = SharedMethods.startSimulation()
    if clientID < 0:
        print("Connection to the remote API server failed! Re-open CoppeliaSim, load the movement.ttt and run this script again.")
        return

    # Start simulation, fetch wheel joints, set the speed to 0
    vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)
    wheelJoints = SharedMethods.getObjectHandles(clientID, ['rollingJoint_fl', 'rollingJoint_rl', 'rollingJoint_rr', 'rollingJoint_fr'])
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    time.sleep(1)

    # Set and get laser handles
    SharedMethods.setIntegerSignal(clientID, "handle_xy_sensor", 2)
    SharedMethods.setIntegerSignal(clientID, "displaylasers", 1)
    handles = SharedMethods.getObjectHandles(clientID, ["fastHokuyo_sensor1", "fastHokuyo_sensor2"])
    hokuyo1 = handles[0]
    hokuyo2 = handles[1]

    # Initialize sensors, move robot and print distances
    for mode in [streaming, buffering]:
        print("Initializing sensors" if mode == streaming else "Reading sensors")
        auxD1, auxD2 = SharedMethods.getVisionSensor(clientID, [hokuyo1, hokuyo2], mode)
        time.sleep(1)
    
    left, front, right = getLeftFrontRightDistances(auxD1, auxD2)
    printDistances(left, front, right)
    pos, orient = checkPose(clientID)
    print(str(pos), str(orient))
    moveForward(-1, 5, clientID, wheelJoints) # Move backwards 1 meter
    odometry(0, -1)
    pos, orient = checkPose(clientID)
    print(str(pos), str(orient), "\nRead sensors\n")
    time.sleep(1)
    left, front, right = getLeftFrontRightDistances(auxD1, auxD2)
    printDistances(left, front, right)
    readSensors(clientID, hokuyo1, hokuyo2, wheelJoints) # make a full robot rotation

    pos, orient = checkPose(clientID)
    print(str(pos))
    print(str(orient))

    x = []
    y = []
    for obstacle_x, obstacle_y in Obstacles:
        x.append(obstacle_x)
        y.append(obstacle_y)

    print("OBSTACLES !@#!!#", Obstacles)

    # Plotting points on a graph
    plt.plot(x, y, 'ko')
    plt.plot(xPos, yPos, 'r*')
    plt.show()

    SharedMethods.pauseCommunication(clientID, True)
    vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
    SharedMethods.pauseCommunication(clientID, False)
    SharedMethods.closeServerCommunication(clientID)
    print('Program ended')


if __name__ == "__main__": main()
