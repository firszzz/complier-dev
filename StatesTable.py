# -*- coding: utf-8 -*-
from itertools import chain
class StatesTable(object):

    def __init__(self):
        #S - Start, F - Finish, ID - Identifier, N = Number, NF = Number Float, D - Delimiter, STR - String, COM - comment, ERR - error
        self.States = {'S': {"":"F", '_':"ID",'\n': "S", '\t': "S", ' ': "S", "'":"STR1", ';': "D", '@': "D", '^': "D", '+': "D" ,'*': "D" ,'-': "D" ,"/": "SL", "(": "BR" ,")": "D" ,"[": "D" ,"]": "D", ",": "D" ,".": "P", ":": "D", "<": "D" ,">": "D" ,"=": "D", "{": "COM1" ,"}": "ERR", "$": "16", "&": "8", "%":"2", "?":"D","^":"D","@":"D" },
                       'ID': {"":"F", '_':"ID",'\n': "F", '\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "F" ,'*': "F" ,'-': "F" ,"/": "F", "(": "F", ")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "F", ":": "F", "<": "F" ,">": "F" ,"=": "F"},
                       'N': {"{": "F", "":"F",'_':"ERR",'\n': "F", '\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "F" ,'*': "F" ,'-': "F" ,"/": "F", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "NFPORD", ":": "F", "<": "F" ,">": "F" ,"=": "F"},
                       'D': {"": "F", '_':"F",'\n': "F", '\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "F" ,'*': "F" ,'-': "F" ,"/": "F", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "F", ":": "F", "<": "F" ,">": "D" ,"=": "D"},
                       #'ToDot':{},
                       'P':{"":"F",".": "D", "": "F"," ": "F","\n": "F","/t": "F","{": "F","/": "F","(": "F"},
                       'BR':{"":"F","*": "COM2", "": "F", '_':"F",'\n': "ERR", '\t': "F", ' ': "F", '"':"F","'":"F", ';': "ERR", '@': "F", '^': "F", '+': "F" ,'-': "F" ,"/": "F", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "ERR", ":": "F"},
                       'SL':{"":"F","/": "COMS", "": "F", '_':"F",'\n': "ERR", '\t': "F", ' ': "F", '"':"F","'":"F", ';': "ERR", '@': "F", '^': "F", '+': "F" ,'-': "F" , "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "ERR", ":": "F"},
                       'COMS': {"":"F",'\n': "S", '\r': "S", "": "S"},       #//
                       'COM1':{"":"F",'}': "S"},       #{}
                       'COM2':{"":"F",'*': 'COM2RD'},        #(**)
                       'COM2RD': {"":"F",')': "S"},
                       'STR1':{"":"F","'": "ENDSTR"},       #'
                       'NFPORD':{"":"F",'.':"BACK"},
                       'BACK':{},
                       'NFP': {"":"F", '_':"ERR",'\n': "F", '\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "F" ,'*': "F" ,'-': "F" ,"/": "F", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "ERR", ":": "F", "<": "F" ,">": "F" ,"=": "F"},
                       'NFPEO': {"":"F",'_':"ERR",'\n': "F", '\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "F" ,'*': "F" ,'-': "F" ,"/": "F", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "ERR", ":": "F", "<": "F" ,">": "F" ,"=": "F"},
                       'NFPE': {"":"F",'_':"ERR",'\n': "F", '\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "NFPEO" ,'*': "F" ,'-': "NFPEO" ,"/": "F", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "ERR", ":": "F", "<": "F" ,">": "F" ,"=": "F"},
                       '16':{"":"F","A":"16","B":"16","C":"16","D":"16","E":"16","F":"16","a":"16","b":"16","c":"16","d":"16","e":"16","f":"16",  "{": "F",'\n': "F",'\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "F" ,'*': "F" ,'-': "F" ,"/": "F", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "F", ":": "F", "<": "F" ,">": "F" ,"=": "F"},
                       '8':{"":"F", "{": "F",'\n': "F",'\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "F" ,'*': "F" ,'-': "F" ,"/": "F", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "F", ":": "F", "<": "F" ,">": "F" ,"=": "F"},
                       '2':{"":"F","0":"2", "1":"2", "":"F", "{": "F",'\n': "F",'\t': "F", ' ': "F", '"':"F","'":"F", ';': "F", '@': "F", '^': "F", '+': "F" ,'*': "F" ,'-': "F" ,"/": "F", "(": "F" ,")": "F" ,"[": "F" ,"]": "F", ",": "F" ,".": "F", ":": "F", "<": "F" ,">": "F" ,"=": "F"},

                       }
        self.FillStates()
   
    def FillStates(self):
        for i in chain(range(65,91), range(97,123)):
            self.States["S"][chr(i)] = "ID"
            self.States["ID"][chr(i)] = "ID"
            self.States["D"][chr(i)] = "F"
            self.States["P"][chr(i)] = "F"
            self.States["BR"][chr(i)] = "F"
            self.States["SL"][chr(i)] = "F"
        for i in range(0,10):
            self.States["S"][str(i)] = "N"
            self.States["ID"][str(i)] = "ID"
            self.States["N"][str(i)] = "N"
            self.States["NFPORD"][str(i)] = "NFP"
            self.States["NFP"][str(i)] = "NFP"
            self.States["NFPEO"][str(i)] = "NFPEO"
            self.States["NFPE"][str(i)] = "NFPE"
            self.States["D"][str(i)] = "F"
            self.States["NFPORD"][str(i)] = "NFP"
            self.States["16"][str(i)] = "16"
            self.States["8"][str(i)] = "8"
            self.States["BR"][str(i)] = "F"
            self.States["SL"][str(i)] = "F"
        self.States["8"]["8"] = "ERR"
        self.States["8"]["9"] = "ERR"
        self.States["NFPORD"]['E'] = "NFPE"
        self.States["NFPORD"]['e'] = "NFPE"
        self.States["NFP"]['E'] = "NFPE"
        self.States["NFP"]['e'] = "NFPE"
        self.States["N"]['E'] = "NFPE"
        self.States["N"]['e'] = "NFPE"

    def getNewState(self, _state: str, _char: str):
        _char = _char.lower()
        if _state =="COMS" or _state =="STR1" or _state =="COM1" or _state =="COM2": 
            if _char == "":
                return "S"
            if _char in self.States[_state]:
                return self.States[_state][_char]
            else:
                return _state
        if _state =="COM2RD":
            if _char in self.States[_state]:
                return self.States[_state][_char]
            else:
                return "COM2"
        if _state =="ENDSTR":
            return "F"
        if _state in self.States:
            if _char in self.States[_state]:
                return self.States[_state][_char]
        return "ERR"