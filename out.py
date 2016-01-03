#!/usr/bin/env python3
from PyG import *
class player():
	def __init__(self):
		pass
	def step(self):
		if (1.0+1.0):
			x-=1.0

		if (keyboard_check_pressed(100.0)):
			x+=1.0


	def draw(self):
		draw_point(y,x)

class rm1():
	def __init__(self):
		instance_create(10.0,10.0,player)
		instanceList=[]
current_room=rm1
game_init()
game_main()