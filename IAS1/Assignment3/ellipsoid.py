import math
from shared_methods import SharedMethods


class Ellipsoid:
    @classmethod
    def ellipsoid(cls, radius, speed, clientID, wheelJoints):
        angular_position = 0
        ellipse_factor = 3
        SharedMethods.setWheelVelocity(wheelJoints, clientID)
        
        while angular_position < 2 * math.pi: # limit to one revolution
            angular_position += 0.1
            speed_modulation = abs(math.sin(angular_position)) # 0 - 0.99
            right_wheels_speed = speed * radius
            left_wheels_speed = speed * radius + speed * (speed_modulation * (ellipse_factor - 1))
            wheelVelocities = [right_wheels_speed, right_wheels_speed, left_wheels_speed, left_wheels_speed]

            SharedMethods.pauseCommunication(clientID, True)
            SharedMethods.setWheelVelocity(wheelJoints, clientID, wheelVelocities, 0.15)
            SharedMethods.pauseCommunication(clientID, False)

        SharedMethods.setWheelVelocity(wheelJoints, clientID)
