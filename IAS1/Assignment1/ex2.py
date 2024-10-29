import vrep
import numpy as np
import time
import math
import vrepConst

# Robot Geometry
diameter = 0.1  # Diameter of the wheels in meters
perimeter = math.pi * diameter  # Perimeter of the wheels in meters
wheelDistanceVer = 0.471  # Vertical distance between the wheels
wheelDistanceHor = 0.30046  # Horizontal distance between the wheels


def wheelVel(forwBackVel, leftRightVel, rotVel):
    """Calculate individual wheel velocities."""
    frontLeft = forwBackVel - leftRightVel - rotVel
    rearLeft = forwBackVel - leftRightVel - rotVel
    rearRight = forwBackVel + leftRightVel + rotVel
    frontRight = forwBackVel + leftRightVel + rotVel
    return np.array([frontLeft, rearLeft, rearRight, frontRight])


def moveForward(distance, speed, clientID, wheelJoints):
    """Move the robot forward by a specified distance at a given speed."""
    correctionFactor = 1.045

    # Stop wheels initially
    for joint in wheelJoints:
        vrep.simxSetJointTargetVelocity(clientID, joint, 0, vrep.simx_opmode_oneshot)

    # Calculate wheel velocities for forward movement
    velocities = wheelVel(speed, 0, 0)

    # Set wheel velocities
    for i, joint in enumerate(wheelJoints):
        vrep.simxSetJointTargetVelocity(clientID, joint, velocities[i], vrep.simx_opmode_oneshot)

    # Calculate required movement time
    timeRequired = (distance / perimeter) * (2 * math.pi) / (speed * correctionFactor)
    time.sleep(timeRequired)

    # Reset wheel velocities to zero after moving
    for joint in wheelJoints:
        vrep.simxSetJointTargetVelocity(clientID, joint, 0, vrep.simx_opmode_oneshot)


def turnRight(degree, speed, clientID, wheelJoints):
    """Rotate the robot to the right by a specified degree at a given speed."""
    for joint in wheelJoints:
        vrep.simxSetJointTargetVelocity(clientID, joint, 0, vrep.simx_opmode_oneshot)

    # Calculate wheel velocities for rotation
    velocities = wheelVel(0, 0, speed)

    # Set wheel velocities for turning
    for i, joint in enumerate(wheelJoints):
        vrep.simxSetJointTargetVelocity(clientID, joint, velocities[i], vrep.simx_opmode_oneshot)

    # Calculate required time for the turn
    timeRequired = (degree * math.pi / 180) / (
                2 * math.pi * speed / (perimeter * (wheelDistanceVer + wheelDistanceHor)))
    time.sleep(timeRequired)

    # Reset wheel velocities to zero after turning
    for joint in wheelJoints:
        vrep.simxSetJointTargetVelocity(clientID, joint, 0, vrep.simx_opmode_oneshot)


def main():
    """Main function to initialize connection, control robot movement and handle communication with V-REP."""
    print('Program started')
    vrep.simxFinish(-1)  # Close all open connections
    clientID = vrep.simxStart('127.0.0.1', 23050, True, True, 2000, 5)

    if clientID != -1:
        print('Connected to remote API server')

        emptyBuff = bytearray()

        # Start the simulation
        vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

        # Initialize robot wheels
        wheelJoints = np.empty(4, dtype=int)
        wheelJoints.fill(-1)  # front left, rear left, rear right, front right

        # Retrieve wheel joint handles
        res, wheelJoints[0] = vrep.simxGetObjectHandle(clientID, 'wheel_joint_fl', vrep.simx_opmode_oneshot_wait)
        res, wheelJoints[1] = vrep.simxGetObjectHandle(clientID, 'wheel_joint_rl', vrep.simx_opmode_oneshot_wait)
        res, wheelJoints[2] = vrep.simxGetObjectHandle(clientID, 'wheel_joint_rr', vrep.simx_opmode_oneshot_wait)
        res, wheelJoints[3] = vrep.simxGetObjectHandle(clientID, 'wheel_joint_fr', vrep.simx_opmode_oneshot_wait)

        # Initialize arm
        armJointsHandle = [0] * 5
        for i in range(5):
            res, armJointsHandle[i] = vrep.simxGetObjectHandle(clientID, f'youBotArmJoint{i}',
                                                               vrep.simx_opmode_oneshot_wait)

        # Move the arm
        for i in range(4):
            vrep.simxSetJointTargetPosition(clientID, armJointsHandle[2], i * math.pi / 8, vrep.simx_opmode_oneshot)
            time.sleep(1)

        # Move robot in a square as main loop
        for _ in range(4):
            moveForward(1.0, 0.5, clientID, wheelJoints)  # move forward by 1 meter
            turnRight(90, 0.5, clientID, wheelJoints)  # turn right 90 degrees

        # Stop simulation
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
        vrep.simxFinish(clientID)
        print('Program ended')
    else:
        print('Failed connecting to remote API server')


if __name__ == "__main__":
    main()
