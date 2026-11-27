
from compiler.errors.errors import compilererror, errorreporter
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.reporter = errorreporter()
    def syntaxerror(self, expected):
        token = self.currenttoken()

        if token is not None and not self.reporter.has_errors():
            error = compilererror(
                "Syntax",
                token.line,
                token.column,
                f"Expected {expected}, found {token.type}"
            )
            self.reporter.add(error)

    def avance(self):
        self.position += 1

    def currenttoken(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None
    def currenttokenwithposition(self,position):
       if position < len(self.tokens):
                   return self.tokens[position]
       return None
        
    #token0 token1 token2 pos2 ->nexttoken will return token3 and this not exist
    def nexttoken(self):
        if self.position < len(self.tokens)-1:
            return self.tokens[self.position+1]
        return None

        
    def movetonexttoken(self):
        self.avance()
            
  
    def value(self):
        if self.currenttoken() is None:
            self.syntaxerror("INTEGER_NUMBER, REAL_NUMBER or STRING_LITERAL")
            return False

        if (self.currenttoken().type == "STRING_LITERAL"
            or self.currenttoken().type == "REAL_NUMBER"
            or self.currenttoken().type == "INTEGER_NUMBER"):
            token = self.currenttoken()
            self.avance()
            return token

        self.syntaxerror("INTEGER_NUMBER, REAL_NUMBER or STRING_LITERAL")
        return False

    def valuetail(self):
        if self.currenttoken() is None:
            self.syntaxerror("COMMA or RIGHT_PARENTEZ")
            return False

        if self.currenttoken().type == "COMMA":
            self.avance()

            if self.value():
                return self.valuetail()

            return False

        if self.currenttoken().type == "RIGHT_PARENTEZ":
            return True

        self.syntaxerror("COMMA or RIGHT_PARENTEZ")
        return False

            
    def valuelist(self):
        if self.value():
            return self.valuetail()

        return False

    def insertstatment(self):
        if self.currenttoken() is None or self.currenttoken().type != "INSERT":
            self.syntaxerror("INSERT")
            return False

        self.avance()

        if self.currenttoken() is None or self.currenttoken().type != "INTO":
            self.syntaxerror("INTO")
            return False

        self.avance()

        if self.currenttoken() is None or self.currenttoken().type != "IDENTIFIER":
            self.syntaxerror("IDENTIFIER")
            return False

        self.avance()

        if self.currenttoken() is None or self.currenttoken().type != "VALUES":
            self.syntaxerror("VALUES")
            return False

        self.avance()

        if self.currenttoken() is None or self.currenttoken().type != "LEFT_PARENTEZ":
            self.syntaxerror("LEFT_PARENTEZ")
            return False

        self.avance()

        if not self.valuelist():
            return False

        if self.currenttoken() is None or self.currenttoken().type != "RIGHT_PARENTEZ":
            self.syntaxerror("RIGHT_PARENTEZ")
            return False

        self.avance()

        if self.currenttoken() is None or self.currenttoken().type != "SEMICOLON":
            self.syntaxerror("SEMICOLON")
            return False

        self.avance()
        return True
                   
    def comparison(self):
        if self.currenttoken() is None:
            self.syntaxerror("RELATIONAL OPERATOR")
            return False

        if (self.currenttoken().type == "EQUALS"
            or self.currenttoken().type == "DIFFERENT"
            or self.currenttoken().type == "LESS_THAN"
            or self.currenttoken().type == "GREATER_THAN"
            or self.currenttoken().type == "LESS_THAN_EQUAL"
            or self.currenttoken().type == "GREATER_THAN_EQUAL"):

            self.avance()
            return True

        self.syntaxerror("RELATIONAL OPERATOR")
        return False

    def condition(self):
        if self.currenttoken() is None or self.currenttoken().type != "IDENTIFIER":
            self.syntaxerror("IDENTIFIER")
            return False

        self.avance()

        if self.comparison():
            return self.value()

        return False

    def whereoption(self):
        if self.currenttoken() is None:
            self.syntaxerror("WHERE or SEMICOLON")
            return False

        if self.currenttoken().type == "WHERE":
            self.avance()
            return self.condition()

        if self.currenttoken().type == "SEMICOLON":
            return True

        self.syntaxerror("WHERE or SEMICOLON")
        return False

    def idtail(self):
        if self.currenttoken() is None:
            self.syntaxerror("COMMA or FROM")
            return False

        if self.currenttoken().type == "COMMA":
            self.avance()

            if self.currenttoken() is None or self.currenttoken().type != "IDENTIFIER":
                self.syntaxerror("IDENTIFIER")
                return False

            self.avance()
            return self.idtail()

        if self.currenttoken().type == "FROM":
            return True

        self.syntaxerror("COMMA or FROM")
        return False

    def selectlist(self):
        if self.currenttoken() is None:
            self.syntaxerror("NEDJMA or IDENTIFIER")
            return False

        if self.currenttoken().type == "NEDJMA":
            self.avance()
            return True

        if self.currenttoken().type == "IDENTIFIER":
            self.avance()
            return self.idtail()

        self.syntaxerror("NEDJMA or IDENTIFIER")
        return False

    def selectstatement(self):
        if self.currenttoken() is None or self.currenttoken().type != "SELECT":
            self.syntaxerror("SELECT")
            return False

        self.avance()

        if not self.selectlist():
            return False

        if self.currenttoken() is None or self.currenttoken().type != "FROM":
            self.syntaxerror("FROM")
            return False

        self.avance()

        if self.currenttoken() is None or self.currenttoken().type != "IDENTIFIER":
            self.syntaxerror("IDENTIFIER")
            return False

        self.avance()

        if not self.whereoption():
            return False

        if self.currenttoken() is None or self.currenttoken().type != "SEMICOLON":
            self.syntaxerror("SEMICOLON")
            return False

        self.avance()
        return True

    def instructions(self):
        if self.currenttoken() is None:
            self.syntaxerror("INSERT, SELECT or FIN")
            return False

        if self.currenttoken().type == "INSERT":
            if self.insertstatment():
                return self.instructions()
            return False

        if self.currenttoken().type == "SELECT":
            if self.selectstatement():
                return self.instructions()
            return False

        if self.currenttoken().type == "FIN":
            return True

        self.syntaxerror("INSERT, SELECT or FIN")
        return False

    def tailledestring(self):
        if self.currenttoken() is None:
            self.syntaxerror("LEFT_BRACKET, COMMA or RIGHT_PARENTEZ")
            return False

        if self.currenttoken().type == "LEFT_BRACKET":
            self.avance()

            if self.currenttoken() is None or self.currenttoken().type != "INTEGER_NUMBER":
                self.syntaxerror("INTEGER_NUMBER")
                return False

            self.avance()

            if self.currenttoken() is None or self.currenttoken().type != "RIGHT_BRACKET":
                self.syntaxerror("RIGHT_BRACKET")
                return False

            self.avance()
            return True

        if (self.currenttoken().type == "COMMA"
            or self.currenttoken().type == "RIGHT_PARENTEZ"):
            return True

        self.syntaxerror("LEFT_BRACKET, COMMA or RIGHT_PARENTEZ")
        return False

    def typededonnes(self):
        if self.currenttoken() is None:
            self.syntaxerror("TYPE_INTEGER, TYPE_REAL or TYPE_STRING")
            return False

        if self.currenttoken().type == "TYPE_INTEGER":
            self.avance()
            return True

        if self.currenttoken().type == "TYPE_REAL":
            self.avance()
            return True

        if self.currenttoken().type == "TYPE_STRING":
            self.avance()
            return self.tailledestring()

        self.syntaxerror("TYPE_INTEGER, TYPE_REAL or TYPE_STRING")
        return False

    def singleattribut(self):
        if self.currenttoken() is None or self.currenttoken().type != "IDENTIFIER":
            self.syntaxerror("IDENTIFIER")
            return False

        self.avance()
        return self.typededonnes()

    def attributetail(self):
        if self.currenttoken() is None:
            self.syntaxerror("COMMA or RIGHT_PARENTEZ")
            return False

        if self.currenttoken().type == "COMMA":
            self.avance()

            if self.singleattribut():
                return self.attributetail()

            return False

        if self.currenttoken().type == "RIGHT_PARENTEZ":
            return True

        self.syntaxerror("COMMA or RIGHT_PARENTEZ")
        return False

    def attributelist(self):
        if self.singleattribut():
            return self.attributetail()

        return False

    def createstatment(self):
        if self.currenttoken() is None or self.currenttoken().type != "CREATE":
            self.syntaxerror("CREATE")
            return False

        self.avance()

        if self.currenttoken() is None or self.currenttoken().type != "TABLE":
            self.syntaxerror("TABLE")
            return False

        self.avance()

        if self.currenttoken() is None or self.currenttoken().type != "IDENTIFIER":
            self.syntaxerror("IDENTIFIER")
            return False

        self.avance()

        if self.currenttoken() is None or self.currenttoken().type != "LEFT_PARENTEZ":
            self.syntaxerror("LEFT_PARENTEZ")
            return False

        self.avance()

        if not self.attributelist():
            return False

        if self.currenttoken() is None or self.currenttoken().type != "RIGHT_PARENTEZ":
            self.syntaxerror("RIGHT_PARENTEZ")
            return False

        self.avance()

        if self.currenttoken() is None or self.currenttoken().type != "SEMICOLON":
            self.syntaxerror("SEMICOLON")
            return False

        self.avance()
        return True

    def declarations(self):
        if self.currenttoken() is None:
            self.syntaxerror("CREATE, INSERT, SELECT or FIN")
            return False

        if self.currenttoken().type == "CREATE":
            if self.createstatment():
                return self.declarations()
            return False

        if (self.currenttoken().type == "INSERT"
            or self.currenttoken().type == "SELECT"
            or self.currenttoken().type == "FIN"):
            return True

        self.syntaxerror("CREATE, INSERT, SELECT or FIN")
        return False

    def program(self):
        if self.currenttoken() is None or self.currenttoken().type != "PROGRAMME":
            self.syntaxerror("PROGRAMME")
            return False

        self.avance()

        if self.currenttoken() is None or self.currenttoken().type != "IDENTIFIER":
            self.syntaxerror("IDENTIFIER")
            return False

        self.avance()

        if self.currenttoken() is None or self.currenttoken().type != "SEMICOLON":
            self.syntaxerror("SEMICOLON")
            return False

        self.avance()

        if not self.declarations():
            return False

        if not self.instructions():
            return False

        if self.currenttoken() is None or self.currenttoken().type != "FIN":
            self.syntaxerror("FIN")
            return False

        self.avance()

        if (self.currenttoken() is None
            or self.currenttoken().type == "EOF"):
            return True

        self.syntaxerror("EOF")
        return False
