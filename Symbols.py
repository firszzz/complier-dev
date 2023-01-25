from abc import ABC, abstractmethod

import Lexem

def treeLine(space) -> str:
    return("│"*(space) + "├──")

def default_wl(space) -> str:
    if space != 0:
        return(treeLine(space - 1))
    else:
        return("")

class Symbol():
    @abstractmethod
    def __init__(self, name):
        self.name = name
    def Print(self):
        pass

class SymType(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def Print(self,fw, space):
        writeline = default_wl(space)
        fw.write(writeline + self.name + '\n')

class SymVar(Symbol):
    def __init__(self, name, typeref):
        super().__init__(name)
        self.typeref = typeref

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + self.name.lex + '\n')
        self.typeref.Print(fw, space+1)

class SymInt(SymType):
    def __init__(self, name, typeref):
        super().__init__(name)
        self.typeref = typeref

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + self.name.lex + '\n')
        self.typeref.Print(fw, space+1)

class SymFloat(SymType):
    def __init__(self, name, typeref):
        super().__init__(name)
        self.typeref = typeref

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + self.name.lex + '\n')
        self.typeref.Print(fw, space+1)

class SymStr(SymType):
    def __init__(self, name, typeref):
        super().__init__(name)
        self.typeref = typeref

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + self.name.lex + '\n')
        self.typeref.Print(fw, space+1)

class SymArray(SymType):
    def __init__(self, name, diap):
        super().__init__(name)
        self.diap = diap #[[]]
        self.typeref = SymType(name)
         
    def Print(self, fw, space):
        writeline = treeLine(space)
        writeline2 = treeLine(space + 1)
        for i in self.diap:
            fw.write(writeline  + '[\n')
            fw.write(writeline2 + str(i[0]) + '\n')
            fw.write(writeline2 + str(i[1]) + '\n')
            fw.write(writeline  + ']\n')
        writeline = default_wl(space)
        fw.write(writeline + self.name + '\n')

class SymStruct(Symbol):
    def __init__(self, name):
        super().__init__(name)

class SymFunc(Symbol):
    def __init__(self, name, typeref, args):
        super().__init__(name)
        self.typeref = typeref
        self.args = args

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + self.name + '\n')
        writeline = treeLine(space)
        fw.write(writeline +'(\n')
        for i in self.args:
            i.Print(fw, space+2)
        self.typeref.Print(fw, space+1)
        fw.write(writeline +')\n')

class SymPointer(Symbol):
    def __init__(self, name):
        super().__init__(name)

class SymVoid(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def Print(self, fw, space):
        pass

class SymExpr(Symbol):
    def __init__(self, name, left, right, typeref):
        super().__init__(name)
        self.left = left
        self.right = right
        self.typeref = typeref

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + self.name.lex + '\n')
        self.left.Print(fw, space+1)
        self.right.Print(fw, space+1)
        self.typeref.Print(fw, space+1)

class Node():
    @abstractmethod
    def Print(self):
        pass

class Expression(Node):
    def Print(self):
        pass

class ProgrammNode(Node):
    def __init__(self, stmts):
        self.stmts = stmts

    def Print(self, fw, space):
        for i in self.stmts:
            i.Print(fw, space)

class ProgramNameNode(Node):
    def __init__(self, lex, progname):
        self.lex = lex
        self.progname = progname

    def Print(self, fw, space):
        self.lex.Print(fw, space+1)
        fw.write("├──" + self.progname.lex + '\n')

class ProgVarBlockNode(Node):
    def __init__(self, lex, stmts):
        self.lex = lex
        self.stmts = stmts

    def Print(self, fw, space):
        self.lex.Print(fw, space)
        for i in self.stmts:
            i.Print(fw, space+1)

class ProgVarNode(Node):
    def __init__(self, varanme, _type, numnode, oprtn):
        self.varanme = varanme
        self.vartype = _type
        self.numnode = numnode
        self.oprtn = oprtn

    def Print(self, fw, space):
        writeline = default_wl(space)
        sp = space
        self.oprtn.Print(fw, sp)
        if type(self.oprtn) != NullNode:
            sp +=1
        if sp > space:
            writeline = treeLine(sp - 1)
        fw.write(writeline + str(self.varanme.lex)+'\n')
        sp+=1
        writeline = treeLine(sp - 1)
        if type(self.vartype) == str:
            fw.write(writeline + str(self.vartype)+'\n')
        else:
            self.vartype.Print(fw,sp)
        self.numnode.Print(fw, sp-1)

class SingleTypeNode(Node):
    def __init__(self, lex):
        self.lex = lex
        self.typename = lex.lex

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + str(self.typename)+'\n')

class ArrTypeNode(Node):
    def __init__(self, callW, ofType, ofW, diap, rbrc, lbrc):
        self.callW = callW
        self.ofType = ofType
        self.ofW = ofW
        self.diap = diap
        self.rbrc = rbrc
        self.lbrc = lbrc

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + str(self.callW.lex)+'\n')
        self.ofW.Print(fw, space+1)
        self.ofType.Print(fw, space+2)
        writeline1 = treeLine(space)
        fw.write(writeline1 + str(self.rbrc.lex)+'\n')
        writeline2 = treeLine(space + 1)
        sp = space+2
        if len(self.diap) >1:
            fw.write(writeline2 + ',\n')
            sp = space+3
        for i in self.diap:
            i.Print(fw, sp)
        fw.write(writeline1 + str(self.lbrc.lex)+'\n')

class DiapnNode(Node):
    def __init__(self, delim, right, left):
        self.delim = delim
        self.right = right
        self.left = left

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + str(self.delim.lex)+'\n')
        self.right.Print( fw, space+1)
        self.left.Print( fw, space+1)

class StmtNode(Node):
    def __init__(self, stmt):
        self.stmt = stmt

    def Print(self, fw, space):
        self.stmt.Print(fw, space)

class BlockNode(Node):
    def __init__(self, stmts):
        self.stmts = stmts

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + 'begin\n')
        for i in self.stmts:
            i.Print(fw, space+1)
        fw.write(writeline + 'end\n')

class FuncNode(Node):
    def __init__(self, resulttype, body):
        self.lexref = resulttype
        self.body = body

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + 'function\n')
        self.lexref.Print(fw, space+1)
        self.body.Print(fw, space+1)


class ProcedureNode(Node):
    def __init__(self, resulttype, body):
        self.lexref = resulttype
        self.body = body

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + 'procedure\n')
        self.lexref.Print(fw, space+1)
        self.body.Print(fw, space+1)

class FuncProcRefArg(Node):
    def __init__(self, callW, varNode):
        self.callW = callW
        self.varNode = varNode

    def Print(self, fw, space):
        self.callW.Print(fw, space)
        self.varNode.Print(fw, space+1)

class FuncProcValArg(Node):
    def __init__(self, varNode):
        self.varNode = varNode

    def Print(self, fw, space):
        self.varNode.Print(fw, space)

class WhileNode(Node):
    def __init__(self,cond, body):
        self.condition = cond
        self.body = body

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + 'while\n')
        self.condition.Print(fw, space+1)
        fw.write(writeline + 'do\n')
        self.body.Print(fw, space+1)

class repeatUntilNode(Node):
    def __init__(self, cond, body):
        self.condition = cond
        self.body = body

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + 'repeat\n')
        self.body.Print(fw, space+1)
        fw.write(writeline + 'until\n')
        self.condition.Print(fw, space+1)

class ForNode(Node):
    def __init__(self, condit1, condit2, body, toW):
        self.condition1 = condit1
        self.condition2 = condit2
        self.body = body
        self.toW = toW

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + 'for\n')
        self.condition1.Print(fw, space+1)
        fw.write(writeline + self.toW.lex +'\n')
        self.condition2.Print(fw, space+1)
        fw.write(writeline + 'do\n')
        self.body.Print(fw, space+1)


class IfNode(Node):
    def __init__(self, cond, body, elsebody):
        self.condition = cond
        self.body = body
        self.elsebody = elsebody

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + 'if\n')
        self.condition.Print(fw, space+1)
        fw.write(writeline + 'then\n')
        self.body.Print(fw, space+1)
        if type(self.elsebody) != NullNode:
            fw.write(writeline + 'else\n')
            self.elsebody.Print(fw, space+1)

class KeyWordNode(Node):
     def __init__(self, lex):
         self.lex = lex
         self.name = lex.lex

     def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + str(self.name)+'\n')


class NodeRanger(Node): #????
    def __init__(self, node):
        self.node = node

    def Print(self, space):
        self.node.Print(space)

class NumberNode(Expression):
    def __init__(self,symref):
        self.lexref = symref

    def Print(self, fw, space):
        self.lexref.Print(fw, space)

class StringConstNode(Expression):
    def __init__(self, symref):
         self.lexref = symref

    def Print(self, fw, space):
        self.lexref.Print(fw, space)
    
class IdentNode(Expression):

    def __init__(self, lexref):
        self.lexref = lexref

    def Print(self,fw,  space):
        self.lexref.Print(fw,  space)
        
class BinaryOpNode(Expression):
    def __init__(self, lexref):
        self.lexref = lexref

    def Print(self,fw,  space):
        self.lexref.Print(fw,  space+1)

class UnaryOpNode(Expression):
    def __init__(self, lexref):
        self.lexref = lexref

    def Print(self,fw,  space):
        self.lexref.Print(fw,  space)

class RecordNode(Expression):
    def __init__(self, lex, left, right):
        self.operetion = lex.lex
        self.lex = lex
        self.left = left
        self.right = right

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + self.operetion+'\n')
        for i in self.left:
            i.Print(fw, space+1)
        self.right.Print(fw, space+1)

class ArrayNode(Expression):
    def __init__(self, lex, middle):
        self.lexref = lex
        self.position = middle #[]

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + self.lexref.name.lex+'\n')
        writeline1 = treeLine(space)
        fw.write(writeline1 +'[\n')
        writeline2 = treeLine(space + 1)
        for i in self.position:
            fw.write(writeline2 + i +'\n')
        fw.write(writeline1 +']\n')
        fw.write(writeline1 + self.lexref.typeref.name+'\n')

class СallNode(Expression):
    def __init__(self, lex, middle):
        self.lexref = lex
        self.middle = middle

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + self.lexref.name+'\n')
        writeline = treeLine(space)
        fw.write(writeline+  '(\n')
        for i in self.middle:
            i.Print(fw, space+2)
        fw.write(writeline + ')\n')

class NullNode(Node):
    def __init__(self):
        self.name = ""
        lexref = SymVoid('')

    def Print(self, fw, space):
        pass

class WritelnNode(Node):
    def __init__(self, callW, toinput):
        self.callW = callW
        self.toinput = toinput

    def Print(self, fw, space):
        self.callW.Print(fw, space)
        for i in self.toinput:
            i.Print(fw, space+1)

class ReadlnNode(Node):
    def __init__(self,callW, tooutput):
        self.callW = callW
        self.tooutput = tooutput

    def Print(self, fw, space):
        self.callW.Print(fw, space)
        for i in self.tooutput:
            i.Print(fw, space+1)


class AssignNode(Node):
    def __init__(self, lex, right, left):
        self.operation = lex.lex
        self.lex = lex
        self.right = right
        self.lexref = left

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + self.operation + '\n')
        for i in [self.lexref]:
            i.Print(fw, space+1)
        for i in [self.right]:
            i.Print(fw, space+1)

class BoolOpNode(Node):
    def __init__(self, lex, left, right):
        self.operation = lex.lex
        self.lex = lex
        self.left = left
        self.right = right

    def Print(self, fw, space):
        writeline = default_wl(space)
        fw.write(writeline + self.operation + '\n')
        for i in self.left:
            i.Print(fw, space+1)
        for i in self.right:
            i.Print(fw, space+1)

class VarAssignNode(Node):
    def __init__(self, lex):
        self.lex = lex
        self.name = lex.lex

    def Print(self, fw, space):
        if space != 0:
            writeline = treeLine(space - 1)
        else:
            writeline = ""
        fw.write(writeline + self.name + '\n')

class ErrorNode(Node):
    def __init__(self, errortext:str):
        self.errortext = errortext

    def Print(self, fw, space):
        fw.write(str(self.errortext) + '\n')
