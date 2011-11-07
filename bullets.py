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

#temporary - variables need to be changed

class Bullet():
    def __init__(self, parent):
    
        self.parent = parent
        self.bulletNode = render.attachNewNode("bullet")
        self.bulletNP = loader.loadModel("models/ball")
        self.bulletNP.setScale(.25)
        B = self.bulletNP
        B.reparentTo(self.bulletNode)
        B.setPythonTag("owner", self)
        B.setPos(parent.actor,0,1,0)
        B.setHpr(parent.actor,0,0,0)
        
        #Setup Collision
        #Bullet
        self.bulletTrav = CollisionTraverser()
        self.bulletTrav.showCollisions(render)
        self.bulletHandler = CollisionHandlerEvent()
        self.bulletSphere = CollisionSphere(0,0,0,1)
        self.bulletColNode = CollisionNode("bullet")
        self.bulletColNode.addSolid(self.bulletSphere)
        self.bulletColNode.setIntoCollideMask(BitMask32.allOff())
        self.bulletColNode.setFromCollideMask(BitMask32.bit(5))
        self.bulletColNodePath = B.attachNewNode(self.bulletColNode)
        self.bulletColNodePath.setName("bullet")
        self.bulletColNodePath.show()
        self.bulletTrav.addCollider(self.bulletColNodePath, self.bulletHandler)
        #messenger.toggleVerbose()
        
        #vars like speed, damage, distance will be passed to some method later
        self.speed = 100.0
        self.distance = 50.0
        self.deleteMe = 0
        self.damage = 12
        #tmaxLife is created var, we need it so bullets dont go on forever
        self.maxLife = self.distance / self.speed
        self.life = 0.00001  
        
        taskMgr.add(self.traverseAll, "traverseAll")
        taskMgr.add(self.move, "move", uponDeath=self.destroyMe)
        
        
    def move(self, Task):
        if self.deleteMe == 1:
            return Task.done
        
        elif self.life > self.maxLife:
            return Task.done
        else:
            #move bullet forward, dependant on delta time
            B = self.bulletNP
            self.dt = self.parent.dt
            B.setX(B, self.dt * self.speed)
            self.life += self.dt
            return Task.cont
            
    def traverseAll(self, task):
        self.bulletTrav.traverse(render)
        return Task.cont


    def destroyMe(self, x):
        self.bulletNP.clearPythonTag("owner")
        self.bulletNode.removeNode()