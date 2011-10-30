import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions

class Player(object):
    def __init__(self):
        # Set ALL the variables!
        self.health = 100
        self.speed = 0
        self.shotgun_ammo = 32
        self.shotgun_mag = 8
        self.shotgun_can_fire = True
        self.shotgun_fire_rate = 10
        self.shotgun_fire_counter = 0
        self.shotgun_reloading = False
        self.shotgun_reload_time = 20
        self.shotgun_reload_counter = 0
        self.mortars = 12
        self.mortar_loaded = True
        self.mortar_load_time = 40
        self.mortar_load_counter = 0
        self.smg_mag = 30
        self.smg_reload_time = 10
        self.smg_reload_counter = 0
        self.smg_burst_count = 3
        self.smg_fire_rate = 5
        self.smg_fire_counter = 0
        
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()
            
    def die(self):
        pass
        # Call the game over stuffs
       