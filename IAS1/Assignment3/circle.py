import time
import math
from shared_methods import SharedMethods

# Robot Geometry
wheelDistanceHor = 0.30046  # Horizontal distance between the wheels
correctionFactor = 1.045


class Circle:
    def circle(radius, speed, clientID, wheelJoints):
        left_wheels_speed = speed + (wheelDistanceHor * (speed / radius)) / 2 # angular velocity = speed / radius
        right_wheels_speed = speed - (wheelDistanceHor * (speed / radius)) / 2
        wheelVelocities = [right_wheels_speed, right_wheels_speed, left_wheels_speed, left_wheels_speed]

        SharedMethods.setWheelVelocity(wheelJoints, clientID)
        SharedMethods.pauseCommunication(clientID, True)
        SharedMethods.setWheelVelocity(wheelJoints, clientID, wheelVelocities)
        SharedMethods.pauseCommunication(clientID, False)

        path_time = 5 * right_wheels_speed * ((2 * radius * math.pi)) * correctionFactor
        time.sleep(path_time)
        SharedMethods.setWheelVelocity(wheelJoints, clientID)
