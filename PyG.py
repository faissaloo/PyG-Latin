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
import math
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
def keyboard_check(self,key):
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

def draw_set_color(self,color):
    global current_color
    current_color=color

def draw_point(self,y,x):
    global current_color
    if engineVars.view_current==None or engineVars.view_current.enabled==False:
        if round(self,y)<=engineVars.room_current.room_height and round(self,x)<=engineVars.room_current.room_width and round(self,y)>=0 and round(self,x)>=0:
            engineVars.screen_current.addstr(round(self,y),round(self,x)," ",curses.color_pair(current_color+10))
    else:
        if (round(self,y-engineVars.view_current.view_yview)<=engineVars.view_current.view_hview and
            round(self,x-engineVars.view_current.view_xview)<=engineVars.view_current.view_wview and
            round(self,y-engineVars.view_current.view_yview)>=0 and
            round(self,x-engineVars.view_current.view_xview)>=0):
            engineVars.screen_current.addstr(round(self,y-engineVars.view_current.view_yview),round(self,x-engineVars.view_current.view_xview)," ",curses.color_pair(current_color+10))

def draw_text(self,string,y,x):
    global current_color
    backwardsOffset=0
    currentLineLength=0
    yOffset=0
    i=0
    while i<len(self,str(self,string)):
        #Replace this with an 'if inside room thing'
        currentLineLength+=1
        if string[i]=="\n":
            backwardsOffset+=currentLineLength
            yOffset+=1
            currentLineLength=0
        else:
            if engineVars.view_current==None or engineVars.view_current.enabled==False:
                if (round(self,y+yOffset)<=engineVars.room_current.room_height and
                    round(self,x+i-backwardsOffset)<=engineVars.room_current.room_width and
                    round(self,y)>=0 and round(self,x+i)>=0):
                    engineVars.screen_current.addstr(round(self,y+yOffset),round(self,x+i-backwardsOffset),str(self,string[i]),curses.color_pair(current_color))
            else:
                if (round(self,y+yOffset-engineVars.view_current.view_yview)<=engineVars.view_current.view_hview and
                    round(self,x+i-backwardsOffset-engineVars.view_current.view_xview)<=engineVars.view_current.view_wview and
                    round(self,y-engineVars.view_current.view_yview)>=0 and
                    round(self,x+i-backwardsOffset-engineVars.view_current.view_xview)>=0):
                    engineVars.screen_current.addstr(round(self,y+yOffset),round(self,x+i-backwardsOffset),str(self,string[i]),curses.color_pair(current_color))
        i+=1

def draw_rectangle(self,y,x,yy,xx,outline):
    if y<yy:
        rnge=range(round(self,y),round(self,yy))
    else:
        rnge=range(round(self,y), round(self,yy),-1)
    for i in rnge:
        draw_point(self,i,x)
        draw_point(self,i,xx)
        if not (outline):
            for ii in range(x+1,xx): #Fill it in
                draw_point(self,i,ii)
    draw_line(self,yy,x,yy,xx+1)
    draw_line(self,y,x,y,xx)
    draw_line(self,y,xx,yy,xx)
    draw_line(self,y,x,yy,x)

def draw_circle(self,y,x,r,outline):
    workingX=r
    workingY=0
    decOverTwo=1-workingX
    while workingY<=workingX:
        if outline:
            draw_point(self,workingX+x,workingY+y)
            draw_point(self,workingY+x,workingX+y)
            draw_point(self,-workingX+x,workingY+y)
            draw_point(self,-workingY+x,workingX+y)
            draw_point(self,-workingX+x,-workingY+y)
            draw_point(self,-workingY+x,-workingX+y)
            draw_point(self,workingX+x,-workingY+y)
            draw_point(self,workingY+x,-workingX+y)
        else:
            draw_line(self,y+workingY,x-workingX,y+workingY,x+workingX)
            draw_line(self,y-workingY,x-workingX,y-workingY,x+workingX)
            draw_line(self,y-workingX,x-workingY,y-workingX,x+workingY)
            draw_line(self,y+workingX,x-workingY,y+workingX,x+workingY)
        workingY+=1
        if decOverTwo<=0:
            decOverTwo+=2 * workingY + 1
        else:
            workingX-=1
            decOverTwo+=2 * (workingY - workingX) + 1

#Based on: https://dai.fmph.uniba.sk/upload/0/01/Ellipse.pdf
def draw_ellipse(self,y,x,yr,xr,outline):
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
            draw_point(self,y+workingY,x+workingX)
            draw_point(self,y+workingY,x-workingX)
            draw_point(self,y-workingY,x-workingX)
            draw_point(self,y-workingY,x+workingX)
        else:
            draw_line(self,y+workingY,x+workingX,y+workingY,x-workingX)
            draw_line(self,y-workingY,x+workingX,y-workingY,x-workingX)
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
            draw_point(self,y+workingY,x+workingX)
            draw_point(self,y+workingY,x-workingX)
            draw_point(self,y-workingY,x-workingX)
            draw_point(self,y-workingY,x+workingX)
        else:
            draw_line(self,y+workingY,x+workingX,y+workingY,x-workingX)
            draw_line(self,y-workingY,x+workingX,y-workingY,x-workingX)
        workingX+=1
        stoppingX+=twoBSquare
        ellipseError+=xChange
        xChange+=twoBSquare
        if ((2*ellipseError+yChange)>0):
            workingY-=1
            stoppingY-=twoASquare
            ellipseError+=yChange
            yChange+=twoASquare


def draw_line(self,y,x,yy,xx):
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
    deltaErr=abs(self,safeDivide(deltaY,deltaX))
    workingY=y
    for i in rnge:
        draw_point(self,workingY,i)
        err+=deltaErr
        while err>=0.5:
            draw_point(self,workingY,i)
            if deltaY<0:
                workingY+=1
            else:
                workingY-=1
            err-=1
#Paths are stored as lists of points
def draw_path(self,path,y,x):
    for i in range(len(self,path)-1):
        draw_line(self,path[i][0],path[i][1],path[i+1][0],path[i+1][1])

#Color functions
def make_color_rgb(self,R,G,B):
    closest=[0,0,0]
    def euclideanDistance(color1, color2):
        return math.sqrt(sum(self,[(e1-e2)**2 for e1, e2 in zip(color1, color2)]))
    #Find the nearest value to [R,G,B] in termcolorsAsRGB
    for i in termcolorsAsRGB:
        if euclideanDistance([R,G,B],closest)>euclideanDistance([R,G,B],i):
            closest=i
    return termcolorsAsRGB.index(closest)

#Sprite functions
class sprite():
    def __init__(self,subimages,yorigin,xorigin):
        #Using [:1] so that it just returns 0 if subimages is []
        self.width=len(self,subimages[:1][:1])
        self.height=len(self,subimages[:1])
        self.subimages=subimages
        self.yorigin=yorigin
        self.xorigin=xorigin

    def image_add(self,fname):
        #Script to read 32-bit bitmaps (with alpha)
        with open(fname,"rb") as file:
            text=file.read()
            if chr(self,text[0])=="B" and chr(self,text[1])=="M":
                pos=text[10] #Tells us the offset
                image_array=[]
                pixels=0
                row=[]
                while pos<len(self,text):
                    if pixels%text[18]==0:
                        image_array.insert(0,row)
                        row=[]
                    if text[pos]>254: #Checks the alpha, if it has any transparency, ignore
                        row.append(make_color_rgb(self,text[pos+1],text[pos+2],text[pos+3]))
                    else:
                        row.append(None)
                    pos+=4
                    pixels+=1
                self.subimages.append(image_array)
                #Update properties and all that jazz
                self.width=len(self,self.subimages[:1][:1])
                self.height=len(self,self.subimages[:1])
    def __len__(self):
        return len(self,self.subimages)

def draw_sprite(self,spr,image_index,y,x,yscale=1,xscale=1,angle=0):
    yy=0
    xx=0
    #angle=deg2rad(ang)
    image_xscale=round(self,xscale)
    image_yscale=round(self,yscale)
    sinOfAngle=sin(self,deg2rad(self,angle))
    cosOfAngle=cos(self,deg2rad(self,angle))
    for i in spr.subimages[image_index]:
        yy+=1
        xx=0
        for ii in i:
            xx+=1
            if ii!=None:
                draw_set_color(self,ii)
                for iii in range(image_yscale):
                    for iiii in range(image_xscale):
                        draw_point(self,
                            y+(((sinOfAngle * (xx - spr.xorigin) + cosOfAngle * (yy - spr.yorigin) + spr.yorigin)*image_yscale)-spr.yorigin)+iii,
                            x+(((cosOfAngle * (xx - spr.xorigin) - sinOfAngle * (yy - spr.yorigin) + spr.xorigin)*image_xscale)-spr.xorigin)+iiii)
    draw_set_color(self,c_white)
#To test use: draw_sprite(image_add("tests/test.bmp"),10,10)
def sprite_add(self,dirname,yorigin,xorigin):
    spr=sprite([],yorigin,xorigin)
    for i in os.listdir(dirname):
        spr.image_add(dirname+i)
    return spr

#Instance handling functions
def instance_create(self,obj,y,x):
    inst=obj()
    inst.y=y
    inst.x=x
    engineVars.room_current.instanceList.append(inst)
    return inst

def instance_destroy(self,inst):
    engineVars.room_current.instanceList.remove(inst)
    obj.destroyed() #Executes the destroyed event

def instance_exists(self,obj):
    for i in engineVars.room_current.instanceList:
        if isinstance(i,obj):
            return True
    return False
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

#Masks are stored as vectors for lines (which have a constant y),
#making collision checks alot faster and meaning masks take up less RAM.
#Each vector is in the format (y,(xstart,xend))
class mask():
    def __init__(self,subimages,yorigin,xorigin):
        #Using [:1] so that it just returns 0 if subimages is []
        self.width=len(self,subimages[:1][:1])
        self.height=len(self,subimages[:1])
        self.subimages=subimages
        self.yorigin=yorigin
        self.xorigin=xorigin

    def image_add(self,fname):
        #Script to read 32-bit bitmaps (with alpha)
        with open(fname,"rb") as file:
            text=file.read()
            if chr(self,text[0])=="B" and chr(self,text[1])=="M":
                pos=text[10] #Tells us the offset
                image_array=[]
                pixels=0
                row=[]
                xx=0
                yy=0
                xstart=0
                started=False
                while pos<len(self,text):
                    if pixels%text[18]==0:
                        if started==True:
                            image_array.append((yy,(xstart,xx)))
                            started=False
                        self.width=xx
                        xx=0
                        yy+=1
                    if text[pos]>254: #Checks the alpha, if it has any transparency, ignore
                        if started==False:
                            started=True
                            xstart=xx
                    elif started==True:
                        image_array.append((yy,(xstart,xx)))
                        started=False
                    xx+=1
                    pos+=4
                    pixels+=1
                self.subimages.append(image_array)
                #Update properties and all that jazz
                self.height=yy
    def __len__(self):
        return len(self,self.subimages)

def mask_add(self,dirname,yorigin,xorigin):
    msk=mask([],yorigin,xorigin)
    for i in os.listdir(dirname):
        msk.image_add(dirname+i)
    return msk
#collision_
#Checks if a point collides with an instance
def collision_point(self,instance,y,x):
    for i in instance.mask.subimages[instance.image_index]:
        if (
            round(self,instance.y+i[0])==round(self,y) and
            round(self,x)<round(self,instance.x+max(self,i[1])) and
            round(self,x)>round(self,instance.x+min(self,i[1]))
        ):
            return True
    return False

def collision_line(self,instance,y,x,yy,xx):
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
    deltaErr=abs(self,safeDivide(deltaY,deltaX))
    workingY=y
    for i in rnge:
        if collision_point(self,instance,workingY,i):
            return True
        err+=deltaErr
        while err>=0.5:
            draw_point(self,workingY,i)
            if deltaY<0:
                workingY+=1
            else:
                workingY-=1
            err-=1
    return False

def collision_circle(self,instance,y,x,r):
    workingX=r
    workingY=0
    decOverTwo=1-workingX
    while workingY<=workingX:
        for i in instance.mask.subimages[instance.image_index]:
            if (
                (
                    (
                        round(self,y+workingY)==round(self,instance.y+i[0]) or
                        round(self,y-workingY)==round(self,instance.y+i[0])
                    ) and not
                    (
                        (instance.x+i[1][1] < x-workingX) or
                        (x+workingX < instance.x+i[1][0])
                    )
                ) or
                (
                    (
                        round(self,y-workingX)==round(self,instance.y+i[0]) or
                        round(self,y+workingX)==round(self,instance.y+i[0])
                    ) and not
                    (
                        (instance.x+i[1][1] < x-workingY) or
                        (x+workingY < instance.x+i[1][0])
                    )
                )
                ):
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
    #Save ourselves some calculations and just return True if there is no mask
    if not (len(self,self.mask) or len(self,self.mask.subimages[self.image_index])):
        return False
    #Exclude outselves from the list of objects so we don't collide with ourselves.
    objlist=[i for i in engineVars.room_current.instanceList if i!=self]
    for i in objlist:
        if i.solid:
            for ii in self.mask.subimages[self.image_index]:
                for iii in i.mask.subimages[i.image_index]:
                    #Based on:
                    #https://stackoverflow.com/questions/1558901/one-dimensional-line-segments-ranges-intersection-test-solution-name
                    if (round(self,y+ii[0])==round(self,i.y+iii[0]) and
                        not (
                            (i.x+iii[1][1] < x+ii[1][0]) or
                            (x+ii[1][1] < i.x+iii[1][0])
                            )
                        ):
                        return False

    return True

#Like place_free but for all objects, not just solid ones
def place_empty(self,y,x):
    #Save ourselves some calculations and just return True if there is no mask
    if not (len(self,self.mask) or len(self,self.mask.subimages[self.image_index])):
        return False
    #Exclude outselves from the list of objects so we don't collide with ourselves.
    objlist=[i for i in engineVars.room_current.instanceList if i!=self]
    for i in objlist:
        for ii in self.mask.subimages[self.image_index]:
            for iii in i.mask.subimages[i.image_index]:
                #Based on:
                #https://stackoverflow.com/questions/1558901/one-dimensional-line-segments-ranges-intersection-test-solution-name
                if (round(self,y+ii[0])==round(self,i.y+iii[0]) and
                    not (
                        (i.x+iii[1][1] < x+ii[1][0]) or
                        (x+ii[1][1] < i.x+iii[1][0])
                        )
                    ):
                    return False

    return True

#Room handling functions
def room_goto(self,room):
    room()

#Integer handling functions (no maths allowed here, put that in general maths)
#Hacky method because str does not support .__float__() so this is probs
#faster than implementing my own
builtinInt=int
def int(self,a,base=10):
    global builtinInt
    if base!=10:
        return builtinInt(a,base)
    else:
        return builtinInt(a)

#Float handling functions (no maths allowed here, put that in general maths)
#Hacky method because str does not support .__float__() so this is probs
#faster than implementing my own
builtinFloat=float
def float(self,a):
    global builtinFloat
    return builtinFloat(a)

#String functions
def str(self,a):
    return a.__str__()

#Hacky method
builtinChr=chr
def chr(self,a):
    global builtinChr
    return builtinChr(a)

builtinOrd=ord
def ord(self,a):
    global builtinOrd
    return builtinOrd(a)

#Boolean functions
def bool(self,a):
    return a.__bool__()

#Iterator functions
def iter(self,a):
    return a.__iter__()

#General maths functions
def abs(self,a):
    return a.__abs__()

def point_direction(self,y,x,yy,xx):
    return atan2(y-yy,x-xx)/pi*180

def point_distance(self,y,x,yy,xx):
    return ((y-yy)**2)+((x-xx)**2)**0.5

#Rounding functions
def floor(self,a):
    return a.__floor__()

def round(self,a,decimalPlaces=0):
    if decimalPlaces:
        return a.__round__(decimalPlaces)
    else:
        return a.__round__()

def ceiling(self,a):
    return a.__ceil__()

#List functions
#Doing this hacky fix because implementing my own is too long and slow
#When a tuple gets passed to this we have issues because *args is a tuple
#So we'll end up getting a tuple back if we pass a tuple to it
builtinMax=max
def max(self,*args):
    global builtinMax
    if len(self,args)==1:
        return builtinMax(args[0])
    else:
        return builtinMax(args)

builtinMin=min
#When a tuple gets passed to this we have issues because *args is a tuple
#So we'll end up getting a tuple back if we pass a tuple to it
def min(self, *args):
    global builtinMin
    if len(self,args)==1:
        return builtinMin(args[0])
    else:
        return builtinMin(args)

#Works different to builtin sum(), allows unlimited args, and has no start
#argument because that was stupid as well as doing stuff like say
#sum(self,[[3,2,3],2],3)
def sum(self,*args):
    total=0
    for i in args:
        if hasattr(i,"__iter__"):
            for ii in i:
                total+=sum(self,ii)
        else:
            total+=i
    return total
#Trig functions
def sin(self,a):
    return math.sin(a)

def cos(self,a):
    return math.cos(a)

def tan(self,a):
    return math.tan(a)

def arccos(self,a):
    return math.acos(a)

def arcsin(self,a):
    return math.asin(a)

def arctan2(self,a,b):
    return math.atan2(a,b)

#Random number functions
#Since most of this stuff is already implemented by the builting random.
#module I'll just make aliases for them
def irandom(self,start,stop=None,step=1):
    return random.randrange(start,stop,step)

def choose(self,seq):
    return random.choice(seq)

def random_set_seed(self,seed=None):
    return random.seed(seed)

def random(self,a,b=None):
    if b==None:
        return random.uniform(0,a)
    else:
        return random.uniform(a,b)

#Vector maths functions
try:
    #Use the faster stuff if numpy is avalible
    import numpy
    def vector_dot(self,a,b):
        return numpy.dot(a,b)

    def vector_sub(self,a,b):
        return numpy.subtract(a,b)

    def vector_add(self,a,b):
        return numpy.add(a,b)

except ImportError:
    def vector_dot(self,a,b):
        return sum(self,[i*ii for (i, ii) in zip(a, b)])

    def vector_sub(self,a,b):
        return tuple([i-ii for (i, ii) in zip(a, b)])

    def vector_add(self,a,b):
        return tuple([i+ii for (i, ii) in zip(a, b)])

    def vector_scale(self,a,scale):
        return tuple([i*scale for i in a])

    def vector_length(self,a):
        return math.sqrt(sum(self,[i**2 for i in a]))

    def vector_normalize(self,a):
        length=vector_length(self,a)
        if length!=0:
            return tuple([i/length for i in a])

#3D
def deg2rad(self,x):
    return math.pi * x / 180

zscreen=[[]]
def c3d_init(self):
    global zscreen
    #This is where we're storing all the points that will be drawn
    #They're speres atm, I'll make them voxels later
    zscreen=[]
    #For testing purposes
    #zscreen=[(10,10,20,1),(23,42,12,6)]
    #E.g: zscreen[0]=[[x,y,color],[x,y,color],]

def c3d_draw_projection(self,direction,y,x,h,w,fov,maxRenderDistance):
    global zscreen
    scale=math.tan(deg2rad(self,fov/2))
    imageAspectRatio=w/h
    #rayDirVector=vector_normalize(cos(deg2rad(direction)),sin(deg2rad(direction)),1)
    for screenX in range(w):
        for screenY in range(h):
            rayDirVector=vector_normalize(self,(screenX,screenY,10))
            #Generate ray direction
            #castRay(direction)
            #origin=[i,ii] #x,y
            for i in zscreen:
                #For collision detection code:
                #https://www.cs.unc.edu/~rademach/xroads-RT/RTarticle.html
                #Under 'Intersecting a Sphere
                if i[2]<maxRenderDistance:
                    A=vector_dot(self,rayDirVector, rayDirVector)
                    dist=vector_sub(self,(x,y,0),i[:3])
                    B= 2 * vector_dot(self,rayDirVector, dist)
                    C = vector_dot(self,dist, dist)-1
                    #print(A,B,C)
                    if B **2 - 4 * A * C>0:
                        draw_set_color(self,i[3])
                        draw_point(self,screenX,screenY)

                else:
                    #If we've reached the render distance limit break to prevent
                    #lag
                    break

#Main game stuff
class game_root():
    #This class is what 'self' will be at the top level
    pass

#Misc functions
def len(self,a):
    return a.__len__()

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
