# Main Driver Functions
# Creates game instance, handles general menu logic

# Import ALL the things!
import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.gui.DirectGui import * #for buttons and stuff
import sys
#Import our game stuff
import game


class Game:
    """Game Instance, contains the menus, world, etc."""
    def __init__(self):
        self.state = None
        self.world = None
        self.cfont = loader.loadFont('Coalition_v2.ttf')
        self.add_menu()

        

        
    def start_game(self):
        self.remove_menu()
        self.world = game.World()
    
    def exit_game(self):
        self.remove_menu()
        sys.exit()
        
    def add_menu(self):
        self.start_button = DirectButton(text = "START", scale = .12, text_font = self.cfont, text_fg = ((0,0,0,1)), command = self.start_game, pos=(0, 0, 0.4))
        self.exit_button = DirectButton(text = ("EXIT"), scale = 0.12, text_font = self.cfont, command = self.exit_game, pos=(0, 0, 0))
        
    def remove_menu(self):
        if self.start_button:
            self.start_button.removeNode()
        if self.exit_button:
            self.exit_button.removeNode()
        
    
# Create game instance
the_game = Game()
# Run
run()