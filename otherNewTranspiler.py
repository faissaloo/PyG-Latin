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
    currentTabulation=0
    def getCorrectTabulation():
        nonlocal currentTabulation
        return "\t"*currentTabulation

    class codeBlock():
        def __init__(self,BODY):
            self.BODY=BODY
        def py3(self):
            nonlocal currentTabulation
            #To do: Add code for handling tabulation
            currentTabulation+=1
            codeToReturn=""
            for i in self.BODY:
                codeToReturn+=getCorrectTabulation()+i.py3()+"\n"
            currentTabulation-=1
            return codeToReturn
    #Special case statements
    class objDefinition():
        def __init__(self,NAME,BODY):
            self.NAME=NAME
            self.BODY=BODY
        def py3(self):
            nonlocal currentTabulation
            codeToReturn=getCorrectTabulation()+"class "+self.NAME+"():\n"
            if self.BODY!=None:
                codeToReturn+=self.BODY.py3()
            else:
                currentTabulation+=1
                codeToReturn+=getCorrectTabulation()+"pass"
                currentTabulation-=1
            return codeToReturn

    class eventDefinition():
        def __init__(self,TYPE,BODY):
            self.TYPE=TYPE
            self.BODY=BODY
        def py3(self):
            nonlocal currentTabulation
            if self.TYPE!="create":
                codeToReturn="def "+self.TYPE+"(self):\n"
            else:
                codeToReturn="def __init__(self):\n"
            #Add your own code here
            if self.BODY!=None:
                codeToReturn+=self.BODY.py3()
            else:
                currentTabulation+=1
                codeToReturn+=getCorrectTabulation()+"pass"
                currentTabulation-=1
            return codeToReturn

    class roomDefinition():
        def __init__(self,NAME,BODY):
            self.NAME=NAME
            self.BODY=BODY
        def py3(self):
            nonlocal currentTabulation
            codeToReturn="class "+self.NAME+"():\n"
            currentTabulation+=1
            codeToReturn+=getCorrectTabulation()+"def __init__(self):\n"
            codeToReturn+=self.BODY.py3()
            currentTabulation+=1
            codeToReturn+=getCorrectTabulation()+"instanceList=[]\n"
            currentTabulation-=2
            return codeToReturn
    #General Statements
    class ifStatement():
        def __init__(self,EXPRESSION,BODY):
            self.EXPRESSION=EXPRESSION
            self.BODY=BODY
        def py3(self):
            nonlocal currentTabulation
            codeToReturn="if ("+self.EXPRESSION.py3()+"):\n"
            codeToReturn+=self.BODY.py3()
            return codeToReturn

    class whileStatement():
        def __init__(self,EXPRESSION,BODY):
            self.EXPRESSION=EXPRESSION
            self.BODY=BODY
        def py3(self):
            nonlocal currentTabulation
            codeToReturn=getCorrectTabulation()+"while ("+self.EXPRESSION.py3()+"):\n"
            codeToReturn+=self.BODY.py3()
            return codeToReturn
    class forStatement():
        def __init__(self,EXPRESSION,BODY):
            self.EXPRESSION=EXPRESSION
            self.BODY=BODY

    #Maths stuff
    class variable():
        def __init__(self,VARIABLENAME):
            self.VARIABLENAME=VARIABLENAME
        def py3(self):
            return self.VARIABLENAME

    class expression():
        def __init__(self,BODY):
            self.BODY=BODY
        def py3(self):
            nonlocal currentTabulation
            codeToReturn=""
            for i in self.BODY:
                codeToReturn+=i.py3()
            return codeToReturn

    class function():
        def __init__(self,FUNCTIONNAME,ARGUMENTS):
            self.FUNCTIONNAME=FUNCTIONNAME
            self.ARGUMENTS=ARGUMENTS #Arguments should be a list
        def py3(self):
            return self.FUNCTIONNAME+"("+self.ARGUMENTS.py3()+")"

    class arguments():
        def __init__(self,ARGUMENTS):
            self.ARGUMENTS=ARGUMENTS
        def py3(self):
            codeToReturn=""
            for i in range(len(self.ARGUMENTS)):
                codeToReturn+=self.ARGUMENTS[i].py3()
                if i!=len(self.ARGUMENTS)-1:
                    codeToReturn+=","
            return codeToReturn

    class additionOperation():
        def __init__(self,OPERAND1,OPERAND2):
            self.OPERANDS=OPERAND1,OPERAND2
        def py3(self):
            return self.OPERANDS[0].py3()+"+"+self.OPERANDS[1].py3()

    class subtractionOperation():
        def __init__(self,OPERAND1,OPERAND2):
            self.OPERANDS=OPERAND1,OPERAND2
        def py3(self):
            return self.OPERANDS[0].py3()+"-"+self.OPERANDS[1].py3()

    class multiplicationOperation():
        def __init__(self,OPERAND1,OPERAND2):
            self.OPERANDS=OPERAND1,OPERAND2
        def py3(self):
            return self.OPERANDS[0].py3()+"*"+self.OPERANDS[1].py3()

    class divisionOperation():
        def __init__(self,OPERAND1,OPERAND2):
            self.OPERANDS=OPERAND1,OPERAND2
        def py3(self):
            return self.OPERANDS[0].py3()+"/"+self.OPERANDS[1].py3()

    class additionAssignmentOperation():
        def __init__(self,OPERAND1,OPERAND2):
            self.OPERANDS=OPERAND1,OPERAND2
        def py3(self):
            return self.OPERANDS[0]+"+="+self.OPERANDS[1].py3()

    class subtractionAssignmentOperation():
        def __init__(self,OPERAND1,OPERAND2):
            self.OPERANDS=OPERAND1,OPERAND2
        def py3(self):
            return self.OPERANDS[0]+"-="+self.OPERANDS[1].py3()

    class multiplicationAssignmentOperation():
        def __init__(self,OPERAND1,OPERAND2):
            self.OPERANDS=OPERAND1,OPERAND2
        def py3(self):
            return self.OPERANDS[0]+"*="+self.OPERANDS[1].py3()

    class divideAssignmentOperation():
        def __init__(self,OPERAND1,OPERAND2):
            self.OPERANDS=OPERAND1,OPERAND2
        def py3(self):
            return self.OPERANDS[0]+"/="+self.OPERANDS[1].py3()

    class simpleAssignmentOperation():
        def __init__(self,OPERAND1,OPERAND2):
            self.OPERANDS=OPERAND1,OPERAND2
        def py3(self):
            return self.OPERANDS[0]+"="+self.OPERANDS[1].py3()

    #Datatypes
    #Real numbers are just all floats, because screw having two different types
    class realNumber():
        def __init__(self,REAL):
            self.REAL=REAL
        def py3(self):
            return str(self.REAL)

    class string():
        def __init__(self,STRING):
            self.STRING=STRING
        def py3(self):
            return '"'+self.STRING+'"'

    class list():
        def __init__(self,LIST):
            self.LIST=LIST
        def py3(self):
            codeToReturn="["
            for i in range(len(self.LIST)):
                codeToReturn+=self.LIST[i].py3()
                if i!=len(self.LIST)-1:
                    codeToReturn+=","
            codeToReturn+="]"
    def parse(source):
        def expect(string,enforce=False):
            nonlocal i
            nonlocal source
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
                if enforce:
                    print("Error: Expected whitespace, got "+source[i]+" instead")
                return False
            else:
                while source[i] in " \t\n" and i<len(source)-1:
                    i+=1 #Skip over whitespace, for some reason this is going to far
                return True

        def expect_whitespacebefore(enforce=False):
            nonlocal i
            nonlocal source
            if source[i] not in " \t\n":
                if enforce:
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
            if name!="" and not name.isdigit():
                return name
            else:
                if enforce:
                    print("Error: Expected name")
                return None #Just incase there's no name

        def takename_before(operationString):
            nonlocal i
            nonlocal source
            i-=len(operationString)+1
            #Goes back until there's no alphanumeric or underscore character
            while source[i] in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_":
                i-=1
            i+=1 #Go 1 position forward because it goes 1 over
            name=takename(True)
            expect_whitespace()
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
            if value!="":
                return realNumber(float(value))
            else:
                return None

        def takevalue_beforeoperation(operationString):
            nonlocal i
            nonlocal source
            i-=len(operationString)+1
            expect_whitespacebefore()
            while source[i] in "0123456789.": #Goes back until there's no numerical/period character
                i-=1
            i+=1
            value=takevalue()
            expect_whitespace()
            return value

        #For handling things like "+" and "/" etc
        def handleOperation(operationString,classToStoreIn):
            nonlocal i
            nonlocal source
            OPERAND1=realNumber(0.0)
            OPERAND2=realNumber(0.0)
            if expect(operationString):
                OPERAND1=takevalue_beforeoperation(operationString)
                expect(operationString)
                expect_whitespace()
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

        def parseArguments():
            nonlocal i
            nonlocal source
            argsBody=[]
            argsBody.append(parseExpression("),"))
            while expect(","):
                argsBody.append(parseExpression("),"))
            #print(argsBody)
            return arguments(argsBody)

        def parseFunction():
            nonlocal i
            nonlocal source
            if expect("("):
                FUNCTIONNAME=takename_before("(")
                expect("(")
                ARGUMENTS=parseArguments()
                if FUNCTIONNAME!=None:
                    return function(FUNCTIONNAME,ARGUMENTS)
                else:
                    return None
            else:
                return None

        def parseExpression(endOn="{"):
            nonlocal i
            nonlocal source
            expressionBody=[]
            start=i
            while i<len(source)-1 and source[i] not in endOn: #It's stopping here when it needs to
                i+=1
                for ii in [parseDivision(),
                    parseMultiplication(),
                    parseAddition(),
                    parseSubtraction(),
                    parseString()]:
                    if ii!=None:
                        expressionBody.append(ii)
                #Add something to interpret functions here pls so that the expression parser doesn't get it
                if source[i]=="(":
                    for ii in [parseFunction(),parseExpression()]:
                        if ii!=None:
                            expressionBody.append(ii)
                    expect(")")
            #If nothing is found assume there is this simple value
            if expressionBody==[]:
                i=start
                for ii in [takevalue(),parseVariable()]:
                    if ii!=None:
                        expressionBody.append(ii)
            return expression(expressionBody)

        def handleAssignment(operationString,classToStoreIn):
            nonlocal i
            nonlocal source
            OPERAND1=realNumber(0.0)
            OPERAND2=realNumber(0.0)
            if expect(operationString):
                #Takename before needs an argument for what the operationString is
                #So that it can go as far back as it needs to and I don't have
                #To deal with it
                expect_whitespacebefore()
                OPERAND1=takename_before(operationString)
                expect(operationString)
                expect_whitespace()
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
            if expect("if") and expect_whitespace(True):
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
            line=[]
            if expect("{",True):
                while i<len(source)-1 and source[i]!="}":
                    i+=1
                    for ii in [parseWhileStatement(),
                        parseIfStatement(),
                        parseEventDefinition(),
                        parseDivisionAssignment(),
                        parseMultiplicationAssignment(),
                        parseAdditionAssignment(),
                        parseSubtractionAssignment(),
                        parseString(),
                        parseFunction() #This is currently having problems
                        ]:
                        if ii!=None:
                            body.append(ii)
                expect("}",True)
            if body!=[]:
                return codeBlock(body)
            else:
                return None

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
            if expect("event") and expect_whitespace(True):
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

        i=0
        line=""
        #This is the root loop
        while i<len(source):
            #Put all the other parse*() functions here
            #Adding parseExpression() to the end of this for loop is unconditionally
            #appending it to rawParsedData, fix
            for ii in [parseEventDefinition(),
                parseObjDefinition(),
                parseRoomDefinition(),
                parseDivisionAssignment(),
                parseMultiplicationAssignment(),
                parseAdditionAssignment(),
                parseSubtractionAssignment(),
                parseSimpleAssignment()]:
                if ii!=None:
                    rawParsedData.append(ii)
            i+=1
        #Debug
        return rawParsedData

    def transpileToPython(structure):
        pythonCode="#!/usr/bin/env python3\nfrom PyG import *\n"
        for i in structure:
            pythonCode+=i.py3()
        pythonCode+="\ngame_init()\ngame_main()"
        return pythonCode
    return transpileToPython(parse(inputSource))

with open(inputFile,'r') as f:
    latinSource = f.read()
print(transpile(latinSource))
#Not yet fit for use
#with open(outputFile,'w') as f:
#    f.write(transpile(latinSource))
