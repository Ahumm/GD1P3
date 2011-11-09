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
    def __init__(self, player, game,manoffset = (3,0,8)):
    
        
        self.mortarNode = render.attachNewNode("mortar")
        self.mortarNode.setName("mortar")
        self.mortarNP = loader.loadModel("models/mortar")
        self.mortarNP.setName("mortar")
        self.mortarNP.setScale(.1)
        self.M = self.mortarNP
        self.M.setName("mortar")
        self.M.reparentTo(self.mortarNode)
        self.M.setPythonTag("owner", self)
        self.M.setPos(player.actor,manoffset[0],manoffset[1],manoffset[2])
        self.M.setHpr(player.actor,0,0,0)
        
        #Setup Collision
        #mortar
        self.mortarTrav = CollisionTraverser()
        self.mortarTrav.showCollisions(render)
        self.mortarHandler = CollisionHandlerQueue()
        self.mortarSphere = CollisionSphere(0,0,0,2)
        self.mortarColNode = CollisionNode("mortar")
        self.mortarColNode.addSolid(self.mortarSphere)
        self.mortarColNode.setIntoCollideMask(BitMask32.allOff())
        self.mortarColNode.setFromCollideMask(BitMask32.bit(5))
        self.mortarColNodePath = self.M.attachNewNode(self.mortarColNode)
        self.mortarColNodePath.setName("mortar")
        self.mortarColNodePath.show()
        self.mortarTrav.addCollider(self.mortarColNodePath, self.mortarHandler)
        #messenger.toggleVerMose()
        self.xSpeed = 30.0
        self.zSpeed = 20.0
        self.zSpeeddec = 0.5
        self.deleteMe = 0
        self.damage = 12
        self.destroy = False
        #tmaxLife is created var, we need it so mortars dont go on forever

        
        
        taskMgr.add(self.move, "MortarMove", extraArgs = [game])
        taskMgr.add(self.traverseAll, "traverseAll", extraArgs=[game])
            
            
    def traverseAll(self, game):
        if not game.paused:
            self.mortarTrav.traverse(render)
        return Task.cont
        
    def move(self, game):
        if not game.paused:
            if self.destroy:
                self.destroyMe(game)
                return Task.done
            else:
                self.M.setX(self.M, self.xSpeed * globalClock.getDt())
                self.M.setZ(self.M, self.zSpeed * globalClock.getDt())
                self.zSpeed -= self.zSpeeddec
                if self.zSpeed < 0:
                    self.M.setP(-180)
                self.m_entries = []
                for i in range(self.mortarHandler.getNumEntries()):
                    entry = self.mortarHandler.getEntry(i)
                    if entry.getIntoNode().getName() == "fence_c" or entry.getIntoNode().getName() =="terrain" or entry.getIntoNode().getName() =="debris" or entry.getIntoNode().getName() =="Enemy":
                        self.m_entries.append(entry)
                if len(self.m_entries) > 0:
                    self.mortarSphere.setRadius(20)
                    print self.mortarColNode.getName()
                    self.destroy = True

        return Task.cont


    def destroyMe(self, game):
        game.explosions_handler.Mortar_Explosion(self.M.getPos())
        self.mortarNP.clearPythonTag("owner")
        self.mortarNode.removeNode()
        del self
        