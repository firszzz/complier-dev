import GetLex
import Node
import sys

class Parser():

    def __init__(self, testname):
        self.lexAnalizer = GetLex.GetLex(testname)
        self.curlex = ''

    def Require(self, name):
        if self.lexAnalizer.getLex().lex not in name:
            waited = "' или '".join(name)
            raise  Exception(f'Строка  {str(self.lexAnalizer.lexStartsFromLine)}, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено "{self.lexAnalizer.getLex().lex}", ожидалось "{waited}"')
        self.lexAnalizer.nextLex()

    def RequireType(self, typename):
        if self.lexAnalizer.getLex().type not in typename:
            waited = "' или '".join(typename)
            raise  Exception(f'Строка  {str(self.lexAnalizer.lexStartsFromLine)}, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено "{self.lexAnalizer.getLex().lex}", ожидалось "{waited}"')

    def checkNodeType(self, Nodetypes, nodetocheck):
        if type(nodetocheck) in Nodetypes:
            raise Exception(f'Строка  {str(self.lexAnalizer.lexStartsFromLine)}, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено "{self.lexAnalizer.getLex().lex}", ожидалось выражение')

    def parseProgramm(self):
        try:
            stmts = []
            self.curlex = self.lexAnalizer.getLex()
            if self.curlex.lex == 'program':
                progW = Node.KeyWordNode(self.curlex)
                self.curlex = self.lexAnalizer.nextLex()
                self.RequireType(["Identifier"])
                stmts.append(Node.ProgramNameNode(progW, self.curlex))
                self.Require([";"])
            self.curlex = self.lexAnalizer.getLex()
            while self.curlex.lex in ["function","procedure", 'var']:
                if self.curlex.lex =="function":
                    parsed = self.parseFunction()
                elif self.curlex.lex == "procedure":
                    parsed = self.parsePocedure()
                elif self.curlex.lex == "var":
                    varstmts = []
                    progW = Node.KeyWordNode(self.curlex)
                    self.lexAnalizer.nextLex()
                    while self.curlex.lex != 'begin':
                        varstmts.append(self.parseVar())
                        self.Require([";"])
                        self.curlex = self.lexAnalizer.getLex()
                    parsed = Node.ProgVarBlockNode(progW, varstmts)
                stmts.append(parsed)
                self.curlex = self.lexAnalizer.getLex()
            if self.curlex.lex == 'begin':
                stmts.append(self.parseStmt())
                self.Require(["."])
            return (Node.ProgrammNode(stmts))
        except Exception as e:
            e_type, e_val, e_tb = sys.exc_info()
            return(Node.ErrorNode(e))

    def procedfunc(self, name):
        funcCallW  = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require([name])
        funcname = self.lexAnalizer.getLex()
        self.RequireType(["Identifier"])
        self.lexAnalizer.nextLex()
        self.curlex = self.lexAnalizer.getLex()
        args = []
        if self.curlex.lex == "(":
            rbrac = self.lexAnalizer.getLex()
            self.lexAnalizer.nextLex()
            while self.curlex.lex == ";" or self.curlex.lex == "(":
                self.curlex = self.lexAnalizer.getLex()
                if self.curlex.lex == 'var':
                    varcallW = Node.KeyWordNode(self.curlex)
                    self.curlex = self.lexAnalizer.nextLex()
                    args.append(Node.FuncProcRefArg(varcallW, self.parseVar()))
                else:
                    args.append(Node.FuncProcValArg(self.parseVar()))
                self.curlex = self.lexAnalizer.getLex()
            lbrac = self.lexAnalizer.getLex()
            self.Require([")"])
        else:
            rbrac = ''
            lbrac = ''
            args.append(Node.NullNode())
        return [funcCallW, funcname, rbrac, args, lbrac]

    def parseFunction(self):
        params = self.procedfunc("function")
        dotdot = self.lexAnalizer.getLex()
        self.Require([":"])
        self.RequireType(["Identifier"])
        resulttype = self.lexAnalizer.getLex()
        self.lexAnalizer.nextLex()
        self.Require([";"])
        body = self.parseStmt()
        self.Require([";"])
        return Node.FuncNode(params[0], params[1], params[2], params[4],dotdot,resulttype, body, params[3])
    
    def parsePocedure(self):
        params = self.procedfunc("procedure")
        self.Require([";"])
        body = self.parseStmt()
        self.Require([";"])
        return Node.ProcedureNode(params[0], params[1], params[2], params[4], body, params[3])

    
    def parseVar(self):
        self.curlex = self.lexAnalizer.getLex()
        varnames = []
        if self.curlex.type == 'Delimiter':
            return(Node.NullNode())
        self.RequireType(["Identifier"])
        varibl = self.parseFactor()
        oplex = self.lexAnalizer.getLex()
        varnames.append(varibl)
        while oplex.lex == ",":
            self.curlex = self.lexAnalizer.nextLex()
            self.RequireType(["Identifier"])
            varibl = self.parseFactor()
            varnames.append(varibl)
            oplex = self.lexAnalizer.getLex()
        oprtn = Node.VarAssignNode(self.lexAnalizer.getLex())
        self.Require([":", ":="])
        self.curlex = self.lexAnalizer.getLex()
        if self.curlex.lex ==";":
            raise Exception(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено "{self.curlex.lex}", ожидалось выражение или тип переменной')
        if (self.curlex.type =="Identifier" or self.curlex.lex == "array") and oprtn.name == ':':
            _type = self.parseInitType()
            oprtn = Node.NullNode()
            self.curlex = self.lexAnalizer.nextLex()
        else:
            _type = Node.NullNode()
        if oprtn.name == ':=':
            exprnode = self.parseExpression()
            return Node.ProgVarNode(varnames, _type, exprnode, oprtn)
        oplex = self.lexAnalizer.getLex()
        if oplex.lex == "=" or oplex.lex == ":=":
            oprtn = Node.VarAssignNode(oplex)
            self.lexAnalizer.nextLex()
            exprnode = self.parseExpression()
        else:
            oprtn = Node.NullNode()
            exprnode = Node.NullNode()
        return Node.ProgVarNode(varnames, _type, exprnode, oprtn)

    def parseInitType(self):
        typeLex = self.lexAnalizer.getLex()
        if typeLex.lex == "array":
            oplex = self.lexAnalizer.nextLex()
            if oplex.lex == '[':
                rbrc = oplex
                diap = []
                while oplex.lex in [",", "["]:
                    self.lexAnalizer.nextLex()
                    diap.append(self.parseDiap())
                    oplex = self.lexAnalizer.getLex()
                lbrc = self.lexAnalizer.getLex()
                self.Require([']'])
            ofW = self.lexAnalizer.getLex()
            self.Require(['of'])
            typel = self.parseInitType()
            return Node.ArrTypeNode(typeLex, typel, Node.KeyWordNode(ofW), diap, rbrc, lbrc)
        else:
            return Node.SingleTypeNode(typeLex)

    def parseDiap(self):
        fromexpr = self.parseExpression()
        delim = self.lexAnalizer.getLex()
        if delim.lex in [',', ']']:
            return fromexpr
        self.Require(['..',','])
        toexpr = self.parseExpression()
        if type(fromexpr) == Node.NullNode:
            return Node.ErrorNode(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено {self.curlex.lex}, ожидалось выражение')
        if type(toexpr) == Node.NullNode:
            return Node.ErrorNode(f'Строка {str(self.lexAnalizer.lexStartsFromLine) }, символ {str(self.lexAnalizer.lexStartsFrom)}. Встречено {self.curlex.lex}, ожидалось выражение')
        return Node.DiapnNode(delim, fromexpr, toexpr)

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
            self.lexAnalizer.nextLex()
            varW = Node.KeyWordNode(self.curlex)
            stmt = Node.ProgVarBlockNode(varW, [self.parseVar()])
        elif self.curlex.lex == "for":
            stmt = self.parseFor()
        elif self.curlex.lex == "break":
            self.lexAnalizer.nextLex()
            stmt = Node.KeyWordNode(self.curlex)
        elif self.curlex.lex == "continue":
            self.lexAnalizer.nextLex()
            stmt = Node.KeyWordNode(self.curlex)
        elif self.curlex.type == "Identifier":
            stmt = self.parseAssigmOrFunc()
        elif self.curlex.lex == "readln": 
            stmt = self.parseReadln()
        elif self.curlex.lex == "writeln":
            stmt = self.parseWriteln()
        elif self.curlex.lex == "end" or self.curlex.lex == ";" :
            return Node.NullNode()
        if stmt:
            return Node.StmtNode(stmt)
        else:
            return Node.NullNode()

    def parseWriteln(self):
        callW = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['writeln'])
        oplex = self.lexAnalizer.getLex()
        self.Require(['('])
        tooutput = []
        while oplex.lex ==',' or oplex.lex =='(':
            tooutput.append(self.parseExpression())
            oplex = self.lexAnalizer.getLex()
        self.Require([')'])
        return Node.WritelnNode(callW, tooutput)


    def parseReadln(self):
        callW = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['readln'])
        oplex = self.lexAnalizer.getLex()
        self.Require(['('])
        toinput = []
        while oplex.lex ==',' or oplex.lex =='(':
            toinput.append(self.parseExpression())
            oplex = self.lexAnalizer.getLex()
        self.Require([')'])
        return Node.ReadlnNode(callW, toinput)
        
    def parseAssigmOrFunc(self):
        left = self.parseFactor()
        self.curlex = self.lexAnalizer.getLex()
        if self.curlex.lex in [";", "end"]:
            return left
        elif self.curlex.lex in  [":=","+=","-=","*=","/="]:
            oper = self.curlex
            self.lexAnalizer.nextLex()
            right = self.parseExpression()
            return Node.AssignNode(oper, right, left)
        else:
            self.Require([":=","+=","-=","*=","/="])
            

    def parseBlock(self):
        open = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['begin'])
        self.curlex = self.lexAnalizer.getLex()
        stmnts = []
        while self.curlex.lex != "end":
            stmnts.append(self.parseStmt())
            self.curlex = self.lexAnalizer.getLex()
            if self.curlex.lex != ";":
                break;
            self.lexAnalizer.nextLex()
        close = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['end'])
        return Node.BlockNode(stmnts, open, close)
    
    def parseWhile(self):
        call = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['while'])
        expression = self.parseExpression()
        doW = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['do'])
        body = self.parseStmt()
        return Node.WhileNode(call, expression, body, doW)

    def parseRepeatUntil(self):
        call = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['repeat'])
        body = self.parseStmt()
        untilW = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['until'])
        expression = self.parseExpression()
        return Node.repeatUntilNode(call, expression, body, untilW)

    def parseFor(self):
        call = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['for'])
        condit1 = self.parseStmt()
        toW = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['to', 'downto'])
        condit2 = self.parseExpression()
        doW = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['do'])
        body = self.parseStmt()
        return Node.ForNode(call, condit1, toW, condit2, doW, body)

    def parseIf(self):
        call = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['if'])
        expression = self.parseExpression()
        thenW = Node.KeyWordNode(self.lexAnalizer.getLex())
        self.Require(['then'])
        body = self.parseStmt()
        if self.lexAnalizer.getLex() == 'else':
            elseW = Node.KeyWordNode(self.lexAnalizer.getLex())
            self.lexAnalizer.nextLex()
            elsebody = self.parseStmt()
        else:
            elseW = Node.NullNode()
            elsebody = Node.NullNode()
        return Node.IfNode(call, expression, body, thenW, elsebody, elseW)

    def parseExpression(self):
        # получение левой части выражения
        left = self.parseTerm()
        oplex = self.lexAnalizer.getLex()
        leftpoints = left

         # проверка на бинарные операторы и ключевые слова
        while (oplex.type == "Operator" or oplex.type == "Key Word") and oplex.lex.lower() in ['+','-', 'or','xor']:
            self.curlex = self.lexAnalizer.nextLex()
            right = self.parseTerm()
            self.checkNodeType([Node.NullNode], right)
            leftpoints = Node.BinOpNode(oplex, [leftpoints], right)
            oplex = self.lexAnalizer.getLex()

        # Обработка логических операций '=','<>', '<','>', '>=', '<=', 'in'
        if (oplex.type == "Operator" or oplex.type == "Key Word") and oplex.lex.lower() in ['=','<>', '<','>', '>=', '<=', 'in']:
            self.curlex = self.lexAnalizer.nextLex()
            right = self.parseExpression()
            self.checkNodeType([Node.NullNode], right)
            return Node.BoolOpNode(oplex, [leftpoints], [right])
        return leftpoints

    def parseTerm(self):
        # получение левой части
        left = self.parseFactor()
        oplex = self.lexAnalizer.getLex()
        leftpoints = [left]
        
        # проверка на точку, как разделитель
        if oplex.type == "Delimiter" and oplex.lex == ".":
            self.curlex = self.lexAnalizer.nextLex()
            right = self.parseTerm()
            leftpoints = [Node.RecordNode(oplex, leftpoints, right)]
        while oplex.type == "Operator" or oplex.type == "Key Word":
            if oplex.lex.lower() in ['*','/', 'div','mod', 'as', 'is', 'and']:
                self.curlex = self.lexAnalizer.nextLex() 
                right = self.parseFactor()
                self.checkNodeType([Node.NullNode], right)
                leftpoints = [Node.BinOpNode(oplex, leftpoints, right)]
                oplex = self.lexAnalizer.getLex()
            else:
                return leftpoints[0]
        return leftpoints[0]

    def parseFactor(self):
        self.curlex = self.lexAnalizer.getLex()
        oplex = self.lexAnalizer.getLex()

        # проверка на унарные операторы
        if oplex.lex.lower() in ['not','+', '-','^', '@']:
            operation = oplex
            self.lexAnalizer.nextLex()
            right = self.parseFactor()
            self.checkNodeType([Node.NullNode], right)
            return Node.UnarOpNode(operation, right)

        # проверка на идентификатор, readln, writeln
        if self.curlex.type == "Identifier" or self.curlex.lex == "readln" or self.curlex.lex == "writeln":
            self.lexAnalizer.nextLex() 
            oplex = self.lexAnalizer.getLex()   
            if oplex.type == "Delimiter" and oplex.lex == "[":
                main = self.curlex
                open = oplex
                self.lexAnalizer.nextLex() 
                mid = self.parseExpression()
                self.curlex = self.lexAnalizer.getLex()
                self.Require(["]"])
                return Node.toMassNode(main, [mid], open, self.curlex)
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
                        self.Require([")", ","])
                # возвращает узел функции
                return Node.callNode(main, mid, open, self.curlex)
            return Node.IdentNode(self.curlex)
        # Этот код обрабатывает случай, когда лексема является целым или дробным числом. Он возвращает экземпляр класса NumberNode с лексемой как аргументом.
        elif self.curlex.type == "Integer" or self.curlex.type == "Float":  
            self.lexAnalizer.nextLex() 
            return Node.NumberNode(self.curlex)
        #Этот код обрабатывает случай, когда лексема является строковой константой. Он возвращает экземпляр класса StringConstNode с лексемой как аргумент
        elif self.curlex.type == "String":
            self.lexAnalizer.nextLex() 
            return Node.StringConstNode(self.curlex)
        elif self.curlex.lex == "(":
            self.lexAnalizer.nextLex() 
            self.curlex = self.lexAnalizer.getLex()
            curNode = self.parseExpression()
            self.checkNodeType([Node.NullNode], curNode)
            self.curlex = self.lexAnalizer.getLex()
            self.Require([")"])
            return curNode
        return Node.NullNode()

## Метод parseExpression используется для анализа выражений, метод parseTerm — для анализа терминов, а метод parseFactor — для анализа факторов.