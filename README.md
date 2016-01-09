Preamble
===
PyG-Latin is an object oriented programming language intended for creating games that use the curses library.
The way it works is loosely based on the Enigma Game Maker in that it uses a library to implement
custom functions but keeps most of the syntax of the language it's transpiling to (obviously, with a bit of modification).
The language itself is based on GML. It is case sensitive, but not tab sensitive.


In this repo you will 3 things:
1. The Python library which implements the engine functionality, this is called PyG.py
2. The transpiler for the language, this is called alice.py
3. Small games and programs with which to test compilation and functionality

Objects
===
An object is structured like so:
```
obj <OBJECTNAME> {
    event create
    {

    }
    event step
    {

    }
    event draw
    {

    }
    event destroyed
    {

    }
}
```
Events
===
Events are optional, you do not need to put all of them in an object if you're not going to use them.
create
--
The create event is where you must initialise all your object specific variables. This is done like so:
```
self.varA=1
```
step
--
The step event is what is executed after every time the screen is redrawn.
This is where you will put things like keyboard checks, which must be done constantly.

draw
--
The draw event is what is executed right before every time the screen is redrawn, this is where you put all your draw_* function calls.

destroyed
--
This is when you put anything you wish to be executed when an object is destroyed (i.e: removed from the list of objects in the room).

Rooms
===
A room is structured like so:
```
room <ROOMNAME> {
    room_speed=<ROOMSPEED>
    room_width=<ROOMWIDTH>
    room_height=<ROOMHEIGHT>
}
```
room_speed is how often the screen will be refreshed. room_height is the height in terminal cells and room_width is the width in terminal cells.

At the end of your code you must indicate what the default room will be or nothing will happen, you can do this with either:
```
current_room=<ROOMNAME>()
```
or
```
room_goto(<ROOMNAME>)
```
Though room_goto is preferred because it doesn't require the brackets at the end of the name.

Scripts
===
In PyG-Latin scripts are what you would call 'functions' in other languages, you define them like so:
```
script <SCRIPTNAME>(<ARGUMENTS>)
{

}
```
Arguments are seperated by commas.

Datatypes
===
Real
--
In PyG-Latin, integers and floats are all 'reals' when transpiled. They are not differentiated between so treat them as such.

Strings
--
Strings are denoted like so:
```
"<STRING>"
```
or
```
'<STRING>'
```
Sprites
--
Sprites are 2D lists of a number between 0 and 8, these represent the color of each pixel. This is what is returned by sprite_add().

Statements
===

if
--
If statements are done like so:
```
if <EXPRESSION>
{

}
```

else
--
Else is only executed if the expression in the previous if statement was false.
```
if <EXPRESSION>
{

}
else
{

}
```
else if
--
Else if is only executed if the expression in the previous if statement was false and if the expression in this statement is true.
```
if <EXPRESSION>
{

}
else if <EXPRESSION>
{

}
```
while
--
While repeats the block of code until the expression is false.
```
while <EXPRESSION>
{

}
```
for
--
For loops aren't working yet, I have yet to decide whether I wish to go for a c style. Input on this matter would be very much appreciated.
```
for (ii=0;ii<10;i+=1)
```
or a
```
for i in range(10)
```
Operations
===
The following are all the operations in PyG-Latin:
* !=
* >
* >=
* <
* <=
* =
* +
* -
* *
* /
* NOT
* AND
* OR
* XOR
* LSHIFT
* RSHIFT

Assignments
===
The following assignments are possible:
* +=
* -=
* *=
* /=
* =
Functions
===
In addition to the normal Python functions, the following functions are added by the PyG library:
* sleep(real seconds) (from the python module 'time')
* Everything from the python module 'random'
* Everything from the python module 'math'
* keyboard_check(real key)
* keyboard_check_pressed(real key)
* draw_set_color(real color)
* draw_point(real y, real x)
* draw_text(real y, real x, str string)
* draw_rectangle(real y1, real x1, real y2, real x2, bool outline)
* draw_circle(real y, real x, real r, bool outline)
* draw_line(real y1, real x1, real y2, real x2)
* draw_path(real y,real x,list path)
* make_color_rgb(real red, real green, real blue)
* draw_sprite(spr sprite, real y, real x)
* sprite_add(str fname)
* instance_create(real y, real x, obj object)
* sprite_get_height(spr sprite)
* sprite_get_width(sprite)
* instance_destroy()
* room_goto(rm room)

In addition to the normal Python constants, the following constants are added by the PyG library (they're not actually constants, just variables, but that's because Python doesn't have constants):
* c_black
* c_red
* c_green
* c_yellow
* c_blue
* c_magenta
* c_cyan
* c_white
