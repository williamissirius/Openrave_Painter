import cv2
import time
from openravepy import *
import numpy as np


img = cv2.imread('obj.jpg')
img  = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
(thresh, im_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
im_bw = cv2.threshold(im_bw, thresh, 255, cv2.THRESH_BINARY)[1]
rows, cols = im_bw.shape[:2]  # dimensions of resized m-cap
img = []




for i in range(0,rows) :
    for j in range(0,cols) :
        if im_bw[i][j] < 255 and i%6 == 0 and j%6 == 0:
            img.append([j*0.002,-i*0.002,0, 1])


env = Environment()
env.SetViewer('qtcoin')
env.Load('robots/puma.robot.xml')
robot = env.GetRobots()[0]

manip = robot.GetActiveManipulator()
ikmodel = databases.inversekinematics.InverseKinematicsModel(robot,iktype=IkParameterization.Type.Transform6D)

if not ikmodel.load():
    ikmodel.autogenerate()

manipprob = interfaces.BaseManipulation(robot) # create the interface for basic manipulation programs
Tgoal = numpy.array([[0,-1,0,-0.21],[-1,0,0,0.04],[0,0,-1,0.92],[0,0,0,1]])
res = manipprob.MoveToHandPosition(matrices=[img],seedik=10) # call motion planner with goal joint angles
raw_input('press any key')


# with env: # lock environment and save robot state
#     Tgoal = np.array([[0,-1,0,-0.21],[-1,0,0,0.04],[0,0,-1,0.92],[0,0,0,1]])
#     # #Tgoal = img
#     # ikparam = IkParameterization(Tgoal,ikmodel.iktype) # build up the translation3d ik query
#     # sol = manip.FindIKSolution(Tgoal, IkFilterOptions.CheckEnvCollisions) # get collision-free solution
    

#     manipprob = interfaces.BaseManipulation(robot) # create the interface for basic manipulation programs
#     Tgoal = numpy.array([[0,-1,0,-0.21],[-1,0,0,0.04],[0,0,-1,0.92],[0,0,0,1]])
#     res = manipprob.MoveToHandPosition(matrices=[Tgoal],seedik=10) # call motion planner with goal joint angles
#     robot.WaitForController(0) # wait


    # with robot: # save robot state
    #     robot.SetDOFValues(sol,manip.GetArmIndices()) # set the current solution
    #     Tee = manip.GetEndEffectorTransform()
    #     print Tee
    #     env.UpdatePublishedBodies() # allow viewer to update new robot
    #     raw_input('press any key')
    #     # time.sleep(0.1)

    #print  robot


    # angle = 0.0
    # handles = []
    # color = [0,0,0]
# for point in img:
    #     handles.append(env.plot3(points=point,pointsize=2.0, colors=color))

