# -*- coding: utf-8 -*-

class Lexem(object):

    def __init__(self, _lex, _type, _line, _charn):
        self.lex = _lex.lower()
        self.type = _type
        self.line = _line
        self.charn = _charn
        self.mean = self.ismeannum()

    def ismeannum(self):
        if  self.lex:
            if self.lex[0] == "$":
                return int(self.lex[1:], 16)
            elif self.lex[0] == "&":
                return int(self.lex[1:], 8)
            elif self.lex[0] == "%":
                return int(self.lex[1:], 2)
            elif self.type == "String":
                mean = self.lex[1:len(self.lex)-1]
                return mean
            try: 
                mean = float(self.lex)
                if mean.is_integer():
                    return int(mean)
                return mean
            except: pass
        return ""

    def output(self):
        if self.type == "Empty":
            return ''
        if self.mean != '':
            nummean = self.mean
            if type(self.mean) is int:
                nummean = self.mean
            elif type(self.mean) is str:
                nummean = self.mean
            else:
                nummean = "{0:.15f}".format(self.mean).rstrip('0')
            return f'{self.line}' +'\t' + f'{self.charn}'+'\t' + f'{self.type}'+'\t' + f'{self.lex}' + '\t' + f'{nummean}'
        return f'{self.line}' +'\t' + f'{self.charn}'+'\t' + f'{self.type}'+'\t' + f'{self.lex}'