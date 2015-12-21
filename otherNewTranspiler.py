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
        class ifStatement():
            def __init__(self,STATEMENT,BODY):
                self.STATEMENT=STATEMENT
                self.BODY=BODY
        class whileStatement():
            def __init__(self,STATEMENT,BODY):
                self.STATEMENT=STATEMENT
                self.BODY=BODY
        class forStatement():
            def __init__(self,STATEMENT,BODY):
                self.STATEMENT=STATEMENT
                self.BODY=BODY

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
            print(name)
            return name

        def parseCodeBlock():
            nonlocal i
            nonlocal source
            body=[]
            line=""
            while source[i]!="}":
                i+=1 #Putting this here at the beginning instead of at the end seems to fix things kinda, why?
                event=parseEventDefinition()
                if event!=None:
                    body.append(event)
            if expect("\n"):
                body.append(line)
                line=""
            else:
                line+=source[i]
            print(body)
            return body

        def parseObjDefinition():
            nonlocal i
            nonlocal source
            objBody=""
            if expect("obj") and expect_whitespace(True): #Nesting them because I need them in this specific order and I'm not sure how Python's parsing tree for logic statements works
                    objName=takename()
                    expect_whitespace()
                    if expect("{",True):
                        objBody=parseCodeBlock()
                    expect("}",True)
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
                if expect("{"):
                    eventBody=parseCodeBlock()
                expect("}")
                return eventDefinition(eventName,eventBody)
        i=0
        line=""
        while i<len(source):
            #Put all the other parse*() functions here
            if expect("\n"):
                rawParsedData.append(line)
                line=""
            else:
                line+=source[i]
            for ii in [parseEventDefinition(),parseObjDefinition()]:
                if ii!=None:
                    rawParsedData.append(ii)

            i+=1
        #Debug
        if len(rawParsedData)>0:
            print(rawParsedData[0])
        return rawParsedData

    return parse(inputSource)

with open(inputFile,'r') as f:
    latinSource = f.read()
with open(outputFile,'w') as f:
    f.write(transpile(latinSource))
