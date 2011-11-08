# Generic block of import statements!
import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions
from panda3d.ai import * # AI logic
import math,bullets

#Class for each enemy, lot of (planned) variance, seemed easier than subclassing, feel free to change
class Enemy1(object):
    def __init__(self,game,spawnloc = (0,0,0)):
        self.health = 20
        self.value = 10
        self.maxspeed = 5
        
        # Load the enemy model and set the initial position of it
        self.loadModel()
        self.actor.setPos(spawnloc)
        self.enemy_start_pos = spawnloc
        
        #Set the clock stuff
        self.dt = globalClock.getDt()
        
        # Enemy Rays
        self.ralphGroundRay = CollisionRay()
        self.ralphGroundRay.setOrigin(0,0,100)
        self.ralphGroundRay.setDirection(0,0,-1)
        self.ralphGroundCol = CollisionNode('ralphRay')
        self.ralphGroundCol.addSolid(self.ralphGroundRay)
        self.ralphGroundCol.setFromCollideMask(BitMask32.bit(0))
        self.ralphGroundCol.setIntoCollideMask(BitMask32.allOff())
        self.ralphGroundColNp = self.actor.attachNewNode(self.ralphGroundCol)
        self.ralphGroundHandler = CollisionHandlerQueue()
        game.cTrav.addCollider(self.ralphGroundColNp, self.ralphGroundHandler)
        self.ralphGroundColNp.show()
        
        self.pursue_start = False
        self.evade_start = False
        self.timer = 300
        self.fire_rate = 180
        
        # Collision stuff for bullets
        #self.cTrav = CollisionTraverser()
        self.cHandler = CollisionHandlerEvent()
        self.cSphere = CollisionSphere(0,0,2, 4)
        self.cNode = CollisionNode("Enemy")
        self.cNodePath = self.actor.attachNewNode(self.cNode)
        self.cNodePath.node().addSolid(self.cSphere)
        self.cNodePath.show()
        game.cTrav.addCollider(self.cNodePath, self.cHandler)
        
        #self.heightTask = taskMgr.add(self.updateHeight,'EnemyHeight',extraArgs=[game])
    
    def take_damage(self, damage):
        """
            Cause an enemy to take damage.
            Negative health means object is immortal (negative damage kills anything instantly)
        """
        if damage < 0:
            self.health = 0
            return self.value
        if self.health > 0:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                return self.value
        return 0
        
    def loadModel(self):
        self.actor = Actor("models/ralph",
                                {"run":"models/ralph-run",
                                 "walk":"models/ralph-walk"})
        self.actor.reparentTo(render)
        self.actor.setScale(0.2)
        
    def distanceToTarget(self):
        return math.sqrt((self.actor.getX() - self.target.getX())**2 + (self.actor.getY() - self.target.getY())**2 )#+ (self.actor.getZ() - self.target.getZ()))
     
    def setupAI(self, target):
        """ Start the enemy's AI """
        self.target = target
        self.AIchar = AICharacter("enemy",self.actor,100,0.05,self.maxspeed)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        self.AIbehaviors.evade(self.target,2,10,1.0)
        self.AIbehaviors.pursue(self.target,1.0)
        self.AIbehaviors.wander(4,3,100,0.5)
        self.pause_e()
        self.resume_e()
        self.actor.loop("run")
        return self.AIchar
        
    def updateAI(self,game):
        self.pause_e()
        if self.distanceToTarget() > 40 or self.pursue_start:
            self.pursue_start = True
            self.evade_start = False
            self.AIbehaviors.pursue(game.player.actor,1.0)
        else:
            self.pursue_start = False
            self.evade_start = True
            self.AIbehaviors.flee(game.player.actor,30,10,0.5)
            
        if self.distanceToTarget() <= 20:
            self.pursue_start = False
        if self.distanceToTarget() > 100:
            self.evade_start = False
            
        self.resume_e()
            
        #print "%s ::: %s ::: %s" % (self.AIbehaviors.behaviorStatus("pursue"),self.AIbehaviors.behaviorStatus("flee"),self.AIbehaviors.behaviorStatus("wander"))
    
    def updateHeight(self,game):
        startpos = self.actor.getPos()
        self.updateAI(game)
        self.fire(game)
        entries = []
        for i in range(self.ralphGroundHandler.getNumEntries()):
            entry = self.ralphGroundHandler.getEntry(i)
            entries.append(entry)
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if (len(entries)>1) and (entries[1].getIntoNode().getName() == "terrain"):
            self.actor.setZ(entries[1].getSurfacePoint(render).getZ()+1)
        else:
            self.actor.setPos(startpos)
        self.actor.setHpr(self.actor.getH(),0,0)
        
        # Keep enemy within bounds (HACK)
        if self.actor.getX() > 50:
            self.actor.setPos(50,self.actor.getY(),self.actor.getZ())
        if self.actor.getX() < -50:
            self.actor.setPos(-50,self.actor.getY(),self.actor.getZ())
        if self.actor.getY() < -50:
            self.actor.setPos(self.actor.getX(),-50,self.actor.getZ())
        if self.actor.getX() > 50:
            self.actor.setPos(self.actor.getX(),50,self.actor.getZ())
        
        return Task.cont
    
    #AI Controls
    def pause_e(self):
        self.AIbehaviors.pauseAi("pursue")
        self.AIbehaviors.pauseAi("evade")
        self.AIbehaviors.pauseAi("flee")
        self.AIbehaviors.pauseAi("wander")
        
    def resume_e(self):
        self.AIbehaviors.resumeAi("wander")
    
    def fire(self,game):
        # Get the angle between current heading and that looking directly at the player
        h1 = self.actor.getH()
        self.actor.lookAt(game.player.actor)
        h2 = self.actor.getH()
        self.actor.setH(h1)
        hpr = self.actor.getHpr()
        h = math.fabs(h1 - h2) - 180
        
        # Firing angle and fire rate code
        if math.fabs(h) < 15 and self.timer <= 0:
            ## Put firing code here
            print h
            b1 = bullets.Bullet(self)
            b2 = bullets.Bullet(self)
            b3 = bullets.Bullet(self)
            b1.bulletNP.setZ(2)
            b2.bulletNP.setZ(2)
            b3.bulletNP.setZ(2)
            b1.bulletNP.setH(self.actor.getH() + h)
            b2.bulletNP.setH(self.actor.getH() + h)
            b3.bulletNP.setH(self.actor.getH() + h)
            self.timer = self.fire_rate
        else:
            self.timer -= 1
        
    def die(self):
        taskMgr.remove(self.heightTask)
        
class Enemy2(object):
    def __init__(self):
        self.health = 20
        self.value = 10
        
class Enemy3(object):
    def __init__(self):
        self.health = 20
        self.value = 10
        
class Enemy4(object):
    def __init__(self):
        self.health = 20
        self.value = 10
