import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject

class World(DirectObject):
	def __init__(self):
		base.disableMouse()
		self.speed = 0
		self.throttle = 0
		self.maxSpeed = 200
		self.accel = 25
		self.handling = 20
		base.setBackgroundColor(0,0,0)
		self.track = loader.loadModel("Track.egg")
		self.track.reparentTo(render)
		self.track.setPos(0,0,-5)
		self.cycle = loader.loadModel("car.egg")
		self.cycle.reparentTo(render)
		self.cycle.setPos(1,15,0)
		base.camera.reparentTo(self.cycle)
		base.camera.setY(base.camera, -10)
		self.keyMap = {"w" : False, "s" : False, "a" : False, "d" : False, "mouse1" : False, "mouse3" : False}
		taskMgr.add(self.cycleControl, "Cycle Control")
		taskMgr.doMethodLater(10, self.debugTask, "Debug Task")
		self.accept("w", self.setKey, ["w", True])
		self.accept("s", self.setKey, ["s", True])
		self.accept("a", self.setKey, ["a", True])
		self.accept("d", self.setKey, ["d", True])
		self.accept("w-up", self.setKey, ["w", False])
		self.accept("s-up", self.setKey, ["s", False])
		self.accept("a-up", self.setKey, ["a", False])
		self.accept("d-up", self.setKey, ["d", False])
		self.accept("mouse1", self.setKey, ["mouse1", True])
		self.accept("mouse3", self.setKey, ["mouse3", True])
		self.accept("mouse1-up", self.setKey, ["mouse1", False])
		self.accept("mouse3-up", self.setKey, ["mouse3", False])
		
	def setKey(self, key, value):
		self.keyMap[key] = value
		
	def cycleControl(self, task):
		dt = globalClock.getDt()
		if(dt > .20):
			return task.cont
		if(self.keyMap["w"] == True):
			self.adjustThrottle("up", dt)
		elif(self.keyMap["s"] == True):
			self.adjustThrottle("down", dt)
		if(self.keyMap["d"] == True):
			self.turn("r", dt)
		elif(self.keyMap["a"] == True):
			self.turn("1", dt)
		if(self.keyMap["mouse1"] == True):
			self.cameraZoom("in", dt)
		elif(self.keyMap["mouse3"] == True):
			self.cameraZoom("out",dt)
		if(base.mouseWatcherNode.hasMouse() == True):
			mpos = base.mouseWatcherNode.getMouse()
			base.camera.setP(mpos.getY() * 30)
			base.camera.setH(mpos.getX() * -30)
		self.speedCheck(dt)
		self.move(dt)
		return task.cont
		
	def cameraZoom(self, dir, dt):
		if(dir == "in"): base.camera.setY(base.camera, 10 * dt)
		else: base.camera.setY(base.camera, -10 * dt)
		
	def turn(self, dir, dt):
		turnRate = self.handling * (2 - (self.speed / self.maxSpeed))
		if(dir == "r"): turnRate = -turnRate
		self.cycle.setH(self.cycle, turnRate * dt)
	
	def adjustThrottle(self, dir, dt):
		if(dir == "up"):
			self.throttle += .25 * dt
			if(self.throttle > 1): self.throttle = 1
		else:
			self.throttle -= .25 * dt
			if(self.throttle < -1): self.throttle = -1
		
	def debugTask(self, task):
		print(taskMgr)
		taskMgr.removeTasksMatching("Cycle Move *")
		return task.again
		
	def speedCheck(self, dt):
		tSetting = (self.maxSpeed * self.throttle)
		if(self.speed < tSetting):
			if((self.speed + (self.accel * dt)) > tSetting):
				self.speed = tSetting
			else:
				self.speed += (self.accel * dt)
		elif(self.speed > tSetting):
			if((self.speed - (self.accel * dt)) < tSetting):
				self.speed = tSetting
			else:
				self.speed -= (self.accel * dt)
	
	def move(self,dt):
		mps = self.speed * 1000 /3600
		self.cycle.setY(self.cycle, mps * dt)
w = World()
run()