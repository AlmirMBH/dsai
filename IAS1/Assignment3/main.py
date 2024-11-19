import vrep
import time
import math
from shared_methods import SharedMethods
from polygon import Polygon
from circle import Circle
from ellipsoid import Ellipsoid
from rectangle import Rectangle
from triangle import Triangle
from parallelogram import Parallelogram
from hexagonal import Hexagonal
from trapezoid import Trapezoid


# Robot Geometry
diameter = 0.1  # Diameter of the wheels in m
perimeter = math.pi * diameter  # Perimeter of the wheels in m
wheelDistanceVer = 0.471  # Vertical distance between the wheels
wheelDistanceHor = 0.30046  # Horizontal distance between the wheels
correctionFactor = 1.045

def rectangle(wheelJoints, clientID):
    rectangle_sides = [1, 2, 1, 2]

    for i in rectangle_sides:
        Rectangle.moveForward(i, 5, clientID, wheelJoints)
        Rectangle.turnRight(90, 5, clientID, wheelJoints)
    time.sleep(3)


def circle(wheelJoints, clientID):
    radius = 0.5
    speed = 5
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    Circle.circle(radius, speed, clientID, wheelJoints)
    time.sleep(3)


def ellipsoid(wheelJoints, clientID):
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    radius = 2
    speed = 5
    Ellipsoid.ellipsoid(radius, speed, clientID, wheelJoints)
    time.sleep(3)


def polygon(wheelJoints, clientID):
    polygon_sides = 5
    angle = 360 / polygon_sides
    distance = 0.2
    speed = 5
    SharedMethods.setWheelVelocity(wheelJoints, clientID)

    for _ in range(polygon_sides):
        Polygon.moveForward(distance, speed, clientID, wheelJoints)
        Polygon.turnRight(angle, speed, clientID, wheelJoints)
    time.sleep(3)


def triangle(wheelJoints, clientID):
    triangle_sides = 3
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    for i in range(triangle_sides):
        Triangle.moveForward(1, 5, clientID, wheelJoints)
        Triangle.turnRight(120, 5, clientID, wheelJoints)
    time.sleep(3)


def parallelogram(wheelJoints, clientID):
    trianglparallelogram_sides = 4
    angles = [45, 135, 45, 135]
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    for i in range(trianglparallelogram_sides):
        Parallelogram.moveForward(1, 5, clientID, wheelJoints)
        Parallelogram.turnRight(angles[i], 5, clientID, wheelJoints)
    time.sleep(3)

def hexagonal(wheelJoints, clientID):
    polygon_sides = 6
    angle = 360 / polygon_sides
    distance = 0.2
    speed = 5
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    for _ in range(polygon_sides):
        Hexagonal.moveForward(distance, speed, clientID, wheelJoints)
        Hexagonal.turnRight(angle, speed, clientID, wheelJoints)
    time.sleep(3)


def trapezoid(wheelJoints, clientID):
    speed = 5
    trapezoid_sides = [2, 2, 4, 2] # top, right, bottom, left
    angles = [60, 120, 120, 60]
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    for i, side in enumerate(trapezoid_sides):
        Trapezoid.moveForward(side, speed, clientID, wheelJoints)
        Trapezoid.turnRight(angles[i], speed, clientID, wheelJoints)
    time.sleep(3)


def startSimulation():
    print("Program started")
    SharedMethods.closeServerCommunication(-1)
    clientID = vrep.simxStart("127.0.0.1", 19997, True, True, 2000, 5)

    if clientID != -1:
        print("Connected to remote API server")
        res = vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)

        if res != vrep.simx_return_ok:
            print("Failed to start simulation")
            return
        
        return clientID
    else:
        print("Connection to the remote API server failed! Re-open CoppeliaSim, load the movement.ttt and run this script again.")



def main():
    clientID = startSimulation()
    wheelJoints = SharedMethods.getObjectHandles(clientID, ['rollingJoint_fl', 'rollingJoint_rl', 'rollingJoint_rr', 'rollingJoint_fr'])
    time.sleep(5)
    
    # Uncomment a path or any of them to execute them one after the other
    rectangle(wheelJoints, clientID)
    circle(wheelJoints, clientID)
    ellipsoid(wheelJoints, clientID)
    polygon(wheelJoints, clientID)
    triangle(wheelJoints, clientID)
    parallelogram(wheelJoints, clientID)
    hexagonal(wheelJoints, clientID)
    trapezoid(wheelJoints, clientID)

    SharedMethods.pauseCommunication(clientID, False)
    vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
    SharedMethods.closeServerCommunication(clientID)

    print("Program ended")



    # movementLengths = [6, 3, 6, 3]
    # movementSegments = [1, 2, 3]
    # speed = 1

    # for i, length in enumerate(movementLengths):
    #     for index, segment in enumerate(movementSegments):
    #         if i % 2 == 0 or index == 1:
    #             speed = segment * segment
    #         elif index == 2:
    #             speed = segment / segment

    # moveForward(length/8, speed, clientID, wheelJoints)
    # turnRight(90, speed, clientID, wheelJoints)


if __name__ == "__main__":
    main()
