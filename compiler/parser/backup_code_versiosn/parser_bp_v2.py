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
            return False #si epsilon exist -> true sinon False
         if(self.currenttoken().type == "STRING_LITERAL" 
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

            self.syntaxerror("COMMA or RIGHT_PARENTEZ")
            return False

        if self.currenttoken().type == "RIGHT_PARENTEZ":
            return True

        self.syntaxerror("COMMA or RIGHT_PARENTEZ")
        return False

            
    def valuelist(self):
        if self.currenttoken() is None:
                    self.syntaxerror("VALUE")
                    return False #si epsilon exist -> true sinon False
        if(self.value()):
             if(self.valuetail()):
                  return True
        self.syntaxerror("VALUE")
        return False
    def insertstatment(self):
        savingposition = self.position

        if self.currenttoken() is None:
            return False

        temppos = self.position

        if self.currenttokenwithposition(temppos).type == "INSERT":
            temppos += 1
            if self.currenttokenwithposition(temppos) is None:
                return False

            if self.currenttokenwithposition(temppos).type == "INTO":
                temppos += 1
                if self.currenttokenwithposition(temppos) is None:
                    return False

                if self.currenttokenwithposition(temppos).type == "IDENTIFIER":
                    temppos += 1
                    if self.currenttokenwithposition(temppos) is None:
                        return False

                    if self.currenttokenwithposition(temppos).type == "VALUES":
                        temppos += 1
                        if self.currenttokenwithposition(temppos) is None:
                            return False

                        if self.currenttokenwithposition(temppos).type == "LEFT_PARENTEZ":
                            temppos += 1
                            self.position = temppos

                            if self.valuelist():
                                if self.currenttoken() is None:
                                    self.position = savingposition
                                    return False

                                if self.currenttoken().type == "RIGHT_PARENTEZ":
                                    self.avance()

                                    if self.currenttoken() is None:
                                        self.position = savingposition
                                        return False

                                    if self.currenttoken().type == "SEMICOLON":
                                        self.avance()
                                        return True

            if self.position == savingposition:
                self.position = temppos
                if temppos > 0:
                    previous = self.tokens[temppos-1].type
                    expected = {
                        "INSERT": "INTO",
                        "INTO": "IDENTIFIER",
                        "IDENTIFIER": "VALUES",
                        "VALUES": "LEFT_PARENTEZ"
                    }.get(previous, "INSERT statement")
                    self.syntaxerror(expected)
            else:
                if self.currenttoken() is not None and self.position > 0:
                    previous = self.tokens[self.position-1].type
                    expected = "RIGHT_PARENTEZ" if previous != "RIGHT_PARENTEZ" else "SEMICOLON"
                    self.syntaxerror(expected)

            self.position = savingposition
            return False

        self.position = savingposition
        return False
                   
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
        if self.currenttoken() is None:
            self.syntaxerror("IDENTIFIER, RELATIONAL OPERATOR or VALUE")
            return False

        if self.currenttoken().type == "IDENTIFIER":
            self.avance()

            if self.comparison():
                if self.value():
                    return True

        self.syntaxerror("IDENTIFIER, RELATIONAL OPERATOR or VALUE")
        return False
    def whereoption(self):
        if self.currenttoken() is None:
            self.syntaxerror("WHERE or SEMICOLON")
            return False

        if self.currenttoken().type == "WHERE":
            self.avance()

            if self.condition():
                return True

            self.syntaxerror("WHERE or SEMICOLON")
            return False

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

            if self.currenttoken() is None:
                self.syntaxerror("COMMA or FROM")
                return False

            if self.currenttoken().type == "IDENTIFIER":
                self.avance()
                return self.idtail()

            self.syntaxerror("COMMA or FROM")
            return False

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

            if self.idtail():
                return True

        self.syntaxerror("NEDJMA or IDENTIFIER")
        return False
    def selectstatement(self):
        if self.currenttoken() is None:
            self.syntaxerror("SELECT, selection list, FROM, table name or SEMICOLON")
            return False

        if self.currenttoken().type == "SELECT":
            self.avance()

            if self.selectlist():
                if self.currenttoken() is None:
                    self.syntaxerror("SELECT, selection list, FROM, table name or SEMICOLON")
                    return False

                if self.currenttoken().type == "FROM":
                    self.avance()

                    if self.currenttoken() is None:
                        self.syntaxerror("SELECT, selection list, FROM, table name or SEMICOLON")
                        return False

                    if self.currenttoken().type == "IDENTIFIER":
                        self.avance()

                        if self.whereoption():
                            if self.currenttoken() is None:
                                self.syntaxerror("SELECT, selection list, FROM, table name or SEMICOLON")
                                return False

                            if self.currenttoken().type == "SEMICOLON":
                                self.avance()
                                return True

        if self.currenttoken() is not None and self.position > 0:
            previous = self.tokens[self.position-1].type
            expected = {
                "SELECT": "NEDJMA or IDENTIFIER",
                "FROM": "IDENTIFIER",
                "IDENTIFIER": "WHERE or SEMICOLON"
            }.get(previous, "FROM or SEMICOLON")
            self.syntaxerror(expected)
        else:
            self.syntaxerror("SELECT statement")
        return False
    def instructions(self):
        if (self.currenttoken() is None
            or self.currenttoken().type == "EOF"):
            return True

        if self.currenttoken().type == "INSERT":
            if self.insertstatment():
                return self.instructions()
            self.syntaxerror("INSERT, SELECT or FIN")
            return False

        if self.currenttoken().type == "SELECT":
            if self.selectstatement():
                return self.instructions()
            self.syntaxerror("INSERT, SELECT or FIN")
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

            if self.currenttoken() is None:
                self.syntaxerror("LEFT_BRACKET, COMMA or RIGHT_PARENTEZ")
                return False

            if self.currenttoken().type == "INTEGER_NUMBER":
                self.avance()

                if self.currenttoken() is None:
                    self.syntaxerror("LEFT_BRACKET, COMMA or RIGHT_PARENTEZ")
                    return False

                if self.currenttoken().type == "RIGHT_BRACKET":
                    self.avance()
                    return True

            self.syntaxerror("LEFT_BRACKET, COMMA or RIGHT_PARENTEZ")
            return False

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

            if self.tailledestring():
                return True

        self.syntaxerror("TYPE_INTEGER, TYPE_REAL or TYPE_STRING")
        return False
    def singleattribut(self):
        if self.currenttoken() is None:
            self.syntaxerror("IDENTIFIER and TYPE")
            return False

        if self.currenttoken().type == "IDENTIFIER":
            self.avance()

            if self.typededonnes():
                return True

        self.syntaxerror("IDENTIFIER and TYPE")
        return False
    def attributetail(self):
        if self.currenttoken() is None:
            self.syntaxerror("COMMA or RIGHT_PARENTEZ")
            return False

        if self.currenttoken().type == "COMMA":
            self.avance()

            if self.singleattribut():
                return self.attributetail()

            self.syntaxerror("COMMA or RIGHT_PARENTEZ")
            return False

        if self.currenttoken().type == "RIGHT_PARENTEZ":
            return True

        self.syntaxerror("COMMA or RIGHT_PARENTEZ")
        return False
    def attributelist(self):
        if self.singleattribut():
            if self.attributetail():
                return True

        self.syntaxerror("ATTRIBUTE")
        return False
    def createstatment(self):
        if self.currenttoken() is None:
            self.syntaxerror("CREATE TABLE statement")
            return False

        if self.currenttoken().type == "CREATE":
            self.avance()

            if self.currenttoken() is None:
                self.syntaxerror("CREATE TABLE statement")
                return False
            if self.currenttoken().type == "TABLE":
                self.avance()

                if self.currenttoken() is None:
                    self.syntaxerror("CREATE TABLE statement")
                    return False
                if self.currenttoken().type == "IDENTIFIER":
                    self.avance()

                    if self.currenttoken() is None:
                        self.syntaxerror("CREATE TABLE statement")
                        return False
                    if self.currenttoken().type == "LEFT_PARENTEZ":
                        self.avance()

                        if self.attributelist():
                            if self.currenttoken() is None:
                                self.syntaxerror("CREATE TABLE statement")
                                return False
                            if self.currenttoken().type == "RIGHT_PARENTEZ":
                                self.avance()

                                if self.currenttoken() is None:
                                    self.syntaxerror("CREATE TABLE statement")
                                    return False
                                if self.currenttoken().type == "SEMICOLON":
                                    self.avance()
                                    return True

        if self.currenttoken() is not None and self.position > 0:
            previous = self.tokens[self.position-1].type
            expected = {
                "CREATE": "TABLE",
                "TABLE": "IDENTIFIER",
                "IDENTIFIER": "LEFT_PARENTEZ",
                "RIGHT_PARENTEZ": "SEMICOLON"
            }.get(previous, "RIGHT_PARENTEZ")
            self.syntaxerror(expected)
        else:
            self.syntaxerror("CREATE TABLE statement")
        return False
    def declarations(self):
        if (self.currenttoken() is None
            or self.currenttoken().type == "EOF"):
            return True

        if self.currenttoken().type == "CREATE":
            if self.createstatment():
                return self.declarations()
            self.syntaxerror("CREATE, INSERT, SELECT or FIN")
            return False

        if (self.currenttoken().type == "INSERT"
            or self.currenttoken().type == "SELECT"
            or self.currenttoken().type == "FIN"):
            return True

        self.syntaxerror("CREATE, INSERT, SELECT or FIN")
        return False
    def program(self):
        if self.currenttoken() is None:
            self.syntaxerror("PROGRAMME")
            return False

        if self.currenttoken().type == "PROGRAMME":
            self.avance()

            if self.currenttoken() is None:
                self.syntaxerror("IDENTIFIER")
                return False

            if self.currenttoken().type == "IDENTIFIER":
                self.avance()

                if self.currenttoken() is None:
                    self.syntaxerror("SEMICOLON")
                    return False

                if self.currenttoken().type == "SEMICOLON":
                    self.avance()

                    if self.declarations():
                        if self.instructions():
                            if self.currenttoken() is None:
                                self.syntaxerror("FIN")
                                return False

                            if self.currenttoken().type == "FIN":
                                self.avance()

                                if (self.currenttoken() is None
                                    or self.currenttoken().type == "EOF"):
                                    return True

                                self.syntaxerror("EOF")
                                return False

                            self.syntaxerror("FIN")
                            return False

                        return False

                    return False

                self.syntaxerror("SEMICOLON")
                return False

            self.syntaxerror("IDENTIFIER")
            return False

        self.syntaxerror("PROGRAMME")
        return False
    
        