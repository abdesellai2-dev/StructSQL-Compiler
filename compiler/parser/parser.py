class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

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
            return False #si epsilon exist -> true sinon False
         if(self.currenttoken().type == "STRING_LITERAL" 
            or self.currenttoken().type == "REAL_NUMBER" 
            or self.currenttoken().type == "INTEGER_NUMBER"):
              token = self.currenttoken()
              self.avance()
              return token
         return False  
    def valuetail(self):
        if self.currenttoken() is None:
            return False

        if self.currenttoken().type == "COMMA":
            self.avance()

            if self.value():
                return self.valuetail()

            return False

        if self.currenttoken().type == "RIGHT_PARENTEZ":
            return True

        return False

            
    def valuelist(self):
        if self.currenttoken() is None:
                    return False #si epsilon exist -> true sinon False
        if(self.value()):
             if(self.valuetail()):
                  return True
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

            self.position = savingposition
            return False

        self.position = savingposition
        return False
                   
    def comparison(self):
        if self.currenttoken() is None:
            return False

        if (self.currenttoken().type == "EQUALS"
            or self.currenttoken().type == "DIFFERENT"
            or self.currenttoken().type == "LESS_THAN"
            or self.currenttoken().type == "GREATER_THAN"
            or self.currenttoken().type == "LESS_THAN_EQUAL"
            or self.currenttoken().type == "GREATER_THAN_EQUAL"):

            self.avance()
            return True

        return False
    def condition(self):
        if self.currenttoken() is None:
            return False

        if self.currenttoken().type == "IDENTIFIER":
            self.avance()

            if self.comparison():
                if self.value():
                    return True

        return False
    def whereoption(self):
        if self.currenttoken() is None:
            return False

        if self.currenttoken().type == "WHERE":
            self.avance()

            if self.condition():
                return True

            return False

        if self.currenttoken().type == "SEMICOLON":
            return True

        return False
    def idtail(self):
        if self.currenttoken() is None:
            return False

        if self.currenttoken().type == "COMMA":
            self.avance()

            if self.currenttoken() is None:
                return False

            if self.currenttoken().type == "IDENTIFIER":
                self.avance()
                return self.idtail()

            return False

        if self.currenttoken().type == "FROM":
            return True

        return False
    def selectlist(self):
        if self.currenttoken() is None:
            return False

        if self.currenttoken().type == "NEDJMA":
            self.avance()
            return True

        if self.currenttoken().type == "IDENTIFIER":
            self.avance()

            if self.idtail():
                return True

        return False
    def selectstatement(self):
        if self.currenttoken() is None:
            return False

        if self.currenttoken().type == "SELECT":
            self.avance()

            if self.selectlist():
                if self.currenttoken() is None:
                    return False

                if self.currenttoken().type == "FROM":
                    self.avance()

                    if self.currenttoken() is None:
                        return False

                    if self.currenttoken().type == "IDENTIFIER":
                        self.avance()

                        if self.whereoption():
                            if self.currenttoken() is None:
                                return False

                            if self.currenttoken().type == "SEMICOLON":
                                self.avance()
                                return True

        return False
    def instructions(self):
        if self.currenttoken() is None:
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

        return False
    def tailledestring(self):
        if self.currenttoken() is None:
            return False

        if self.currenttoken().type == "LEFT_BRACKET":
            self.avance()

            if self.currenttoken() is None:
                return False

            if self.currenttoken().type == "INTEGER_NUMBER":
                self.avance()

                if self.currenttoken() is None:
                    return False

                if self.currenttoken().type == "RIGHT_BRACKET":
                    self.avance()
                    return True

            return False

        if (self.currenttoken().type == "COMMA"
            or self.currenttoken().type == "RIGHT_PARENTEZ"):
            return True

        return False
    def typededonnes(self):
        if self.currenttoken() is None:
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

        return False
    def singleattribut(self):
        if self.currenttoken() is None:
            return False

        if self.currenttoken().type == "IDENTIFIER":
            self.avance()

            if self.typededonnes():
                return True

        return False
    def attributetail(self):
        if self.currenttoken() is None:
            return False

        if self.currenttoken().type == "COMMA":
            self.avance()

            if self.singleattribut():
                return self.attributetail()

            return False

        if self.currenttoken().type == "RIGHT_PARENTEZ":
            return True

        return False
    def attributelist(self):
        if self.singleattribut():
            if self.attributetail():
                return True

        return False
    def createstatment(self):
        if self.currenttoken() is None:
            return False

        if self.currenttoken().type == "CREATE":
            self.avance()

            if self.currenttoken() is None:
                return False
            if self.currenttoken().type == "TABLE":
                self.avance()

                if self.currenttoken() is None:
                    return False
                if self.currenttoken().type == "IDENTIFIER":
                    self.avance()

                    if self.currenttoken() is None:
                        return False
                    if self.currenttoken().type == "LEFT_PARENTEZ":
                        self.avance()

                        if self.attributelist():
                            if self.currenttoken() is None:
                                return False
                            if self.currenttoken().type == "RIGHT_PARENTEZ":
                                self.avance()

                                if self.currenttoken() is None:
                                    return False
                                if self.currenttoken().type == "SEMICOLON":
                                    self.avance()
                                    return True

        return False
    def declarations(self):
        if self.currenttoken() is None:
            return False

        if self.currenttoken().type == "CREATE":
            if self.createstatment():
                return self.declarations()
            return False

        if (self.currenttoken().type == "INSERT"
            or self.currenttoken().type == "SELECT"
            or self.currenttoken().type == "FIN"):
            return True

        return False
    def program(self):
        if self.currenttoken() is None:
            return False

        if self.currenttoken().type == "PROGRAMME":
            self.avance()

            if self.currenttoken() is None:
                return False
            if self.currenttoken().type == "IDENTIFIER":
                self.avance()

                if self.currenttoken() is None:
                    return False
                if self.currenttoken().type == "SEMICOLON":
                    self.avance()

                    if self.declarations():
                        if self.instructions():
                            if self.currenttoken() is None:
                                return False
                            if self.currenttoken().type == "FIN":
                                self.avance()

                                if self.currenttoken() is None:
                                    return True

        return False
        