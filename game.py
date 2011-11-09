import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions
from direct.gui.DirectGui import * #for buttons and stuff
from panda3d.ai import * # AI logic
from direct.gui.OnscreenText import OnscreenText
import sys, math, random

import player
import enemies
import explosions


class World(DirectObject): #subclassing here is necessary to accept events
    def __init__(self):
        # Marc's stuff
        #turn off mouse control, otherwise camera is not repositionable
        base.disableMouse()
        #camera.setPosHpr(0, -15, 7, 0, -15, 0)
        #self.update()
        self.setupLights()
        render.setShaderAuto() #you probably want to use this
        self.cfont = loader.loadFont('Coalition_v2.ttf')
        self.wave_size = 3
        self.max_enemies = 6
        self.score = 0
        self.wave = 0
        
        
        # Mapping some keys
        self.keyMap = {"left":0, "right":0, "forward":0, "back":0, "shoot":0, "rot_left":0, "rot_right":0}
        self.accept("escape", self.pause)
        self.accept("space", self.setKey, ["shoot", 1])
        self.accept("space-up",self.setKey, ["shoot", 0])
        self.accept("e", self.create_explosion)
        self.accept("l", self.toggle_light)
        self.accept("1", self.setSMG)
        self.accept("2", self.setShotgun)
        self.accept("3", self.setMortar)
        self.accept("w", self.setKey, ["forward", 1])
        self.accept("d", self.setKey, ["right", 1])
        self.accept("a", self.setKey, ["left", 1])
        self.accept("s", self.setKey, ["back",1])
        self.accept("arrow_left", self.setKey, ["rot_left",1])
        self.accept("arrow_left-up", self.setKey, ["rot_left",0])
        self.accept("arrow_right", self.setKey, ["rot_right",1])
        self.accept("arrow_right-up", self.setKey, ["rot_right", 0])
        self.accept("mouse1", self.setKey, ["fire", True])
        self.accept("w-up", self.setKey, ["forward", 0])
        self.accept("d-up", self.setKey, ["right", 0])
        self.accept("a-up", self.setKey, ["left", 0])
        self.accept("s-up", self.setKey, ["back", 0])
        self.accept("mouse1-up", self.setKey, ["fire", False])


        # Empty lists to track stuff
        self.enemies = []
        self.bullets = []
        self.mortars = []
        
        
        
        
        # Find the start position
        self.player_start = (0,0,20)
        # Make a player object
        self.player = player.Player(self)
        self.count = 0
        
        
        #Load Environment
        self.environ = loader.loadModel("models/terrain")      
        self.environ.reparentTo(render)
        self.environ.setScale(0.66)
        self.environ.setPos(0,0,0)
        
        # Setup the collision detection rays
        self.cTrav = CollisionTraverser()
        
        
        # Player Rays
        self.player_cgray = CollisionRay()
        self.player_cgray.setOrigin(0,0,100)
        self.player_cgray.setDirection(0,0,-1)
        self.player_cgcol = CollisionNode("player_gray")
        self.player_cgcol.addSolid(self.player_cgray)
        self.player_cgcol.setFromCollideMask(BitMask32.bit(0))
        self.player_cgcol.setIntoCollideMask(BitMask32.allOff())
        self.player_cgcolnp = self.player.actor.attachNewNode(self.player_cgcol)
        self.player_cghandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.player_cgcolnp, self.player_cghandler)
        
        # Ground Rays
        self.cgray=CollisionRay()
        self.cgray.setOrigin(0,0,100)
        self.cgray.setDirection(0,0,-1)
        self.cgcol = CollisionNode("cgray")
        self.cgcol.addSolid(self.cgray)
        self.cgcol.setFromCollideMask(BitMask32.bit(0))
        self.cgcol.setIntoCollideMask(BitMask32.allOff())
        self.cgcolnp = camera.attachNewNode(self.cgcol)
        self.cghandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.cgcolnp, self.cghandler)
        

        
   
        self.paused = False
        self.setAI()

        
        
        self.hud_weapon = OnscreenText(text = "WEAPON: "+ str(self.player.selected_weapon), pos = (0.75, -0.8), scale = 0.07, font = self.cfont, fg=(180,180,180,1), shadow = (0,0,0,1))
        self.hud_health = OnscreenText(text = "HEALTH: "+ str(self.player.health), pos= (-0.9, -0.8), scale = 0.07, font = self.cfont, fg=(180,180,180,1), shadow=(0,0,0,1)) 
        self.hud_ammo = OnscreenText(text = "AMMO: ", pos=(0.75, -0.9), scale=0.07, font = self.cfont, fg=(180,180,180,1), shadow=(0,0,0,1))
        self.hud_wave = OnscreenText(text = "WAVE: "+str(self.wave), pos= (-0.9, -0.9), scale = 0.07, font = self.cfont, fg=(180,180,180,1), shadow=(0,0,0,1))
        self.hud_score = OnscreenText(text = "SCORE: "+str(self.score),pos= (0, -0.9), scale = 0.07, font = self.cfont, fg=(180,180,180,1), shadow=(0,0,0,1))
        # Set the enemy spawn points and frequenct of spawns
        self.wavetimer = 30
        self.spawnlocs = [(-1,-30,0),(3,30,0),(-13,2,0),(13,0,0)]#
        
        self.spawnTask = taskMgr.doMethodLater(2,self.spawnEnemies,'spawnTask')
        
        #self.explosions_handler = explosions.Explosions_Manager()
        self.explosions_handler = explosions.Explosions_Manager()
        
        taskMgr.add(self.update, "update")
        taskMgr.add(self.player_shoot, "Shoot")
        
        
    def create_explosion(self):
        self.explosions_handler.Small_Explosion(VBase3(0,0,3))
        
    def setKey(self, key, value):
        self.keyMap[key] = value
        
    def setSMG(self):
        self.player.set_weapon("SMG")
    
    def setShotgun(self):
        self.player.set_weapon("SHOTGUN")
        
    def setMortar(self):
        self.player.set_weapon("MORTAR")
        
        
    def toggle_light(self):
        self.player.toggle_light()
        
    def player_shoot(self, task):
        if not self.paused:
            if self.keyMap["shoot"]:
                self.player.fire(self)
        return Task.cont
        
    def setupLights(self):
        #ambient light
        self.ambientLight = AmbientLight("ambientLight")
        #four values, RGBA (alpha is largely irrelevent), value range is 0:1
        self.ambientLight.setColor((.5, .5, .4, 1))
        self.ambientLightNP = render.attachNewNode(self.ambientLight)
        #the nodepath that calls setLight is what gets illuminated by the light
        render.setLight(self.ambientLightNP)
        #call clearLight() to turn it off
        
        self.keyLight = DirectionalLight("keyLight")
        self.keyLight.setColor((.6,.6,.6, 1))
        self.keyLightNP = render.attachNewNode(self.keyLight)
        self.keyLightNP.setHpr(0, -26, 0)
        render.setLight(self.keyLightNP)
        """
        self.fillLight = DirectionalLight("fillLight")
        self.fillLight.setColor((.4,.4,.4, 1))
        self.fillLightNP = render.attachNewNode(self.fillLight)
        self.fillLightNP.setHpr(30, 0, 0)
        render.setLight(self.fillLightNP)    """
        
    def pause(self):
        self.paused = True
        self.resume_button = DirectButton(text = ("Resume"), scale = 0.25, command = self.resume_game, pos=(0, 0, 0.4))
        self.exit_button = DirectButton(text = ("Exit"), scale = 0.25, command = self.exit_game, pos=(0, 0, 0))
    
    def setAI(self):
        """ Set up The AI world"""
        # Create the world
        self.AIworld = AIWorld(render)

        # Add the AIworld updater
        taskMgr.add(self.AIUpdate, "AIUpdate")
    
    def spawnEnemies(self,task):
        print "Spawning Wave!"
        task.delayTime = self.wavetimer
        if not self.paused:
            if len(self.enemies) + self.wave_size <= self.max_enemies:
                self.wave += 1
                for i in range(self.wave_size):
                    self.newEnemy = enemies.Enemy3(self,random.choice(self.spawnlocs),"Enemy-%d-%d"%(self.wave,i))    
                    self.enemies.append(self.newEnemy)
                    self.AIworld.addAiChar(self.newEnemy.setupAI(self.player.actor))
        return task.again
    
    def AIUpdate(self,task):
        """ Update the AIWorld """
        if not self.paused:
            self.AIworld.update()
            for e in self.enemies:
                if e.health <= 0:
                    e.die(self)
                    self.enemies.remove(e)
                else:
                    e.updateHeight(self)
        return Task.cont
    
    def resume_game(self):
        self.remove_pause_menu()
        self.paused = False
        
    def exit_game(self):
        self.remove_pause_menu()
        sys.exit()
        
        
    def remove_pause_menu(self):
        if self.resume_button:
            self.resume_button.removeNode()
        if self.exit_button:
            self.exit_button.removeNode()
            
    def update(self, task):
        self.hud_health.setText("HEALTH: " + str(self.player.health))
        self.hud_weapon.setText("WEAPON: " + str(self.player.selected_weapon))
        self.hud_wave.setText("WAVE: " + str(self.wave))
        self.hud_score.setText("SCORE: " + str(self.score))
        if self.player.health <= 25:
            self.hud_health.setFg((180,0,0,1))
        else: 
            self.hud_health.setFg((180,180,180,1))
        if self.player.selected_weapon == "SMG":
            self.hud_ammo.setText("AMMO: " + str(self.player.smg_mag))
            if self.player.smg_mag == 0:
                self.hud_ammo.setFg((180,0,0,1))
            else:
                self.hud_ammo.setFg((180,180,180,1))
        elif self.player.selected_weapon == "SHOTGUN":
            self.hud_weapon.setText("WEAPON: " + self.player.selected_weapon)
            if self.player.shotgun_mag == 0:
                self.hud_ammo.setFg((180,0,0,1))
            else:
                self.hud_ammo.setFg((180,180,180,1))
            self.hud_ammo.setText("AMMO: " + str(self.player.shotgun_mag))
        else:
            self.hud_ammo.setText("LOADED")
            if self.player.mortar_loaded == False:
                self.hud_ammo.setFg((180,0,0,1))
            else:
                self.hud_ammo.setFg((180,180,180,1))
        if self.pause == True:
            print "PAUSED"
        return task.cont
            
