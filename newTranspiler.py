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
def transpile(source):
    global formattedString
    #First remove all the whitespace from the beginning of each line
    text=""
    #Parser tree (Based on BIDMAS) Parse in reverse order:
    #New lines
    #Spaces
    #Curly brackets aka code blocks
    #Strings
    #statements
    #functions
    #opening/closing brackets aka arguments
    #constants
    #maths
    arithmeticOperations=["+=","-=","*=","/=","=","*","/","-","+"] #Order is important
    parsedBlocks=[]
    parsedNewlines=[]
    parsedSpaces=[]
    parsedStatements=[]
    parsedFunctions=[]
    parsedArguments=[]
    index=[]
    tempList=[]

    def parse_nested(text, left=r'[{]', right=r'[}]', sep=r','):
        """ Based on http://stackoverflow.com/a/17141899/190597 (falsetru) """
        pat = r'({}|{}|{})'.format(left, right, r'')
        tokens = re.split(pat, text)
        stack = [[]]
        for x in tokens:
            if not x or re.match(sep, x): continue
            if re.match(left, x):
                stack[-1].append([])
                stack.append(stack[-1][-1])
            elif re.match(right, x):
                stack.pop()
                if not stack:
                    raise ValueError('Error: opening bracket is missing')
            else:
                for i in x.split("\n"):
                    if i.lstrip(' \t')!="":
                        stack[-1].append(i.lstrip(' \t'))

        if len(stack) > 1:
            print(stack)
            raise ValueError('Error: closing bracket is missing')
        return stack.pop()

    #Here we create a list that also handles the ()s
    def parseBrackets(lst):
        toReturn=[]
        for i in lst:
            if isinstance(i,list):
                toReturn.append(parseBrackets(i))
            else:
                toReturn.append(parse_nested(i,r'[(]',r'[)]'))
        return toReturn

    #Here we build the class list
    def parseCreateList(lst,level=0):
        toReturn=[]
        tmpList=[]
        for i in lst:
            if isinstance(i,list): #Go deeper
                toReturn.append(parseCreateList(i,level+1))
            else:
                for ii in i.split(" "):
                    #Handles arithmetic operations
                    for iii in arithmeticOperations:
                        if iii in ii:
                            print("Depth: "+str(level),"Data: "+str([iii]+ii.split("=")))
                            toReturn.append([iii]+ii.split(iii))
                            break
                    else:
                        print("Depth: "+str(level),"Data: "+str(ii))
                        toReturn.append(ii)

        return toReturn

    print(parseCreateList(parseBrackets(parse_nested(source))))
    return ""

with open(inputFile,'r') as f:
    latinSource = f.read()
with open(outputFile,'w') as f:
    f.write(transpile(latinSource))
