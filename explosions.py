import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions
import sys, math, random


class Explosion(object):
    def __init__(self, position, textures, scale):
        self.exp_plane = loader.loadModel('models/plane')
        self.exp_plane.node().setEffect(BillboardEffect.makePointEye())
        self.exp_plane.setScale(20)
        self.exp_plane.reparentTo(render)
        self.exp_plane.setTransparency(1)
        self.exp_plane.setPos(position)
        self.exp_task = taskMgr.add(self.textureMovie, "explosion")
        self.exp_task.fps = 60
        self.exp_task.obj = self.exp_plane
        self.exp_task.textures = textures
        
    def textureMovie(self, task):
        currentFrame = int(task.time * task.fps)
        if currentFrame < len(task.textures):
            task.obj.setTexture(task.textures[currentFrame % len(task.textures)], 1)
            return task.cont
        else:
            self.exp_plane.removeNode()
            self = None

class Explosions_Manager(object):
    def __init__(self):
        # Load ALL the images!
        self.exp_tex = self.loadTextureMovie(160, 'explosion/explosion', 'png', padding = 4)
        self.mexp_tex = self.loadTextureMovie(120, 'mortar_explosion/mortar_explosion', 'png', padding = 4)
        self.sexp_tex = self.loadTextureMovie(80, 'small_explosion/small_explosion', 'png', padding = 4)
        self.explosion_1 = loader.loadSfx("sounds/explosion_1.wav")
        self.explosion_2 = loader.loadSfx("sounds/explosion_2.wav")
        
        
    def Mortar_Explosion(self, position):
        self.explosion_1.setVolume(0.6)
        self.explosion_1.play()
        Explosion(position, self.mexp_tex, 6)
        
    def Explosion(self, position):
        self.explosion_2.setVolume(0.6)
        self.explosion_2.play()
        Explosion(position,self.exp_tex, 20)
        
    def Small_Explosion(self, position):
        self.explosion_1.setVolume(0.6)
        self.explosion_1.play()
        Explosion(position,self.sexp_tex, 10)

    def loadTextureMovie(self, frames, name, suffix, padding = 1):
        return [loader.loadTexture((name+"%0"+str(padding)+"d."+suffix) % i) 
        for i in range(frames)]