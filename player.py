import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions
from direct.gui.DirectGui import * #for buttons and stuff
from direct.gui.OnscreenText import OnscreenText
import sys
import bullets
import mortar
import time



class Player(DirectObject):
    def __init__(self, game):
        # Set ALL the variables!
        self.continue_on_screen = False
        self.health = 100
        self.cfont = loader.loadFont('Coalition_v2.ttf')
        self.shotgun_mag = 8
        self.shotgun_can_fire = True
        self.shotgun_fire_rate = 20
        self.shotgun_fire_counter = 0
        self.shotgun_reloading = False
        self.shotgun_reload_time = 120
        self.shotgun_reload_counter = 0
        self.mortar_loaded = True
        self.mortar_load_time = 180
        self.mortar_load_counter = 0
        self.smg_mag = 15
        self.smg_reload_time = 90
        self.smg_reload_counter = 0
        self.smg_burst_count = 1
        self.smg_fire_rate = 30
        self.smg_fire_counter = 0
        self.smg_reloading = False
        self.smg_can_fire = True
        self.rotate_counter = 0
        self.rotate_timer = 10
        self.actor = Actor("models/player")
        self.actor.reparentTo(render)
        self.actor.setScale(0.2)
        self.actor.setH(-90)
        self.actor.setPos(0,0,4)
        self.max_velocity = 45
        self.max_negative_velocity = -45
        self.x_vel = 0
        self.y_vel = 0
        self.min_velocity = 0
        self.acceleration = 1
        self.drift = 0.5
        self.min_expo = 50
        self.max_expo= 100
        self.expo = 75
        self.expo_increasing = True
        self.min_bob = -0.1
        self.max_bob = 0.1
        self.bob = 0
        self.bob_rate = 0.005
        self.bob_up = False
        camera.reparentTo(self.actor)
        camera.setPosHpr(20,10,4,0,0,0)
        self.last_shot_fired = 0.0
        self.dt = globalClock.getDt()
        #camera.lookAt(self.actor)
        
        # Collision for bullets
        self.cTrav = CollisionTraverser()
        self.cHandler = CollisionHandlerQueue()
        self.cSphere = CollisionSphere(0,0,0,7)
        self.cNode = CollisionNode("Player")
        self.cNode.addSolid(self.cSphere)
        self.cNodePath = self.actor.attachNewNode(self.cNode)
        #self.cNodePath.show()
        self.cTrav.addCollider(self.cNodePath, self.cHandler)
        
        
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
        self.left_light_node.node().setAttenuation(Vec3(0.5,0.0,0.0))
        self.left_light_node.setPosHpr(0,3,-1,-90,-10,0)
        self.right_light.setLens(self.lens)
        self.right_light_node = self.actor.attachNewNode(self.right_light)
        self.right_light_node.node().setAttenuation(Vec3(0.5,0.0,0.0))
        self.right_light_node.setPosHpr(0,-3,-1,-90,-10,0)
        
        # Some hover lights
        self.left_hover = Spotlight('left_hover')
        self.left_hover.setColor(VBase4(0,0.1,1,1))
        self.hover_lens = PerspectiveLens()
        self.hover_lens.setFov(36,36)
        self.left_hover_node = self.actor.attachNewNode(self.left_hover)
        self.left_hover_node.node().setAttenuation(Vec3(0.75,0.0,0.0))
        self.left_hover_node.node().setExponent(100)
        self.left_hover.setSpecularColor(VBase4(0.2,0.2,0,1))
        self.left_hover_node.setPosHpr(1,4,-2,-90,-95,0)
        self.right_hover = Spotlight('right_r_hover')
        self.right_hover.setColor(VBase4(0,0,1,1))
        self.right_hover_node = self.actor.attachNewNode(self.right_hover)
        self.right_hover_node.node().setAttenuation(Vec3(0.75,0.0,0.0))
        self.right_hover_node.node().setExponent(100)
        self.right_hover.setSpecularColor(VBase4(0.2,0.2,0,1))
        self.right_hover_node.setPosHpr(1,-4,-2,-90,-95,0)
        render.setLight(self.left_hover_node)
        render.setLight(self.right_hover_node)

        
        
        # Add Movement Task
        taskMgr.add(self.move, "PlayerMove", extraArgs= [game])
        
        # Add Rotate Task
        taskMgr.add(self.rotate, "PlayerRotate", extraArgs=[game])
        
        
        # Hover Task
        taskMgr.add(self.hover, "PlayerHover", extraArgs=[game])
        
        # Hit Task
        taskMgr.add(self.hit_check, "PlayerHit", extraArgs=[game])
        
        # Add Logic Update Task
        taskMgr.add(self.update_counters, "PlayerUpdate", extraArgs=[game])
        
    def take_damage(self, damage, game):
        
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print "DEAD"
            self.die(game)
            
    def set_weapon(self, weapon):
        self.selected_weapon = weapon
        
        
    def hit_check(self, game):
        if not game.paused:
            for i in range(self.cHandler.getNumEntries()):
                entry = self.cHandler.getEntry(i)
                if entry.getIntoNode().getName() == "ball":
                    game.hit.setVolume(0.6)
                    game.hit.play()
                    self.take_damage(10,game)
        return Task.cont
                

    

        
    def fire(self, game):
        if not game.paused:
            if self.selected_weapon == "SMG":
                if self.smg_can_fire:
                    if self.smg_mag >= 1:
                        self.smg_mag -= 1
                        self.smg_fire_counter += self.smg_fire_rate
                        self.smg_can_fire = False
                        game.smg_fire.setVolume(0.8)
                        game.smg_fire.play()
                        b1 = bullets.Bullet(self, game)
                    if self.smg_mag == 0:
                        self.smg_reload_counter +=self.smg_reload_time
                        self.smg_reloading = True
            elif self.selected_weapon == "SHOTGUN":
                if self.shotgun_can_fire:
                    if self.shotgun_mag > 0:
                        self.shotgun_mag -= 1
                        self.shotgun_fire_counter += self.shotgun_fire_rate
                        self.shotgun_can_fire = False
                        game.shotgun_fire.setVolume(0.6)
                        game.shotgun_fire.play()
                        b1 = bullets.Bullet(self,game, True)
                        b2 = bullets.Bullet(self,game, True)
                        b3 = bullets.Bullet(self, game,True)
                        b4 = bullets.Bullet(self, game,True)
                        b5 = bullets.Bullet(self,game, True)
                        b6 = bullets.Bullet(self, game,True)
                        #print "Shotgun fired, " + str(self.shotgun_mag)+" rounds remaining"
                    if self.shotgun_mag == 0:
                        self.shotgun_reload_counter += self.shotgun_reload_time
                        self.shotgun_reloading = True
                        #print "Shotgun reloading"
            elif self.selected_weapon == "MORTAR":
                if self.mortar_loaded:
                    game.mortar_fire.setVolume(0.7)
                    game.mortar_fire.play()
                    self.mortar_loaded = False
                    self.mortar_load_counter += self.mortar_load_time
                    m = mortar.Mortar(self, game)
                    #print "Mortar launched"
    
    def update_counters(self, game):
        if not game.paused:
            if self.selected_weapon == "SMG":
                if not self.smg_can_fire and not self.smg_reloading:
                    if self.smg_fire_counter > 0:
                        self.smg_fire_counter -= 1
                    if self.smg_fire_counter == 0:
                        self.smg_can_fire = True
                if self.smg_reloading:
                    if self.smg_reload_counter > 0:
                        self.smg_reload_counter -= 1
                    if self.smg_reload_counter == 0:
                        self.smg_mag = 15
                        self.smg_reloading = False
                        game.smg_load.setVolume(0.7)
                        game.smg_load.play()
                        self.smg_can_fire = True
                        #print "SMG reloaded"
        
            elif self.selected_weapon =="SHOTGUN":
                if not self.shotgun_can_fire and not self.shotgun_reloading:
                    if self.shotgun_fire_counter > 0:
                        self.shotgun_fire_counter -=1
                    if self.shotgun_fire_counter == 0:
                        self.shotgun_can_fire = True
                if self.shotgun_reloading:
                    if self.shotgun_reload_counter > 0:
                        self.shotgun_reload_counter -= 1
                    if self.shotgun_reload_counter == 0:
                        self.shotgun_mag = 8
                        game.shotgun_load.setVolume(0.7)
                        game.shotgun_load.play()
                        self.shotgun_reloading = False
                        self.shotgun_can_fire = True
                        #print "Shotgun reloaded"
                        
            elif self.selected_weapon == "MORTAR":
                if not self.mortar_loaded:
                    if self.mortar_load_counter > 0:
                        self.mortar_load_counter -= 1
                    if self.mortar_load_counter == 0:
                        game.mortar_load.setVolume(0.7)
                        game.mortar_load.play()
                        self.mortar_loaded = True
                        #print "Mortar loaded"
            
        return Task.cont
            
    def move(self, game):
        if not game.paused:
            self.moving = False
            self.player_start_pos = self.actor.getPos()
            if game.keyMap["left"]:
                self.moving = True
                self.y_vel += self.acceleration
                if self.y_vel > self.max_velocity:
                    self.y_vel = self.max_velocity
          
            if game.keyMap["right"]:
                self.moving = True
                self.y_vel -= self.acceleration
                if self.y_vel < self.max_negative_velocity:
                    self.y_vel = self.max_negative_velocity
               
            if game.keyMap["forward"]:
                self.moving = True
                self.x_vel += self.acceleration
                if self.x_vel > self.max_velocity:
                    self.x_vel = self.max_velocity
                
            if game.keyMap["back"]:
                self.moving = True
                self.x_vel -= self.acceleration
                if self.x_vel < self.max_negative_velocity:
                    self.x_vel = self.max_negative_velocity
               
            if self.moving:
                self.bob = 0
            if  not self.moving:
                if self.x_vel > self.min_velocity:
                    self.x_vel -= self.drift
                    if self.x_vel < self.min_velocity:
                        self.x_vel = self.min_velocity
                elif self.x_vel < self.min_velocity:
                    self.x_vel += self.drift
                    if self.x_vel > self.min_velocity:
                        self.x_vel = self.min_velocity
                if self.y_vel > self.min_velocity:
                    self.y_vel -= self.drift
                    if self.y_vel < self.min_velocity:
                        self.y_vel = self.min_velocity
                elif self.y_vel < self.min_velocity:
                    self.y_vel += self.drift
                    if self.y_vel > self.min_velocity:
                        self.y_vel = self.min_velocity
            
            self.actor.setY(self.actor, self.y_vel * globalClock.getDt())
            self.actor.setX(self.actor, self.x_vel * globalClock.getDt())
            # Check for terrain collisions
            game.cTrav.traverse(render)
            self.cTrav.traverse(render)
            
            # Now update the player's Z coordinate, or don't move at all
            entries = []
            for i in range(game.player_cghandler.getNumEntries()):
                entry = game.player_cghandler.getEntry(i)
                if entry.getIntoNode().getName() != "Player":
                    entries.append(entry)
            entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(), x.getSurfacePoint(render).getZ()))
            if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
                self.actor.setZ(entries[0].getSurfacePoint(render).getZ()+2)
            else:
                self.actor.setPos(self.player_start_pos)
                
            # Check boundaries
            b_entries = []
            for i in range(self.cHandler.getNumEntries()):
                entry = self.cHandler.getEntry(i)
                if entry.getIntoNode().getName() == "fence_c" or "debris":
                    self.actor.setPos(self.player_start_pos)

            
            # Bobbing when still
            
            if self.x_vel == 0 and self.y_vel == 0:
                if not self.bob_up :
                    self.bob -= self.bob_rate
                    if self.bob < self.min_bob:
                        self.bob = self.min_bob
                        self.bob_up = True
                else:
                    self.bob+=self.bob_rate
                    if self.bob > self.max_bob:
                        self.bob=self.max_bob
                        self.bob_up = False
                        
                self.actor.setZ(self.actor.getZ()+self.bob)
            
            camera.setPosHpr(-60,0,13,-90,-10,0)
            if (len(entries)>0):
                if camera.getZ() <= entries[0].getSurfacePoint(render).getZ()+2:
                    camera.setZ(entries[0].getSurfacePoint(render).getZ()+10)
            
            
            
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
            if game.keyMap["rot_left"]:
                self.actor.setH(self.actor.getH() +  1)
            if game.keyMap["rot_right"]:
                self.actor.setH(self.actor.getH() - 1)
                   

        return Task.cont
    
    def hover(self,game):
        if not game.paused: 
            self.left_hover_node.node().setExponent(self.expo)
            self.right_hover_node.node().setExponent(self.expo)

            if self.expo_increasing:
                self.expo += 1
                if self.expo > self.max_expo:
                    self.expo = self.max_expo
                    self.expo_increasing = False
            else:
                self.expo -= 1
                if self.expo < self.min_expo:
                    self.expo = self.min_expo
                    self.expo_increasing = True
                    
        return Task.cont
    
    def die(self, game):
        game.paused = True
        if not self.continue_on_screen:
            self.you_lose = OnscreenText(text = "CONTINUE?", pos = (0, 0), scale = 0.05, font = self.cfont, fg=(180,180,180,1), shadow = (0,0,0,1))
            self.restart_button = DirectButton(text = "CONTINUE", scale = .12, text_font = self.cfont, text_fg = ((0,0,0,1)), command = self.restart_game, extraArgs=[game],pos=(0, 0, 0.5))
            self.exit_button = DirectButton(text = "EXIT", scale = 0.12, text_font = self.cfont, command = self.exit_game, pos=(0, 0, -0.5))
            self.continue_on_screen = True
        
    def remove_menu(self):
        if self.you_lose:
            self.you_lose.removeNode()
        if self.restart_button:
            self.restart_button.removeNode()
        if self.exit_button:
            self.exit_button.removeNode()
    
    def restart_game(self,game):
        game.paused = False
        self.continue_on_screen = False
        game.score += 1
        self.remove_menu()
        self.health = 100
            
    def exit_game(self):
        self.remove_menu()
        sys.exit()
        
       