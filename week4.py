# Make sure to have the server side running in CoppeliaSim: 
# in a child script of a CoppeliaSim scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time
import math
import sys
import random # need in order to perform the random wander

class Robot():

    def __init__(self) -> None:
        
        # Setup Motors
        res, self.leftMotor = sim.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',sim.simx_opmode_blocking)
        res, self.rightMotor = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor',sim.simx_opmode_blocking)

        # Setup Sonars
        res, self.frontLeftSonar = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx_ultrasonicSensor5',sim.simx_opmode_blocking)
        res, self.RightSonar = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx_ultrasonicSensor8',sim.simx_opmode_blocking)
        res, self.backRightSonar = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx_ultrasonicSensor9',sim.simx_opmode_blocking)

         # Start Sonars
        res,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector = sim.simxReadProximitySensor(clientID,self.frontLeftSonar,sim.simx_opmode_streaming)
        res,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector = sim.simxReadProximitySensor(clientID,self.RightSonar,sim.simx_opmode_streaming)
        res,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector = sim.simxReadProximitySensor(clientID,self.backRightSonar,sim.simx_opmode_streaming)

        #Starting Sensors, front and back

    def getDistanceReading(self, objectHandle):
        # Get reading from sensor
        res,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector = sim.simxReadProximitySensor(clientID,objectHandle,sim.simx_opmode_buffer)

        if detectionState == 1:
            # return magnitude of detectedPoint
            return math.sqrt(sum(i**2 for i in detectedPoint))
        else:
            # resturn another value that we know cannon be true and handle it (use a large number so that if you do 'distance < reading' it will work)
            return 9999

    def move(self, velocity):
        # velocity < 0 = reverse
        # velocity > 0 = forward
        res = sim.simxSetJointTargetVelocity(clientID, self.leftMotor, velocity, sim.simx_opmode_blocking)
        res = sim.simxSetJointTargetVelocity(clientID, self.rightMotor, velocity, sim.simx_opmode_blocking)

    def turn(self, turnVelocity):
        # turnVelocity < 0 = trun left
        # turnVelocity > 0 = turn right
        res = sim.simxSetJointTargetVelocity(clientID, self.leftMotor, turnVelocity, sim.simx_opmode_blocking)
        res = sim.simxSetJointTargetVelocity(clientID, self.rightMotor, turnVelocity, sim.simx_opmode_blocking)
        
    def curveCorner(self, leftMotorVelocity, rightMotorVelocity):
        res = sim.simxSetJointTargetVelocity(clientID, self.leftMotor, leftMotorVelocity, sim.simx_opmode_blocking)
        res = sim.simxSetJointTargetVelocity(clientID, self.rightMotor, rightMotorVelocity, sim.simx_opmode_blocking)

    def stop(self):
        res = sim.simxSetJointTargetVelocity(clientID, self.leftMotor, 0, sim.simx_opmode_blocking)
        res = sim.simxSetJointTargetVelocity(clientID, self.rightMotor, 0, sim.simx_opmode_blocking)

    def slowdown(self):
        res = sim.simxSetJointTargetVelocity(clientID, self.leftMotor, .1, sim.simx_opmode_blocking)
        res = sim.simxSetJointTargetVelocity(clientID, self.rightMotor, .1, sim.simx_opmode_blocking)
        


        

print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim

if clientID!=-1:
    print ('Connected to remote API server')


    
    robot = Robot()
    # Now try to retrieve data in a blocking fashion (i.e. a service call):
    res,objs=sim.simxGetObjects(clientID,sim.sim_handle_all,sim.simx_opmode_blocking)
    if res==sim.simx_return_ok:
        print ('Number of objects in the scene: ',len(objs))
    else:
        print ('Remote API fucnction call returned with error code: ',res)


    for i in range(10):
        print(robot.getDistanceReading(robot.frontLeftSonar))
        print(robot.getDistanceReading(robot.RightSonar))
        print(robot.getDistanceReading(robot.backRightSonar))
        
        time.sleep(0.5)

        # Function used to return a random integer within the range of 0 and 100 for the random wander

    randomNumber = random.randint(0, 100)    

    # Loop execution (nested while statement)
    while True:
        # the robot will move untill it detects an object
        robot.move(1)
        # if...elif ..else statements that allows us to check for multiple expressions
        if robot.getDistanceReading(robot.frontLeftSonar) <= 0.5: #threshold value
            robot.slowdown()
            # robot.stop()
            robot.curveCorner(-3, 3) # velocity adjectment
            # print(robot.getDistanceReading(robot.frontLeftSonar))
            print("Wall detected in (L)front 0.5")
            # the robot will turn if a wall is detected
 
        elif robot.getDistanceReading(robot.RightSonar) <= 0.40:
            # robot.stop()
            # robot.curveCorner(0.25, 0.35)             
            robot.curveCorner(0.85, 1)             
            # robot.move(0.5)           
            print("0.40 Change direction to the Left") # the robot will turn to adjust direction;
            print(robot.getDistanceReading(robot.RightSonar))
            


        # elif robot.getDistanceReading(robot.RightSonar) <= 0.44:
        #     # robot.stop()
        #     # robot.curveCorner(0.25, 0.35)             
        #     robot.curveCorner(1, 1)             
        #     # robot.move(0.5)           
        #     print("0.44 Change direction to the Left") # the robot will turn to adjust direction;

        elif robot.getDistanceReading(robot.RightSonar) <= 0.45:
            # robot.stop()
            # robot.curveCorner(0.25, 0.35)             
            robot.curveCorner(2, 0.15)             
            # robot.move(0.5)           
            print("0.45 Change direction to the Left") # the robot will turn to adjust direction;

        elif robot.getDistanceReading(robot.RightSonar) <= 0.50:
            # robot.stop()
            # robot.curveCorner(0.40, 0.30)    
            robot.curveCorner(0.85, 1)    
            # robot.move(0.5)                    
            print("0.50 Change direction to the Left") # the robot will turn to adjust direction;

        # elif robot.getDistanceReading(robot.RightSonar) <= 0.55:
        #     # robot.stop()
        #     robot.curveCorner(0.38, 0.30)                        
        #     print("0.55 Change direction to the Left") # the robot will turn to adjust direction;
            
        elif robot.getDistanceReading(robot.RightSonar) <= 0.60:
            # robot.stop()
            # robot.curveCorner(0.35, 0.25)                        
            robot.curveCorner(2, 0.25)                        
            print("0.60 Change direction to the Left") # the robot will turn to adjust direction;

        # elif robot.getDistanceReading(robot.RightSonar) <= 0.70:
        #     # robot.stop()
        #     robot.curveCorner(1, 0.1)                        
        #     print("Robot have too much a gap from the wall on the Left") # the robot will turn to adjust direction;

        elif robot.getDistanceReading(robot.RightSonar) <= 2:
            robot.stop()
            robot.curveCorner(3, 0.1)                        
            print("Big TurnRight") # the robot will turn to adjust direction;

        elif robot.getDistanceReading(robot.backRightSonar) <= 2:
            robot.stop()
            robot.curveCorner(3, 0.1)
            print("Searching the wall")
            # print(robot.getDistanceReading(robot.backRightSonar))
        
        # else:
        #     # for i in range(5):
        #     #     if i == 5:
        #     robot.curveCorner(randomNumber - 1, randomNumber + 1)
        #         # else :
        #         #     robot.move(1)

        else: 
            robot.curveCorner(randomNumber - 1, randomNumber + 1)


    robot.stop()

print ('Failed connecting to remote API server')
print ('Program ended')
sys.exit('Could not connect')