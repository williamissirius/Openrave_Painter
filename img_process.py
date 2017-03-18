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
for i in range(0,rows):
    for j in range(0,cols):
        if im_bw[i][j] == 255:
            img.append([i*0.01,j*0.01,0])

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

    print  robot


    angle = 0.0
    handles = []
    color = [0,0,1]
    handles.append(env.plot3(points=img),pointsize=1.0, colors=color)

    raw_input("Press enter to exit...")
