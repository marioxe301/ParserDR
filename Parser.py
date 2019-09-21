from Lexer import Lexer
from treelib import Node, Tree
import re

class Parser(object):
    def __init__(self,path):
        lex = Lexer(path)
        lex.tokenize()
        self.TOKENS = lex.tokenList
        self.TYPES= re.compile(".*-TY")
        

    def nextToken(self):
        if len(self.TOKENS) != 0:
            x = self.TOKENS[0]
            self.TOKENS.pop(0)
            return [True,x]
        else:
            return [False]

    def seekNextToken(self):
        if len(self.TOKENS) > 2:
            return [True,self.TOKENS[1]]
        else:
            return [False]

    def seekActualToken(self):
        if len(self.TOKENS)!= 0:
            return [True,self.TOKENS[0]]
        else:
            return [False]

    def Parse(self):
        if self.Program():
            print('Gramatica Correcta')
        else:
            print('Gramatica Incorrecta')
    
    def Program(self):
        if self.Opt_funct_decl():
            return True
        else:
            return False

    
    def Opt_funct_decl(self):
        if self.Funct_head():
            if self.Body():
                return True
            else:
                return False
        else:
            return False
    
    def Funct_head(self):
        if self.Funct_name():
            token = self.nextToken()
            if token[0] and token[1].tag == 'PAR-OP-TOK':
                if self.Param_list_opt():
                    return True
                else:
                    return False
        else:
            return False
    
    def Funct_name(self):
        if self.Funct_type():
            token = self.nextToken()
            if token[0] and token[1].tag == 'ID-TOK':
                return True
            else:
                return False
        else:
            return False
    
    def Funct_type(self):
        token = self.nextToken()
        if token[0] and token[1].tag == 'STATIC-TY':
            if self.Decl_type():
                return True
            else:
                return False
        else:
            return False

    def Decl_type(self):
        token = self.nextToken()
        if token[0] and self.TYPES.match(token[1].tag) is not None:
            return True
        else:
            return False
    
    def Param_list_opt(self):
        Token = self.seekActualToken()
        if Token[0] and Token[1].tag == 'PAR-CL-TOK':
            self.nextToken() # para quitar el parentesis
            return True
        elif Token[0] and self.TYPES.match(Token[1].tag) is not None:
            while True:
                if self.Decl_param():
                    Token = self.seekActualToken()
                    if Token[0] and Token[1].tag == 'COMA-TOK':
                        self.nextToken() #solo para descartar la coma
                        continue
                    elif Token[0] and Token[1].tag == 'PAR-CL-TOK':
                        self.nextToken() # para descartar el parentesis
                        return True
                else:
                    return False
        else:
            return False

    def Decl_param(self):
        if self.Decl_type():
            token = self.nextToken()
            if token[0] and token[1].tag == 'ID-TOK':
                return True
            else:
                return False
        else:
            return False
    
    def Body(self):
        token = self.nextToken()
        if token[0] and token[1].tag == 'BRACK-OP-TOK':
            if self.Stmt_list():
                return True
            else:
                return False
        else:
            return False

    def Stmt_list(self):
        if self.Stmts():
            return True
        else:
            return False

    def Stmts(self):
        BrackToken = self.seekActualToken()
        if BrackToken[0] and BrackToken[1].tag == 'BRACK-CL-TOK':
            self.nextToken() # para quitar el braket
            return True
        else:
            while True:
                if self.Stmt():
                    BrackToken = self.seekActualToken()
                    if BrackToken[0] and BrackToken[1].tag == 'BRACK-CL-TOK':
                        self.nextToken() # descarta el bracket
                        return True
                    else:
                        continue
                else:
                    return False
    
    def Stmt(self):
        Token = self.seekActualToken()
        if Token[0] and Token[1].tag == 'IF-TOK':
            if self.If_stmt():
                return True
            else:
                return False
        elif Token[0] and Token[1].tag == 'WHILE-TOK' :
            if self.While_stmt():
                return True
            else:
                return False
        elif Token[0] and Token[1].tag == 'RETURN-TOK':
            if self.Return_stmt():
                return True
            else:
                return False
        elif Token[0] and self.TYPES.match(Token[1].tag) is not None:
            if self.Assign_stmt():
                return True
            else:
                return False
        else:
            return False
    
    def If_stmt(self):
        IfToken = self.nextToken()
        ParToken = self.nextToken()
        if IfToken[0] and IfToken[1].tag == 'IF-TOK' and ParToken[0] and ParToken[1].tag == 'PAR-OP-TOK':
            if self.Bool_expr():
                ParToken = self.nextToken()
                if ParToken[0] and ParToken[1].tag == 'PAR-CL-TOK':
                    if self.Body():
                        return True
                    else:
                        return False
            else:
                return False
    def Bool_expr(self):
        Token = self.seekActualToken()
        if Token[0] and Token[1].tag == 'BOOLEAN-TOK':
            self.nextToken() #Descartar el token 
            return True
        else:
            if self.Constant():
                Token = self.nextToken()
                if Token[0] and (Token[1].tag == 'REL-OP-TOK' or Token[1].tag == 'LOG-OP-TOK'): 
                    if self.Constant():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
    
    def Constant(self):
        Token = self.nextToken()
        if Token[0] and Token[1].tag == 'INT-TOK':
            return True
        elif Token[0] and Token[1].tag == 'STRING-TOK':
            return True
        elif Token[0] and Token[1].tag == 'REAL-TOK':
            return True
        elif Token[0] and Token[1].tag == 'DATE-TOK':
            return True
        elif Token[0] and Token[1].tag == 'BOOLEAN-TOK':
            return True
        else:
            return False

    def While_stmt(self):
        WhileToken = self.nextToken()
        ParToken = self.nextToken()
        if WhileToken[0] and ParToken[0] and WhileToken[1].tag == 'WHILE-TOK' and ParToken[1].tag == 'PAR-OP-TOK':
            if self.Bool_expr():
                ParToken = self.nextToken()
                if ParToken[0] and ParToken[1].tag == 'PAR-CL-TOK':
                    if self.Body():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def Return_stmt(self):
        Token = self.nextToken()
        if Token[0] and Token[1].tag == 'RETURN-TOK':
            Semicolon = self.seekActualToken()
            if Semicolon[0] and Semicolon[1].tag == 'SEMICOLON-TOK':
                self.nextToken()
                return True
            else:
                if self.Constant():
                    if Semicolon[0] and Semicolon[1].tag == 'SEMICOLON-TOK':
                        self.nextToken()
                        return True
                    else:
                        return False
                else:
                    return False
        else:
            return False
    
    def Assign_stmt(self):
        if self.Decl_type():
            Token = self.nextToken()
            if Token[0] and Token[1].tag == 'ID-TOK':
                Token = self.nextToken()
                if Token[0] and Token[1].tag == 'ASIG-TOK':
                    if self.Constant():
                        Token = self.nextToken()
                        if Token[0] and Token[1].tag == 'SEMICOLON-TOK':
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False

Pars = Parser('Program.g4')
Pars.Parse()