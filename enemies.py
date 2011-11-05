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
        self.AIchar = AICharacter("enemy",self.actor,100,0.05,5)
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
            
        if self.distanceToTarget() < 2:
            self.pursue_start = False
        if self.distanceToTarget() > 10:
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
        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            self.actor.setZ(entries[0].getSurfacePoint(render).getZ())
        else:
            self.actor.setPos(startpos)
        self.actor.setHpr(self.actor.getH(),0,0)
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
        heading = self.actor.getH()
        player_angle = math.degrees(math.arctan((self.actor.getX()-game.player.actor.getX())**2 + (self.actor.getY()-game.player.actor.getY())**2))
        angle_to_player = heading - playerangle
        
        print "%s ::: %s ::: %s" %(heading,player_angle,angle_to_player)
        if self.pursue_start:
            print "PEWPEW!"
            pass
    
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
