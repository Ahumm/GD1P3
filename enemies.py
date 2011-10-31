# Generic block of import statements!
import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions
from panda3d.ai import * # AI logic

#Class for each enemy, lot of (planned) variance, seemed easier than subclassing, feel free to change
class Enemy1(object):
    def __init__(self,startPos):
        self.health = 20
        self.value = 10
        
        # Load the enemy model and set the initial position of it
        self.loadModel()
        self.actor.setPos((0,0,0))
    
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
        self.AIbehaviors.seek(self.target,0.5)
        #self.AIbehaviors.flee(self.target,1,2,0.4)
        self.AIbehaviors.wander(0.5,0,0.5,0.2)
        return self.AIchar
        
    def setBehavior(self):
        pass
        
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
