import numpy as np
import time
import math
from shared_methods import SharedMethods

# Robot Geometry
diameter         = 0.1                 # Diameter of the wheels in m
perimeter        = math.pi * diameter  # Perimeter of the wheels in m
wheelDistanceVer = 0.471               # Vertical distance between the wheels
wheelDistanceHor = 0.30046             # Horizontal distance between the wheels
correctionFactor = 1.045


class Polygon:
    @classmethod
    def moveForward(cls, distance, speed, clientID, wheelJoints):
        SharedMethods.setWheelVelocity(wheelJoints, clientID)
        wheelVelocities = Polygon.wheelVel(speed, 0, 0)
        SharedMethods.pauseCommunication(clientID, True)
        SharedMethods.setWheelVelocity(wheelJoints, clientID, wheelVelocities)
        SharedMethods.pauseCommunication(clientID, False)
        required_sleep_time = (distance/perimeter) * (2 * math.pi/speed) * correctionFactor # time required to travel one side
        time.sleep(required_sleep_time)
        SharedMethods.setWheelVelocity(wheelJoints, clientID)

    @classmethod
    def turnRight(cls, degree, speed, clientID, wheelJoints):
        SharedMethods.setWheelVelocity(wheelJoints, clientID)
        wheelVelocities = Polygon.wheelVel(0, 0, speed)
        SharedMethods.pauseCommunication(clientID, True)
        SharedMethods.setWheelVelocity(wheelJoints, clientID, wheelVelocities)
        SharedMethods.pauseCommunication(clientID, False)
        time_required = ((wheelDistanceVer + wheelDistanceHor) / perimeter) * math.pi * (degree / abs(speed)) * (math.pi / 180) * correctionFactor
        time.sleep(time_required)
        SharedMethods.setWheelVelocity(wheelJoints, clientID)     


    def wheelVel(forwBackVel , leftRightVel , rotVel):
        frontLeft = forwBackVel - leftRightVel - rotVel
        rearLeft = forwBackVel - leftRightVel - rotVel
        rearRight = forwBackVel + leftRightVel + rotVel
        frontRight = forwBackVel + leftRightVel + rotVel
        return np.array([frontLeft, rearLeft, rearRight, frontRight])
