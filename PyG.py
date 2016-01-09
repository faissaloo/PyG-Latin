#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################LICENCE####################################
#Copyright (c) 2015 Faissal Bensefia
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
################################################################################
#Imports
#In places I have imported with 'from' because I want the user to also be able to
#Use the functions from that library
from time import sleep
import curses
from threading import Thread
from random import *
from math import *

#Color constants
c_black=0
c_red=1
c_green=2
c_yellow=3
c_blue=4
c_magenta=5
c_cyan=6
c_white=7
#This is based on what it looks like on the default XFCE4 terminal, it's good enough
termcolorsAsRGB=[[0,0,0],[170,0,0],[0,170,0],[170,85,0],[0,0,170],[170,0,170],[0,170,170],[255,255,255]]

#Start basic screen drawing stuff
screen=curses.initscr()
curses.start_color()
curses.noecho()
screen.clear()
curses.use_default_colors()
current_color=0
for i in range(0, 8):
    curses.init_pair(i + 1, i, -1)
for i in range(0, 8):
    curses.init_pair(i + 10, i, i)
#Variables
keyboard_lastkey=-1

#Custom functions
class emptyRm(): #Just a placeholder room for room initialisation
    instanceList=[]
    room_speed=60
    room_width=24
    room_height=88
current_room=emptyRm()
#Keyboard handling
def start_keyboard_thread():
    global keyboard_lastkey
    def checkKey():
        while True:
            global keyboard_lastkey
            keyboard_lastkey=screen.getch()
    Thread(target = checkKey).start()

def keyboard_check(key):
    global keyboard_lastkey
    if (keyboard_lastkey==key):
        return True
    else:
        return False

def keyboard_check_pressed(key):
    global keyboard_lastkey
    if (keyboard_lastkey==int(key)):
        keyboard_lastkey=-1
        return True
    else:
        return False

#Drawing functions
def draw_set_color(color):
    global current_color
    current_color=color

def draw_point(y,x):
    global screen
    global current_room
    global current_color
    if round(y)<current_room.room_width and round(x)<current_room.room_height and round(y)>0 and round(x)>0:
        screen.addstr(round(y),round(x),"█",curses.color_pair(current_color+10))

def draw_text(y,x, string):
    global screen
    global current_room
    global current_color
    for i in range(len(str(string))):
        #Replace this with an 'if inside room thing'
        if round(y)<current_room.room_width and round(x+i)<current_room.room_height and round(y)>0 and round(x+i)>0:
            screen.addstr(round(y),round(x+i),str(string[i]),curses.color_pair(current_color))

def draw_rectangle(y,x,yy,xx,outline):
    for i in range(y,yy+1):
        draw_point(i,x)
        draw_point(i,xx)
        if (outline):
            for ii in range(x+1,xx): #Fill it in
                draw_point(i,ii)

    for i in range(x,xx+1):
        draw_point(y,i)
        draw_point(yy,i)

def draw_circle(y,x,r,outline):
    if outline:
        for i in range(round(r)):
            for ii in range(10*round((2*(pi*r)))):
                #draw_line(y+(cos(ii/10)*i),x+(sin(ii/10)*r),y+(cos((ii/10))*i)+1,x+(sin((ii/10))*r)+1)
                draw_point(y+(cos(ii/10)*i),x+(sin(ii/10)*i))
    else:
        for ii in range(10*round((2*(pi*r)))):
            #draw_line(y+(cos(ii/10)*i),x+(sin(ii/10)*r),y+(cos((ii/10))*i)+1,x+(sin((ii/10))*r)+1)
            draw_point(y+(cos(ii/10)*r),x+(sin(ii/10)*r))
def draw_line(y,x,yy,xx):
    def safeDivide(a,b): #Return 0 if it can't be divided
        try:
            return a/b
        except ZeroDivisionError:
            return 0
    for i in range(round(abs(xx-x))):
        draw_point(y + safeDivide((yy - y) * (i - x) , (xx - x)),x+i)
#Paths are stored as lists of points
def draw_path(y,x,path):
    for i in range(len(path)-1):
        draw_line(path[i][0],path[i][1],path[i+1][0],path[i+1][1])

#Color functions
def make_color_rgb(R,G,B):
    closest=[0,0,0]
    #Find the nearest value to [R,G,B] in termcolorsAsRGB
    for i in termcolorsAsRGB:
        if abs(R-closest[0])>abs(R-i[0]) or abs(G-closest[1])>abs(G-i[1]) or abs(B-closest[2])>abs(B-i[2]):
            closest=i
    return termcolorsAsRGB.index(closest)

#Sprite functions
def draw_sprite(sprite,y,x):
    yy=0
    xx=0
    for i in sprite:
        yy+=1
        xx=0
        for ii in i:
            xx+=1
            if ii!=None:
                draw_set_color(ii)
                draw_point(y+yy,x+xx)
    draw_set_color(c_white)
#To test use: draw_sprite(sprite_add("tests/test.bmp"),10,10)
def sprite_add(fname):
    #Script to read 32-bit bitmaps (with alpha)
    with open(fname,"rb") as file:
        text=file.read()
        if chr(text[0])=="B" and chr(text[1])=="M":
        	pos=text[10] #Tells us the offset
        	image_array=[]
        	pixels=0
        	row=[]
        	while pos<len(text):
        		if pixels%text[18]==0:
        			image_array.insert(0,row)
        			row=[]
        		if text[pos]>254: #Checks the alpha, if it has any transparency, ignore
        			row.append(make_color_rgb(text[pos+1],text[pos+2],text[pos+3]))
        		else:
        			row.append(None)
        		pos+=4
        		pixels+=1
        	return image_array

def sprite_get_height(sprite):
    return len(sprite)

def sprite_get_width(sprite):
    return len(sprite[0])

def redraw():
    screen.refresh()
    screen.clear()

#Instance handling functions
def instance_create(y,x,object):
    global current_room
    inst=object()
    inst.y=y
    inst.x=x
    current_room.instanceList.append(inst)
    return inst

def instance_destroy():
    global current_room
    current_room.instanceList.remove(self)
    self.destroyed() #Executes the destroyed event
#Room handling functions
def room_goto(room):
    global current_room
    current_room=room()

def game_init():
    start_keyboard_thread()

def game_main():
    while True:
        sleep(1/current_room.room_speed)
        #Draw
        for i in current_room.instanceList:
            if hasattr(i, 'draw'):
                i.draw()
        for i in current_room.instanceList:
            if hasattr(i, 'step'):
                i.step()
        redraw()
