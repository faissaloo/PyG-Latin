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
#This transpiler uses classes to hold information instead of just plain old lists
import argparse
import functools
import re
#Argument handling
parser = argparse.ArgumentParser(description='Transpile a PyG-Latin program to Python3')
parser.add_argument('inputFile', help='The file with the source code to be transpiled')
parser.add_argument('outputFile', help='The file to output the Python3 code to')
args = parser.parse_args()
inputFile = args.inputFile
outputFile = args.outputFile

latinSource = ""
def transpile(inputSource):
    rawParsedData=[]

    def parse(source):
        class objDefinition():
            def __init__(self,NAME,BODY):
                self.NAME=NAME
                self.BODY=BODY

        class eventDefinition():
            def __init__(self,TYPE,BODY):
                self.TYPE=TYPE
                self.BODY=BODY

        class roomDefinition():
            def __init__(self,NAME,BODY):
                self.NAME=NAME
                self.BODY=BODY

        class ifStatement():
            def __init__(self,EXPRESSION,BODY):
                self.EXPRESSION=EXPRESSION
                self.BODY=BODY

        class whileStatement():
            def __init__(self,STATEMENT,BODY):
                self.STATEMENT=STATEMENT
                self.BODY=BODY
        class forStatement():
            def __init__(self,STATEMENT,BODY):
                self.STATEMENT=STATEMENT
                self.BODY=BODY

        class expression():
            def __init__(self,EXPRESSION):
                self.EXPRESSION=EXPRESSION

        class addition():
            def __init__(self,OPERAND1,OPERAND2):
                self.OPERAND1=OPERAND1
                self.OPERAND2=OPERAND2

        class subtraction():
            def __init__(self,OPERAND1,OPERAND2):
                self.OPERAND1=OPERAND1
                self.OPERAND2=OPERAND2

        def expect(string,required=False):
            nonlocal i
            nonlocal source
            #print(source[i:i+len(string)],"=",string)
            if source[i:i+len(string)]==string:
                i+=len(string)#Skip over the thing
                return True
            else:
                if required:
                    print("Error: Expected '"+string+"'")
                return False

        def expect_whitespace(throwError=False):
            nonlocal i
            nonlocal source
            if source[i] not in " \t\n" and throwError:
                print("Error: Expected whitespace")
                return False
            else:
                while source[i] in " \t\n":
                    i+=1 #Skip over whitespace, for some reason this is going to far
                return True

        def takename():
            nonlocal i
            nonlocal source
            name=""
            while source[i] in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_":
                name+=source[i]
                i+=1
            #print(name)
            return name

        def takeexpression():
            nonlocal i
            nonlocal source
            expression=""
            while source[i]!="{":
                expression+=source[i]
                i+=1
            #print(expression)
            return expression


        def parseExpression():
            nonlocal i
            nonlocal source

        def parseAddition():
            nonlocal i
            nonlocal source

        def parseSubtraction():
            nonlocal i
            nonlocal source

            return
        def parseCodeBlock():
            nonlocal i
            nonlocal source
            body=[]
            line=""
            if expect("{",True):
                while source[i]!="}":
                    i+=1 #Putting this here at the beginning instead of at the end seems to fix things kinda, why?
                    ifcomp=parseIfStatement()
                    event=parseEventDefinition()
                    if ifcomp!=None:
                        body.append(ifcomp)
                    elif event!=None:
                        body.append(event)
                    elif expect("\n"):
                        a=line
                        #print(a)
                        body.append(a) #We need to figure out parsing for this
                        line=""
                    else:
                        line+=source[i]
            expect("}",True)
            return body

        def parseIfStatement():
            nonlocal i
            nonlocal source
            objBody=""
            if expect("if") and expect_whitespace(True): #Nesting them because I need them in this specific order and I'm not sure how Python's parsing tree for logic statements works
                    ifExpression=expression(takeexpression())
                    ifBody=parseCodeBlock()
                    return ifStatement(ifExpression,ifBody)
            else:
                return None

        def parseObjDefinition():
            nonlocal i
            nonlocal source
            objBody=""
            if expect("obj") and expect_whitespace(True): #Nesting them because I need them in this specific order and I'm not sure how Python's parsing tree for logic statements works
                    objName=takename()
                    expect_whitespace()
                    objBody=parseCodeBlock()
                    return objDefinition(objName,objBody)
            else:
                return None

        def parseEventDefinition():
            nonlocal i
            nonlocal source
            eventBody=""
            if expect("event") and expect_whitespace(True): #Nesting them because I need them in this specific order and I'm not sure how Python's parsing tree for logic statements works
                eventName=takename()
                expect_whitespace()
                eventBody=parseCodeBlock()
                return eventDefinition(eventName,eventBody)

        def parseRoomDefinition():
            nonlocal i
            nonlocal source
            roomBody=""
            if expect("room") and expect_whitespace(True): #Nesting them because I need them in this specific order and I'm not sure how Python's parsing tree for logic statements works
                    roomName=takename()
                    expect_whitespace()
                    roomBody=parseCodeBlock()
                    return roomDefinition(roomName,roomBody)
            else:
                return None
        def parseLine():
            nonlocal i
            nonlocal source
            pass
        i=0
        line=""
        while i<len(source):
            #Put all the other parse*() functions here
            if expect("\n"):
                rawParsedData.append(line)
                line=""
            else:
                line+=source[i]
            for ii in [parseEventDefinition(),parseObjDefinition(),parseRoomDefinition()]:
                if ii!=None:
                    rawParsedData.append(ii)

            i+=1
        #Debug

        return rawParsedData
    return parse(inputSource)

with open(inputFile,'r') as f:
    latinSource = f.read()
print(transpile(latinSource))
#Not yet fit for use
#with open(outputFile,'w') as f:
#    f.write(transpile(latinSource))
