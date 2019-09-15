from Lexer import Lexer
from treelib import Node, Tree
from ParserMethods import ParserFunctions

class Parser(ParserFunctions):
    def __init__(self,path):
        lex = Lexer(path)
        lex.tokenize()
        self.TOKENS = lex.tokenList
        

    def nextToken(self):
        if len(self.TOKENS) != 0:
            x = self.TOKENS[0]
            self.TOKENS.pop(0)
            return [True,x]
        else:
            return [False]

    def seekToken(self):
        if len(self.TOKENS) > 2:
            return [True,self.TOKENS[1]]
        else:
            return [False]

