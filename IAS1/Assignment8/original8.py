import vrep
import time
import os
import math as m
import numpy as np
import cv2
import array
from PIL import Image

# robot state information
orientationVector = [0.0, -1.0]
startPos = [0.0, 0.0]
startOri = 0.0
clientID = -1
wheels = [-1] * 4

imaging=None

#Initialize the image in the function initimg
def initimg(clientID):
    # INSERT YOUR CODE HERE
    #Explore and find appropriate API functions to set the floating and integer signals for the scan angle and rbg sensor
    #Get the object handle of the rgb sensor
    #Get the image using the API function GetVisionSensorImage and the previous object handle
    #Add a title to the plot (hint: you will find this name in a different function in the script so name it like that)
    #Don't forget to add a waiting term
    #Return the object handle
    

# display new image
def updateImage(img):
    cv2.imshow("display", img)
    cv2.waitKey(25)

#get image from youbot
def getImage(clientID, youBotCam):
    start = time.time()
    err, res, image = vrep.simxGetVisionSensorImage(clientID, youBotCam, 0, vrep.simx_opmode_buffer)
    if err == vrep.simx_return_ok:
        data1 = array.array('b', image)
        image_buffer = Image.frombytes("RGB", (res[0],res[1]), bytes(data1), "raw", "RGB", 0, 1)
        img = np.asarray(image_buffer)
        rimg = cv2.cvtColor(cv2.flip(img, 0), cv2.COLOR_BGR2RGB)
        return rimg
    return None

# gets blobs of certain color from imageBGR
def extractBlobsOfColor(imageBGR, detector, color, KeypointColor):
    # INSERT YOUR CODE HERE
    # Determine which blob should be extracted.
    # In terms of the parameter color, change the variable img by calling the appropriate function
    # Hint: Take a look at how this function is called in the provided code, and find a way to do the task
    
    # can be used for drawing a circle/square around blobs
    keypoints = detector.detect(img)
    for i in range(0, len(keypoints)):
        KeypointColor[keypoints[i].pt] = color
    return img

# functions for extracting red and blue blobs
# inRange functions scans each pixel and determines which are between upper and lower RGB values
# only blobs of certain area will be recognized
def redBlobExtract(imageBGR):
    # INSERT YOUR CODE HERE
    #RGB STYLE
    #Determine the lower and upper boundaries for the detection of the red colour.
    #Experiment a few RGB values, or seek help on the internet for general detection criteria
    #Remember the lower and upper boundaries are arrays of RGB values
    return cv2.inRange(imageBGR, lower, upper)

def blueBlobExtract(imageBGR):
    # INSERT YOUR CODE HERE
    #RGB STYLE
    #Determine the lower and upper boundaries for the detection of the blue colour.
    #Experiment a few RGB values, or seek help on the internet for general detection criteria
    #Remember the lower and upper boundaries are arrays of RGB values
    return cv2.inRange(imageBGR, lower, upper)

# get angle from the orientationVector
def oriPhi():
    global orientationVector
    
    # INSERT YOUR CODE HERE
    #Determine the resulting angle in terms of the values of the orientationVector
    #Keep in mind the change of the axis in Coppelia sim.
    #The x axis in Coppelia is the same as the -y axis in our world, and the y axis is the same as our x axis
    #From this we can determine the angle phi in terms of orientationVector [0] and orientationVector[1] as follows
    
    # 0+, 1+ = 0 <= phi <= 90
    # 0-, 1+ = 90 < phi <= 180
    # 0-, 1- = 180 < phi <= 270
    # 0+, 1- = 270 < phi <= 360
    
    
    print(phi)
    return phi

# used to get image, setup detectors and show the image
def imagingSetup():
    global clientID
    global imaging
    imaging = initimg(clientID)
    if(imaging is None):
        print("could not get cam handle")
        return

    test = getImage(clientID, imaging)
    updateImage(test)
    

    # params are parameters for blob detection
    # this determines which blobs will be recognized
    params = cv2.SimpleBlobDetector_Params()
    params.minDistBetweenBlobs = 1
    params.filterByColor = True
    params.blobColor = 255
    params.filterByArea = True
    params.minArea = 1
    params.maxArea = 50000
    params.filterByCircularity = False
    params.filterByConvexity = False
    params.filterByInertia = True
    params.minInertiaRatio = 0.01
    params.maxInertiaRatio = 1
    
    # detectors are used to find the blobs in an image
    detector = cv2.SimpleBlobDetector_create(params)
    
    keypointColor={}
    image=extractBlobsOfColor(test, detector, "r", keypointColor)
    detector2 = cv2.SimpleBlobDetector_create(params)
    image2=extractBlobsOfColor(test, detector2, "b", keypointColor)

    cv2.imshow("red", image)
    cv2.imshow("blue", image2)
    cv2.waitKey(0)
    return detector, detector2

# main function for completing the task
def sim():
    # determine the robots state (optional since youbot doesn't move)
    global startPos
    global startOri
    global clientID
    ori = getObjectOrientation("youBot")
    startPos = getObjectPosition("youBot")
    startOri = oriPhi()
    detector, detector2 = imagingSetup()


# used to find the global position of youbot
def getObjectPosition(oname, fromname = None):
    global clientID
    res, t = vrep.simxGetObjectHandle(clientID, oname, vrep.simx_opmode_oneshot_wait)
    res, pos = vrep.simxGetObjectPosition(clientID, t, -1, vrep.simx_opmode_oneshot_wait)
    if (fromname):
        res, f = vrep.simxGetObjectHandle(clientID, fromname, vrep.simx_opmode_oneshot_wait)
        res, posf = vrep.simxGetObjectPosition(clientID, f, -1, vrep.simx_opmode_oneshot_wait)
        pos = [pos[0] - posf[0], pos[1] - posf[1], pos[2] - posf[2]]
    return pos

# used to find global orientation of youbot
def getObjectOrientation(oname, fromname = None):
    global clientID
    res, t = vrep.simxGetObjectHandle(clientID, oname, vrep.simx_opmode_oneshot_wait)
    res, ori = vrep.simxGetObjectOrientation(clientID, t, -1, vrep.simx_opmode_oneshot_wait)
    if (fromname):
        res, f = vrep.simxGetObjectHandle(clientID, fromname, vrep.simx_opmode_oneshot_wait)
        res, orif = vrep.simxGetObjectOrientation(clientID, f, -1, vrep.simx_opmode_oneshot_wait)
        ori = [ori[0] - orif[0], ori[1] - orif[1], ori[2] - orif[2]]
    return ori

def start():
    global clientID
    global wheels
    # send any random signal to wake vrep up
    vrep.simxReadStringStream(clientID, "test", vrep.simx_opmode_streaming);

    print("waiting for response ...")

    # check simulation status
    res, state = vrep.simxGetInMessageInfo(clientID, 17);
    while (res == -1):
        res, state = vrep.simxGetInMessageInfo(clientID, 17);

    # if simulation already runs, stop it
    if (state == 5 or state == 7):
        print("simulation is already running. stopping simulation ...")
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
        time.sleep(5.5)

    # start simulation
    print("starting simulation ...")
    vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)

    time.sleep(1)

    # INSERT YOUR CODE HERE
    #Get wheel handles (as done in previous exercises) and set velocity to 0

def quit():
    global clientID
    global wheels   
    # set wheel velocity to 0
    for i in range(0, 3):
        vrep.simxSetJointTargetVelocity(clientID, wheels[i], 0, vrep.simx_opmode_oneshot)

    # stop simulation
    vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)

def main():
    #Create the main function the same way as in exercise 7
    # INSERT YOUR CODE HERE
    # close all connections from vrep and print a message (connecting status)
    # connect to vrep, otherwise print information disconnected
    # call 3 most functions if established connection (think about the commands we regularly put in main and conclude which functions are they)
    # disconnect from vrep and print status message


if __name__ == "__main__": main()