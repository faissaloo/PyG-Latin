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
            def __init__(self,EXPRESSION,BODY):
                self.EXPRESSION=EXPRESSION
                self.BODY=BODY
        class forStatement():
            def __init__(self,STATEMENT,BODY):
                self.EXPRESSION=EXPRESSION
                self.BODY=BODY

        class expression():
            def __init__(self,BODY):
                self.BODY=BODY

        class additionOperation():
            def __init__(self,OPERAND1,OPERAND2):
                self.OPERAND1=OPERAND1
                self.OPERAND2=OPERAND2

        class subtractionOperation():
            def __init__(self,OPERAND1,OPERAND2):
                self.OPERAND1=OPERAND1
                self.OPERAND2=OPERAND2

        class multiplicationOperation():
            def __init__(self,OPERAND1,OPERAND2):
                self.OPERAND1=OPERAND1
                self.OPERAND2=OPERAND2

        class divisionOperation():
            def __init__(self,OPERAND1,OPERAND2):
                self.OPERAND1=OPERAND1
                self.OPERAND2=OPERAND2

        class additionAssignmentOperation():
            def __init__(self,OPERAND1,OPERAND2):
                self.OPERAND1=OPERAND1
                self.OPERAND2=OPERAND2

        class subtractionAssignmentOperation():
            def __init__(self,OPERAND1,OPERAND2):
                self.OPERAND1=OPERAND1
                self.OPERAND2=OPERAND2

        class multiplicationAssignmentOperation():
            def __init__(self,OPERAND1,OPERAND2):
                self.OPERAND1=OPERAND1
                self.OPERAND2=OPERAND2

        class divideAssignmentOperation():
            def __init__(self,OPERAND1,OPERAND2):
                self.OPERAND1=OPERAND1
                self.OPERAND2=OPERAND2

        class simpleAssignmentOperation():
            def __init__(self,OPERAND1,OPERAND2):
                self.OPERAND1=OPERAND1
                self.OPERAND2=OPERAND2

        class realNumber(): #Real numbers are just all floats, because screw having two different types
            def __init__(self,REAL):
                self.REAL=REAL

        def expect(string,enforce=False):
            nonlocal i
            nonlocal source
            #print(source[i:i+len(string)],"=",string)
            if source[i:i+len(string)]==string:
                i+=len(string)#Skip over the thing
                return True
            else:
                if enforce:
                    print("Error: Expected '"+string+"'")
                return False

        def expect_whitespace(enforce=False):
            nonlocal i
            nonlocal source
            if source[i] not in " \t\n" and enforce:
                print("Error: Expected whitespace, got "+source[i]+" instead")
                return False
            else:
                while source[i] in " \t\n":
                    i+=1 #Skip over whitespace, for some reason this is going to far
                return True

        def takename(enforce=False):
            nonlocal i
            nonlocal source
            name=""
            while source[i] in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_":
                name+=source[i]
                i+=1
            #print(name)
            if name!="":
                return name
            else:
                if enforce:
                    print("Error: Expected name")
                return None #Just incase there's no name

        def takename_before():
            nonlocal i
            nonlocal source
            while source[i] in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_": #Goes back until there's no numerical/period character
                i-=1
            name=takename(True)
            return name

        def takevalue():
            nonlocal i
            nonlocal source
            value=""
            expect_whitespace()
            while source[i] in "0123456789.":
                value+=source[i]
                i+=1
            return realNumber(value)

        def takevalue_beforeoperation():
            nonlocal i
            nonlocal source
            while source[i] in "0123456789.": #Goes back until there's no numerical/period character
                i-=1
            value=takevalue()
            return value

        def parseAddition():
            nonlocal i
            nonlocal source
            OPERAND1=realNumber("0.0")
            OPERAND2=realNumber("0.0")
            if expect("+"):
                OPERAND1=takevalue_beforeoperation()
                expect("+")
                OPERAND2=takevalue()
                return additionOperation(OPERAND1,OPERAND2)
            else:
                return None

        def parseSubtraction():
            nonlocal i
            nonlocal source
            OPERAND1=realNumber("0.0")
            OPERAND2=realNumber("0.0")
            if expect("-"):#This is reading -= and taking it as a subtraction, it should not be looking in the body of the if statement, why is it doing that?
                OPERAND1=takevalue_beforeoperation()
                expect("-")
                OPERAND2=takevalue()
                return subtractionOperation(OPERAND1,OPERAND2)
            else:
                return None

        def parseMultiplication():
            nonlocal i
            nonlocal source
            OPERAND1=realNumber("0.0")
            OPERAND2=realNumber("0.0")
            if expect("*"):
                OPERAND1=takevalue_beforeoperation()
                expect("*")
                OPERAND2=takevalue()
                return additionOperation(OPERAND1,OPERAND2)
            else:
                return None

        def parseDivision():
            nonlocal i
            nonlocal source
            OPERAND1=realNumber("0.0")
            OPERAND2=realNumber("0.0")
            if expect("/"):
                OPERAND1=takevalue_beforeoperation()
                expect("/")
                OPERAND2=takevalue()
                return subtractionOperation(OPERAND1,OPERAND2)
            else:
                return None

        def parseExpression():
            nonlocal i
            nonlocal source
            expressionBody=[]
            while source[i]!="{": #It's stopping here when it needs to
                i+=1
                add=parseAddition()
                sub=parseSubtraction()
                mul=parseMultiplication()
                div=parseDivision()
                if add!=None:
                    expressionBody.append(add)
                if sub!=None:
                    expressionBody.append(sub)
                if mul!=None:
                    expressionBody.append(mul)
                if div!=None:
                    expressionBody.append(div)
                #Add something to interpret functions here pls so that the expression parser doesn't get it
                if expect("("):
                    expressionBody.append(parseExpression())
                    expect(")")
            return expression(expressionBody)

        def parseAdditionAssignment():
            nonlocal i
            nonlocal source
            OPERAND1=realNumber("0.0")
            OPERAND2=realNumber("0.0")
            if expect("+="):
                OPERAND1=takename_before()
                expect("+=")
                OPERAND2=parseExpression()
                return additionAssignmentOperation(OPERAND1,OPERAND2)
            else:
                return None

        def parseSubtractionAssignment():
            nonlocal i
            nonlocal source
            OPERAND1=realNumber("0.0")
            OPERAND2=realNumber("0.0")
            if expect("-="):
                OPERAND1=takename_before()
                expect("-=")
                OPERAND2=parseExpression()
                return subtractionAssignmentOperation(OPERAND1,OPERAND2)
            else:
                return None

        def parseMultiplicationAssignment():
            nonlocal i
            nonlocal source
            OPERAND1=realNumber("0.0")
            OPERAND2=realNumber("0.0")
            if expect("*="):
                OPERAND1=takename_before()
                expect("*=")
                OPERAND2=parseExpression()
                return multiplicationAssignmentOperation(OPERAND1,OPERAND2)
            else:
                return None

        def parseDivisionAssignment():
            nonlocal i
            nonlocal source
            OPERAND1=realNumber("0.0")
            OPERAND2=realNumber("0.0") #It should be possible for these to be expressions too
            if expect("/="):
                OPERAND1=takename_before()
                expect("/=")
                OPERAND2=parseExpression()
                return divideAssignmentOperation(OPERAND1,OPERAND2)
            else:
                return None
        def parseSimpleAssignment(): #Make sure to parse relative assignments before this like -=,+=,*= and /=
            nonlocal i
            nonlocal source
            OPERAND1=realNumber("0.0")
            OPERAND2=realNumber("0.0")
            if expect("="):
                OPERAND1=takename_before()
                expect("=")
                OPERAND2=parseExpression()
                return simpleAssignmentOperation(OPERAND1,OPERAND2)
            else:
                return None

        def parseIfStatement():
            nonlocal i
            nonlocal source
            if expect("if") and expect_whitespace(True): #This if statement is spilling, fix pls
                    ifExpression=parseExpression()
                    ifBody=parseCodeBlock()
                    return ifStatement(ifExpression,ifBody)
            else:
                return None

        def parseWhileStatement():
            nonlocal i
            nonlocal source
            if expect("while") and expect_whitespace(True):
                    whileExpression=parseExpression(takeexpression())
                    whileBody=parseCodeBlock()
                    return whileStatement(whileExpression,whileBody)
            else:
                return None

        def parseCodeBlock():
            nonlocal i
            nonlocal source
            body=[]
            line=""
            if expect("{",True):
                while source[i]!="}":
                    i+=1
                    whileloop=parseWhileStatement()
                    ifcomp=parseIfStatement()
                    event=parseEventDefinition()
                    if whileloop!=None:
                        body.append(whileloop)
                    elif ifcomp!=None:
                        body.append(ifcomp)
                    elif event!=None:
                        body.append(event)
                    elif expect("\n"):
                        a=line
                        body.append(a) #We need to figure out parsing for this
                        line=""
                    else:
                        line+=source[i]
                expect("}",True)
            return body

        def parseObjDefinition():
            nonlocal i
            nonlocal source
            if expect("obj") and expect_whitespace(True):
                    objName=takename()
                    expect_whitespace()
                    objBody=parseCodeBlock()
                    return objDefinition(objName,objBody)
            else:
                return None

        def parseEventDefinition():
            nonlocal i
            nonlocal source
            if expect("event") and expect_whitespace(True): #Nesting them because I need them in this specific order and I'm not sure how Python's parsing tree for logic statements works
                eventName=takename()
                expect_whitespace()
                eventBody=parseCodeBlock()
                return eventDefinition(eventName,eventBody)

        def parseRoomDefinition():
            nonlocal i
            nonlocal source
            roomBody=""
            #This is causing issues whenever room is in something else because it is being skipped over
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
        #This is the root loop
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
