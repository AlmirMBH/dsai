import vrep
import math
import time
from shared_methods import SharedMethods
from shared_methods import OnTarget

# Robot Geometry
diameter         = 0.1                 # Diameter of the wheels in m
perimeter        = math.pi * diameter  # Perimeter of the wheels in m
wheelDistanceVer = 0.471               # Vertical distance between the wheels
wheelDistanceHor = 0.30046             # Horizontal distance between the wheels
WHEEL_DIAMETER = 0.1 # wheel diameter [m]
TOLERANCE = 0.1 # odometry calculation tolerance
dt = 0.001 # intervall for movement
speed = 5
numberOfLasers = 342
sensorCoverageAngle = 120
message = "You reached the target destination!!!"
mode_streaming = vrep.simx_opmode_streaming
mode_buffering = vrep.simx_opmode_buffer
youBot_center = "youBot_center"


def getGoalDirection(clientID, goalPosition):
    youbotPosition, youbotOrientation = SharedMethods.getObjectPositionAndOrientation(clientID, youBot_center)
    goalDirection = math.atan2(youbotPosition[1][1]-goalPosition[1], youbotPosition[1][0]-goalPosition[0])
    return SharedMethods.adjustAngle(goalDirection)


def findGoalDirection(clientID, goalPosition, wheelJoints):
    goalDirection = getGoalDirection(clientID, goalPosition)
    SharedMethods.rotateRobot(clientID, wheelJoints, speed)
    while True:
        youbotPosition, youbotOrientation = SharedMethods.getObjectPositionAndOrientation(clientID, youBot_center)
        if abs(youbotOrientation[1][2] - goalDirection) < TOLERANCE:
            SharedMethods.setWheelVelocity(wheelJoints, clientID)
            break
        time.sleep(dt)


def directToObstacle(clientID, wheelJoints, hokuyoRight):
    youbotPosition, youbotOrientation = SharedMethods.getObjectPositionAndOrientation(clientID, youBot_center)
    auxD1 =  SharedMethods.getVisionSensor(clientID, [hokuyoRight], mode_buffering)
    distanceRight = auxD1[1][4 * int((30 / sensorCoverageAngle) * numberOfLasers) + 5]
    distanceFront = auxD1[1][4 * (len(auxD1[1]) // 4 - 1) + 5]
    alpha = math.atan2(distanceRight, distanceFront) # angle towards wall
    theta = (alpha) + SharedMethods.transformAngle(youbotOrientation[1][2])
    theta = SharedMethods.adjustAngle(theta)
    SharedMethods.rotateRobot(clientID, wheelJoints, speed)
    while True:
        youbotPosition, youbotOrientation = SharedMethods.getObjectPositionAndOrientation(clientID, youBot_center)
        if abs(youbotOrientation[1][2] - theta) < TOLERANCE:
            SharedMethods.setWheelVelocity(wheelJoints, clientID)
            break
        time.sleep(dt)


def moveAlongWall(clientID, wheelJoints, hokuyoRight):
    directToObstacle(clientID, wheelJoints, hokuyoRight)
    SharedMethods.moveForward(clientID, wheelJoints, speed)
    while True:
        auxD1 = SharedMethods.getVisionSensor(clientID, [hokuyoRight], mode_buffering)
        distanceRight = SharedMethods.getDistance(auxD1, 5)
        distanceFront = SharedMethods.getDistance(auxD1, 5)
        if distanceRight > 1.5:
            SharedMethods.setWheelVelocity(wheelJoints, clientID)
            break
        if distanceFront < 0.5 or distanceRight < 0.2:
            SharedMethods.setWheelVelocity(wheelJoints, clientID) # stop, direct, move
            directToObstacle(clientID, wheelJoints, hokuyoRight)
            SharedMethods.moveForward(clientID, wheelJoints, speed)
        time.sleep(dt)


def getToGoal(clientID, goalPosition, wheelJoints, hokuyoRight):
    findGoalDirection(clientID, goalPosition, wheelJoints)
    SharedMethods.moveForward(clientID, wheelJoints, speed)
    while True:
        youbotPosition, youbotOrientation = SharedMethods.getObjectPositionAndOrientation(clientID, youBot_center)
        print("Position:", youbotPosition, "Orientation:", youbotOrientation)
        auxD1 = SharedMethods.getVisionSensor(clientID, [hokuyoRight], mode_buffering)
        if abs(youbotPosition[1][0] - goalPosition[0]) < TOLERANCE and abs(youbotPosition[1][1] - goalPosition[1]) < TOLERANCE:
            SharedMethods.setWheelVelocity(wheelJoints, clientID)
            vrep.simxGetPingTime(clientID)
            SharedMethods.stopCoppelia(clientID) # goal reached turn off coppelia and stop the robot
            raise OnTarget("Your journey has come to an end!!!")
        distanceFront = SharedMethods.getDistance(auxD1, len(auxD1[1]) // 4 - 1)
        if distanceFront < 0.5:
            SharedMethods.setWheelVelocity(wheelJoints, clientID)
            break


def directToGoal(clientID, goalPosition, wheelJoints, hokuyoRight):
    while True:
        getToGoal(clientID, goalPosition, wheelJoints, hokuyoRight)
        moveAlongWall(clientID, wheelJoints, hokuyoRight)


def main():
    clientID = SharedMethods.startSimulation()
    if clientID is None or clientID < 0:
        print("Connection to the remote API server failed! Re-open CoppeliaSim, load the movement.ttt and run this script again.")
        return
    
    wheelJoints = SharedMethods.getObjectHandles(clientID, ['rollingJoint_fl', 'rollingJoint_rl', 'rollingJoint_rr', 'rollingJoint_fr'])
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    time.sleep(1)
    SharedMethods.setIntegerSignal(clientID, "handle_xy_sensor", 2)
    SharedMethods.setIntegerSignal(clientID, "displaylasers", 1)

    handles = SharedMethods.getObjectHandles(clientID, ["fastHokuyo_sensor1", "fastHokuyo_sensor2"])
    hokuyoRight = handles[0]
    hokuyoLeft = handles[1]
    auxD1, auxD2 = SharedMethods.getVisionSensor(clientID, [hokuyoRight, hokuyoLeft], mode_streaming)

    youbotPosition, youbotOrientation = SharedMethods.getObjectPositionAndOrientation(clientID, youBot_center)
    angle = youbotOrientation[1][2]
    time.sleep(1)
    
    try:
        goalHandle = SharedMethods.getObjectHandles(clientID, ["Goal"])
        res, goalPosition = SharedMethods.getObjectPosition(clientID, goalHandle, mode_streaming)
        time.sleep(0.05)
        res, goalPosition = SharedMethods.getObjectPosition(clientID, goalHandle, mode_buffering)
        auxD1, auxD2 = SharedMethods.getVisionSensor(clientID, [hokuyoRight, hokuyoLeft], mode_buffering)
        directToGoal(clientID, goalPosition, wheelJoints, hokuyoRight)
    except OnTarget as e:
        print("Goal position:", goalPosition)
        print("Robot position:", youbotPosition[1])
        print("The following exception occured:", e.message)

    SharedMethods.stopCoppelia(clientID)


if __name__ == "__main__":
    main()
