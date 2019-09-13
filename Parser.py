from Lexer import Lexer
from treelib import Node, Tree

class Parser(object):
    def __init__(self,path):
        lex = Lexer(path)
        lex.tokenize()
        self.TOKENS = lex.tokenList
        self.INDEX = 0
        tree = Tree()
        self.TREE = tree

    def nextToken(self):
        if self.INDEX < len(self.TOKENS):
            x = self.INDEX
            self.INDEX+=1
            return [True ,self.TOKENS[x]]
        else:
            #self.INDEX = 0
            return [False]
    def parseCheck(self):
        if self.variable():
            print("Gramatica Correcta")
        else:
            print("Gramatica Incorrecta")

    def variable(self):
        if self.TYPE():
            if self.ID():
                if self.ASSIG():
                    if self.NUMBER():
                        return True
    def TYPE(self):
        x = self.nextToken()
        if x[0]:
            if x[1].tag == "INT-TY":
                return True
            else:
                return False
        else:
            return False

    def ID(self):
        x = self.nextToken()
        if x[0]:
            if x[1].tag == "ID-TOK":
                return True
            else:
                return False
        else:
            return False
    def ASSIG(self):
        x = self.nextToken()
        if x[0]:
            if x[1].tag == "ASIG-TOK":
                return True
            else:
                return False
        else:
            return False
    def NUMBER(self):
        x = self.nextToken()
        if x[0]:
            if x[1].tag == "INT-TOK":
                return True
            else:
                return False
        else:
            return False

    def ImprimirArbol(self):
        self.TREE.show()

Par = Parser('Program.g4')
Par.parseCheck()
#Par.ImprimirArbol()
