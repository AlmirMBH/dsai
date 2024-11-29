import numpy as np
import vrep
import math
import time
from shared_methods import SharedMethods


# Robot Geometry
diameter         = 0.1                 # Diameter of the wheels in m
perimeter        = math.pi * diameter  # Perimeter of the wheels in m
wheelDistanceVer = 0.471               # Vertical distance between the wheels
wheelDistanceHor = 0.30046             # Horizontal distance between the wheels
speed = 5                              # Global variable for speed

# Initial pose of the robot in 2D space (position + orientation): [x, y, alpha (yaw angle)]
xPos = 0
yPos = 0
angle = 0


def moveRobot(clientID, wheelJoints, angle, distance):
    rotateRobot(clientID, wheelJoints, angle)
    straightRobot(clientID, wheelJoints, distance)


def checkPose(clientID):
    handle = SharedMethods.getObjectHandles(clientID, ['youBot_center'])
    res, base_pos = SharedMethods.getObjectPosition(clientID, handle, "streaming")
    res, base_orient = SharedMethods.getObjectOrientation(clientID, handle, "streaming")
    time.sleep(0.1)
    res, base_pos = SharedMethods.getObjectPosition(clientID, handle, "buffer")
    res, base_orient = SharedMethods.getObjectOrientation(clientID, handle, "buffer")
    base_pos = (res, base_pos)
    base_orient = (res, base_orient)
    return base_pos, base_orient


def printPosition(clientID):
    global xPos
    global yPos
    global angle
    pos, orient = checkPose(clientID)
    print("global [PosX, PosY, AngZ]: " + str(np.round(pos[1][0], 5)) + ", " + str(np.round(pos[1][1], 5)) + ", " + str(np.round(orient[1][2], 5)))
    print("local [PosX, PosY, AngZ]: " + str(np.round(xPos, 5)) + ", " + str(np.round(yPos, 5)) + ", " + str(np.round(angle, 5)))


def straightRobot(clientID, wheelJoints, distanceMeter):
    global speed
    correctionFactor = 1.045
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    if distanceMeter >= 0: moving_speed = speed
    else: moving_speed = -speed
    wheel_velocities = SharedMethods.calculateWheelVelocities(moving_speed, 0, 0)
    SharedMethods.pauseCommunication(clientID, True)
    SharedMethods.setWheelVelocity(wheelJoints, clientID, wheel_velocities)
    SharedMethods.pauseCommunication(clientID, False)
    duration = (abs(distanceMeter)/perimeter) * ((2 * math.pi)/speed) * correctionFactor
    time.sleep(duration)
    SharedMethods.setWheelVelocity(wheelJoints, clientID)


def rotateRobot(clientID, wheelJoints, angle):
    global speed
    if angle >= 0: rotational_velocity = speed
    else: rotational_velocity = -speed
    wheel_velocities = SharedMethods.calculateWheelVelocities(0, 0, rotational_velocity)
    SharedMethods.pauseCommunication(clientID, True)
    SharedMethods.setWheelVelocity(wheelJoints, clientID, wheel_velocities)
    SharedMethods.pauseCommunication(clientID, False)
    radius = (wheelDistanceVer + wheelDistanceHor) / 2
    arc_length = abs(angle) * radius  # Degrees×π/180
    correctionFactor = 1.045
    duration = (arc_length/perimeter) * ((2 * math.pi)/speed) * correctionFactor
    time.sleep(duration)
    SharedMethods.setWheelVelocity(wheelJoints, clientID)


def odometry(angleR, distanceR):
    global xPos
    global yPos
    global angle
    angle += angleR
    angle = (angle + math.pi) % (2 * math.pi) - math.pi

    if angleR < 0:
        print("Scenario 1: " + str(angleR))
        xPos += distanceR * math.cos(angle)
        yPos += distanceR * math.sin(angle)
        angle = angle + (math.pi / 2)

    elif angleR > 0:
        print("Scenario 2: " + str(angleR))
        xPos -= distanceR * math.cos(angle)
        yPos -= distanceR * math.sin(angle)
        angle = angle - (math.pi / 2)

    else:
        print("Scenario 3: " + str(angleR))
        xPos += distanceR * math.cos(angle)
        yPos += distanceR * -math.sin(angle)


def main():
    global xPos
    global yPos
    global angle
    clientID = SharedMethods.startSimulation()

    if clientID:
        print("Connection to the remote API server failed! Re-open CoppeliaSim, load the movement.ttt and run this script again.")
        return

    wheelJoints = SharedMethods.getObjectHandles(clientID, ['rollingJoint_fl', 'rollingJoint_rl', 'rollingJoint_rr', 'rollingJoint_fr'])
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    time.sleep(1)

    pos, orient = checkPose(clientID)
    xPos = pos[1][0]
    yPos = pos[1][1]
    angle = orient[1][2]
    distanceR = -1
    angleRs = [-3.1416 / 4, 0, 3.1416 / 4]

    for i, angleR in enumerate(angleRs):
        print("Scenario " + str(i+1))
        moveRobot(clientID, wheelJoints, angleR, distanceR)
        odometry(angleR, distanceR)
        printPosition(clientID)

    SharedMethods.pauseCommunication(clientID, True)
    vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
    SharedMethods.pauseCommunication(clientID, False)
    SharedMethods.closeServerCommunication(clientID)
    print('Program ended')

if __name__ == "__main__":
    main()
