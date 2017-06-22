import os
from pygame import mixer
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui 

# A simple ping-pong game

#globals
WIDTH = 1000
HEIGHT = 600
PAD_WIDTH = 20
PAD_HEIGHT = 80
vx = 3.0
vy = 2.0
vel_ball = [vx, vy]
delta = 1.1	#increase in velocity per collision
vel_pad = 5
scoreA = 0
scoreB = 0
pos_pad_left = [ [0, HEIGHT/2 - PAD_HEIGHT/2], [PAD_WIDTH, HEIGHT/2 - PAD_HEIGHT/2], [PAD_WIDTH, HEIGHT/2 + PAD_HEIGHT/2], [0, HEIGHT/2 + PAD_HEIGHT/2] ]
pos_pad_right = [ [WIDTH-PAD_WIDTH, HEIGHT/2 - PAD_HEIGHT/2], [WIDTH, HEIGHT/2 - PAD_HEIGHT/2], [WIDTH, HEIGHT/2 + PAD_HEIGHT/2], [WIDTH-PAD_WIDTH, HEIGHT/2 + PAD_HEIGHT/2] ]
pos_ball_init = [WIDTH/2, HEIGHT/2]
pos_ball = pos_ball_init
curr1 = 0
curr2 = 0
rad = 15

#helpers
def reset():
	global vel_ball, pos_ball, vel_init
	vel_ball = [vx, vy]
	pos_ball = [WIDTH/2, HEIGHT/2]

def music():
	# try:
	# 	if(os.name == "nt"): sound = simplegui.load_sound("G/Joker.mp3")
	# 	else: sound = simplegui.load_sound("/home/shashank/city.mp3")
	# 	sound.set_volume(0.7)
	# 	sound.play()
	# except:
	# 	print("Error in playing sound")

	try:
		mixer.init()
		print(os.name)
		if(os.name == "nt"): 
			mixer.music.load('G:\Joker.mp3')
		else: mixer.music.load('/home/shashank/city.mp3')
		mixer.music.play()
	except:
		print("Music file not found")

#handlers
def draw(canvas):
	global pos_pad_left, pos_pad_right, curr1, curr2, scoreA, scoreB, vel_ball, pos_ball, vel_init, pos_ball_init
	#drawing lines
	canvas.draw_line([20, 0], [20, HEIGHT], 1, "White")
	canvas.draw_line([WIDTH-20, 0], [WIDTH-20, HEIGHT], 1, "White")
	canvas.draw_line([WIDTH/2, 0], [WIDTH/2, HEIGHT], 1, "White")
	#scores
	canvas.draw_text(str(scoreA), [WIDTH/4, 20], 18, "White")
	canvas.draw_text(str(scoreB), [3*WIDTH/4, 20], 18, "White")
	#drawing pads
	canvas.draw_polygon(pos_pad_left, 1, "White", "White")
	canvas.draw_polygon(pos_pad_right, 1, "White", "White")
	#drawing ball
	canvas.draw_circle(pos_ball, rad, 1, "White", "White")

	#update position of pads
	if(curr1 == 2 and pos_pad_right[3][1]<=HEIGHT-vel_pad):		#down of right pad and not out of bounds
		pos_pad_right[0][1] += vel_pad
		pos_pad_right[1][1] += vel_pad
		pos_pad_right[2][1] += vel_pad
		pos_pad_right[3][1] += vel_pad
	elif(curr1 == 1 and pos_pad_right[0][1]>=vel_pad):	#up of right
		pos_pad_right[0][1] -= vel_pad
		pos_pad_right[1][1] -= vel_pad
		pos_pad_right[2][1] -= vel_pad
		pos_pad_right[3][1] -= vel_pad
	if(curr2 == 2 and pos_pad_left[3][1]<=HEIGHT-vel_pad):		#down of left pad
		pos_pad_left[0][1] += vel_pad
		pos_pad_left[1][1] += vel_pad
		pos_pad_left[2][1] += vel_pad
		pos_pad_left[3][1] += vel_pad
	elif(curr2 == 1 and pos_pad_left[0][1]>=vel_pad):	#up of left
		pos_pad_left[0][1] -= vel_pad
		pos_pad_left[1][1] -= vel_pad
		pos_pad_left[2][1] -= vel_pad
		pos_pad_left[3][1] -= vel_pad

	#movement of ball
	pos_ball[0] += vel_ball[0]
	pos_ball[1] += vel_ball[1]
	#collision with walls
	if(pos_ball[1]<=rad or pos_ball[1]>=(HEIGHT-1-rad)): vel_ball[1] = -vel_ball[1]
	if(pos_ball[0]<=PAD_WIDTH+rad):
		#check if pad present there
		if(pos_ball[1]>=pos_pad_left[0][1] and pos_ball[1]<=pos_pad_left[3][1]):
			#os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.0003, 1000))
			vel_ball[0] = -vel_ball[0]
			if(vel_ball[0]>=0): vel_ball[0] *= delta
			else: vel_ball[0] -= delta
		else:
			scoreB += 1
			#os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.01, 800))
			reset()
	elif(pos_ball[0]>=WIDTH-PAD_WIDTH-rad):
		#check if pad present there
		if(pos_ball[1]>=pos_pad_right[0][1] and pos_ball[1]<=pos_pad_right[3][1]):
			#os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.0003, 1000))
			vel_ball[0] = -vel_ball[0]
			if(vel_ball[0]>=0): vel_ball[0] *= delta
			else: vel_ball[0] -= delta
		else:
			scoreA += 1
			#os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.01, 800))
			reset()




def keydown(key):
	global curr1, curr2
	if(key == simplegui.KEY_MAP["up"]): curr1=1
	elif(key == simplegui.KEY_MAP["down"]): curr1=2
	elif(key == simplegui.KEY_MAP["w"]): curr2=1
	elif(key == simplegui.KEY_MAP["s"]): curr2=2

def keyup(key):
	global curr1, curr2
	if(key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]): curr1=0
	if(key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]): curr2=0

#frame
frame = simplegui.create_frame("PnigPong", WIDTH, HEIGHT)
music()

#register
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

#start
frame.start()
