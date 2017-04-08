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
		if im_bw[i][j] < 255 and i%10 == 0 and j%10 == 0:
			img.append([-0.2, j*0.001 - 0.1,-i*0.001+1])

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
	env.Load('hw3.env.xml')
	time.sleep(0.1)

	# 1) get the 1st robot that is inside the loaded scene
	# 2) assign it to the variable named 'robot'
	robot = env.GetRobots()[0]
	# jointnames = ['J0','J1','J2','J3','J4','J5']
	# robot.SetActiveDOFs([robot.GetJoint(name).GetDOFIndex() for name in jointnames])

	print  robot
	tuckarms(env, robot)

	robot.SetActiveManipulator(robot.GetManipulator('rightarm_torso'))

	T = robot.GetManipulator('rightarm_torso').GetTransform()
	point = [T[0,3], T[1,3], T[2,3]]
	print T
	print point


	with env:
		ikmodel = openravepy.databases.inversekinematics.InverseKinematicsModel(robot,iktype=IkParameterization.Type.Translation3D)
		print ikmodel
		
		if not ikmodel.load():
			ikmodel.autogenerate()

	#h = env.plot3(Tee[0:3,3],10) # plot one point
	#raw_input('press any key')
	handles = [];
	joint_names = ['torso_lift_joint','r_shoulder_pan_joint','r_shoulder_lift_joint', 'r_upper_arm_roll_joint','r_elbow_flex_joint', 'r_forearm_roll_joint', 'r_wrist_flex_joint']
	robot.SetActiveDOFs([robot.GetJoint(name).GetDOFIndex() for name in joint_names]);
	raw_input("Press enter to continue...")

	for point in img:
		color = [0,0,0]
		handles.append(env.plot3(points=point,pointsize=2.0, colors=color))
		solutions = ikmodel.manip.FindIKSolution(IkParameterization(point, IkParameterization.Type.Translation3D),IkFilterOptions.CheckEnvCollisions)
		robot.SetActiveDOFValues(solutions)
		robot.GetController().SetDesired(robot.GetDOFValues());
		T = robot.GetManipulator('rightarm_torso').GetTransform()
		print "Endeffector After IK"
		point = [T[0,3], T[1,3], T[2,3]]
		print point
		time.sleep(0.02)


	raw_input("Press enter to exit...")
