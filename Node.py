from abc import ABC, abstractmethod

import Lexem

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
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        sp = space
        self.vartype.Print(fw, sp)
        if type(self.vartype) != NullNode:
            sp+=1
        self.oprtn.Print(fw, sp)
        if type(self.oprtn) != NullNode:
            sp+=1
        writeline = "│" * (sp-1) + "├──"
        for i in self.varanme:
            i.Print(fw,sp)
        self.numnode.Print(fw, sp)

class SingleTypeNode(Node):
    def __init__(self, lex):
        self.lex = lex
        self.typename = lex.lex

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
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
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        fw.write(writeline + str(self.callW.lex)+'\n')
        self.ofW.Print(fw, space+1)
        self.ofType.Print(fw, space+2)
        writeline1 = "│"*(space) + "├──"
        fw.write(writeline1 + str(self.rbrc.lex)+'\n')
        writeline2 = "│"*(space+1) + "├──"
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
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        fw.write(writeline + str(self.delim.lex)+'\n')
        self.right.Print( fw, space+1)
        self.left.Print( fw, space+1)

class FrrayInitNode(Node):
    def __init__(self, varanme, _type, numnode, oprtn):
        self.varanme = varanme
        self.vartype = _type
        self.numnode = numnode
        self.oprtn = oprtn

class StmtNode(Node):
    def __init__(self, stmt):
        self.stmt = stmt

    def Print(self, fw, space):
        self.stmt.Print(fw, space)

class BlockNode(Node):
    def __init__(self, stmts, open, close):
        self.stmts = stmts
        self.openW = open
        self.closeW = close

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        self.openW.Print( fw, space)
        for i in self.stmts:
            i.Print(fw, space+1)
        self.closeW.Print( fw, space)

class FuncNode(Node):
    def __init__(self, callW, funcName, rbrac, lbrac, dotdot,resulttype, body, args):
        self.callW = callW
        self.funcName = funcName
        self.rbrac = rbrac
        self.lbrac = lbrac
        self.dotdot = dotdot
        self.resulttype = resulttype
        self.body = body
        self.args = args

    def Print(self, fw, space):
        self.callW.Print(fw, space)
        sp = space
        writeline1 = "│"*space + "├──"
        fw.write(writeline1 + str(self.funcName.lex)+'\n')
        writeline2 = "│"*(space +1) + "├──"
        sp+=2
        if self.rbrac:
            fw.write(writeline2 + str(self.rbrac.lex)+'\n')
            sp = space + 3
        for i in self.args:
            i.Print(fw, sp)
        if self.lbrac:
            fw.write(writeline2 + str(self.lbrac.lex)+'\n')
            sp -= 1
        fw.write(writeline1 + str(self.dotdot.lex)+'\n')
        fw.write(writeline2 + str(self.resulttype.lex)+'\n')
        self.body.Print(fw, space+1)


class ProcedureNode(Node):
    def __init__(self, callW, funcName, rbrac, lbrac, body, args):
        self.callW = callW
        self.funcName = funcName
        self.rbrac = rbrac
        self.lbrac = lbrac
        self.body = body
        self.args = args

    def Print(self, fw, space):
        self.callW.Print(fw, space)
        sp = space
        writeline1 = "│"*space + "├──"
        fw.write(writeline1 + str(self.funcName.lex)+'\n')
        writeline2 = "│"*(space +1) + "├──"
        sp+=2
        if self.rbrac:
            fw.write(writeline2 + str(self.rbrac.lex)+'\n')
            sp = space + 3
        for i in self.args:
            i.Print(fw, sp)
        if self.lbrac:
            fw.write(writeline2 + str(self.lbrac.lex)+'\n')
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
    def __init__(self, lex, cond, body,doW:Node):
        self.call = lex
        self.condition = cond
        self.body = body
        self.doW = doW

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        self.call.Print( fw, space)
        self.condition.Print(fw, space+1)
        self.doW.Print( fw, space)
        self.body.Print(fw, space+1)

class repeatUntilNode(Node):
    def __init__(self, repeatW, cond, body, untilW:Node):
        self.call = repeatW
        self.condition = cond
        self.body = body
        self.untilW = untilW

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        self.call.Print( fw, space)
        self.body.Print(fw, space+1)
        self.untilW.Print( fw, space)
        self.condition.Print(fw, space+1)

class ForNode(Node):
    def __init__(self, callW, condit1, toW, condit2, doW, body : Node):
        self.call = callW
        self.condition1 = condit1
        self.condition2 = condit2
        self.body = body
        self.toW = toW
        self.doW = doW

    def Print(self, fw, space):
        self.call.Print(fw, space)
        self.condition1.Print(fw, space+1)
        self.toW.Print(fw, space)
        self.condition2.Print(fw, space+1)
        self.doW.Print(fw, space)
        self.body.Print(fw, space+1)

class IfNode(Node):
    def __init__(self, lex:Lexem.Lexem, cond, body,thenW, elsebody, elseW:Node):
        self.call = lex
        self.condition = cond
        self.body = body
        self.thenW = thenW
        self.elseW = elseW
        self.elsebody = elsebody

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        self.call.Print( fw, space)
        self.condition.Print(fw, space+1)
        self.thenW.Print( fw, space)
        self.body.Print(fw, space+1)
        self.elseW.Print( fw, space)
        self.elsebody.Print(fw, space+1)

class KeyWordNode(Node):
     def __init__(self, lex):
         self.lex = lex
         self.name = lex.lex

     def Print(self, fw, space):
         if space != 0:
            writeline = "│"*(space-1) + "├──"
         else:
            writeline = ""
         fw.write(writeline + str(self.name)+'\n')


class NodeRanger(Node): #????
    def __init__(self, node):
        self.node = node

    def Print(self, space):
        self.node.Print(space)

class NumberNode(Expression):

    def __init__(self, lex):
        self.lex = lex
        self.value = lex.mean

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        fw.write(writeline + str(self.value)+'\n')

class StringConstNode(Expression):

    def __init__(self, lex):
        self.lex = lex
        self.value = lex.mean

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        fw.write(writeline + str(self.value)+'\n')
    
class IdentNode(Expression):

    def __init__(self, lex):
        self.name = lex.lex
        self.lex = lex

    def Print(self,fw,  space):
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        fw.write(writeline + self.name+'\n')
        
class BinOpNode(Expression):

    def __init__(self, oplex, left, right):
        self.oplex = oplex
        self.operetion = oplex.lex
        self.left = left
        self.right = right

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        fw.write(writeline + self.operetion+'\n')
        for i in self.left:
            i.Print(fw, space+1)
        self.right.Print(fw, space+1)

class UnarOpNode(Expression):
    def __init__(self, lex, right):
        self.name = lex.lex
        self.lex = lex
        self.right = right

    def Print(self,fw,  space):
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        fw.write(writeline + str(self.name)+'\n')
        self.right.Print(fw,  space+1)

class RecordNode(Expression):
    def __init__(self, lex, left, right):
        self.operetion = lex.lex
        self.lex = lex
        self.left = left
        self.right = right

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        fw.write(writeline + self.operetion+'\n')
        for i in self.left:
            i.Print(fw, space+1)
        self.right.Print(fw, space+1)

class toMassNode(Expression):
    def __init__(self, lex, middle, opensk, closesk):
        self.mainname = lex.lex
        self.opensk = opensk
        self.closesk = closesk
        self.lex = lex
        self.middle = middle

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        fw.write(writeline + self.mainname+'\n')
        if space != 0:
            writeline = "│"*(space) + "├──"
        else:
            writeline = ""
        fw.write(writeline + self.opensk.lex + '\n')
        for i in self.middle:
            i.Print(fw, space+2)
        fw.write(writeline + self.closesk.lex+'\n')

class callNode(Expression):
    def __init__(self, lex, middle, opensk, closesk):
        self.mainname = lex.lex
        self.opensk = opensk
        self.closesk = closesk
        self.lex = lex
        self.middle = middle

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        fw.write(writeline+ self.mainname + '\n')
        writeline = "│"*(space) + "├──"
        fw.write(writeline + self.opensk.lex +'\n')
        for i in self.middle:
            i.Print(fw, space+2)
        fw.write(writeline + self.closesk.lex + '\n')

class NullNode(Node):
    def __init__(self):
        self.name = ""

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
        self.left = left

    def Print(self, fw, space):
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        fw.write(writeline + self.operation + '\n')
        for i in [self.left]:
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
        if space != 0:
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
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
            writeline = "│"*(space-1) + "├──"
        else:
            writeline = ""
        fw.write(writeline + self.name + '\n')

class ErrorNode(Node):
    def __init__(self, errortext:str):
        self.errortext = errortext

    def Print(self, fw, space):
        fw.write(str(self.errortext) + '\n')