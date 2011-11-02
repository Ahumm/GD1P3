import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions
from direct.gui.DirectGui import * #for buttons and stuff
from panda3d.ai import * # AI logic
from pandac.PandaModules import Vec3
import sys, math, random

class Bullet(DirectObject):
	def __init__ (self, type, parent):
        self.parent = parent
            
        self.bulletNode = base.bullets.attatchNewNode("bullet")
        self.bulletNP = loader.loadModel("Models/ball.egg")
        P = self.bulletNP
        P.reparentTo(self.bulletNode)
        P.setPythonTag("owner",self)
        P.setPos(parent.shipNP,0, 1, 0)
        P.setHpr(parent.shipNP,0, 0, 0)
        #vars like speed, damage, distance will be passed to some method later
        self.speed = 100.0
        self.distance = 50.0
        self.deleteMe = 0
        
        #tmaxLife is created var, we need it so bullets dont go on forever
        self.maxLife = self.distance/self.speed
        self.life = 0.00001
        
        taskMgr.add(self.move,"move",uponDeath=self.destroyMe,sort = 999)
        
        self.setupCollision()
    
    def move(self,Task):
        if self.deleteMe == 1:
            return Task.done
    
        elif self.life> self.maxLife:
            return Task.done
        else:
        #move bullet forward, dependant on delta time
            P = self.bulletNP
            dt = self.parent.dt
            P.setY(P,dt*self.speed)
            self.life += dt
            return Task.cont
  
    def destroyMe(self,x):
        print "deleting"
        self.bulletNP.clearPythonTag("owner")
        self.bulletNode.removeNode()
    
    def setupCollision(self):
        fromObject = self.bulletNP.find('**/+CollisionNode')
        fromObject.setName("bullet")
        base.cTrav.addCollider(fromObject,base.pusher)
        base.pusher.addCollider(fromObject,self.bulletNP)
