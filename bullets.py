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

#temporary - variables need to be changed

class Bullet():
    def init(self, type, parent):
        self.parent = parent

        self.bulletNode = base.bullets.attachNewNode("bullet")
        self.bulletNP = loader.loadModel("models/ball")
        self.bulletNP.setScale(.25)
        P = self.bulletNP
        P.reparentTo(self.bulletNode)
        P.setPythonTag("owner", self)
        P.setPos(parent.actor, 0, 1, 0)
        P.setHpr(parent.actor, 0, 0, 0)
        #vars like speed, damage, distance will be passed to some method later
        self.speed = 40.0
        self.distance = 20.0
        self.deleteMe = 0
        self.damage = 12
        #tmaxLife is created var, we need it so bullets dont go on forever
        self.maxLife = self.distance / self.speed
        self.life = 0.00001
        
        taskMgr.add(self.move, "move", uponDeath=self.destroyMe)
        
        
    def move(self, Task):
        if self.deleteMe == 1:
            return Task.done
        
        elif self.life > self.maxLife:
            return Task.done
        else:
            #move bullet forward, dependant on delta time
            P = self.bulletNP
            dt = self.parent.dt
            P.setX(P, dt * self.speed)
            self.life += dt
            return Task.cont
    
    def destroyMe(self, x):
        self.bulletNP.clearPythonTag("owner")
        self.bulletNode.removeNode()
        

