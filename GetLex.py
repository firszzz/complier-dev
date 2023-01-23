# -*- coding: utf-8 -*-

import StatesTable
import Lexem

class LexAnalyzer(object):
    def __init__(self, testname):
        self.keyWords = ['readln', 'writeln','and', 'array', 'begin', 'case', 'const', 'div', 'do', 'downto', 'else', 'end', 'file', 'for', 'function', 'goto', 'if', 'in', 'label', 'mod', 'nil', 'not', 'of', 'or', 'packed', 'procedure', 'program', 'record', 'repeat', 'set', 'then', 'to', 'type', 'until', 'var', 'while', 'with']
        self.Delimiter = ['.', ';', ',', '(', ')',  '[', ']', ':', '{','}','$', '..']
        self.operators = ['+', '-', '*', '/', '=', '>', '<','<>',':=','>=','<=','+=','-=','/=','*=', '^', "@"]
        self.separ = [' ','\n', '\t', '\0', '\r']
        self.state = "S" 
        self.fr = open(testname, 'r', encoding="utf-8")
        self.currChar = ' '
        self.buf = ''
        self.lexStartsFrom = 0
        self.lexStartsFromLine = 0
        self.currIndexChar = 0
        self.currLine = 1
        self.stateTable = StatesTable.StatesTable()
        self.type = ''
        self.numbuf = ''
        self.numstartPos = ''

    def nextLex(self):
        self.numbuf = ''
        self.numstartPos = ''
        
        while True:
            if self.state == "S":
                self.buf = ''
                self.lexStartsFrom = self.currIndexChar
                self.lexStartsFromLine = self.currLine
            if self.state == 'BACK':
                self.state = 'D'
                self.numbuf = self.buf[:len(self.buf)-2]
                self.numstartPos = self.lexStartsFrom
                self.buf = self.buf[len(self.buf)-2:]
                self.lexStartsFrom = self.currIndexChar - 2
                return Lexem.Lexem(self.numbuf, 'Integer', self.lexStartsFromLine, self.numstartPos)
            if self.state == "ERR":
                raise Exception(f'Строка  {str(self.lexStartsFromLine)}, символ {str(self.lexStartsFrom)}. Встречена лексическая ошибка в лексеме "{self.buf}"')
            prevState = self.state
            self.state = self.stateTable.getNewState(self.state, self.currChar)
            if self.state != "F":
                self.buf += self.currChar
            else:
                break

            self.currChar = str(self.fr.read(1))
            self.currIndexChar +=1
            
            if self.currChar == '\n':
                self.currIndexChar = 0
                self.currLine += 1

        if prevState == "ENDSTR":
            self.type = 'String'
        if prevState == "ID": 
            if self.buf in self.keyWords:
                self.type = 'Key Word'
            else: self.type = 'Identifier'
        if prevState == "N" or prevState == "16" or prevState == "8" or prevState == "2":
            self.type = 'Integer'
        if prevState == "NFP" or prevState == "NFPORD" or prevState == "NFPE"or prevState == "NFPEO":
            self.type = 'Float'
        if prevState in ["D", "P","BR","SL"]:
            if self.buf in self.operators:
                self.type = 'Operator'
            elif self.buf in self.Delimiter: self.type = 'Delimiter'

        self.state = "S"
        
        if self.buf != '':
            return Lexem.Lexem(self.buf, self.type, self.lexStartsFromLine, self.lexStartsFrom)
        else:
            return Lexem.Lexem("", "Empty", self.lexStartsFromLine, self.lexStartsFrom)

    def getLex(self):
        if self.numbuf:
            return Lexem.Lexem(self.numbuf, 'Integer', self.lexStartsFromLine, self.numstartPos)
        if self.buf:
            return Lexem.Lexem(self.buf, self.type, self.lexStartsFromLine, self.lexStartsFrom)
        else:
            lex = self.nextLex()
            return lex