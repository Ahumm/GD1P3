import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions
from direct.gui.DirectGui import * #for buttons and stuff
from panda3d.ai import * # AI logic
import sys, math, random

import player
import enemies


class World(DirectObject): #subclassing here is necessary to accept events
    def __init__(self):
        # Marc's stuff
        #turn off mouse control, otherwise camera is not repositionable
        base.disableMouse()
        #camera.setPosHpr(0, -15, 7, 0, -15, 0)
        self.loadModels()
        self.setupLights()
        self.setupCollisions()
        render.setShaderAuto() #you probably want to use this
        
        # Mapping some keys
        self.keyMap = {"left":0, "right":0, "forward":0, "back":0}
        self.accept("escape", self.pause)
        self.accept("l", self.toggle_light)
        self.accept("1", self.setSMG)
        self.accept("2", self.setShotgun)
        self.accept("3", self.setMortar)
        self.accept("w", self.setKey, ["forward", 1])
        self.accept("d", self.setKey, ["right", 1])
        self.accept("a", self.setKey, ["left", 1])
        self.accept("s", self.setKey, ["back",1])
        self.accept("w-up", self.setKey, ["forward", 0])
        self.accept("d-up", self.setKey, ["right", 0])
        self.accept("a-up", self.setKey, ["left", 0])
        self.accept("s-up", self.setKey, ["back", 0])

        # Empty lists to track stuff
        self.enemies = []
        self.bullets = []
        self.mortars = []
        
        # Find the start position
        self.player_start = (0,0,10)
        # Make a player object
        self.player = player.Player(self)
        
        
        #Load Environment
        self.environ = loader.loadModel("models/ground")      
        self.environ.reparentTo(render)
        self.environ.setScale(0.2)
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
        
        #self.player_cgcolnp.show()
       # self.cgcolnp.show()
        #self.cTrav.showCollisions(render)
        
        self.paused = False
        self.setAI()
        
        self.newEnemy = enemies.Enemy1(self.player)
        self.enemies.append(self.newEnemy)
        self.AIworld.addAiChar(self.newEnemy.setupAI(Vec3(5,5,0)))
        
        
    def setKey(self, key, value):
        self.keyMap[key] = value
        
    def setSMG(self):
        self.player.set_weapon("SMG")
    
    def setShotgun(self):
        self.player.set_weapon("Shotgun")
        
    def setMortar(self):
        self.player.set_weapon("Mortar")
        
    def loadModels(self):
        """loads models into the world"""
        pass
        
    def toggle_light(self):
        self.player.toggle_light()
        
    def setupLights(self):
        #ambient light
        self.ambientLight = AmbientLight("ambientLight")
        #four values, RGBA (alpha is largely irrelevent), value range is 0:1
        self.ambientLight.setColor((.25, .25, .25, 1))
        self.ambientLightNP = render.attachNewNode(self.ambientLight)
        #the nodepath that calls setLight is what gets illuminated by the light
        render.setLight(self.ambientLightNP)
        #call clearLight() to turn it off
        
        self.keyLight = DirectionalLight("keyLight")
        self.keyLight.setColor((.6,.6,.6, 1))
        self.keyLightNP = render.attachNewNode(self.keyLight)
        self.keyLightNP.setHpr(0, -26, 0)
        render.setLight(self.keyLightNP)
        self.fillLight = DirectionalLight("fillLight")
        self.fillLight.setColor((.4,.4,.4, 1))
        self.fillLightNP = render.attachNewNode(self.fillLight)
        self.fillLightNP.setHpr(30, 0, 0)
        render.setLight(self.fillLightNP)
        
    def setupCollisions(self):
        pass
        
        
    def pause(self):
        self.paused = True
        self.resume_button = DirectButton(text = ("Resume"), scale = 0.25, command = self.resume_game, pos=(0, 0, 0.4))
        self.exit_button = DirectButton(text = ("Exit"), scale = 0.25, command = self.exit_game, pos=(0, 0, 0))
    
    def setAI(self):
        """ Set up The AI world"""
        # Create the world
        self.AIworld = AIWorld(render)
        
        # Example from the Panda3D manual:
            # Make the AI character
            #self.AIchar = AICharacter("seeker",self.seeker, 100, 0.05, 5)
            # Add the character to the world
            #self.AIworld.addAiChar(self.AIchar)
            # Get the possible AI behaviors
            #self.AIbehaviors = self.AIchar.getAiBehaviors()
            # Set the character's behavior
            #self.AIbehaviors.seek(self.target)
            # Run it
            #self.seeker.loop("run")
        
        # Add the AIworld updater
        taskMgr.add(self.AIUpdate, "AIUpdate")
        
    def AIUpdate(self,task):
        """ Update the AIWorld """
        self.AIworld.update()
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
            
