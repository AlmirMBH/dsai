import vrep
import time
from datetime import datetime
from shared_methods import SharedMethods
from circle import Circle
from ellipsoid import Ellipsoid


def rectangle(wheelJoints, clientID):
    angle = 90
    rectangle_sides = [1, 2, 1, 2]
    for sideIndex, side in enumerate(rectangle_sides):
        SharedMethods.changeSpeed(side, sideIndex, len(rectangle_sides), angle, clientID, wheelJoints)
    time.sleep(2)


def circle(wheelJoints, clientID):
    radius = 0.5
    speed = 5
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    Circle.circle(radius, speed, clientID, wheelJoints)
    time.sleep(2)


def ellipsoid(wheelJoints, clientID):
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    radius = 2
    speed = 5
    Ellipsoid.ellipsoid(radius, speed, clientID, wheelJoints)
    time.sleep(2)


def polygon(wheelJoints, clientID):
    polygon_sides = 5
    length_of_polygon_side = 0.2
    angle = 360 / polygon_sides
    SharedMethods.setWheelVelocity(wheelJoints, clientID)

    for sideIndex in range(polygon_sides):
        SharedMethods.changeSpeed(length_of_polygon_side, sideIndex, polygon_sides, angle, clientID, wheelJoints)
    time.sleep(2)


def triangle(wheelJoints, clientID):
    triangle_sides = 3
    length_of_triangle_side = 2
    angle = 180/triangle_sides
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    for sideIndex in range(triangle_sides):
        SharedMethods.changeSpeed(length_of_triangle_side, sideIndex, triangle_sides, angle, clientID, wheelJoints)
    time.sleep(2)


def parallelogram(wheelJoints, clientID):
    parallelogram_sides = 4
    length_of_triangle_side = 1
    angles = [45, 135, 45, 135]
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    for sideIndex in range(parallelogram_sides):
        SharedMethods.changeSpeed(length_of_triangle_side, sideIndex, parallelogram_sides, angles[sideIndex], clientID, wheelJoints)
    time.sleep(2)

def hexagonal(wheelJoints, clientID):
    polygon_sides = 6
    angle = 360 / polygon_sides
    length_of_polygon_side = 0.2
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    for sideIndex in range(polygon_sides):
        SharedMethods.changeSpeed(length_of_polygon_side, sideIndex, polygon_sides, angle, clientID, wheelJoints)
    time.sleep(2)


def trapezoid(wheelJoints, clientID):
    trapezoid_sides = [2, 2, 4, 2] # top, right, bottom, left
    angles = [60, 120, 120, 60]
    SharedMethods.setWheelVelocity(wheelJoints, clientID)
    for sideIndex, trapezoid_side in enumerate(trapezoid_sides):
        SharedMethods.changeSpeed(trapezoid_side, sideIndex, len(trapezoid_sides), angles[sideIndex], clientID, wheelJoints)
    time.sleep(2)


def main():
    start_time = datetime.now()
    clientID = SharedMethods.startSimulation()
    wheelJoints = SharedMethods.getObjectHandles(clientID, ['rollingJoint_fl', 'rollingJoint_rl', 'rollingJoint_rr', 'rollingJoint_fr'])
    time.sleep(5)
    
    print("Starting rectangle")
    rectangle(wheelJoints, clientID)
    print("Starting circle")
    circle(wheelJoints, clientID)
    print("Starting ellipsoid")
    ellipsoid(wheelJoints, clientID)
    print("Starting 5-sided polygon")
    polygon(wheelJoints, clientID)
    print("Starting triangle")
    triangle(wheelJoints, clientID)
    print("Starting parallelogram")
    parallelogram(wheelJoints, clientID)
    print("Starting hexagonal")
    hexagonal(wheelJoints, clientID)
    print("Starting trapezoid")
    trapezoid(wheelJoints, clientID)

    SharedMethods.pauseCommunication(clientID, False)
    vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
    SharedMethods.closeServerCommunication(clientID)
    end_time = datetime.now()

    print("Program ended. Execution time: " + str(end_time - start_time))


if __name__ == "__main__":
    main()
