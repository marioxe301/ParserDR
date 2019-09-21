from Lexer import Lexer
from treelib import Node, Tree
import re
from termcolor import colored,cprint

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
            cprint("Grammar Correct\n","green",attrs=['bold'])
        else:
            cprint("Grammar Incorrect\n","red",attrs=['bold'])
    
    def Program(self):
        print("Program\n")
        if self.Opt_funct_decl():
            return True
        else:
            return False

    
    def Opt_funct_decl(self):
        print("Opt_funct_decl\n")
        if self.Funct_head():
            if self.Body():
                return True
            else:
                return False
        else:
            return False
    
    def Funct_head(self):
        print("Funct_head\n")
        if self.Funct_name():
            token = self.nextToken()
            if token[0] and token[1].tag == 'PAR-OP-TOK':
                print("PAREN_OP_TOKEN")
                print("Token: ",token[1].token,"\n")
                if self.Param_list_opt():
                    return True
                else:
                    cprint("Expected a ( TOKEN\n","red",attrs=['bold'])
                    return False
        else:
            return False
    
    def Funct_name(self):
        print("Funct_name\n")
        if self.Funct_type():
            token = self.nextToken()
            if token[0] and token[1].tag == 'ID-TOK':
                print("ID_TOKEN")
                print("Token: ",token[1].token,"\n")
                return True
            else:
                cprint("Expected a ID TOKEN\n","red",attrs=['bold'])
                return False
        else:
            return False
    
    def Funct_type(self):
        print("Funct_type\n")
        token = self.nextToken()
        if token[0] and token[1].tag == 'STATIC-TY':
            print("STATIC_TOKEN")
            print("Token: ",token[1].token,"\n")
            if self.Decl_type():
                return True
            else:
                cprint("Expected a STATIC TOKEN\n","red",attrs=['bold'])
                return False
        else:
            return False

    def Decl_type(self):
        print("Decl_type\n")
        token = self.nextToken()
        if token[0] and self.TYPES.match(token[1].tag) is not None:
            print("TYPE_TOKEN")
            print("Token: ",token[1].token,"\n")
            return True
        else:
            cprint("Expected a TYPE TOKEN\n","red",attrs=['bold'])
            return False
    
    def Param_list_opt(self):
        print("Param_list_opt\n")
        Token = self.seekActualToken()
        if Token[0] and Token[1].tag == 'PAR-CL-TOK':
            print("PAREN_CL_TOKEN")
            print("Token: ",Token[1].token,"\n")
            self.nextToken() # para quitar el parentesis
            return True
        elif Token[0] and self.TYPES.match(Token[1].tag) is not None:
            while True:
                if self.Decl_param():
                    Token = self.seekActualToken()
                    if Token[0] and Token[1].tag == 'COMA-TOK':
                        print("COMA_TOKEN")
                        print("Token: ",Token[1].token,"\n")
                        self.nextToken() #solo para descartar la coma
                        continue
                    elif Token[0] and Token[1].tag == 'PAR-CL-TOK':
                        print("PAREN_CL_TOKEN")
                        print("Token: ",Token[1].token,"\n")
                        self.nextToken() # para descartar el parentesis
                        return True
                else:
                    cprint("Expected a COMA or ) TOKEN\n","red",attrs=['bold'])
                    return False
        else:
            cprint("Expected a ) TOKEN\n","red",attrs=['bold'])
            return False

    def Decl_param(self):
        print("Decl_param\n")
        if self.Decl_type():
            token = self.nextToken()
            if token[0] and token[1].tag == 'ID-TOK':
                print("ID_TOKEN")
                print("Token: ",token[1].token,"\n")
                return True
            else:
                cprint("Expected a ID TOKEN\n","red",attrs=['bold'])
                return False
        else:
            return False
    
    def Body(self):
        print("Body\n")
        token = self.nextToken()
        if token[0] and token[1].tag == 'BRACK-OP-TOK':
            print("BRACK_OP_TOKEN")
            print("Token: ",token[1].token,"\n")
            if self.Stmt_list():
                return True
            else:
                
                return False
        else:
            cprint("Expected a { TOKEN\n","red",attrs=['bold'])
            return False

    def Stmt_list(self):
        print("Stmt_list\n")
        if self.Stmts():
            return True
        else:
            return False

    def Stmts(self):
        print("Stmts\n")
        BrackToken = self.seekActualToken()
        if BrackToken[0] and BrackToken[1].tag == 'BRACK-CL-TOK':
            print("BRACK_CL_TOKEN")
            print("Token: ",BrackToken[1].token,"\n")
            self.nextToken() # para quitar el braket
            return True

        else:
            while True:
                if self.Stmt():
                    BrackToken = self.seekActualToken()
                    if BrackToken[0] and BrackToken[1].tag == 'BRACK-CL-TOK':
                        print("BRACK_CL_TOKEN")
                        print("Token: ",BrackToken[1].token,"\n")
                        self.nextToken() # descarta el bracket
                        return True
                    else:
                        continue
                else:
                    cprint("Unexpected TOKEN found\n","red",attrs=['bold'])
                    return False
    
    def Stmt(self):
        print("Stmt\n")
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
        print("If_stmt\n")
        IfToken = self.nextToken()
        ParToken = self.nextToken()
        if IfToken[0] and IfToken[1].tag == 'IF-TOK' and ParToken[0] and ParToken[1].tag == 'PAR-OP-TOK':
            print("IF_TOKEN")
            print("Token: ",IfToken[1].token,"\n")
            print("PAR_OP_TOKEN")
            print("Token: ",ParToken[1].token,"\n")
            if self.Bool_expr():
                ParToken = self.nextToken()
                if ParToken[0] and ParToken[1].tag == 'PAR-CL-TOK':
                    print("PAR_CL_TOKEN")
                    print("Token: ",ParToken[1].token,"\n")
                    if self.Body():
                        return True
                    else:
                        return False
                else:
                    cprint("Expected a ) TOKEN\n","red",attrs=['bold'])
                    return False
            else:
                return False
        else:
            cprint("Expected a IF or ( or TOKEN\n","red",attrs=['bold'])
            return False

    def Bool_expr(self):
        print("Bool_expr\n")
        Token = self.seekActualToken()
        if Token[0] and Token[1].tag == 'BOOLEAN-TOK':
            print("BOOLEAN_TOKEN")
            print("Token: ",Token[1].token,"\n")
            self.nextToken() #Descartar el token 
            return True
        else:
            if self.Constant():
                Token = self.nextToken()
                if Token[0] and (Token[1].tag == 'REL-OP-TOK' or Token[1].tag == 'LOG-OP-TOK'): 
                    print("LOGICAL_TOKEN")
                    print("Token: ",Token[1].token,"\n")
                    if self.Constant():
                        return True
                    else:
                        return False
                else:
                    cprint("Expected a RELATIONAL or LOGICAL TOKEN\n","red",attrs=['bold'])
                    return False
            else:
                return False
    
    def Constant(self):
        print("Constant\n")
        Token = self.nextToken()
        if Token[0] and Token[1].tag == 'INT-TOK':
            print("INT_TOKEN")
            print("Token: ",Token[1].token,"\n")
            return True
        elif Token[0] and Token[1].tag == 'STRING-TOK':
            print("STRING_TOKEN")
            print("Token: ",Token[1].token,"\n")
            return True
        elif Token[0] and Token[1].tag == 'REAL-TOK':
            print("REAL_TOKEN")
            print("Token: ",Token[1].token,"\n")
            return True
        elif Token[0] and Token[1].tag == 'DATE-TOK':
            print("DATE_TOKEN")
            print("Token: ",Token[1].token,"\n")
            return True
        elif Token[0] and Token[1].tag == 'BOOLEAN-TOK':
            print("BOOLEAN_TOKEN")
            print("Token: ",Token[1].token,"\n")
            return True
        else:
            cprint("Expected a CONSTANT TOKEN\n","red",attrs=['bold'])
            return False

    def While_stmt(self):
        print("While_stmt\n")
        WhileToken = self.nextToken()
        ParToken = self.nextToken()
        if WhileToken[0] and ParToken[0] and WhileToken[1].tag == 'WHILE-TOK' and ParToken[1].tag == 'PAR-OP-TOK':
            print("WHILE_TOKEN")
            print("Token: ",WhileToken[1].token,"\n")
            print("PAR_OP_TOKEN")
            print("Token: ",ParToken[1].token,"\n")
            if self.Bool_expr():
                ParToken = self.nextToken()
                if ParToken[0] and ParToken[1].tag == 'PAR-CL-TOK':
                    print("PAR_CL_TOKEN")
                    print("Token: ",ParToken[1].token,"\n")
                    if self.Body():
                        return True
                    else:
                        return False
                else:
                    
                    return False
            else:
                return False
        else:
            cprint("Expected a WHILE or ( TOKEN\n","red",attrs=['bold'])
            return False

    def Return_stmt(self):
        print("Return_stmt\n")
        Token = self.nextToken()
        if Token[0] and Token[1].tag == 'RETURN-TOK':
            print("RETURN_TOKEN")
            print("Token: ",Token[1].token,"\n")
            Semicolon = self.seekActualToken()
            if Semicolon[0] and Semicolon[1].tag == 'SEMICOLON-TOK':
                print("SEMICOLON_TOKEN")
                print("Token: ",Semicolon[1].token,"\n")
                self.nextToken()
                return True
            else:
                if self.Constant():
                    Semicolon = self.seekActualToken()
                    if Semicolon[0] and Semicolon[1].tag == 'SEMICOLON-TOK':
                        print("SEMICOLON_TOKEN")
                        print("Token: ",Semicolon[1].token,"\n")
                        self.nextToken()
                        return True
                    else:
                        return False
                else:
                    return False
        else:
            cprint("Expected a RETURN TOKEN\n","red",attrs=['bold'])
            return False
    
    def Assign_stmt(self):
        print("Assign_stmt\n")
        if self.Decl_type():
            Token = self.nextToken()
            if Token[0] and Token[1].tag == 'ID-TOK':
                print("ID_TOKEN")
                print("Token: ",Token[1].token,"\n")
                Token = self.nextToken()
                if Token[0] and Token[1].tag == 'ASIG-TOK':
                    print("ASSIGN_TOKEN")
                    print("Token: ",Token[1].token,"\n")
                    if self.Constant():
                        Token = self.nextToken()
                        if Token[0] and Token[1].tag == 'SEMICOLON-TOK':
                            print("SEMICOLON_TOKEN")
                            print("Token: ",Token[1].token,"\n")
                            return True
                        else:
                            cprint("Expected a SEMICOLON TOKEN\n","red",attrs=['bold'])
                            return False
                    else:
                        return False
                else:
                    cprint("Expected a ASSIGN TOKEN\n","red",attrs=['bold'])
                    return False
            else:
                cprint("Expected a ID TOKEN\n","red",attrs=['bold'])
                return False

Pars = Parser('Program.g4')
Pars.Parse()