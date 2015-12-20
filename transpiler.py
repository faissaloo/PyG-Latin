#!/usr/bin/env python3
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
import argparse
#Argument handling
parser = argparse.ArgumentParser(description='Transpile a PyG-Latin program to Python3')
parser.add_argument('inputFile', help='The file with the source code to be transpiled')
parser.add_argument('outputFile', help='The file to output the Python3 code to')
args = parser.parse_args()
inputFile = args.inputFile
outputFile = args.outputFile

latinSource = ""
def transpile(source):
    global formattedString
    #First remove all the whitespace from the beginning of each line
    text=""
    for i in source.split("\n"):
        text+=i.lstrip(' \t')+"\n"
    #Define the other variables
    formattedString="#!/usr/bin/env python3\nfrom PyG import *\n"
    lineWidth=0 #For styling warnings
    currentLine=0
    singleMarkString=False
    doubleMarkString=False
    currentIndent=0
    objDefining=False
    roomDefining=False
    eventDefining=False
    scriptDefining=False
    ifStatement=False
    forStatement=False
    whileStatement=False
    #This is for the offset for skipping whitespace between 'event' and 'create'
    temppos=0

    def indent():
        global formattedString
        if i<len(text)-1:
            if text[i+1]!="\n":
                formattedString+="\n"
                for ii in range(currentIndent):
                    formattedString+="\t" #Corrects the tabbing

    for i in range(len(text)):
        if text[i:i+2]=="//" and not (singleMarkString or doubleMarkString): #There is no 'integer division' in PyG-Latin anyways
            formattedString+="#"
        elif text[i:i+3]=="if " and not (singleMarkString or doubleMarkString):
            formattedString+="if ("
            ifStatement=True #Put here because it might make things easier in future
        elif text[i:i+6]=="while " and not (singleMarkString or doubleMarkString):
            formattedString+="while ("
            ifStatement=True #Put here because it might make things easier in future
        elif text[i:i+4]=="for " and not (singleMarkString or doubleMarkString):
            formattedString+=text[i]
            forStatement=True
        elif text[i:i+6]=="event " and not (singleMarkString or doubleMarkString):
            formattedString+="def " #Add something so that if it's a 'create' event it gets replaced with an __init__
            while text[i+6+temppos]==" " and i+6+temppos<len(text)-1: #Skip the whitespace and check that we're still in range to prevent errors
                temppos+=1
            if text[i+6+temppos:i+12+temppos]=="create": #Replaces 'create' with '__init__'
                formattedString+="__init__"
            temppos=0
            eventDefining=True
        elif text[i:i+4]=="obj " and not (singleMarkString or doubleMarkString):
            formattedString+="class"
            objDefining=True
        elif text[i:i+5]=="room " and not (singleMarkString or doubleMarkString):
            formattedString+="class "
            roomDefining=True
        elif text[i:i+7]=="script " and not (singleMarkString or doubleMarkString):
            formattedString+="def"
            scriptDefining=True
        elif ifStatement and text[i+1]=="{" and not (singleMarkString or doubleMarkString):
            formattedString+="):" #Appends : at the end of the line
            ifStatement=False
        elif whileStatement and text[i+1]=="{" and not (singleMarkString or doubleMarkString):
            formattedString+=text[i]+"):"
            whileStatement=False
        elif forStatement and text[i+1]=="{" and not (singleMarkString or doubleMarkString):
            formattedString+=text[i]+":" #Appends currentLetter+':' at the end of the line
            forStatement=False
        elif text[i]=="{" and not (singleMarkString or doubleMarkString or objDefining or roomDefining): #indentation
            currentIndent+=1
            indent()#Corrects indent
        elif text[i]=="}" and not (singleMarkString or doubleMarkString): #indentation
            currentIndent-=1
            indent()#Corrects indent
        elif text[i]=="'": #String
            if not doubleMarkString:
                singleMarkString = not singleMarkString
                #Turning string mode on and off if this ' isn't in a "
        elif text[i]=='"': #String
            if not singleMarkString:
                doubleMarkString = not doubleMarkString
                #Turning string mode on and off if this " isn't in a '

        elif ((text[i]!="\n" #Find a better way to do this pls
            and text[i-1:i+2]!="if "
            and text[i-2:i+1]!="if "
            and text[i-1:i+3]!="obj "
            and text[i-2:i+2]!="obj "
            and text[i]!="{"
            and text[i]!="}"
            and text[i-1:i+6]!="script "
            and text[i-2:i+5]!="script "
            and text[i-3:i+4]!="script "
            and text[i-4:i+3]!="script "
            and text[i-5:i+2]!="script "
            and text[i-6:i+1]!="script "
            and text[i-1:i+5]!="while "
            and text[i-2:i+4]!="while "
            and text[i-3:i+3]!="while "
            and text[i-4:i+2]!="while "
            and text[i-5:i+1]!="while "
            and text[i-2:i]!="//"
            and text[i-1:i+4]!="room "
            and text[i-2:i+3]!="room "
            and text[i-3:i+2]!="room "
            and text[i-4:i+1]!="room "
            and text[i-1:i+5]!="event "
            and text[i-2:i+4]!="event "
            and text[i-3:i+3]!="event "
            and text[i-4:i+2]!="event "
            and text[i-5:i+1]!="event "
            and ((text[i:i+6]!="create"
            and text[i-1:i+5]!="create"
            and text[i-2:i+4]!="create"
            and text[i-3:i+3]!="create"
            and text[i-4:i+2]!="create"
            and text[i-5:i+1]!="create"
            ) or not eventDefining)
            ) or
            (singleMarkString #Write the stuff out if it's in a string regardless of what it is
            or doubleMarkString)):
            formattedString+=text[i]

        #Handles the end of a statement
        if (text[i]=="\n" and text[i:i+1]!="{") or text[i]=="{":
            #The following chooses the stuff to append at the end of a statement
            if objDefining:
                formattedString+=":"
                objDefining=False
                currentIndent+=1
            elif roomDefining:
                formattedString+=":\n" #Has a \n because we want to add our own code after
                for i in range(currentIndent+1):
                    formattedString+="\t" #Corrects the tabbing
                formattedString+="instanceList=[]" #There's an issue here where it'll leave a gap if the code is room rmname() {} not room rmname() {\n}
                roomDefining=False
                currentIndent+=1
            elif scriptDefining:
                formattedString+=":"
                scriptDefining=False
                currentIndent+=1
            elif eventDefining:
                formattedString+="(self):" #Add something so that if it's a 'create' event it gets replaced with an __init__
                eventDefining=False
            lineWidth=0
            currentLine+=1
            indent()
        else:
            lineWidth+=1
            if lineWidth>80:
                print("Warning: Line "+str(currentLine)+" exceeds length limit")
    formattedString+="\ngame_init()\ngame_main()"
    return formattedString

with open(inputFile,'r') as f:
    latinSource = f.read()
with open(outputFile,'w') as f:
    f.write(transpile(latinSource))
