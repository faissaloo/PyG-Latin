#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyG import *
class player():
	def __init__(self):
		self.y=0.0
		self.x=0.0

	def step(self):
		if (keyboard_check_pressed(97.0)):
			self.x-=1.0

		elif (keyboard_check_pressed(100.0)):
			self.x+=1.0

		elif (keyboard_check_pressed(119.0)):
			self.y-=1.0

		elif (keyboard_check_pressed(115.0)):
			self.y+=1.0


	def draw(self):
		draw_point(self.y,self.x)

class mobTest():
	def __init__(self):
		self.y=0.0
		self.x=0.0

	def step(self):
		if (randrange(0.0,2.0)):
			self.x-=1.0

		if (randrange(0.0,2.0)):
			self.x+=1.0

		if (randrange(0.0,2.0)):
			self.y-=1.0

		if (randrange(0.0,2.0)):
			self.y+=1.0


	def draw(self):
		draw_point(self.y,self.x)

class ctrl():
	def draw(self):
		draw_text(3.0,4.0,"Topdown Game Demo")

class rm1():
	def __init__(self):
		room_speed=60.0
		room_width=24.0
		room_height=88.0
		nstance_create(10.0,10.0,player)
		instance_create(3.0,4.0,ctrl)
		instance_create(20.0,20.0,mobTest)
		instanceList=[]
current_room=rm1()
game_init()
game_main()