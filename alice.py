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

    class itemClass():
        def __init__(self,NAME):
            self.NAME=NAME

    class codeBlock():
        def __init__(self,BODY):
            self.BODY=BODY
        def py3(self):
            nonlocal currentTabulation
            currentTabulation+=1
            codeToReturn=""
            for i in self.BODY:
                returnedStr=i.py3()
                codeToReturn+=getCorrectTabulation()+returnedStr+"\n"
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

    class elseifStatement():
        def __init__(self,EXPRESSION,BODY):
            self.EXPRESSION=EXPRESSION
            self.BODY=BODY
        def py3(self):
            nonlocal currentTabulation
            codeToReturn="elif ("+self.EXPRESSION.py3()+"):\n"
            codeToReturn+=self.BODY.py3()
            return codeToReturn

    class elseStatement():
        def __init__(self,EXPRESSION,BODY):
            self.EXPRESSION=EXPRESSION
            self.BODY=BODY
        def py3(self):
            nonlocal currentTabulation
            codeToReturn="else:\n"
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

    class scriptStatement():
        def __init__(self,FUNCTION,BODY):
            self.FUNCTION=FUNCTION
            self.BODY=BODY
        def py3(self):
            nonlocal currentTabulation
            codeToReturn="def "+self.FUNCTION.py3()+":\n"
            codeToReturn+=self.BODY.py3()
            return codeToReturn

    #Maths stuff
    class variable():
        def __init__(self,VARIABLENAME):
            self.VARIABLENAME=VARIABLENAME
        def py3(self):
            return self.VARIABLENAME

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
                if self.ARGUMENTS[i]!=None:
                    codeToReturn+=self.ARGUMENTS[i].py3()
                    if i!=len(self.ARGUMENTS)-1:
                        codeToReturn+=","
            return codeToReturn

    class notEqualToComparison():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return "!="+self.OPERAND.py3()

    class greaterThanComparison():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return ">"+self.OPERAND.py3()

    class greaterThanEqualToComparison():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return ">="+self.OPERAND.py3()

    class lessThanComparison():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return "<"+self.OPERAND.py3()

    class lessThanEqualToComparison():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return "<="+self.OPERAND.py3()

    class equalToComparison():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return "=="+self.OPERAND.py3()

    class additionOperation():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return "+"+self.OPERAND.py3()

    class subtractionOperation():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return "-"+self.OPERAND.py3()

    class multiplicationOperation():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return "*"+self.OPERAND.py3()

    class divisionOperation():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return "/"+self.OPERAND.py3()

    class notOperation():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return "not "+self.OPERAND.py3()

    class andOperation():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return "&"+self.OPERAND.py3()

    class orOperation():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return "|"+self.OPERAND.py3()

    class xorOperation():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return "^"+self.OPERAND.py3()

    class lshiftOperation():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return "<<"+self.OPERAND.py3()

    class rshiftOperation():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return ">>"+self.OPERAND.py3()

    class additionAssignmentOperation():
        def __init__(self,OPERAND1,OPERAND2,LIST=None):
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

    class expression():
        def __init__(self,VALUE,NEXT):
            self.VALUE=VALUE #Either REAL or STR (later add list etc)
            self.NEXT=NEXT
            #We use this to store the staircase format
        def py3(self):
            nonlocal currentTabulation
            if self.NEXT!=None:
                return self.VALUE.py3()+self.NEXT.py3()
            else:
                return self.VALUE.py3()

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

    class listType():
        def __init__(self,LIST):
            self.LIST=LIST
        def py3(self):
            codeToReturn="["
            codeToReturn+=self.LIST.py3()
            codeToReturn+="]"
            return codeToReturn

    class itemInList():
        def __init__(self,LISTNAME,EXPRESSION):
            self.LISTNAME=LISTNAME
            self.EXPRESSION=EXPRESSION #Arguments should be a list
        def py3(self):
            return self.LISTNAME+"["+self.EXPRESSION.py3()+"]"

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
            if source[i] not in " \t\n":
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
                    i-=1
                return True

        def takename(enforce=False):
            nonlocal i
            nonlocal source
            name=""
            while source[i] in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.":
                name+=source[i]
                i+=1
            if name!="" and not name.isdigit():
                return name
            else:
                if enforce:
                    print("Error: Expected name, got "+source[i]+" instead")

        def takename_before(operationString):
            nonlocal i
            nonlocal source
            i-=len(operationString)+1
            #Goes back until there's no alphanumeric or underscore character
            while source[i] in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.":
                i-=1
            i+=1 #Go 1 position forward because it goes 1 over
            name=takename(True)
            expect_whitespace()
            if name!="":
                return name

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

        def parseExpression():
            nonlocal i
            nonlocal source
            realValue=""
            expect_whitespace()
            for ii in [takevalue(),
                parseList(),
                parseName(),
                parseString()
                ]:
                if ii!=None:
                    return expression(ii,getNextOperation())
        #^This^ and vthisv are meant to replace the old parseExpression()
        def getNextOperation():
            expect_whitespace()
            for ii in [parseNotOperation(),
                parseAndOperation(),
                parseOrOperation(),
                parseXorOperation(),
                parseLshiftOperation(),
                parseRshiftOperation(),
                parseDivision(),
                parseMultiplication(),
                parseAddition(),
                parseSubtraction(),
                parseGreaterThanEqualTo(),
                parseGreaterThan(),
                parseLessThanEqualTo(),
                parseLessThan(),
                parseNotEqual(),
                parseEqualTo()]:
                if ii!=None:
                    return ii

        def handleOperation(operationString,classToStoreIn):
            nonlocal i
            nonlocal source
            OPERAND=None
            if expect(operationString):
                OPERAND=parseExpression()
                return classToStoreIn(OPERAND)

        def parseName(allowVar=True,allowFunc=True): #Replaces both the old parseFunction() and parseVariable()
            nonlocal i
            nonlocal source
            NAME=takename()
            if NAME!=None:
                if expect("(") and allowFunc: #If there's a bracket parse this as a function
                    ARGUMENTS=parseArguments()
                    expect(")")
                    return function(NAME,ARGUMENTS)
                elif expect("[") and allowVar:
                    EXPRESSION=parseExpression()
                    expect("]")
                    if EXPRESSION!=None:
                        return itemInList(NAME,EXPRESSION)
                elif allowVar:
                    return variable(NAME)

        def parseNotEqual():
            nonlocal i
            nonlocal source
            return handleOperation("!=",notEqualToComparison)

        def parseGreaterThan():
            nonlocal i
            nonlocal source
            return handleOperation(">",greaterThanComparison)

        def parseGreaterThanEqualTo():
            nonlocal i
            nonlocal source
            return handleOperation(">=",greaterThanEqualToComparison)

        def parseLessThan():
            nonlocal i
            nonlocal source
            return handleOperation("<",lessThanComparison)

        def parseLessThanEqualTo():
            nonlocal i
            nonlocal source
            return handleOperation("<=",lessThanEqualToComparison)

        def parseEqualTo():
            nonlocal i
            nonlocal source
            return handleOperation("=",equalToComparison)

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

        def parseNotOperation():
            nonlocal i
            nonlocal source
            return handleOperation("NOT",notOperation)

        def parseAndOperation():
            nonlocal i
            nonlocal source
            return handleOperation("AND",andOperation)

        def parseOrOperation():
            nonlocal i
            nonlocal source
            return handleOperation("OR",orOperation)

        def parseXorOperation():
            nonlocal i
            nonlocal source
            return handleOperation("XOR",xorOperation)

        def parseLshiftOperation():
            nonlocal i
            nonlocal source
            return handleOperation("LSHIFT",lshiftOperation)

        def parseRshiftOperation():
            nonlocal i
            nonlocal source
            return handleOperation("RSHIFT",rshiftOperation)

        def parseArguments():
            nonlocal i
            nonlocal source
            argsBody=[]
            argsBody.append(parseExpression())
            while expect(","):
                argsBody.append(parseExpression())
            return arguments(argsBody)

        def handleAssignment(operationString,classToStoreIn):
            nonlocal i
            nonlocal source
            OPERAND1=parseName(True,False)
            OPERAND2=realNumber(0.0)
            if expect(operationString):
                expect_whitespace()
                OPERAND1=takename_before(operationString)
                expect(operationString)
                expect_whitespace()
                OPERAND2=parseExpression()
                i-=1
                return classToStoreIn(OPERAND1,OPERAND2)

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

        def parseScriptStatement():
            nonlocal i
            nonlocal source
            if expect("script") and expect_whitespace(True):
                    scriptFunction=parseName(False,True)
                    scriptBody=parseCodeBlock()
                    return scriptStatement(scriptFunction,scriptBody)

        def parseIfStatement():
            nonlocal i
            nonlocal source
            if expect("if") and expect_whitespace(True):
                    ifExpression=parseExpression()
                    ifBody=parseCodeBlock()
                    return ifStatement(ifExpression,ifBody)

        def parseElseIfStatement():
            nonlocal i
            nonlocal source
            if expect("else") and expect_whitespace(True):
                    if expect("if") and expect_whitespace(True):
                        elseifExpression=parseExpression()
                        elseifBody=parseCodeBlock()
                        return elseifStatement(elseifExpression,elseifBody)
                    else:
                        elseBody=parseCodeBlock()
                        return elseStatement(elseBody)

        def parseWhileStatement():
            nonlocal i
            nonlocal source
            if expect("while") and expect_whitespace(True):
                    whileExpression=parseExpression(takeexpression())
                    whileBody=parseCodeBlock()
                    return whileStatement(whileExpression,whileBody)

        def parseCodeBlock():
            nonlocal i
            nonlocal source
            body=[]
            line=[]
            expect_whitespace()
            if expect("{",True):
                while i<len(source)-1 and source[i]!="}":
                    i+=1
                    for ii in [parseElseIfStatement(),
                        parseWhileStatement(),
                        parseIfStatement(),
                        parseScriptStatement(),
                        parseEventDefinition(),
                        parseName(False),
                        parseDivisionAssignment(),
                        parseMultiplicationAssignment(),
                        parseAdditionAssignment(),
                        parseSubtractionAssignment(),
                        parseSimpleAssignment()
                        ]:
                        if ii!=None:
                            body.append(ii)
                expect("}",True)
            if body!=[]:
                return codeBlock(body)

        def parseList():
            nonlocal i
            nonlocal source
            LIST=[]
            if expect("["):
                LIST=parseArguments()
                expect("]",True)
                return listType(LIST)

        def parseString():
            nonlocal i
            nonlocal source
            def parseStringDeliniator(deliniator):
                nonlocal i
                nonlocal source
                STRING=""
                if expect(deliniator):
                    while source[i]!=deliniator:
                        if expect("\\") and (expect("\\\"") or expect("\\\'")):
                            STRING+=deliniator
                        else:
                            STRING+=source[i]
                        i+=1
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
            if expect("room") and expect_whitespace(True):
                    roomName=takename()
                    expect_whitespace()
                    roomBody=parseCodeBlock()
                    return roomDefinition(roomName,roomBody)

        i=0
        line=""
        #This is the root loop
        while i<len(source)-1:
            #Put all the parse*() functions here
            for ii in [parseRoomDefinition(),
                parseEventDefinition(),
                parseObjDefinition(),
                parseScriptStatement(),
                parseDivisionAssignment(),
                parseMultiplicationAssignment(),
                parseAdditionAssignment(),
                parseSubtractionAssignment(),
                parseSimpleAssignment()]:
                if ii!=None:
                    rawParsedData.append(ii)
            i+=1
        return rawParsedData

    def transpileToPython(structure):
        pythonCode="#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\nfrom PyG import *\n"
        tempForObject=None
        for i in structure:
            tempForObject=i.py3()
            if tempForObject!=None:
                pythonCode+=tempForObject
        pythonCode+="\ngame_init()\ngame_main()"
        return pythonCode
    return transpileToPython(parse(inputSource))

with open(inputFile,'r') as f:
    latinSource = f.read()
a=transpile(latinSource)
print(a)
with open(outputFile,'w') as f:
    f.write(a)
