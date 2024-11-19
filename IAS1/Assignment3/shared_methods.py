import vrep
import time


class SharedMethods:
    @classmethod
    def closeServerCommunication(cls, clientID):
        vrep.simxFinish(clientID)


    @classmethod
    def getObjectHandles(cls, clientID, handles):
        wheelJoints = []

        for joint_name in handles:
                res, joint_handle = vrep.simxGetObjectHandle(clientID, joint_name, vrep.simx_opmode_oneshot_wait)
                wheelJoints.append(joint_handle)

        return wheelJoints


    @classmethod
    def setWheelVelocity(cls, wheelJoints, clientID, wheelVelocities = None, pause = None):
        if wheelVelocities is None:
            wheelVelocities = [0, 0, 0, 0]

        for i, wheelJoint in enumerate(wheelJoints):
                vrep.simxSetJointTargetVelocity(clientID, wheelJoint, wheelVelocities[i], vrep.simx_opmode_oneshot)
                if pause:
                    time.sleep(pause)


    @classmethod
    def pauseCommunication(cls, clientID, pauseStatus):
        vrep.simxPauseCommunication(clientID, pauseStatus)
