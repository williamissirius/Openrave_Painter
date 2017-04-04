import time
import openravepy

if not __openravepy_build_doc__:
    from openravepy import *
    from numpy import *

env = Environment()
kinbody = env.ReadRobotXMLFile('robots/barrettwam.robot.xml')
env.Add(kinbody)
solver = ikfast.IKFastSolver(kinbody=kinbody)
chaintree = solver.generateIkSolver(baselink=0,eelink=7,freeindices=[2],solvefn=ikfast.IKFastSolver.solveFullIK_6D)
code = solver.writeIkSolver(chaintree)
open('ik.cpp','w').write(code)