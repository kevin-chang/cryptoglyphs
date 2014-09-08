import cairocffi as C
import math, time
from random import uniform

WIDTH, HEIGHT = 960, 540
output = "pen " + time.strftime("%Y-%m-%d %H.%M.%S") + ".png"

surf = C.ImageSurface(C.FORMAT_RGB24, WIDTH, HEIGHT)
ctx = C.Context(surf)

# fill everything with white
ctx.new_path()
ctx.set_source_rgb(0.9, 0.9, 0.9)
ctx.rectangle(0, 0, WIDTH, HEIGHT)
ctx.fill()  # fill current path

class Pen():
	def __init__(self):
	
		# print("Pen Constructor Called")
		
		self.scale = 1.0
		self.age = 0
		self.angle = 0.0
		self.dAngle = 0.0
		self.ddAngle = 0.0
		self.dampDAngle = 1.0
		self.dampDDAngle = 1.0
		self.changeDirectionChance = 0.0
		self.maxLength = 10000
		self.weight = 2.0
		
		self.margin = min(100, 0.1 * WIDTH)
		self.lineHeight = 30
		self.letterSpacing = 10
		self.cursorX = self.margin
		self.cursorY = self.margin + self.lineHeight * self.scale
		
		self.done = 0
		self.strokeCount = 0
		
		self.resetPoint()
		
	def randAngle(self):
		return uniform(0, 2 * math.pi)
		
	def finalAngle(self):
		return self.angle
		
	def resetPoint(self):
	
		#print("resetPoint() Called")
	
		self.age = 0
		# paintbrush position = position of cursor
		self.posX = self.cursorX
		self.posY = self.cursorY
		self.newLineIfNeeded()
		# reset all angle values
		self.changeDirection()
		
		print "posX = %d, posY = %d" % (self.posX, self.posY)
		
		self.strokeCount += 1
		print "strokeCount = %d" % self.strokeCount
		
	def newLineIfNeeded(self):
	
		#print("newLineIfNeeded() Called")
		
		# x-coord of cursor
		self.cursorX += self.letterSpacing * self.scale
		# if end of line reached, set cursor to start of new line
		if self.cursorX > WIDTH - self.margin:
			self.cursorX = self.margin
			self.cursorY += self.lineHeight * self.scale
		# if end of page reached, done = true
		if self.cursorY > HEIGHT - self.margin:
			self.done = 1

	def changeDirection(self):
	
		#print("changeDirection() Called")
	
		self.angle = self.randAngle()
		self.dAngle = uniform(0, 0.005)
		self.ddAngle = uniform(0, 0.0005)
		self.changeDirectionChance = 0.001
		self.dampDAngle = 1
		self.dampDDAngle = 1
		self.maxLength = 200 + uniform(0, 100)
		print "maxLength = %d" % self.maxLength
		
	def step(self):
	
		#print("step() Called")
	
		# Reset point if max iteration limit reached
		if self.age > self.maxLength:
			self.resetPoint()
			
		# Reset point if the position of the 'paintbrush' is outside the canvas limits
		if (self.posX < 0 or self.posY < 0 or self.posX > WIDTH or self.posY > HEIGHT):
			self.resetPoint()
			
		# Increment count
		self.age += 1
		# Increment paintbrush position by 0.1 * 'scale' * horizontal/vertical component of vector
		self.posX += self.scale * 0.1 * math.cos(self.finalAngle())
		self.posY += self.scale * 0.1 * math.sin(self.finalAngle())
		
		# Increase angle by the magnitude of the 'sub-angle'
		self.dAngle += self.ddAngle
		self.angle += self.dAngle
		
		# Decrease 'sub-angles' by relevant damping factors
		self.dAngle *= self.dampDAngle
		self.ddAngle *= self.dampDDAngle

		# Change direction if the random number generated is less 
		# than the set chance of changing direction
		if uniform(0, 1) < self.changeDirectionChance:
			self.changeDirection()
			
	def draw(self):
	
		#print("draw() Called")
	
		ctx.save()
		# move context to brush position
		ctx.move_to(self.posX, self.posY)
		# set ink colour to 90% transparency black
		ctx.set_source_rgba(0, 0, 0, 0.9)
		# arc (xc, yc, radius, angle1, angle2)
		ctx.arc(self.posX, self.posY, self.weight * self.scale, 0, math.pi * 2)
		ctx.fill()
		ctx.restore()
		
testPen = Pen()
#while (testPen.done == 0) and (testPen.strokeCount < 150):
while (testPen.done == 0):
	testPen.step()
	testPen.draw()

# save to PNG
surf.write_to_png(output)