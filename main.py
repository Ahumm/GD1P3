# Main Driver Functions
# Creates game instance, handles general menu logic

# Import ALL the things!
import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.gui.DirectGui import * #for buttons and stuff
import sys
from direct.gui.OnscreenImage import OnscreenImage
#Import our game stuff
import game

class Game:
    """Game Instance, contains the menus, world, etc."""
    def __init__(self, game):
        self.state = None
        self.world = None
        ##self.cfont = loader.loadFont('Coalition_v2.ttf')
        self.add_menu()
        

        
    def start_game(self):
        self.remove_menu()
        self.world = game.World()
    
    def exit_game(self):
        self.remove_menu()
        sys.exit()
        
    def add_menu(self):
        self.bg = OnscreenImage(image = "textures/Title_Screen_Final.png", pos=(0,0,0), scale=(1.35,1,1))
        self.start_button = DirectButton(text = "START", scale = .12, text_fg = ((0,0,0,1)), command = self.start_game, pos=(0, 0, 0.4))
        self.exit_button = DirectButton(text = ("EXIT"), scale = 0.12, command = self.exit_game, pos=(0, 0, 0))
        self.bar = DirectWaitBar(text = "", value = 0, range = 10000, pos = (0,-.9,-.9), relief = DGG.SUNKEN, borderWidth = (.01,.01), barColor = (0,180,0,1))
        self.bar.setSz(0.5)
            
    def remove_menu(self):
        if self.start_button:
            self.bar.finish(9000) 
            self.start_button.removeNode()
        if self.bar:
            self.bar.removeNode()
        if self.bg:
            self.bg.removeNode()
        if self.exit_button:
            self.exit_button.removeNode()
        
    
# Create game instance
the_game = Game(game)
# Run
run()

