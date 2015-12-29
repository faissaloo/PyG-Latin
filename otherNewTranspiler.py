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
        #Special case statements
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

        #General Statements
        class ifStatement():
            def __init__(self,EXPRESSION,BODY):
                self.EXPRESSION=EXPRESSION
                self.BODY=BODY

        class whileStatement():
            def __init__(self,EXPRESSION,BODY):
                self.EXPRESSION=EXPRESSION
                self.BODY=BODY
        class forStatement():
            def __init__(self,EXPRESSION,BODY):
                self.EXPRESSION=EXPRESSION
                self.BODY=BODY

        #Maths stuff
        class variable():
            def __init__(self,VARIABLENAME):
                self.VARIABLENAME=VARIABLENAME

        class expression():
            def __init__(self,BODY):
                self.BODY=BODY

        class function():
            def __init__(self,FUNCTIONNAME,ARGUMENTS):
                self.FUNCTIONNAME=FUNCTIONNAME
                self.ARGUMENTS=ARGUMENTS #Arguments should be a list

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

        #Datatypes
        class realNumber(): #Real numbers are just all floats, because screw having two different types
            def __init__(self,REAL):
                self.REAL=REAL

        class string():
            def __init__(self,STRING):
                self.STRING=STRING

        class list():
            def __init__(self,LIST):
                self.LIST=LIST

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
                while source[i] in " \t\n" and i<len(source)-1:
                    i+=1 #Skip over whitespace, for some reason this is going to far
                return True

        def expect_whitespacebefore(enforce=False):
            nonlocal i
            nonlocal source
            if source[i] not in " \t\n" and enforce:
                print("Error: Expected whitespace, got "+source[i]+" instead")
                return False
            else:
                while source[i] in " \t\n" and i>0:
                    i-=1 #Skip over whitespace, for some reason this is going to far
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

        def takename_before(operationString):
            nonlocal i
            nonlocal source
            i-=len(operationString)+1
            while source[i] in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_": #Goes back until there's no numerical/period character
                i-=1
            i+=1 #Go 1 position forward because it goes 1 over
            name=takename(True)
            i+=1
            if name!="":
                return name
            else:
                return None

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
            i+=1
            value=takevalue()
            return value

        #For handling things like "+" and "/" etc
        def handleOperation(operationString,classToStoreIn):
            nonlocal i
            nonlocal source
            OPERAND1=realNumber("0.0")
            OPERAND2=realNumber("0.0")
            if expect(operationString):
                OPERAND1=takevalue_beforeoperation()
                expect(operationString)
                OPERAND2=takevalue()
                return classToStoreIn(OPERAND1,OPERAND2)
            else:
                return None

        def parseVariable():
            nonlocal i
            nonlocal source
            VARIABLENAME=takename()
            if VARIABLENAME!=None:
                return variable(VARIABLENAME)
            else:
                return None

        def parseAddition():
            nonlocal i
            nonlocal source
            return handleOperation("+",additionOperation)

        def parseSubtraction():
            nonlocal i
            nonlocal source
            return handleOperation("-",subtractionOperation)

        def parseMultiplication():
            nonlocal i
            nonlocal source
            return handleOperation("*",multiplicationOperation)

        def parseDivision():
            nonlocal i
            nonlocal source
            return handleOperation("/",divisionOperation)

        def parseFunction():
            nonlocal i
            nonlocal source
            FUNCTIONNAME=takename_before("(")
            ARGUMENTS=[] #Need to add something to split the arguments by ,
            if FUNCTIONNAME!=None:
                return function(FUNCTIONNAME,ARGUMENTS)
            else:
                return None

        def parseExpression(endOn="{"):
            nonlocal i
            nonlocal source
            expressionBody=[]
            while source[i] not in endOn and i<len(source)-1: #It's stopping here when it needs to
                i+=1
                for ii in [parseDivision(),parseMultiplication(),parseAddition(),parseSubtraction(),parseString(),parseVariable()]:
                    if ii!=None:
                        expressionBody.append(ii)
                #Add something to interpret functions here pls so that the expression parser doesn't get it
                if expect("("):
                    for ii in [parseFunction(),parseExpression()]:
                        if ii!=None:
                            expressionBody.append(ii)
                    expect(")")
            return expression(expressionBody)

        def handleAssignment(operationString,classToStoreIn):
            nonlocal i
            nonlocal source
            OPERAND1=realNumber("0.0")
            OPERAND2=realNumber("0.0")
            if expect(operationString):
                #Takename before needs an argument for what the operationString is
                #So that it can go as far back as it needs to and I don't have
                #To deal with it
                OPERAND1=takename_before(operationString)
                expect(operationString)
                OPERAND2=parseExpression("{\n")
                return classToStoreIn(OPERAND1,OPERAND2)
            else:
                return None

        def parseAdditionAssignment():
            nonlocal i
            nonlocal source
            return handleAssignment("+=",additionAssignmentOperation)

        def parseSubtractionAssignment():
            nonlocal i
            nonlocal source
            return handleAssignment("-=",subtractionAssignmentOperation)

        def parseMultiplicationAssignment():
            nonlocal i
            nonlocal source
            return handleAssignment("*=",multiplicationAssignmentOperation)

        def parseDivisionAssignment():
            nonlocal i
            nonlocal source
            return handleAssignment("/=",divideAssignmentOperation)

        def parseSimpleAssignment(): #Make sure to parse relative assignments before this like -=,+=,*= and /=
            nonlocal i
            nonlocal source
            return handleAssignment("=",simpleAssignmentOperation)

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
                while source[i]!="}": #This is causing issues when trying to parse lines, idk why tho
                    i+=1
                    whileloop=parseWhileStatement()
                    ifcomp=parseIfStatement()
                    event=parseEventDefinition()
                    #expr=parseExpression("\n")
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

        def parseString():
            nonlocal i
            nonlocal source
            def parseStringDeliniator(deliniator):
                STRING=""
                if expect(deliniator):
                    while source[i]!=deliniator:
                        i+=1
                        #Escape the deliniator by handling it before looping back
                        #To source[i]!=deliniator so it doesn't catch it
                        #Using or because we don't want escape codes to only works
                        #When using one deliniator
                        if expect("\\") and (expect("\"") or expect("\'")):
                            STRING+=deliniator
                        STRING+=source[i]
                    expect(deliniator,True)
                    return string(STRING)
                else:
                    return None
            for ii in [parseStringDeliniator("\""),parseStringDeliniator("\'")]:
                if ii!=None:
                    return ii

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
            expect_whitespace()
            #This is causing issues whenever room is in something else because it is being skipped over
            if expect("room") and expect_whitespace(True):
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
            #Adding parseExpression() to the end of this for loop is unconditionally
            #appending it to rawParsedData, fix
            for ii in [parseEventDefinition(),parseObjDefinition(),parseRoomDefinition(),parseDivisionAssignment(),parseMultiplicationAssignment(),parseAdditionAssignment(),parseSubtractionAssignment(),parseSimpleAssignment()]:
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
