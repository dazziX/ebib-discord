import random
from PIL import Image
from io import BytesIO

dvdcol = ["red.png", "green.png", "blue.png", "orange.png", "purple.png", "white.png", "yellow.png"]

"""
dvdcol0 = ["/home/dazzix/facebookbot/dvdbot/green.png", "/home/dazzix/facebookbot/dvdbot/blue.png", "/home/dazzix/facebookbot/dvdbot/orange.png", "/home/dazzix/facebookbot/dvdbot/purple.png", "/home/dazzix/facebookbot/dvdbot/white.png", "/home/dazzix/facebookbot/dvdbot/yellow.png"]
dvdcol1 = ["/home/dazzix/facebookbot/dvdbot/red.png", "/home/dazzix/facebookbot/dvdbot/blue.png", "/home/dazzix/facebookbot/dvdbot/orange.png", "/home/dazzix/facebookbot/dvdbot/purple.png", "/home/dazzix/facebookbot/dvdbot/white.png", "/home/dazzix/facebookbot/dvdbot/yellow.png"]
dvdcol2 = ["/home/dazzix/facebookbot/dvdbot/red.png", "/home/dazzix/facebookbot/dvdbot/green.png", "/home/dazzix/facebookbot/dvdbot/orange.png", "/home/dazzix/facebookbot/dvdbot/purple.png", "/home/dazzix/facebookbot/dvdbot/white.png", "/home/dazzix/facebookbot/dvdbot/yellow.png"]
dvdcol3 = ["/home/dazzix/facebookbot/dvdbot/red.png", "/home/dazzix/facebookbot/dvdbot/green.png", "/home/dazzix/facebookbot/dvdbot/blue.png", "/home/dazzix/facebookbot/dvdbot/purple.png", "/home/dazzix/facebookbot/dvdbot/white.png", "/home/dazzix/facebookbot/dvdbot/yellow.png"]
dvdcol4 = ["/home/dazzix/facebookbot/dvdbot/red.png", "/home/dazzix/facebookbot/dvdbot/green.png", "/home/dazzix/facebookbot/dvdbot/blue.png", "/home/dazzix/facebookbot/dvdbot/orange.png", "/home/dazzix/facebookbot/dvdbot/white.png", "/home/dazzix/facebookbot/dvdbot/yellow.png"]
dvdcol5 = ["/home/dazzix/facebookbot/dvdbot/red.png", "/home/dazzix/facebookbot/dvdbot/green.png", "/home/dazzix/facebookbot/dvdbot/blue.png", "/home/dazzix/facebookbot/dvdbot/orange.png", "/home/dazzix/facebookbot/dvdbot/purple.png", "/home/dazzix/facebookbot/dvdbot/yellow.png"]
dvdcol6 = ["/home/dazzix/facebookbot/dvdbot/red.png", "/home/dazzix/facebookbot/dvdbot/green.png", "/home/dazzix/facebookbot/dvdbot/blue.png", "/home/dazzix/facebookbot/dvdbot/orange.png", "/home/dazzix/facebookbot/dvdbot/purple.png", "/home/dazzix/facebookbot/dvdbot/white.png"]
"""


rndx = random.randint(0, 624)
rndy = random.randint(0, 510)
rndcol = random.choice(dvdcol)
rndc = rndcol.split(".")
haha1 = ["neg", "pos"]
haha2 = ["neg", "pos"]
randirx = random.choice(haha1)
randiry = random.choice(haha2)
print("Current color: " + rndc[0])

def createFrame():
	background = Image.open("screen.jpg")
	foreground = Image.open(rndcol)

	background.paste(foreground, (rndx, rndy), foreground)
	return background

def setCol():
	global rndcol, dvdcol
	dvdcol.remove(rndcol)
	rndcol = random.choice(dvdcol)

def ranDirection():
	global rndx, rndy, randirx, randiry
	if randirx == "neg":
		rndx -= 5

	if randirx == "pos":
		rndx += 5

	if randiry == "neg":

		rndy -= 5
	if randiry == "pos":

		rndy += 5
	
def wallHit():
	global rndc
	rndc = rndcol.split(".")
	print("Wallhit at X: " + str(rndx) + " Y: " + str(rndy))
	print("Color changed to: " + rndc[0])

# Create the frames
def make_gif():
	global randirx, randiry
	frames = []
	for i in range(40):
		new_frame = createFrame()
		frames.append(new_frame)
		if rndx >= 624:
			if randirx == "pos":
				randirx = "neg"
				setCol()
				wallHit()
		if rndx <= 0:
			if randirx == "neg":
				randirx = "pos"
				setCol()
				wallHit()
		if rndy >= 510:
			if randiry == "pos":
				randiry = "neg"
				setCol()
				wallHit()
		if rndy <= 0:
			if randiry == "neg":
				randiry = "pos"
				setCol()
				wallHit()
		if rndx >= 624 and rndy >= 510 or rndx <= 0 and rndy <= 0 or rndx >= 624 and rndy <= 0 or rndx <= 0 and rndy >= 510:
			print("CORNERHIT!!!!")



		ranDirection()


	# Save in BytesIO
	animated = BytesIO()
	frames[0].save(animated, format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)
	animated.seek(0)
	return animated
	
	

