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
        self.rotate_counter = 0
        self.rotate_timer = 10
        self.actor = Actor("models/player")
        self.actor.reparentTo(render)
        self.actor.setScale(0.2)
        self.actor.setH(-90)
        self.actor.setPos(game.player_start)
        camera.reparentTo(self.actor)
        camera.setPosHpr(20,10,4,0,0,0)
        #camera.lookAt(self.actor)
        
        # Set Default Weapon
        self.selected_weapon = "SMG"
        
        # Add headlights
        self.left_light = Spotlight('left')
        self.right_light = Spotlight('right')
        self.left_light.setColor(VBase4(1,1,1,1))
        self.right_light.setColor(VBase4(1,1,1,1))
        self.lens = PerspectiveLens()
        self.lens.setFov(16,10)
        self.left_light.setLens(self.lens)
        self.left_light_node = self.actor.attachNewNode(self.left_light)
        self.left_light_node.node().setAttenuation(Vec3(1,0.0,0.0))
        self.left_light_node.setPosHpr(0,3,-1,-90,-10,0)
        self.right_light.setLens(self.lens)
        self.right_light_node = self.actor.attachNewNode(self.right_light)
        self.right_light_node.node().setAttenuation(Vec3(1,0.0,0.0))
        self.right_light_node.setPosHpr(0,-3,-1,-90,-10,0)
        
        # Needed for pitch changes
        self.oldz = self.actor.getZ()
        
        # Add Movement Task
        taskMgr.add(self.move, "PlayerMove", extraArgs= [game])
        
        # Add Rotate Task
        taskMgr.add(self.rotate, "PlayerRotate", extraArgs=[game])
        
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()
            
    def set_weapon(self, weapon):
        self.selected_weapon = weapon
        print "Weapon is now " + weapon
        
        
    def shoot(self, game):
        print "Bang Bang"
    
    def move(self, game):
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
                self.surface_normal_vector = (entries[0].getSurfaceNormal(render))
                print str(self.surface_normal_vector)
                self.actor.setZ(entries[0].getSurfacePoint(render).getZ()+2)
                if self.actor.getZ() > self.oldz:
                    self.actor.setR(500*(0.2-self.surface_normal_vector[2]))
                elif self.actor.getZ() < self.oldz: 
                    self.actor.setR(-500*(0.2-self.surface_normal_vector[2]))
            else:
                self.actor.setPos(self.player_start_pos)
            self.oldz = self.actor.getZ()
            # Basic Camera Repositioning, need to tweak.
            camera.setPosHpr(-45,0,10,0,0,0)
            camera.lookAt(self.actor)
        return Task.cont
        
        
    def toggle_light(self):
        if render.hasLight(self.left_light_node):
            render.clearLight(self.left_light_node)
        else:
            render.setLight(self.left_light_node)
            
        if render.hasLight(self.right_light_node):
            render.clearLight(self.right_light_node)
        else:
            render.setLight(self.right_light_node)
    
    def rotate(self, game):
        if not game.paused:
            if self.selected_weapon is "SMG" or "Shotgun":
                md = base.win.getPointer(0) 
                mouse_x = md.getX() 
                mouse_y = md.getY() 
                if mouse_x < base.win.getXSize()/4:
                    self.actor.setH(self.actor.getH() +  1)
         
                elif mouse_x > 3*base.win.getXSize()/4:
                    self.actor.setH(self.actor.getH() - 1)
                   

        return Task.cont
        
        
    def update_counters(self, game):
        pass
    
    def die(self):
        pass
        # Call the game over stuffs
       