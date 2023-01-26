from collections import OrderedDict

import GetLex
import Symbols
import Node

class Parser():

    def __init__(self, testname):
        self.lexAnalizer = GetLex.LexAnalyzer(testname)
        self.stackTable = []
        self.curlex = ''

    def require(self, name):
        if self.lexAnalizer.getLex().lex not in name:
            waited = "' или '".join(name)
            raise  Exception(f'Строка  {str(self.curlex.line)}, символ {str(self.curlex.charn)}. Встречено "{self.lexAnalizer.getLex().lex}", ожидалось "{waited}"')
        self.lexAnalizer.nextLex()

    def requireType(self, typename):
        if self.lexAnalizer.getLex().type not in typename:
            waited = "' или '".join(typename)
            raise  Exception(f'Строка  {str(self.curlex.line)}, символ {str(self.curlex.charn)}. Встречено "{self.lexAnalizer.getLex().lex}", ожидалось "{waited}"')

    def checkNodeType(self, Nodetypes, nodetocheck):
        if type(nodetocheck) in Nodetypes:
            raise Exception(f'Строка  {str(self.curlex.line)}, символ {str(self.curlex.charn)}. Встречено "{self.lexAnalizer.getLex().lex}", ожидалось выражение')

    def showError(self, massage):
        raise Exception(f'Строка  {str(self.curlex.line)}, символ {str(self.curlex.charn)}. {massage}')

    def parseProgramm(self):
        try:
            stmts = []
            self.curlex = self.lexAnalizer.getLex()
            if self.curlex.lex == 'program':
                progW = Symbols.KeyWordNode(self.curlex)
                self.curlex = self.lexAnalizer.nextLex()
                self.requireType(["Identifier"])
                stmts.append(Symbols.ProgramNameNode(progW, self.curlex))
                self.require([";"])
            self.stackTable.append(OrderedDict())
            self.curlex = self.lexAnalizer.getLex()
            while self.curlex.lex in ["function", "procedure", 'var']:
                if self.curlex.lex =="function":
                    parsed = self.parseFunction()
                elif self.curlex.lex == "procedure":
                    parsed = self.parseProcedure()
                elif self.curlex.lex == "var":
                    varstmts = []
                    progW = Symbols.KeyWordNode(self.curlex)
                    self.lexAnalizer.nextLex()
                    while self.curlex.lex not in ["function", "procedure", 'begin']:
                        for i in self.parseVar():
                            varstmts.append(i)
                        self.require([";"])
                        self.curlex = self.lexAnalizer.getLex()
                    parsed = Symbols.ProgVarBlockNode(progW, varstmts)
                stmts.append(parsed)
                self.curlex = self.lexAnalizer.getLex()
            if self.curlex.lex == 'begin':
                stmts.append(self.parseStmt())
                self.require(["."])
            return (Symbols.ProgrammNode(stmts))
        except Exception as e:
            return(Symbols.ErrorNode(e))

    def formalParameter(self, name):
        funcname = self.lexAnalizer.getLex()
        self.requireType(["Identifier"])
        self.lexAnalizer.nextLex()
        self.curlex = self.lexAnalizer.getLex()
        args = []
        if self.curlex.lex == "(":
            self.lexAnalizer.nextLex()
            while self.curlex.lex == ";" or self.curlex.lex == "(":
                self.curlex = self.lexAnalizer.getLex()
                if self.curlex.lex == 'var':
                    varcallW = Symbols.KeyWordNode(self.curlex)
                    self.curlex = self.lexAnalizer.nextLex()
                    for i in self.parseVar():
                        args.append(Symbols.FuncProcRefArg(varcallW, i))
                else:
                    for i in self.parseVar():
                        args.append(Symbols.FuncProcValArg(i))
                self.curlex = self.lexAnalizer.getLex()
            self.require([")"])
        else:
            args.append(Symbols.NullNode())
        return [funcname, args]

    def parseFunction(self):
        self.require(['function'])
        self.stackTable.append(OrderedDict())
        params = self.formalParameter("function")
        colon = self.lexAnalizer.getLex()
        self.require([":"])
        self.requireType(["Identifier"])
        resulttype = self.lexAnalizer.getLex()
        self.lexAnalizer.nextLex()
        self.require([";"])
        body = self.parseStmt()
        self.require([";"])
        self.stackTable.pop()

        resultLexref = Symbols.SymFunc(params[0].lex, Symbols.SymType(resulttype.lex), params[1])
        self.stackTable[-1][params[0].lex] = resultLexref
        return Symbols.FuncNode(resultLexref, body)
    
    def parseProcedure(self):
        self.require(['procedure'])
        self.stackTable.append(OrderedDict())
        params = self.formalParameter("procedure")
        self.require([";"])
        body = self.parseStmt()
        self.require([";"])
        self.stackTable.pop()
        resultLexref = Symbols.SymFunc(params[0].lex, Symbols.SymVoid(""), params[1])
        self.stackTable[-1][params[0].lex] = resultLexref
        return Symbols.ProcedureNode(resultLexref, body)

    def parseVar(self):
        self.curlex = self.lexAnalizer.getLex()
        varnames = []
        if self.curlex.type == 'Delimiter':
            return(Symbols.NullNode())
        self.requireType(["Identifier"])
        if self.curlex.lex not in self.stackTable[-1]:
            self.stackTable[-1][self.curlex.lex] = ''
        else:
            self.showError(f'Переменная {str(self.curlex.lex)} объявлена повторно')
        oplex = self.lexAnalizer.nextLex()
        varnames.append(self.curlex)
        while oplex.lex == ",":
            self.curlex = self.lexAnalizer.nextLex()
            self.requireType(["Identifier"])
            if self.curlex.lex not in self.stackTable[-1]:
                self.stackTable[-1][self.curlex.lex] = ''
            else:
                self.showError(f'Переменная {str(self.curlex.lex)} объявлена повторно')
            self.parseFactor()
            varnames.append(self.curlex)
            oplex = self.lexAnalizer.getLex()
        oprtn = Symbols.VarAssignNode(self.lexAnalizer.getLex())
        self.require([":", ":="])
        self.curlex = self.lexAnalizer.getLex()
        if self.curlex.lex ==";":
            self.showError(f'Встречено {str(self.curlex.lex)}, ожидалось выражение')
        if (self.curlex.type =="Identifier" or self.curlex.lex == "array") and oprtn.name == ':':
            vartype = self.parseInitType()
            oprtn = Symbols.NullNode()
            self.curlex = self.lexAnalizer.nextLex()
            exprnode = Symbols.NullNode()
        elif oprtn.name == ':=':
            exprnode = self.parseExpression()
            vartype = exprnode.lexref.typeref.name
        varnodeslist = []
        for i in varnames:
            self.stackTable[-1][i.lex] = vartype
            varnodeslist.append(Symbols.ProgVarNode(i, self.stackTable[-1][i.lex], exprnode, oprtn))
        return varnodeslist

    def parseStmt(self):
        self.curlex = self.lexAnalizer.getLex()
        stmt = ''
        if self.curlex.lex == "begin":
            stmt = self.parseBlock()
        elif self.curlex.lex == "if":
            stmt = self.parseIf()
        elif self.curlex.lex == "while":
            stmt = self.parseWhile()
        elif self.curlex.lex == "repeat":
            stmt = self.parseRepeatUntil()
        elif self.curlex.lex == "var":
            varW = Symbols.KeyWordNode(self.curlex)
            self.lexAnalizer.nextLex()
            stmt = Symbols.ProgVarBlockNode(varW, self.parseVar())
        elif self.curlex.lex == "for":
            stmt = self.parseFor()
        elif self.curlex.lex == "break":
            self.lexAnalizer.nextLex()
            stmt = Symbols.KeyWordNode(self.curlex)
        elif self.curlex.lex == "continue":
            self.lexAnalizer.nextLex()
            stmt = Symbols.KeyWordNode(self.curlex)
        elif self.curlex.type == "Identifier":
            stmt = self.parseAssigmOrFunc()
        elif self.curlex.lex == "readln": 
            stmt = self.parseReadln()
        elif self.curlex.lex == "writeln":
            stmt = self.parseWriteln()
        elif self.curlex.lex == "end" or self.curlex.lex == ";" :
            return Symbols.NullNode()
 
        if stmt:
            return stmt
        return Symbols.NullNode()

    def parseWriteln(self):
        callW = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        self.require(['writeln'])
        oplex = self.lexAnalizer.getLex()
        self.require(['('])
        tooutput = []
        while oplex.lex ==',' or oplex.lex =='(':
            tooutput.append(self.parseExpression())
            oplex = self.lexAnalizer.getLex()
        self.require([')'])
        return Symbols.WritelnNode(callW, tooutput)

    def parseInitType(self):
        typeLex = self.lexAnalizer.getLex()
        diap = []

        if typeLex.lex == "array":
            while typeLex.lex == "array":
                oplex = self.lexAnalizer.nextLex()
                if oplex.lex == '[':
                    while oplex.lex in [",", "["]:
                        self.lexAnalizer.nextLex()
                        parsedDiap = self.parseDiap()
                        oplex = self.lexAnalizer.getLex()
                        diap.append(parsedDiap)
                    self.require([']'])
                else:
                    diap.append([0, 1e3])
                self.require(['of'])
                typeLex = self.lexAnalizer.getLex()
            typel = self.parseInitType()
            return Symbols.SymArray(typel.name, diap)
        else:
            return Symbols.SymType(typeLex.lex)

    def parseDiap(self):
        fromexpr = self.parseExpression()

        try:
            fromN = int(fromexpr.lexref.name.lex)
        except:
            self.showError(f'При объявлении массива ожидалась константа')

        delim = self.lexAnalizer.getLex()

        if delim.lex in [',', ']']:
            self.showError(f'Ожидался диапазон')
        self.require(['..',','])

        toexpr = self.parseExpression()
        try:
            toN = int(toexpr.lexref.name.lex)
        except:
            self.showError(f'При объявлении массива ожидалась константа')

        if type(fromexpr) == Symbols.NullNode:
            self.showError(f'Встречено {self.curlex.lex}, ожидалось выражение')
        if type(toexpr) == Symbols.NullNode:
            self.showError(f'Встречено {self.curlex.lex}, ожидалось выражение')

        return [fromN, toN]

    def parseReadln(self):
        callW = Symbols.KeyWordNode(self.lexAnalizer.getLex())
        self.require(['readln'])
        oplex = self.lexAnalizer.getLex()
        self.require(['('])
        toinput = []

        while oplex.lex ==',' or oplex.lex =='(':
            toinput.append(self.parseExpression())
            oplex = self.lexAnalizer.getLex()
        self.require([')'])
        return Symbols.ReadlnNode(callW, toinput)

    def parseAssigmOrFunc(self):
        left = self.parseFactor() #Node
        self.curlex = self.lexAnalizer.getLex()

        if self.curlex.lex in [";", "end"]:
            return left
        elif self.curlex.lex in  [":=","+=","-=","*=","/="]:
            oper = self.curlex
            self.lexAnalizer.nextLex()
            right = self.parseExpression()
            if left.lexref.typeref.name != right.lexref.typeref.name:
                self.showError(f'Нельзя преобразовать тип {str(right.lexref.typeref.name)} к {str(left.lexref.typeref.name)}')
            return Symbols.AssignNode(oper, right, left)
        else:
            self.require([":=","+=","-=","*=","/="]) 

    def parseBlock(self):
        self.require(['begin'])
        self.stackTable.append(OrderedDict())
        self.curlex = self.lexAnalizer.getLex()
        stmnts = []
        while self.curlex.lex != "end":
            stmnts.append(self.parseStmt())
            self.curlex = self.lexAnalizer.getLex()
            if self.curlex.lex != ";":
                break;
            self.lexAnalizer.nextLex()
        self.require(['end'])
        self.stackTable.pop()
        return Symbols.BlockNode(stmnts)
    
    def parseWhile(self):
        self.require(['while'])
        expression = self.parseExpression()
        if expression.lexref.typeref.name!="boolean":
            self.showError(f'Условие должно быть типа boolean')
        self.require(['do'])
        body = self.parseStmt()
        return Symbols.WhileNode(expression, body)

    def parseRepeatUntil(self):
        self.require(['repeat'])
        body = self.parseStmt()
        self.require(['until'])
        expression = self.parseExpression()
        if expression.lexref.typeref.name!="boolean":
            self.showError(f'Условие должно быть типа boolean')
        return Symbols.repeatUntilNode(expression, body)

    def parseFor(self):
        self.require(['for'])
        self.stackTable.append(OrderedDict())
        condit1 = self.parseStmt()
        try:
            if condit1.lexref.lexref.typeref.name!="integer":
                self.showError(f'Ожидался тип integer')
        except:
            if condit1.stmts[0].vartype!="integer":
                self.showError(f'Ожидался тип integer')
                ProgVarBlockNode
        toW = self.lexAnalizer.getLex()
        self.require(['to', 'downto'])
        condit2 = self.parseExpression()
        try:
            if condit2.lexref.typeref.name!="integer":
                self.showError(f'Ожидался тип integer')
        except:
            if condit2.stmts[0].vartype.name!="integer":
                self.showError(f'Ожидался тип integer')
                ProgVarBlockNode
        self.require(['do'])
        body = self.parseStmt()
        self.stackTable.pop()
        return Symbols.ForNode(condit1, condit2, body, toW)

    def parseIf(self):
        self.require(['if'])
        expression = self.parseExpression()
        if expression.lexref.typeref.name!="boolean":
            self.showError(f'Условие должно быть типа boolean')
        self.require(['then'])
        body = self.parseStmt()
        if self.lexAnalizer.getLex() == 'else':
            self.lexAnalizer.nextLex()
            elsebody = self.parseStmt()
        else:
            elsebody = Symbols.NullNode()
        return Symbols.IfNode(expression, body, elsebody)

    def parseExpression(self):
        left = self.parseTerm()
        oplex = self.lexAnalizer.getLex()
        leftpoints =[left]
        while (oplex.type == "Operator" or oplex.type == "Key Word") and oplex.lex in ['+','-', 'or']:
            self.curlex = self.lexAnalizer.nextLex()
            right = self.parseTerm()
            if oplex.lex == "or":
                if right.lexref.typeref.name=="boolean" and left.lexref.typeref.name=="boolean":
                    newtyperef = right.lexref.typeref
                else:
                    self.showError(f'Нельзя сравнить типы {str(right.lexref.typeref.name)} и {str(left.lexref.typeref.name)}')
            elif oplex.lex == '-':
                if right.lexref.typeref.name=="string" or left.lexref.typeref.name=="string":
                    self.showError(f'Оператор "{oplex.lex}" не применим к типу "String"')
            newtyperef = right.lexref.typeref
            if left.lexref.typeref.name == right.lexref.typeref.name:
                symexpr = Symbols.SymExpr(oplex, left, right, newtyperef)
            elif left.lexref.typeref.name in ['integer', 'float'] and right.lexref.typeref.name in ['integer', 'float']:
                if oplex.lex in ['-','+']:
                    newtyperef = Symbols.SymType("float")
                else:
                    newtyperef = Symbols.SymType("integer")
                symexpr = Symbols.SymExpr(oplex, left, right, newtyperef)
            else:
                self.showError(f'Нельзя преобразовать тип {str(right.lexref.typeref.name)} к {str(left.lexref.typeref.name)}')
            leftpoints = [Symbols.BinaryOpNode(symexpr)]
            oplex = self.lexAnalizer.getLex()
        if (oplex.type == "Operator" or oplex.type == "Key Word") and oplex.lex in ['=','<>', '<','>', '>=', '<=', 'in']:
            self.curlex = self.lexAnalizer.nextLex()
            right = self.parseExpression()
            newtyperef = Symbols.SymType("boolean")
            if left.lexref.typeref.name == right.lexref.typeref.name:
                symexpr = Symbols.SymExpr(oplex, left, right, newtyperef)
            else:
                self.showError(f'Нельзя сравнить переменные типа {str(right.lexref.typeref.name)} и {str(left.lexref.typeref.name)}')
            leftpoints = [Symbols.BinaryOpNode(symexpr)]
            oplex = self.lexAnalizer.getLex()
            return leftpoints[0]
        return leftpoints[0]
    
    def parseTerm(self):
        left = self.parseFactor()
        oplex = self.lexAnalizer.getLex()
        leftpoints = [left]
        while oplex.type == "Operator" or oplex.type == "Key Word":
            if oplex.lex in ['*','/', 'div','mod', 'and']:
                self.curlex = self.lexAnalizer.nextLex() 
                right = self.parseFactor()
                if oplex.lex == "and":
                    if right.lexref.typeref.name=="boolean" and left.lexref.typeref.name=="boolean":
                        newtyperef = right.lexref.typeref
                    else:
                        self.showError(f'Нельзя сравнить типы {str(right.lexref.typeref.name)} и {str(left.lexref.typeref.name)}')
                elif oplex.lex in ["/", 'div','mod']:
                    if right.lexref.typeref.name=="string" or left.lexref.typeref.name=="string":
                        self.showError(f'Оператор "{oplex.lex}" не применим к типу "String"')
                    elif oplex.lex=="/":
                        newtyperef = Symbols.SymType("float")
                    else:
                        newtyperef = right.lexref.typeref
                else:
                    newtyperef = right.lexref.typeref
                if left.lexref.typeref.name == right.lexref.typeref.name:
                    symexpr = Symbols.SymExpr(oplex, left, right, newtyperef)
                elif left.lexref.typeref.name in ['integer', 'float'] and right.lexref.typeref.name in ['integer', 'float']:
                    if oplex.lex in ['/'] or left.lexref.typeref.name == 'float' or left.lexref.typeref.name == 'float':
                        newtyperef = Symbols.SymType("float")
                    elif oplex.lex in ['div','mod']:
                        newtyperef = Symbols.SymType("integer")
                    else:
                        self.showError("Операция {oplex.lex} не применима к переменым такого типа")
                    symexpr = Symbols.SymExpr(oplex, left, right, newtyperef)
                else:
                    self.showError(f'Нельзя преобразовать тип {str(right.lexref.typeref.name)} к {str(left.lexref.typeref.name)}')
                leftpoints = [Symbols.BinaryOpNode(symexpr)]
                oplex = self.lexAnalizer.getLex()
            else:
                return leftpoints[0]
        return leftpoints[0]

    def parseFactor(self):
        self.curlex = self.lexAnalizer.getLex()
        oplex = self.lexAnalizer.getLex()
        if oplex.lex.lower() in ['not','+', '-','^', '@']:
            operation = oplex
            self.lexAnalizer.nextLex()
            right = self.parseFactor()
            self.checkNodeType([Symbols.NullNode], right)
            symexpr = Symbols.SymExpr(operation, Symbols.NullNode(), right, right.lexref.typeref)
            return Symbols.UnaryOpNode(symexpr)
        if self.curlex.type == "Identifier":
            ident = self.curlex
            symb_var = ''
            for i in reversed(self.stackTable):
                if ident.lex in i:
                    self.lexAnalizer.nextLex() 
                    symb_var = Symbols.SymVar(ident, i[ident.lex])
                    tableElem = i[ident.lex]
                    break;
            if not symb_var:
                self.showError(f'Переменная {self.curlex.lex} не была объявлена')
            oplex = self.lexAnalizer.getLex()

            if oplex.type == "Delimiter" and oplex.lex == "[":
                mid =[]
                middle = []

                while oplex.lex in [',','[']:
                    self.lexAnalizer.nextLex() 
                    mid.append(self.parseExpression())
                    oplex = self.lexAnalizer.getLex() 
                if len(mid) != len(tableElem.diap):
                    self.showError(f'Неверное количество индексов, ожидалось {len(tableElem.diap)}')
                for i in range(len(mid)):
                    mid_ = ''
                    try:
                        mid_ = int(mid[i].lexref.name.lex)
                    except:
                        pass
                    if mid_:
                        if mid_ <= tableElem.diap[i][0] or mid_ >= tableElem.diap[i][1]:
                            self.showError(f'Индекс за пределами диапазона')
                    else:
                        if mid[i].lexref.typeref.name != 'integer':
                            self.showError(f'Тип должен быть integer')
                    middle.append(mid[i].lexref.name.lex)
                self.curlex = self.lexAnalizer.getLex()
                self.require(["]"])
                return Symbols.ArrayNode(symb_var, middle)

            if oplex.type == "Delimiter" and oplex.lex == "(":
                main = self.curlex
                open = oplex
                self.curlex = self.lexAnalizer.nextLex() 
                mid = []
                
                if self.lexAnalizer.getLex().lex == ')':
                    self.curlex = self.lexAnalizer.nextLex() 
                else:
                    while self.curlex.lex != ")":
                        mid.append(self.parseExpression())
                        self.curlex = self.lexAnalizer.getLex()
                        self.require([")", ","])
                if type(tableElem) != Symbols.SymVoid:
                    if len(mid) != len(tableElem.args):
                        self.showError(f'Передано неверное количество аргументов')
                    for i in range(len(mid)):
                        if mid[i].lexref.typeref.name != tableElem.args[i].varNode.vartype.name:
                            if not (mid[i].lexref.typeref.name == "integer" and tableElem.args[i].varNode.vartype.name == 'float'):
                                self.showError(f'Передана переменная неверного типа')
                return Symbols.CallNode(tableElem, mid)
            return Symbols.IdentNode(symb_var)
        elif self.curlex.type == "Integer":
            varSym = Symbols.SymInt(self.curlex, Symbols.SymType(self.curlex.type.lower()))
            self.lexAnalizer.nextLex() 
            return Symbols.NumberNode(varSym)
        elif self.curlex.type == "Float":  
            varSym = Symbols.SymFloat(self.curlex, Symbols.SymType(self.curlex.type.lower()))
            self.lexAnalizer.nextLex() 
            return Symbols.NumberNode(varSym)
        elif self.curlex.type == "String":
            varSym = Symbols.SymStr(self.curlex, Symbols.SymType(self.curlex.type.lower()))
            self.lexAnalizer.nextLex() 
            return Symbols.StringConstNode(varSym)
        elif self.curlex.lex == "(":
            self.lexAnalizer.nextLex() 
            self.curlex = self.lexAnalizer.getLex()
            curNode = self.parseExpression()
            self.checkNodeType([Symbols.NullNode], curNode)
            self.curlex = self.lexAnalizer.getLex()
            self.require([")"])
            return curNode
        return Symbols.NullNode()