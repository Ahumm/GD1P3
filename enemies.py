# Generic block of import statements!
import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions
from panda3d.ai import * # AI logic
import math

#Class for each enemy, lot of (planned) variance, seemed easier than subclassing, feel free to change
class Enemy1(object):
    def __init__(self,game):
        self.health = 20
        self.value = 10
        
        # Load the enemy model and set the initial position of it
        self.loadModel()
        self.actor.setPos(game.player_start)
        self.enemy_start_pos = game.player_start
        
        # Enemy Rays
        self.player_cgray = CollisionRay()
        self.player_cgray.setOrigin(0,0,100)
        self.player_cgray.setDirection(0,0,-1)
        self.player_cgcol = CollisionNode("enemy_gray")
        self.player_cgcol.addSolid(self.player_cgray)
        self.player_cgcol.setFromCollideMask(BitMask32.bit(0))
        self.player_cgcol.setIntoCollideMask(BitMask32.allOff())
        self.player_cgcolnp = self.actor.attachNewNode(self.player_cgcol)
        self.player_cghandler = CollisionHandlerQueue()
        game.cTrav.addCollider(self.player_cgcolnp, self.player_cghandler)
        self.player_cgcolnp.show()
        
        self.heightTask = taskMgr.add(self.updateHeight,'EnemyHeight',extraArgs=[game])
    
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
        
    def setupAI(self, target):
        """ Start the enemy's AI """
        self.target = target
        self.AIchar = AICharacter("enemy",self.actor,100,0.05,1)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        #self.AIbehaviors.seek(self.target,0.5)
        self.AIbehaviors.evade(self.target,0.1,10,0.4)
        self.AIbehaviors.pursue(self.target, 0.5)
        self.actor.loop("run")
        self.AIbehaviors.wander(5,0,3,0.5)
        return self.AIchar
        
    def distanceToTarget(self):
        return math.sqrt((self.actor.getX() - self.target.getX())**2 + (self.actor.getY() - self.target.getY())**2 + (self.actor.getZ() - self.target.getZ()))
        
    def updateHeight(self,game):
        # Now update the player's Z coordinate, or don't move at all
        entries = []
        for i in range(self.player_cghandler.getNumEntries()):
            entry = self.player_cghandler.getEntry(i)
            entries.append(entry)
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(), x.getSurfacePoint(render).getZ()))
        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            self.actor.setZ(entries[0].getSurfacePoint(render).getZ()+4)
        else:
            self.actor.setPos(self.enemy_start_pos)
        return Task.cont
    
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
