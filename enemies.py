# Generic block of import statements!
import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions

#Class for each enemy, lot of (planned) variance, seemed easier than subclassing, feel free to change
class Enemy1(object):
    def __init__(self):
        self.health = 20
        self.value = 10
    
    def take_damage(self, damage):
        if self.health > 0:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                return self.value
        return 0
        
    def setBehavior(self):
        pass
        
class Enemy2(object):
    def __init__(self):
        self.health = 20
        self.value = 10
    
    def take_damage(self, damage):
        if self.health > 0:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                return self.value
        return 0
        
class Enemy3(object):
    def __init__(self):
        self.health = 20
        self.value = 10
    
    def take_damage(self, damage):
        if self.health > 0:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                return self.value
        return 0
        
class Enemy4(object):
    def __init__(self):
        self.health = 20
        self.value = 10
    
    def take_damage(self, damage):
        if self.health > 0:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                return self.value
        return 0