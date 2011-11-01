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
        self.actor = Actor("models/player")
        self.actor.reparentTo(render)
        self.actor.setScale(0.2)
        self.actor.setH(-90)
        self.actor.setPos(game.player_start)
        
        camera.setPosHpr(self.actor.getX()+20,self.actor.getY()+10,4,0,0,0)
        #camera.lookAt(self.actor)
        
        self.selected_weapon = "SMG"
        
        # Add Movement Task
        taskMgr.add(self.move, "PlayerMove", extraArgs= [game])
        
        # Add Rotate Task
        taskMgr.add(self.rotate, "PlayerRotate", extraArgs=[game])
        
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()
            
    def select_weapon(self, weapon):
        self.selected_weapon = weapon
    
    def move(self, game):
        MOVE = False
        if not game.paused:
            self.player_start_pos = self.actor.getPos()
            if game.keyMap["left"]:
                self.actor.setY(self.actor,  25 * globalClock.getDt())
            if game.keyMap["right"]:
                self.actor.setY(self.actor, - 25 * globalClock.getDt())
            if game.keyMap["forward"]:
                MOVE = True
                self.actor.setX(self.actor,  25 * globalClock.getDt())
            if game.keyMap["back"]:
                self.actor.setX(self.actor, - 25 * globalClock.getDt())
            
            # Check for terrain collisions
            game.cTrav.traverse(render)
            
            # Now update the player's Z coordinate, or don't move at all
            entries = []
            for i in range(game.player_cghandler.getNumEntries()):
                entry = game.player_cghandler.getEntry(i)
                entries.append(entry)
            entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(), x.getSurfacePoint(render).getZ()))
            if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
                self.actor.setZ(entries[0].getSurfacePoint(render).getZ()+4)
            else:
                if MOVE:
                    print "Cant move"
                self.actor.setPos(self.player_start_pos)
                
            # Basic Camera Repositioning, need to tweak.
            camera.setPosHpr(self.actor.getX(),self.actor.getY()+10,self.actor.getZ()+3,self.actor.getH(),0,0)
            camera.lookAt(self.actor)
        return Task.cont
    
    def rotate(self, game):
        if not game.paused:
            if self.selected_weapon is "SMG" or "Shotgun":

                
                
                camera.setPosHpr(self.actor.getX(),self.actor.getY()+10,3,0,0,0)
                camera.lookAt(self.actor)
    
    def die(self):
        pass
        # Call the game over stuffs
       