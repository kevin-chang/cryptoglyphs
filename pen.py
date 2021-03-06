import cairocffi as C
import math, time
from random import uniform
from Tkinter import *

WIDTH, HEIGHT = 960, 540

surf = C.ImageSurface(C.FORMAT_RGB24, WIDTH, HEIGHT)
ctx = C.Context(surf)

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
		
		self.charCount = 0
		self.wordLength = 5
		self.generateWordLength()
		
		self.done = 0
		# self.strokeCount = 0
		
		self.resetPoint()
		
	def randAngle(self):
		return uniform(0, 2.0 * math.pi)
		
	def finalAngle(self):
		return self.angle
		
	def resetPoint(self):	
		self.age = 0
		# paintbrush position = position of cursor
		self.posX = self.cursorX
		self.posY = self.cursorY
		self.newLineIfNeeded()
		# reset all angle values
		self.changeDirection()
		
		# print "posX = %d, posY = %d" % (self.posX, self.posY)
		
		# self.strokeCount += 1
		# print "strokeCount = %d" % self.strokeCount
		
	def newLineIfNeeded(self):
		# x-coord of cursor
		self.cursorX += self.letterSpacing * self.scale
		# if end of line reached, set cursor to start of new line
		if self.cursorX > WIDTH - self.margin:
			self.cursorX = self.margin
			self.cursorY += self.lineHeight * self.scale
		# if end of page reached, done = true
		if self.cursorY > HEIGHT - self.margin:
			self.done = 1
			
	def generateWordLength(self):
		# Word length distribution from:
		# http://norvig.com/mayzner.html
	
		rand100 = uniform(0, 100)
		if rand100 < 2.998:
			self.wordLength = 1
		elif 2.998 <= rand100 < 20.649:
			self.wordLength = 2
		elif 20.649 <= rand100 < 41.16:
			self.wordLength = 3
		elif 41.16 <= rand100 < 55.947:
			self.wordLength = 4
		elif 55.947 <= rand100 < 66.647:
			self.wordLength = 5
		elif 66.647 <= rand100 < 75.035:
			self.wordLength = 6
		elif 75.035 <= rand100 < 82.974:
			self.wordLength = 7
		elif 82.974 <= rand100 < 88.917:
			self.wordLength = 8
		elif 88.917 <= rand100 < 93.354:
			self.wordLength = 9
		elif 93.354 <= rand100 < 96.43:
			self.wordLength = 10
		elif 96.43 <= rand100 < 98.191:
			self.wordLength = 11
		elif 98.191 <= rand100 < 99.149:
			self.wordLength = 12
		elif 99.149 <= rand100 < 99.667:
			self.wordLength = 13
		elif 99.667 <= rand100 < 99.889:
			self.wordLength = 14
		elif 99.889 <= rand100 < 99.965:
			self.wordLength = 15
		elif 99.965 <= rand100:
			self.wordLength = 16
		else:
			# Revert to the average word length of 5
			# if some form of error occurs
			self.wordLength = 5

	def changeDirection(self):
		self.angle = self.randAngle()
		self.dAngle = uniform(-0.005, 0.005)
		self.ddAngle = uniform(-0.0005, 0.0005)
		self.changeDirectionChance = 0.001
		self.dampDAngle = 1.0
		self.dampDDAngle = 1.0
		self.maxLength = uniform(200, 300)
		
		# print "Pen maxLength = %d" % self.maxLength
		
	def step(self):
		# Reset point if max iteration limit reached
		if self.age > self.maxLength:
			self.resetPoint()
			# Increment character count
			self.charCount += 1
			
		# Reset point if the position of the 'paintbrush' is outside the canvas limits
		if (self.posX < 0 or self.posY < 0 or self.posX > WIDTH or self.posY > HEIGHT):
			self.resetPoint()
			self.charCount += 1
			
		# If current character count exceeds the current word length,
		# insert two spaces, reset character count and generate the next word length
		if self.charCount >= self.wordLength:
			self.resetPoint()
			self.resetPoint()
			self.charCount = 0
			self.generateWordLength()
			
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
		ctx.save()
		# move context to brush position
		ctx.move_to(self.posX, self.posY)
		# set ink colour to 90% transparency black
		ctx.set_source_rgba(0, 0, 0, 0.9)
		# arc (xc, yc, radius, angle1, angle2)
		ctx.arc(self.posX, self.posY, self.weight * self.scale, 0, math.pi * 2)
		ctx.fill()
		ctx.restore()
		
class Clef(Pen):
	def __init__(self):
		Pen.__init__(self)
		
		self.scale = 2.0
		
	def finalAngle(self):
		return 2 * math.pi * math.sin(100 * self.angle)
		
	def step(self):
		Pen.step(self)
	
		# Weight increases linearly with iteration count, up to a max of 1
		self.weight = self.age / self.maxLength
		
	def changeDirection(self):
		Pen.changeDirection(self)
	
		self.dAngle = uniform(-0.0005, 0.0005)
		self.ddAngle = 0
		self.maxLength = uniform(500, 1100)
		
class Roboglyph(Pen):
	def finalAngle(self):
		mult = math.pi / 3
		return round(self.angle / mult) * mult
	
class Giraffes(Pen):
	def changeDirection(self):
		Pen.changeDirection(self)
		
		self.angle = -1.0 * math.pi / 2.0
		self.changeDirectionChance = 0.005
		
class Commarabic(Pen):
	def step(self):
		Pen.step(self)
	
		# Weight increases linearly with iteration count, up to a max of 1
		self.weight = self.age / self.maxLength
	
	def changeDirection(self):
		Pen.changeDirection(self)
		
		dAngle = uniform(-0.001, 0.001)
		ddAngle = uniform(-0.005, 0.005)
		changeDirectionChance = 0.5
		dampDAngle = 0.1
		dampDDAngle = 0.1
		maxLength = uniform(200, 800)
	
class BassClef(Pen):
	def __init__(self):
		Pen.__init__(self)
		
		self.scale = 2.0
		
	def finalAngle(self):
		return 2 * math.pi * math.sin(100 * self.angle)
		
	def step(self):
		Pen.step(self)
	
		# Weight decreases linearly with iteration count, from 1.8 to 0
		self.weight = 1.8 * (1.0 - self.age / self.maxLength)
		
	def changeDirection(self):
		Pen.changeDirection(self)
	
		self.dAngle = uniform(-0.0005, 0.0005)
		self.ddAngle = 0
		self.maxLength = uniform(500, 1100)
	
class Staccato(Pen):
	def __init__(self):
		Pen.__init__(self)
		
		self.scale = 2.5
		
	def finalAngle(self):
		return 2 * math.pi * math.sin(100 * self.angle)
		
	def step(self):
		Pen.step(self)
	
		# Weight decreases linearly with iteration count, from 2 to 0
		self.weight = 2.0 * (1.0 - self.age / self.maxLength)
		# Weight = 0.5 for 100 steps, occurring every 200 steps
		if (self.age % 200) < 100:
			self.weight = 0.5
			
	def changeDirection(self):
		Pen.changeDirection(self)
	
		self.dAngle = uniform(-0.0005, 0.0005)
		self.ddAngle = 0
		self.maxLength = uniform(500, 1100)
	
class Madman(Pen):
	def finalAngle(self):
		if self.age % 70 < 60:
			return math.pi * 2 * math.cos(self.angle)
		else:
			return uniform(-1.0 * math.pi, math.pi)
			
	def changeDirection(self):
		Pen.changeDirection(self)
	
		self.weight = uniform(0, 1)
		self.ddAngle = uniform(-0.0001, 0.0001)
		self.changeDirectionChance = 0.1
		self.dampDAngle = 0.9
		self.dampDDAngle = 0.9
		self.maxLength = uniform(500, 1100)


def create():
	if var.get() == 1:
		penStyle = Clef()
		styleName = "Clef "
	elif var.get() == 2:
		penStyle = Roboglyph()
		styleName = "Roboglyph "
	elif var.get() == 3:
		penStyle = Pen()
		styleName = "Loopy "
	elif var.get() == 4:
		penStyle = Giraffes()
		styleName = "Giraffes "
	elif var.get() == 5:
		penStyle = Commarabic()
		styleName = "Commarabic "
	elif var.get() == 6:
		penStyle = BassClef()
		styleName = "Bass Clef "
	elif var.get() == 7:
		penStyle = Staccato()
		styleName = "Staccato "
	elif var.get() == 8:
		penStyle = Madman()
		styleName = "Madman "
	
	# make background parchment coloured
	ctx.new_path()
	ctx.set_source_rgb(235.0/255.0, 213.0/255.0, 161.0/255.0)
	ctx.rectangle(0, 0, WIDTH, HEIGHT)
	ctx.fill()
	
	while (penStyle.done == 0):
		penStyle.step()
		penStyle.draw()

	# save to PNG
	output = styleName + time.strftime("%Y-%m-%d %H.%M.%S") + ".png"
	surf.write_to_png(output)

# Tkinter GUI
root = Tk()
root.wm_title("Cryptoglyphs")
var = IntVar()

msg = StringVar()
instruction = Label( root, textvariable=msg, relief=RAISED )
msg.set(" Select the writing style you'd like to use, \nthen wait for a few seconds!")
instruction.pack()

R1 = Radiobutton(root, text="Clef", variable=var, value=1, command=create)
R1.pack( anchor = W )
R2 = Radiobutton(root, text="Roboglyph", variable=var, value=2, command=create)
R2.pack( anchor = W )
R3 = Radiobutton(root, text="Loopy", variable=var, value=3, command=create)
R3.pack( anchor = W)
R4 = Radiobutton(root, text="Giraffes", variable=var, value=4, command=create)
R4.pack( anchor = W)
R5 = Radiobutton(root, text="Commarabic", variable=var, value=5, command=create)
R5.pack( anchor = W)
R6 = Radiobutton(root, text="Bass Clef", variable=var, value=6, command=create)
R6.pack( anchor = W)
R7 = Radiobutton(root, text="Staccato", variable=var, value=7, command=create)
R7.pack( anchor = W)
R8 = Radiobutton(root, text="Madman", variable=var, value=8, command=create)
R8.pack( anchor = W)

root.mainloop()