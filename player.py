import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions

class Player(DirectObject):
    def __init__(self, game):
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
        self.actor = Actor("models/ralph",
                            {"run":"models/ralph-run",
                             "walk":"models/ralph-walk"})
        self.actor.reparentTo(render)
        self.actor.setScale(0.2)
        self.actor.setPos(game.player_start)
        
        camera.setPos(self.actor.getX(),self.actor.getY()+10,7)
        camera.lookAt(self.actor)
        
        self.selected_weapon = "SMG"
        taskMgr.add(self.move, "PlayerMove", extraArgs= [game])
        
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()
    
    def move(self, game):
        if not game.paused:
            camera.lookAt(self.actor)
            if game.keyMap["left"]:
                self.actor.setX(self.actor,  25 * globalClock.getDt())
            if game.keyMap["right"]:
                self.actor.setX(self.actor, - 25 * globalClock.getDt())
            if game.keyMap["forward"]:
                self.actor.setY(self.actor, - 25 * globalClock.getDt())
            if game.keyMap["back"]:
                self.actor.setY(self.actor,  25 * globalClock.getDt())
                
            # Basic Camera Repositioning, need to tweak.
            camvec = self.actor.getPos() - base.camera.getPos()
            camvec.setZ(0)
            camdist = camvec.length()
            camvec.normalize()
            if (camdist > 10.0):
                camera.setPos(camera.getPos() + camvec*(camdist-10))
                camdist = 10.0
            if (camdist < 5.0):
                camera.setPos(camera.getPos() - camvec*(5-camdist))
                camdist = 5.0
                
        return Task.cont
    
    def die(self):
        pass
        # Call the game over stuffs
       