import cv2
import time
import openravepy
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
			img.append([j*0.002,-i*0.002,1])

if not __openravepy_build_doc__:
	from openravepy import *
	from numpy import *

def waitrobot(robot):
	"""busy wait for robot completion"""
	while not robot.GetController().IsDone():
		time.sleep(0.01)

def tuckarms(env,robot):
	with env:
		jointnames = ['l_shoulder_lift_joint','l_elbow_flex_joint','l_wrist_flex_joint','r_shoulder_lift_joint','r_elbow_flex_joint','r_wrist_flex_joint']
		robot.SetActiveDOFs([robot.GetJoint(name).GetDOFIndex() for name in jointnames])
		robot.SetActiveDOFValues([1.29023451,-2.32099996,-0.69800004,1.27843491,-2.32100002,-0.69799996]);
		robot.GetController().SetDesired(robot.GetDOFValues());
	waitrobot(robot)

if __name__ == "__main__":

	env = Environment()
	env.SetViewer('qtcoin')
	collisionChecker = RaveCreateCollisionChecker(env,'ode')
	env.SetCollisionChecker(collisionChecker)


	env.Reset()
	# load a scene from ProjectRoom environment XML file
	env.Load('robots/puma.robot.xml')
	time.sleep(0.1)

	# 1) get the 1st robot that is inside the loaded scene
	# 2) assign it to the variable named 'robot'
	robot = env.GetRobots()[0]
	# jointnames = ['J0','J1','J2','J3','J4','J5']
	# robot.SetActiveDOFs([robot.GetJoint(name).GetDOFIndex() for name in jointnames])

	print  robot


	angle = 0.0
	handles = []
	color = [0,0,0]

	manip = robot.GetActiveManipulator()
	print manip
	ikmodel = databases.inversekinematics.InverseKinematicsModel(robot,iktype=IkParameterization.Type.Transform6D)
	print 'load ikmodel'
	#print ikmodel.autogenerate()
		


	Tee = manip.GetEndEffectorTransform()
	print Tee
	ikparam = IkParameterization(Tee[0:3,3],ikmodel.iktype) # build up the translation3d ik query
	sols = manip.FindIKSolutions(ikparam, IkFilterOptions.CheckEnvCollisions) 

	h = env.plot3(Tee[0:3,3],10) # plot one point

	for sol in sols[::10]: # go through every 10th solution
		robot.SetDOFValues(sol,manip.GetArmIndices()) # set the current solution
		env.UpdatePublishedBodies() # allow viewer to update new robot
	raw_input('press any key')

	raw_input("Press enter to exit...")
	for point in img:
		handles.append(env.plot3(points=point,pointsize=2.0, colors=color))

	raw_input("Press enter to exit...")
