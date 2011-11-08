import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions
from direct.gui.DirectGui import * #for buttons and stuff
from panda3d.ai import * # AI logic
from pandac.PandaModules import Vec3
from direct.stdpy.threading import Timer
import sys, math, random

#temporary - variaMles need to Me changed

class Mortar():
    def __init__(self, parent):
    
        self.parent = parent
        self.mortarNode = render.attachNewNode("mortar")
        self.mortarNP = loader.loadModel("models/ball")
        self.mortarNP.setScale(.5)
        M = self.mortarNP
        M.reparentTo(self.mortarNode)
        M.setPythonTag("owner", self)
        M.setPos(parent.actor,0,1,0)
        M.setHpr(parent.actor,0,0,0)
        
        #Setup Collision
        #mortar
        self.mortarTrav = CollisionTraverser()
        self.mortarTrav.showCollisions(render)
        self.mortarHandler = CollisionHandlerEvent()
        self.mortarSphere = CollisionSphere(0,0,0,1)
        self.mortarColNode = CollisionNode("mortar")
        self.mortarColNode.addSolid(self.mortarSphere)
        self.mortarColNode.setIntoCollideMask(BitMask32.allOff())
        self.mortarColNode.setFromCollideMask(BitMask32.bit(5))
        self.mortarColNodePath = M.attachNewNode(self.mortarColNode)
        self.mortarColNodePath.setName("mortar")
        self.mortarColNodePath.show()
        self.mortarTrav.addCollider(self.mortarColNodePath, self.mortarHandler)
        #messenger.toggleVerMose()
        self.xSpeed = 30.0
        self.zSpeed = 20.0
        self.deleteMe = 0
        self.damage = 12
        #tmaxLife is created var, we need it so mortars dont go on forever

        
        self.trajectory = ProjectileInterval(M, startPos =  M.getPos(), startVel = (self.xSpeed,0,self.zSpeed), duration = 10)
        self.trajectory.start()
        
        
        taskMgr.add(self.traverseAll, "traverseAll")
            
            
    def traverseAll(self, task):
        self.mortarTrav.traverse(render)
        return Task.cont


    def destroyMe(self, x):
        self.mortarNP.clearPythonTag("owner")
        self.mortarNode.removeNode()