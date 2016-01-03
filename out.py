#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyG import *
class player():
	def __init__(self):
		y=0.0
		x=0.0

	def step(self):
		if (1.0+1.0):
			x-=1.0

		if (keyboard_check_pressed(100.0)):
			x+=1.0


	def draw(self):
		a=1.0
		draw_point(y,x)

class rm1():
	def __init__(self):
		room_speed=60.0
		room_width=24.0
		room_height=88.0
		instance_create(10.0,10.0,player)
		instanceList=[]
current_room=rm1
game_init()
game_main()