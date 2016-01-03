PyG-Latin is an object oriented programming language intended for creating games that use the curses library.
The way it works is loosely based on the Enigma Game Maker in that it uses a library to implement
custom functions but keeps most of the syntax of the language it's transpiling to (obviously, with a bit of modification).
The language itself is based on GML.


In this repo you will 3 things:
1. The Python library which implements the engine functionality, this is called PyG.py
2. The transpiler for the language, this is called alice.py
3. Small games with which to test compilation and functionality

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
A room is structured like so:
```
room <ROOMNAME> {
    room_speed=<ROOMSPEED>
    room_width=<ROOMWIDTH>
    room_height=<ROOMHEIGHT>
}
```
at the end of your code you must indicate what the default room will be or nothing will happen, you can do this with either:
```
current_room=<ROOMNAME>
```
or
```
room_goto(<ROOMNAME>)
```

In addition to the normal Python functions, the following functions are added by the PyG library:
* sleep(float seconds)
* keyboard_check(int key)
* keyboard_check_pressed(int key)
* draw_set_color(int color)
* draw_point(float y,float x)
* draw_text(float y,float x,str string)
* draw_rectangle(float y1,float x1,float y2,float x2,bool outline)
* draw_circle(float y,float x,float r,bool outline)
* draw_line(float y1,float x1,float y2,float x2)
* draw_path(float y,float x,list path)
* instance_create(float y,float x,obj object)
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
