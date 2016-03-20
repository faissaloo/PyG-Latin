#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################LICENCE####################################
#Copyright (c) 2015-2016 Faissal Bensefia
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
import random
import os
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
engineVars.screen_current=curses.initscr()
curses.start_color()
curses.noecho()
engineVars.screen_current.clear()
curses.curs_set(0)
engineVars.screen_current.nodelay(1)
engineVars.screen_current.keypad(1)
curses.mousemask(1)
curses.use_default_colors()
current_color=0
for i in range(0, 8):
    curses.init_pair(i, i, -1)
for i in range(0, 8):
    curses.init_pair(i + 10, i, i)

#Keyboard handling
def keyboard_check(key):
    if (engineVars.keyboard_lastkey==key):
        return True
    else:
        return False

#Drawing functions
#Views
class view():
    def __init__(self,enabled,view_yview,view_xview,view_wview,view_hview):
        self.enabled=enabled
        self.view_xview=view_xview
        self.view_yview=view_yview
        self.view_hview=view_hview
        self.view_wview=view_wview

def draw_set_color(color):
    global current_color
    current_color=color

def draw_point(y,x):
    global current_color
    if engineVars.view_current==None or engineVars.view_current.enabled==False:
        if round(y)<=engineVars.room_current.room_height and round(x)<=engineVars.room_current.room_width and round(y)>=0 and round(x)>=0:
            engineVars.screen_current.addstr(round(y),round(x)," ",curses.color_pair(current_color+10))
    else:
        if (round(y-engineVars.view_current.view_yview)<=engineVars.view_current.view_hview and
            round(x-engineVars.view_current.view_xview)<=engineVars.view_current.view_wview and
            round(y-engineVars.view_current.view_yview)>=0 and
            round(x-engineVars.view_current.view_xview)>=0):
            engineVars.screen_current.addstr(round(y-engineVars.view_current.view_yview),round(x-engineVars.view_current.view_xview)," ",curses.color_pair(current_color+10))

def draw_text(string,y,x):
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
            if engineVars.view_current==None or engineVars.view_current.enabled==False:
                if (round(y+yOffset)<=engineVars.room_current.room_height and
                    round(x+i-backwardsOffset)<=engineVars.room_current.room_width and
                    round(y)>=0 and round(x+i)>=0):
                    engineVars.screen_current.addstr(round(y+yOffset),round(x+i-backwardsOffset),str(string[i]),curses.color_pair(current_color))
            else:
                if (round(y+yOffset-engineVars.view_current.view_yview)<=engineVars.view_current.view_hview and
                    round(x+i-backwardsOffset-engineVars.view_current.view_xview)<=engineVars.view_current.view_wview and
                    round(y-engineVars.view_current.view_yview)>=0 and
                    round(x+i-backwardsOffset-engineVars.view_current.view_xview)>=0):
                    engineVars.screen_current.addstr(round(y+yOffset),round(x+i-backwardsOffset),str(string[i]),curses.color_pair(current_color))
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

#Based on: https://dai.fmph.uniba.sk/upload/0/01/Ellipse.pdf
def draw_ellipse(y,x,yr,xr,outline):
    twoASquare=2*(xr**2)
    twoBSquare=2*(yr**2)
    workingX=xr
    workingY=0
    xChange=(1-2*xr)*(yr**2)
    yChange=xr**2
    ellipseError=0
    stoppingX=twoBSquare*xr
    stoppingY=0
    while stoppingX>=stoppingY:
        if outline:
            draw_point(y+workingY,x+workingX)
            draw_point(y+workingY,x-workingX)
            draw_point(y-workingY,x-workingX)
            draw_point(y-workingY,x+workingX)
        else:
            draw_line(y+workingY,x+workingX,y+workingY,x-workingX)
            draw_line(y-workingY,x+workingX,y-workingY,x-workingX)
        workingY+=1
        stoppingY+=twoASquare
        ellipseError+=yChange
        yChange+=twoASquare
        if ((2*ellipseError+xChange)>0):
            workingX-=1
            stoppingX-=twoBSquare
            ellipseError+=xChange
            xChange+=twoBSquare
    workingX=0
    workingY=yr
    xChange=(yr**2)
    yChange=(xr**2)*(1-2*yr)
    ellipseError=0
    stoppingX=0
    stoppingY=twoASquare*yr
    while stoppingX<=stoppingY:
        if outline:
            draw_point(y+workingY,x+workingX)
            draw_point(y+workingY,x-workingX)
            draw_point(y-workingY,x-workingX)
            draw_point(y-workingY,x+workingX)
        else:
            draw_line(y+workingY,x+workingX,y+workingY,x-workingX)
            draw_line(y-workingY,x+workingX,y-workingY,x-workingX)
        workingX+=1
        stoppingX+=twoBSquare
        ellipseError+=xChange
        xChange+=twoBSquare
        if ((2*ellipseError+yChange)>0):
            workingY-=1
            stoppingY-=twoASquare
            ellipseError+=yChange
            yChange+=twoASquare


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
def draw_path(path,y,x):
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
class sprite():
    def __init__(self,subimages,yorigin,xorigin):
        #Using [:1] so that it just returns 0 if subimages is []
        self.width=len(subimages[:1][:1])
        self.height=len(subimages[:1])
        self.length=len(subimages)
        self.subimages=subimages
        self.yorigin=yorigin
        self.xorigin=xorigin

    def image_add(self,fname):
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
                self.subimages.append(image_array)
                #Update properties and all that jazz
                self.width=len(self.subimages[:1][:1])
                self.height=len(self.subimages[:1])
                self.length=len(self.subimages)

def draw_sprite(sprite,image_index,y,x):
    yy=0
    xx=0
    for i in sprite.subimages[image_index]:
        yy+=1
        xx=0
        for ii in i:
            xx+=1
            if ii!=None:
                draw_set_color(ii)
                draw_point(y+yy-sprite.yorigin,x+xx-sprite.xorigin)
    draw_set_color(c_white)
#To test use: draw_sprite(image_add("tests/test.bmp"),10,10)
def sprite_add(dirname,yorigin,xorigin):
    spr=sprite([],yorigin,xorigin)
    for i in os.listdir(dirname):
        spr.image_add(dirname+i)
    return spr

#Instance handling functions
def instance_create(obj,y,x):
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
def collision_point(instance,y,x):
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

def collision_line(instance,y,x,yy,xx):
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
        if collision_point(instance,workingY,i):
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

def collision_circle(instance,y,x,r):
    workingX=r
    workingY=0
    decOverTwo=1-workingX
    while workingY<=workingX:
        if (collision_line(instance,x+workingX,y-workingY,x+workingX,y+workingY) or
            collision_line(instance,y+workingY,x-workingX,y+workingY,x+workingX) or
            collision_line(instance,y-workingY,x-workingX,y-workingY,x+workingX) or
            collision_line(instance,y-workingX,x-workingY,y-workingX,x+workingY)):
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
    if self.mask_index==[]: #Save ourselves some calculations and just return True if there is no mask
        return True

    obj_collidablePoints=[]
    self_collidablePoints=[]
    for i in engineVars.room_current.instanceList:
        if i.solid: #Place_free is only supposed to do collisions with solid objects
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
    if self.mask_index==[]: #Save ourselves some calculations and just return True if there is no mask
        return True
    obj_collidablePoints=[]
    self_collidablePoints=[]
    for i in engineVars.room_current.instanceList:
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

#Maths functions
def point_direction(y,x,yy,xx):
    return atan2(y-yy,x-xx)/pi*180

#Random number functions
#Since most of this stuff is already implemented by the builting random.
#module I'll just make aliases for them
irandom=random.randrange
choose=random.choice
random_set_seed=random.seed
random=random.uniform

#Vector maths functions
try:
    #Use the faster stuff if numpy is avalible
    import numpy
    vector_dot=numpy.dot
    vector_sub=numpy.subtract
    vector_add=numpy.add
except ImportError:
    def vector_dot(a,b):
        return sum([i*ii for (i, ii) in zip(a, b)])

    def vector_sub(a,b):
        return tuple([i-ii for (i, ii) in zip(a, b)])

    def vector_add(a,b):
        return tuple([i+ii for (i, ii) in zip(a, b)])

    def vector_scale(a,scale):
        return tuple([i*scale for i in a])

    def vector_length(a):
        return sqrt(sum([i**2 for i in a]))

    def vector_normalize(a):
        length=vector_length(a)
        if length!=0:
            return tuple([i/length for i in a])

#3D
def deg2rad(x):
    return pi * x / 180

zscreen=[[]]
def c3d_init():
    global zscreen
    #This is where we're storing all the points that will be drawn
    #They're speres atm, I'll make them voxels later
    zscreen=[]
    #For testing purposes
    #zscreen=[(10,10,20,1),(23,42,12,6)]
    #E.g: zscreen[0]=[[x,y,color],[x,y,color],]

def c3d_draw_projection(direction,y,x,h,w,fov,maxRenderDistance):
    global zscreen
    scale=tan(deg2rad(fov/2))
    imageAspectRatio=w/h
    #rayDirVector=vector_normalize(cos(deg2rad(direction)),sin(deg2rad(direction)),1)
    for screenX in range(w):
        for screenY in range(h):
            rayDirVector=vector_normalize((screenX,screenY,10))
            #Generate ray direction
            #castRay(direction)
            #origin=[i,ii] #x,y
            for i in zscreen:
                #For collision detection code:
                #https://www.cs.unc.edu/~rademach/xroads-RT/RTarticle.html
                #Under 'Intersecting a Sphere
                if i[2]<maxRenderDistance:
                    A=vector_dot(rayDirVector, rayDirVector)
                    dist=vector_sub((x,y,0),i[:3])
                    B= 2 * vector_dot(rayDirVector, dist)
                    C = vector_dot(dist, dist)-1
                    #print(A,B,C)
                    if B **2 - 4 * A * C>0:
                        draw_set_color(i[3])
                        draw_point(screenX,screenY)

                else:
                    #If we've reached the render distance limit break to prevent
                    #lag
                    break

def game_main():
    while True:
        lastCh=engineVars.screen_current.getch()
        if False: #lastCh==curses.KEY_MOUSE:
            mouseEvent=curses.getmouse()
            engineVars.mouse_x=mouseEvent[1]
            engineVars.mouse_y=mouseEvent[2]
            engineVars.mouse_last_button=mouseEvent[4]
        else:
            engineVars.keyboard_lastkey=lastCh
        sleep(1/engineVars.room_current.room_speed)
        engineVars.screen_current.clear()
        engineVars.room_current.instanceList=\
            sorted(engineVars.room_current.instanceList,key=lambda x: x.z)
        #Draw
        for i in engineVars.room_current.instanceList:
            if hasattr(i, 'draw'):
                i.draw()
        for i in engineVars.room_current.instanceList:
            if hasattr(i, 'step'):
                i.step()
        engineVars.screen_current.refresh()
