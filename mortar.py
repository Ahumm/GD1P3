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
        
        #vars like speed, damage, distance will Me passed to some method later
        self.speed = 40.0
        self.distance = 20.0
        self.deleteMe = 0
        self.damage = 12
        #tmaxLife is created var, we need it so mortars dont go on forever
        self.maxLife = self.distance / self.speed
        self.life = 0.0001  
        
        taskMgr.add(self.traverseAll, "traverseAll")
        taskMgr.add(self.move, "move", uponDeath=self.destroyMe)
        
        
    def move(self, Task):
        if self.deleteMe == 1:
            return Task.done
        
        elif self.life > self.maxLife:
            return Task.done
        else:
            #move mortar forward, dependant on delta time
            M = self.mortarNP
            self.dt = self.parent.dt
            M.setX(M, self.dt * self.speed)
            M.setZ(M, self.dt * self.speed)
            if(self.dt == self.parent.dt + 5):
                M.setZ(M,self.dt / self.speed)
            self.life += self.dt
            return Task.cont
            
    def traverseAll(self, task):
        self.mortarTrav.traverse(render)
        return Task.cont


    def destroyMe(self, x):
        self.mortarNP.clearPythonTag("owner")
        self.mortarNode.removeNode()