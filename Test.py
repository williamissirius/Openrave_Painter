#!/usr/bin/env python
# -*- coding: utf-8 -*-
#HW1 for RBE 595/CS 525 Motion Planning
#code based on the simplemanipulation.py example
import time
import openravepy
from openravepy.misc import InitOpenRAVELogging

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
	InitOpenRAVELogging() 

	env = Environment()
	env.SetViewer('qtcoin')
	collisionChecker = RaveCreateCollisionChecker(env,'ode')
	env.SetCollisionChecker(collisionChecker)


	env.Reset()
	# load a scene from ProjectRoom environment XML file
	env.Load('playground.env.xml')

	robot = env.GetRobots()[0]
	print  robot
	robot.SetActiveManipulator(robot.GetManipulator('rightarm_torso'))
	with env:
		ikmodel = openravepy.databases.inversekinematics.InverseKinematicsModel(robot,iktype=IkParameterization.Type.Translation3D)
		print ikmodel
		
		if not ikmodel.load():
			ikmodel.autogenerate()


	physics = RaveCreatePhysicsEngine(env,'ode')
	env.SetPhysicsEngine(physics)
	time.sleep(0.1)

	with env:
		env.GetPhysicsEngine().SetGravity([0,0, -9.8])
		env.StopSimulation()
		env.StartSimulation(timestep=1e-3)
		starttime = time.time()


	# 1) get the 1st robot that is inside the loaded scene
	# 2) assign it to the variable named 'robot'
	
	
	# tuck in the PR2's arms for driving
	print "robot links"
	print robot.GetLinks()[0]
	time.sleep(0.1)
	# with env:
	# 	for link in robot.GetLinks():
	# 		link.SetStatic(True)
	tuckarms(env,robot);
	tuckarms(env,robot);





	#drawing_joint_names = ['r_shoulder_pan_joint','r_shoulder_lift_joint', 'r_upper_arm_roll_joint','r_elbow_flex_joint'] #, 'r_forearm_roll_joint', 'r_wrist_flex_joint', 'r_wrist_roll_joint'
	drawing_joint_names = ['r_shoulder_pan_joint','r_shoulder_lift_joint', 'r_elbow_flex_joint'] 

	robot.SetActiveDOFs([robot.GetJoint(name).GetDOFIndex() for name in drawing_joint_names]);
	upperlimit = [];
	lowerlimit = [];
	limit = robot.GetActiveDOFLimits();
	print limit;
	with env:
		config_joint = [-1.0,0.0, -1.0]
		robot.SetActiveDOFValues(config_joint)
		robot.GetController().SetDesired(robot.GetDOFValues());
	waitrobot(robot)

	T = robot.GetManipulator('rightarm_torso').GetTransform()
	point = [T[0,3], T[1,3], T[2,3]]
	print T
	print point

	print "configuration"
	print config_joint

	print robot.GetActiveDOFLimits();
	

	tuckarms(env,robot);

	raw_input("Press enter to exit...")

	#ikmodel = openravepy.databases.inversekinematics.InverseKinematicsModel(robot,iktype='translationdirection5d')
	with env:

		
	
		goal_endeffector_position = [-0.6, 1.4, 0.52];
		solutions = ikmodel.manip.FindIKSolution(IkParameterization(goal_endeffector_position, IkParameterization.Type.Translation3D),IkFilterOptions.CheckEnvCollisions)
	
		print "solution"

		print solutions


	joint_names = ['torso_lift_joint','r_shoulder_pan_joint','r_shoulder_lift_joint', 'r_upper_arm_roll_joint','r_elbow_flex_joint']

	config = [ solutions[0] ,  solutions[1] , solutions[2] , solutions[3],  solutions[4]]
	
	with env:
		robot.SetActiveDOFs([robot.GetJoint(name).GetDOFIndex() for name in joint_names]);
		robot.SetActiveDOFValues(config)
		robot.GetController().SetDesired(robot.GetDOFValues());
	waitrobot(robot)
	T = robot.GetManipulator('rightarm_torso').GetTransform()
	print "Endeffector After IK"
	point = [T[0,3], T[1,3], T[2,3]]
	print "Goal is " , [-2.6949156636956717, -1.5879999999999999, 1.2827045138538078]
	print point



	#### YOUR CODE HERE ####







	#### END OF YOUR CODE ###


	raw_input("Press enter to exit...")

