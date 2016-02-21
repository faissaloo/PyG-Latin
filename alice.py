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
    constants={"c_black":"0",
        "c_red":"1",
        "c_green":"2",
        "c_yellow":"3",
        "c_blue":"4",
        "c_magenta":"5",
        "c_cyan":"6",
        "c_white":"7",
        "pi":"3.141592653589793",
        "tau":"6.283185307179586"}
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
            currentTabulation+=1
            codeToReturn+=getCorrectTabulation()+"engineVars.current_room=self\n"
            codeToReturn+=getCorrectTabulation()+"self.instanceList=[]\n"
            currentTabulation-=1
            codeToReturn+=self.BODY.py3()
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
        def __init__(self,BODY):
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
    #Python style
    class forInStatement():
        def __init__(self,VARNAME,LIST,BODY):
            self.VARNAME=VARNAME
            self.LIST=LIST
            self.BODY=BODY
        def py3(self):
            nonlocal currentTabulation
            codeToReturn="for "+self.VARNAME.py3()+" in "+self.LIST.py3()+":\n"
            codeToReturn+=self.BODY.py3()
            return codeToReturn
    #C style
    class forFromStatement():
        def __init__(self,VARNAME,START,END,BY,BODY):
            self.VARNAME=VARNAME
            self.START=START
            self.END=END
            if BY!=None:
                self.BY=BY
            else:
                self.BY=1
            self.BODY=BODY
        def py3(self):
            nonlocal currentTabulation
            codeToReturn=self.VARNAME.py3()+"="+self.START.py3()+"\n"
            codeToReturn+=getCorrectTabulation()+"while ("+self.VARNAME.py3()+"<"+self.END.py3()+"):\n"
            codeToReturn+=self.BODY.py3()
            currentTabulation+=1
            codeToReturn+=getCorrectTabulation()+self.VARNAME.py3()+"+="+self.BY.py3()+"\n"
            currentTabulation-=1
            return codeToReturn

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
            #Here we check if the 'variable' is a constant and return the constant value if so
            try:
                return constants[self.VARIABLENAME]
            except KeyError:
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

    class powerOperation():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return "**"+self.OPERAND.py3()

    class notOperation():
        def __init__(self,OPERAND):
            self.OPERAND=OPERAND
        def py3(self):
            return "~"+self.OPERAND.py3()

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
        def __init__(self,VALUE,NEXT,BRACKETED=False):
            self.VALUE=VALUE #Either REAL or STR (later add list etc)
            self.NEXT=NEXT
            self.BRACKETED=BRACKETED
            #We use this to store the staircase format
        def py3(self):
            nonlocal currentTabulation
            if not self.BRACKETED:
                if self.NEXT!=None:
                    return self.VALUE.py3()+self.NEXT.py3()
                else:
                    return self.VALUE.py3()
            else:
                if self.NEXT!=None:
                    try:
                        return str(eval("("+self.VALUE.py3()+self.NEXT.py3()+")"))
                    except:
                        return "("+self.VALUE.py3()+self.NEXT.py3()+")"
                else:
                    return "("+self.VALUE.py3()+")"

    #Datatypes
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
        def raiseException(string):
            nonlocal i
            nonlocal source
            def getLineAndColumn():
                nonlocal i
                nonlocal source
                line=0
                column=0
                for ii in range(len(source)):
                    if source[ii]=="\n":
                        line+=1
                        column=0
                    else:
                        column+=1
                    if i==ii:
                        break
                return line,column
            currentPos=getLineAndColumn()
            print("Error: "+string+" on line "+str(currentPos[0])+" column "+str(currentPos[1]))
            exit()
        def expect(string,whitespace=False):
            nonlocal i
            nonlocal source
            originali=i
            if source[i:i+len(string)]==string:
                i+=len(string)#Skip over the thing
                if whitespace:
                    if expect_whitespace():
                        return True
                    else:
                        i=originali
                        return False
                return True
            else:
                return False

        def expect_whitespace():
            nonlocal i
            nonlocal source
            if source[i] not in " \t\n":
                return False
            else:
                while source[i] in " \t\n" and i<len(source)-1:
                    i+=1 #Skip over whitespace, for some reason this is going to far
                return True

        def expect_whitespacebefore():
            nonlocal i
            nonlocal source
            if source[i] not in " \t\n":
                return False
            else:
                while source[i] in " \t\n" and i>0:
                    i-=1
                return True

        def expectComment():
            nonlocal i
            nonlocal source
            if expect("//"):
                while source[i]!="\n":
                    i+=1

        def takename():
            nonlocal i
            nonlocal source
            name=""
            while source[i] in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.":
                name+=source[i]
                i+=1
            if name!="" and not name.isdigit():
                return name

        def takename_before(operationString):
            nonlocal i
            nonlocal source
            i-=len(operationString)+1
            #Goes back until there's no alphanumeric or underscore character
            while source[i] in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.":
                i-=1
            i+=1 #Go 1 position forward because it goes 1 over
            name=takename()
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
                return realNumber(value)

        def parseExpression(bracketed=False):
            nonlocal i
            nonlocal source
            realValue=""
            expect_whitespace()
            for ii in [parseSubtraction(),
                parseAddition(),
                parseNotOperation(),
                takevalue(),
                parseList(),
                parseName(),
                parseString(),
                parseBracketedExpression()
                ]:
                if ii!=None:
                    return expression(ii,getNextOperation(),bracketed)

        def parseBracketedExpression():
            nonlocal i
            nonlocal source
            if expect("("):
                EXPR=parseExpression(True)
                expect(")")
                return EXPR

        def getNextOperation():
            expect_whitespace()
            expectComment()
            for ii in [parseAndOperation(),
                parseOrOperation(),
                parseXorOperation(),
                parseLshiftOperation(),
                parseRshiftOperation(),
                parsePower(),
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

        def parsePower():
            nonlocal i
            nonlocal source
            return handleOperation("^",powerOperation)

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
            if expect("script",True):
                    scriptFunction=parseName(False,True)
                    scriptBody=parseCodeBlock()
                    return scriptStatement(scriptFunction,scriptBody)

        def parseIfStatement():
            nonlocal i
            nonlocal source
            if expect("if",True):
                    ifExpression=parseExpression()
                    ifBody=parseCodeBlock()
                    return ifStatement(ifExpression,ifBody)

        def parseElseIfStatement():
            nonlocal i
            nonlocal source
            if expect("else",True):
                    if expect("if",True):
                        elseifExpression=parseExpression()
                        elseifBody=parseCodeBlock()
                        return elseifStatement(elseifExpression,elseifBody)
                    else:
                        elseBody=parseCodeBlock()
                        return elseStatement(elseBody)
        def parseForStatement():
            nonlocal i
            nonlocal source

            if expect("for",True):
                VARNAME=parseName(True,False)
                expect_whitespace()
                #C style: for n from 0 to 50 by 5
                if expect("from",True):
                    START=parseExpression()
                    if expect("to",True):
                        END=parseExpression()
                        if expect("by",True):
                            BY=parseExpression()
                            BODY=parseCodeBlock()
                            return forFromStatement(VARNAME,START,END,BY,BODY)
                        else:
                            raiseException("Expected 'by'")
                    else:
                        raiseException("Expected 'to'")

                    #Py style:for elt in collection
                elif expect("in",True):
                    LIST=parseExpression()
                    BODY=parseCodeBlock()
                    return forInStatement(VARNAME,LIST,BODY)
                else:
                    raiseException("Expected 'from' or 'in' statement")

        def parseWhileStatement():
            nonlocal i
            nonlocal source
            if expect("while",True):
                    whileExpression=parseExpression(takeexpression())
                    whileBody=parseCodeBlock()
                    return whileStatement(whileExpression,whileBody)

        def parseCodeBlock():
            nonlocal i
            nonlocal source
            body=[]
            line=[]
            expect_whitespace()
            if expect("{"):
                while i<len(source)-1 and source[i]!="}":
                    i+=1
                    for ii in [parseElseIfStatement(),
                        parseWhileStatement(),
                        parseIfStatement(),
                        parseForStatement(),
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
                if not expect("}"):
                    raiseException("Unterminated block")
            if body!=[]:
                return codeBlock(body)

        def parseList():
            nonlocal i
            nonlocal source
            LIST=[]
            if expect("["):
                LIST=parseArguments()
                expect("]")
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
                    expect(deliniator)
                    return string(STRING)
                else:
                    return None
            for ii in [parseStringDeliniator("\""),parseStringDeliniator("\'")]:
                if ii!=None:
                    return ii

        def parseObjDefinition():
            nonlocal i
            nonlocal source
            if expect("obj",True):
                    objName=takename()
                    expect_whitespace()
                    objBody=parseCodeBlock()
                    return objDefinition(objName,objBody)

        def parseEventDefinition():
            nonlocal i
            nonlocal source
            if expect("event",True):
                eventName=takename()
                expect_whitespace()
                eventBody=parseCodeBlock()
                return eventDefinition(eventName,eventBody)

        def parseRoomDefinition():
            nonlocal i
            nonlocal source
            expect_whitespace()
            if expect("room",True):
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
                parseObjDefinition(),
                parseScriptStatement(),
                parseElseIfStatement(),
                parseWhileStatement(),
                parseIfStatement(),
                parseForStatement(),
                parseScriptStatement(),
                parseEventDefinition(),
                parseName(False),
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
        pythonCode="#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\nfrom PyG import *\nimport engineVars\n"
        tempForObject=None
        for i in structure:
            tempForObject=i.py3()
            if tempForObject!=None:
                pythonCode+=tempForObject
        pythonCode+="\ngame_main()"
        return pythonCode
    return transpileToPython(parse(inputSource))

with open(inputFile,'r') as f:
    latinSource = f.read()
a=transpile(latinSource)
print(a)
with open(outputFile,'w') as f:
    f.write(a)
