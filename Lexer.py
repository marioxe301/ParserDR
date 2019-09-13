from pyparsing import (Regex, White, Literal ,
ZeroOrMore, OneOrMore, Group , Combine , 
Word , alphanums, Suppress)


class Tokens(object):
    def __init__(self,tag,token):
        self.tag = tag
        self.token = token
#esta clase permitira guardar en la lista

class Lexer(object):
    def __init__(self,path):
        #TERMINALES
        WHITESPACE = White(ws=" \t\r")
        LETTER = Regex('[a-zA-Z]')
        DIGIT = Regex('[0-9]')
        DATE_TYPE = Literal('date') 
        STRING_TYPE = Literal('String') 
        REAL_TYPE = Literal('real')
        VOID_TYPE = Literal('void')
        BOOLEAN_TYPE = Literal('boolean') 
        ANYTYPE_TYPE = Literal('anytype') 
        INT_TYPE = Literal('int')
        STATIC_TKN = Literal('static')
        END = Literal('END')
        DO = Literal('DO')
        IF_THEN = Literal('THEN')
        INICIO = Literal('BEGIN')
        RETURN = Literal('EXIT')
        ELSE = Literal('else')
        IF = Literal('if')
        WHILE = Literal('while')
        
        
        
        #TERMINALES LITERALES
        DATE_LITERAL = DIGIT + DIGIT + Literal('/') + DIGIT + DIGIT + Literal('/') + DIGIT + DIGIT + DIGIT + DIGIT
        STRING_LITERAL = Combine(Literal('"')+ ZeroOrMore(LETTER | DIGIT | Literal(' ') | Literal('%')|Literal('@')| Literal(',')| Literal('-')|Literal('=')|Literal('(')|Literal(')')|Literal('_')) +Literal('"'))
        REAL_LITERAL = Combine(OneOrMore(DIGIT) + Literal('.') + OneOrMore(DIGIT))
        INT_LITERAL = Combine(OneOrMore(DIGIT))
        TRUE_LITERAL = Literal('true')
        FALSE_LITERAL = Literal('false')
        BOOLEAN_LITERAL = TRUE_LITERAL | FALSE_LITERAL
        INCR = Literal('++')
        DDPERIOD = Literal('::')
        PAR_OP = Literal('(')
        PAR_CL = Literal(')')
        SEMICOLON = Literal(';')
        COMA = Literal(',')
        BRACK_OP = Literal('{')
        BRACK_CL = Literal('}')
        PERIOD = Literal('.')
        ASIG = Literal(':=')
        REL_OP = Literal('>') | Literal('<') | Literal('==') | Literal('<=') | Literal('>=')
        LOG_OP = Literal('||') | Literal('&&')
        MULT_OP = Literal('/') | Literal('*')
        ADD_OP = Literal('+') | Literal('-')
        ID = Combine((LETTER | Literal('_')) + ZeroOrMore( LETTER | DIGIT )  )
        TEXT = ZeroOrMore(Word(alphanums)| WHITESPACE )
        COMMENT = Combine(Literal('//')+ TEXT + Literal('\n')) 

        
        program = ZeroOrMore( Suppress(COMMENT) | Group(DATE_TYPE)("DATE-TY") | Group(STRING_TYPE)("STRING-TY") | Group(REAL_TYPE)("REAL-TY") | Group( VOID_TYPE)("VOID-TY") | Group(BOOLEAN_TYPE)("BOOLEAN-TY") | Group(ANYTYPE_TYPE)("ANY-TY")
            | Group(INT_TYPE)("INT-TY") | Group(STATIC_TKN)("STATIC-TY") | Group(END)("END-TOK") | Group(DO)("DO-TOK") | Group(IF_THEN)("IF-THEN-TOK") | Group(INICIO)("BEGIN-TOK") | Group(RETURN)("RETURN-TOK") | Group(ELSE)("ELSE-TOK") | Group(IF)("IF-TOK") | Group(WHILE)("WHILE-TOK") | Group(DATE_LITERAL)("DATE-TOK") | Group(STRING_LITERAL)("STRING-TOK")
            | Group(COMA)("COMA-TOK") | Group(REAL_LITERAL)("REAL-TOK") | Group(INT_LITERAL)("INT-TOK") | Group(BOOLEAN_LITERAL)("BOOLEAN-TOK") | Group(INCR)("INCR-TOK") |Group( DDPERIOD)("DDPERIOD-TOK") | Group(PAR_OP)("PAR-OP-TOK") | Group(PAR_CL)("PAR-CL-TOK") | Group(SEMICOLON)("SEMICOLON-TOK")
            | Group(BRACK_OP)("BRACK-OP-TOK") | Group(BRACK_CL)("BRACK-CL-TOK") | Group(PERIOD)("PERIOD-TOK") | Group(ASIG)("ASIG-TOK") | Group( REL_OP)("REL-OP-TOK") | Group(LOG_OP)("LOG-OP-TOK") | Group(MULT_OP)("MULT-OP-TOK") | Group( ADD_OP)("ADD-OP-TOK") | Group(ID)("ID-TOK")
         )
        
        #manda las palabras reservadas que acepta la gramatica
        self.lexer = program
        self.tokenList = []
        self.path = path
       
    #Divide en Tokens el archivo que se le manda
    def tokenFile(self):
        return self.lexer.parseFile(self.path)
    
    def tokenize(self):
        tokenItems = self.tokenFile()
        for items in tokenItems:
            tok = Tokens(items.getName(),items[0])
            self.tokenList.append(tok)

    def printAllTokens(self):
        for tok in self.tokenList:
            print("TAG:",tok.tag," ","TOKEN:",tok.token,"\n")

lex = Lexer('Program.g4')
lex.tokenize()
lex.printAllTokens()