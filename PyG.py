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
import random
from math import *
import engineVars

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
termcolorsAsRGB=[[0,0,0],[170,0,0],[0,170,0],[0,0,170],[170,85,0],[170,0,170],[0,170,170],[170,170,170]]

#Start basic screen drawing stuff
screen=curses.initscr()
curses.start_color()
curses.noecho()
screen.clear()
curses.use_default_colors()
current_color=0
for i in range(0, 8):
    curses.init_pair(i, i, -1)
for i in range(0, 8):
    curses.init_pair(i + 10, i, i)
#Variables
keyboard_lastkey=-1
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
    global current_color
    if round(y)<=engineVars.room_current.room_height and round(x)<=engineVars.room_current.room_width and round(y)>=0 and round(x)>=0:
        screen.addstr(round(y),round(x)," ",curses.color_pair(current_color+10))

def draw_text(y,x, string):
    global screen
    global current_color
    backwardsOffset=0
    currentLineLength=0
    yOffset=0
    i=0
    while i<len(str(string)):
        #Replace this with an 'if inside room thing'
        currentLineLength+=1
        if string[i]=="\n":
            backwardsOffset+=currentLineLength
            yOffset+=1
            currentLineLength=0
        else:
            if round(y+yOffset)<=engineVars.room_current.room_height and round(x+i-backwardsOffset)<=engineVars.room_current.room_width and round(y)>=0 and round(x+i)>=0:
                screen.addstr(round(y+yOffset),round(x+i-backwardsOffset),str(string[i]),curses.color_pair(current_color))
        i+=1

def draw_rectangle(y,x,yy,xx,outline):
    if y<yy:
        rnge=range(round(y),round(yy))
    else:
        rnge=range(round(y), round(yy),-1)
    for i in rnge:
        draw_point(i,x)
        draw_point(i,xx)
        if not (outline):
            for ii in range(x+1,xx): #Fill it in
                draw_point(i,ii)
    draw_line(yy,x,yy,xx+1)
    draw_line(y,x,y,xx)
    draw_line(y,xx,yy,xx)
    draw_line(y,x,yy,x)

def draw_circle(y,x,r,outline):
    workingX=r
    workingY=0
    decOverTwo=1-workingX
    while workingY<=workingX:
        if outline:
            draw_point(workingX+x,workingY+y)
            draw_point(workingY+x,workingX+y)
            draw_point(-workingX+x,workingY+y)
            draw_point(-workingY+x,workingX+y)
            draw_point(-workingX+x,-workingY+y)
            draw_point(-workingY+x,-workingX+y)
            draw_point(workingX+x,-workingY+y)
            draw_point(workingY+x,-workingX+y)
        else:
            draw_line(x+workingX,y-workingY,x+workingX,y+workingY)
            draw_line(y+workingY,x-workingX,y+workingY,x+workingX)
            draw_line(y-workingY,x-workingX,y-workingY,x+workingX)
            draw_line(y-workingX,x-workingY,y-workingX,x+workingY)
        workingY+=1
        if decOverTwo<=0:
            decOverTwo+=2 * workingY + 1
        else:
            workingX-=1
            decOverTwo+=2 * (workingY - workingX) + 1

def draw_line(y,x,yy,xx):
    def safeDivide(numerator,divisor):
        if divisor:
            return numerator/divisor
        else:
            return 0
    if x<xx:
        rnge=range(x,xx)
    else:
        rnge=range(x, xx,-1)
    deltaX=xx-x
    deltaY=yy-y
    err=0
    deltaErr=abs(safeDivide(deltaY,deltaX))
    workingY=y
    for i in rnge:
        draw_point(workingY,i)
        err+=deltaErr
        while err>=0.5:
            draw_point(workingY,i)
            if deltaY<0:
                workingY+=1
            else:
                workingY-=1
            err-=1
#Paths are stored as lists of points
def draw_path(y,x,path):
    for i in range(len(path)-1):
        draw_line(path[i][0],path[i][1],path[i+1][0],path[i+1][1])

#Color functions
def make_color_rgb(R,G,B):
    closest=[0,0,0]
    def euclideanDistance(color1, color2):
        return sqrt(sum([(e1-e2)**2 for e1, e2 in zip(color1, color2)]))
    #Find the nearest value to [R,G,B] in termcolorsAsRGB
    for i in termcolorsAsRGB:
        if euclideanDistance([R,G,B],closest)>euclideanDistance([R,G,B],i):
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
#To test use: draw_sprite(image_add("tests/test.bmp"),10,10)
def image_add(fname):
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

#Instance handling functions
def instance_create(y,x,obj):
    inst=obj()
    inst.y=y
    inst.x=x
    engineVars.room_current.instanceList.append(inst)
    return inst

def instance_destroy(obj):
    engineVars.room_current.instanceList.remove(obj)
    obj.destroyed() #Executes the destroyed event

#Collisions
##################################################################
#Function            Checks using   Checks against     Returns
#-----------------------------------------------------------------
#place_free          mask           solid objects      boolean
#place_empty         mask           all objects        boolean
#place_meeting       mask           specified object   boolean
#position_empty      point          all objects        boolean
#position_meeting    point          specified object   boolean
#instance_place      mask           specified object   instance
#instance_position   point          specified object   instance
##################################################################
#collision_
#Checks if a point collides with an instance
def collision_point(y,x,instance):
    inst_collidablePoints=[]
    yy=0
    xx=0
    for i in instance.mask_index:
        yy+=1
        for ii in i:
            xx+=1
            if ii!=None:
                inst_collidablePoints.append((instance.y+yy,instance.x+xx))
    if (y,x) in inst_collidablePoints:
        return True
    else:
        return False

def collision_line(y,x,yy,xx,instance):
    def safeDivide(numerator,divisor):
        if divisor:
            return numerator/divisor
        else:
            return 0
    if x<xx:
        rnge=range(x,xx)
    else:
        rnge=range(x, xx,-1)
    deltaX=xx-x
    deltaY=yy-y
    err=0
    deltaErr=abs(safeDivide(deltaY,deltaX))
    workingY=y
    for i in rnge:
        if collision_point(workingY,i,instance):
            return True
        err+=deltaErr
        while err>=0.5:
            draw_point(workingY,i)
            if deltaY<0:
                workingY+=1
            else:
                workingY-=1
            err-=1
    return False

def collision_circle(y,x,r,instance):
    workingX=r
    workingY=0
    decOverTwo=1-workingX
    while workingY<=workingX:
        if (collision_line(x+workingX,y-workingY,x+workingX,y+workingY,instance) or
            collision_line(y+workingY,x-workingX,y+workingY,x+workingX,instance) or
            collision_line(y-workingY,x-workingX,y-workingY,x+workingX,instance) or
            collision_line(y-workingX,x-workingY,y-workingX,x+workingY,instance)):
            return True
        workingY+=1
        if decOverTwo<=0:
            decOverTwo+=2 * workingY + 1
        else:
            workingX-=1
            decOverTwo+=2 * (workingY - workingX) + 1
    return False
#place_
#Checks if it would be safe to move to a position
def place_free(self,y,x):
    if not hasattr(self,'mask_index'): #Save ourselves some calculations and just return True if there is no mask
        return True

    obj_collidablePoints=[]
    self_collidablePoints=[]
    for i in engineVars.room_current.instanceList:
        if hasattr(i,'solid') and i.solid and hasattr(i,'mask_index'): #Place_free is only supposed to do collisions with solid objects
            yy=0
            xx=0
            for ii in i.mask_index:
                yy+=1
                for iii in ii:
                    xx+=1
                    if iii!=None:
                        obj_collidablePoints.append((i.y+yy,i.x+xx))
    yy=0
    xx=0
    for ii in self.mask_index:
        yy+=1
        for iii in i:
            xx+=1
            if iii!=None:
                points.append((y+yy,x+xx))
    for i in self_collidablePoints:
        if i in obj_collidablePoints: #If one of the collidable points in self is found in obj_collidablePoints
            return False
    return True

#Like place_free but for all objects, not just solid ones
def place_empty(self,y,x):
    if not hasattr(self,'mask_index'): #Save ourselves some calculations and just return True if there is no mask
        return True
    obj_collidablePoints=[]
    self_collidablePoints=[]
    for i in engineVars.room_current.instanceList:
        yy=0
        xx=0
        if hasattr(i,'mask_index'):
            for ii in i.mask_index:
                yy+=1
                for iii in ii:
                    xx+=1
                    if iii!=None:
                        obj_collidablePoints.append((i.y+yy,i.x+xx))
    yy=0
    xx=0
    for i in self.mask_index:
        yy+=1
        for ii in i:
            xx+=1
            if ii!=None:
                self_collidablePoints.append((y+yy,x+xx))
    for i in self_collidablePoints:
        if i in obj_collidablePoints: #If one of the collidable points in self is found in obj_collidablePoints
            return False
    return True
#Room handling functions
def room_goto(room):
    room()

#Random number functions
#Since most of this stuff is already implemented by the builting random.
#module I'll just make aliases for them
irandom=random.randrange
choose=random.choice
random_set_seed=random.seed
random=random.uniform

def game_main():
    start_keyboard_thread()
    while True:
        sleep(1/engineVars.room_current.room_speed)
        screen.clear()
        #Draw
        for i in engineVars.room_current.instanceList:
            if hasattr(i, 'draw'):
                i.draw()
        for i in engineVars.room_current.instanceList:
            if hasattr(i, 'step'):
                i.step()
        screen.refresh()
