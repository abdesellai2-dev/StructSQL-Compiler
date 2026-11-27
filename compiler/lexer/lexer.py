from compiler.lexer.tokens import KEYWORDS, OPERATORS, SEPERATORS, Token
from compiler.errors.errors import compilererror, errorreporter

quotes = ("'", '’', '‘')


class Lexer:
    def __init__(self,sourcecode):
        self.sourcecode=sourcecode
        self.position=0
        self.line=1
        self.column=1
        self.reporter = errorreporter()
    def add_error(self,line,column,message):
        error = compilererror("LEXICAL",line,column,message)
        self.reporter.add(error)


    def avance(self):
       if (self.position < len(self.sourcecode)):
        if(self.sourcecode[self.position] == "\n"):
                self.line += 1
                self.column = 1
        elif(self.sourcecode[self.position] == "\t"):
                self.column += 4
        else:
            self.column += 1
        self.position = self.position + 1
       
       return self.position

    def readchar(self):
        if(self.position < len(self.sourcecode)):
         char = self.sourcecode[self.position]
         self.avance()
         return char
        else:
         return ""
        
    """def readword(self):
        word = ""
        while ( self.position < len(self.sourcecode) and self.sourcecode[self.position] != " " and self.sourcecode[self.position] != "\n"and self.sourcecode[self.position] != "\t" and self.sourcecode[self.position] not in SEPERATORS and self.sourcecode[self.position] not in OPERATORS):
          word = word + self.readchar()
        return word 
    """
    def readword(self):
        word = ""

        if self.position >= len(self.sourcecode):
            return word

        char = self.sourcecode[self.position]

        match char:
            case "=" | "<" | ">" | "!":
                word = self.readchar()
    
                if self.position < len(self.sourcecode) and word + self.sourcecode[self.position] in OPERATORS:
                    word = word + self.readchar()

            case "*":
                word = self.readchar()

            case "(" | ")" | "[" | "]" | "," | ";":
                word = self.readchar()

            case _:
                while (self.position < len(self.sourcecode)
                        and self.sourcecode[self.position] != " "
                        and self.sourcecode[self.position] != "\n"
                        and self.sourcecode[self.position] != "\t"
                        and self.sourcecode[self.position] != "\r"
                        and self.sourcecode[self.position] not in SEPERATORS
                        and self.sourcecode[self.position] not in OPERATORS
                        and self.sourcecode[self.position] != "!"
                        and self.sourcecode[self.position] not in quotes):

                    word = word + self.readchar()

        return word
    
    def skipwhitess(self):
        while(self.position < len(self.sourcecode) and (self.sourcecode[self.position]== " " or self.sourcecode[self.position]== "\n" or self.sourcecode[self.position]== "\t" or self.sourcecode[self.position]== "\r")):
            self.avance()
    def sireel(self,word):
        checkword = word
        position = 0
        isdotreached=False
        if (checkword == ""):
           return False
        if(checkword[0]== "."):
            return False
        if(checkword[len(checkword)-1]== "."):
            return False
        if("." not in checkword):
            return False
        while(position < len(checkword)):
            if(checkword[position]=="." and isdotreached==True):
                return False
            elif(checkword[position]=="." and isdotreached==False):
                isdotreached=True
            elif checkword[position] < "0" or checkword[position] > "9" :
                return False
            position +=1
        return True

    def sinombre(self,word):
        checkword = word
        position = 0
        if (checkword == ""):
            return False
        while(position < len(checkword)): 
            if checkword[position] < "0" or checkword[position] > "9":
             return False
            position += 1
        return True  
    
    def readtoken(self):
        start_line = self.line
        start_column = self.column
        
        if self.position >= len(self.sourcecode):
            return Token("EOF", "", self.line, self.column)
        if self.sourcecode[self.position] in quotes:
            return self.readstring()
        word = self.readword()

        if(self.sireel(word)):
            return Token("REAL_NUMBER", word, start_line, start_column)
        if(self.sinombre(word)):
            return Token("INTEGER_NUMBER",word,start_line,start_column)
        match(word):

            
            case "PROGRAMME":
                return Token("PROGRAMME",word,start_line,start_column)
            
            case "FIN":
                return Token("FIN",word,start_line,start_column)

            case "CREATE":
                return Token("CREATE",word,start_line,start_column)

            case "TABLE":
                return Token("TABLE",word,start_line,start_column)

            case "INSERT":
                return Token("INSERT",word,start_line,start_column)

            case "INTO":
                return Token("INTO",word,start_line,start_column)

            case "VALUES":
                return Token("VALUES",word,start_line,start_column)

            case "SELECT":
                return Token("SELECT",word,start_line,start_column)

            case "FROM":
                return Token("FROM",word,start_line,start_column)

            case "WHERE":
                return Token("WHERE",word,start_line,start_column)

            case "INTEGER":
                return Token("TYPE_INTEGER",word,start_line,start_column)

            case "REAL":
                return Token("TYPE_REAL",word,start_line,start_column)

            case "String" | "string":
                return Token("TYPE_STRING",word,start_line,start_column)

            case "=":
                return Token("EQUALS",word,start_line,start_column)

            case "<":
                return Token("LESS_THAN",word,start_line,start_column)

            case ">":
                return Token("GREATER_THAN",word,start_line,start_column)

            case "<=":
                return Token("LESS_THAN_EQUAL",word,start_line,start_column)

            case ">=":
                return Token("GREATER_THAN_EQUAL",word,start_line,start_column)

            case "!=":
                return Token("DIFFERENT",word,start_line,start_column)

            case "*":
                return Token("NEDJMA",word,start_line,start_column)

            case "(":
                return Token("LEFT_PARENTEZ",word,start_line,start_column)

            case ")":
                return Token("RIGHT_PARENTEZ",word,start_line,start_column)

            case "[":
                return Token("LEFT_BRACKET",word,start_line,start_column)

            case "]":
                return Token("RIGHT_BRACKET",word,start_line,start_column)

            case ",":
                return Token("COMMA",word,start_line,start_column)

            case ";":
                return Token("SEMICOLON",word,start_line,start_column)
            case _:
                if self.isidentifier(word, start_line, start_column):
                 return Token("IDENTIFIER", word, start_line,start_column)


    def readalltokens(self):
        source_code = self.sourcecode
        tokens = []
        while(self.position < len(source_code)): 
            self.skipwhitess()

            if self.position < len(source_code):
                token = self.readtoken()
                if token is not None:
                    tokens.append(token)
        tokens.append(Token("EOF", "", self.line, self.column))
        return tokens
    def readstring(self):
        start_line = self.line
        start_column = self.column
        the_string_word = ""
        has_space=False
        self.readchar() #skip the 1st quota
        while(self.position < len(self.sourcecode)):
            if self.sourcecode[self.position] == "\n":
                self.add_error(start_line,start_column,"Unterminated string literal")
                return None
            char = self.readchar()
            if char ==" " or char == "\t":
                has_space = True
            if char in quotes and has_space == False:
                return Token("STRING_LITERAL", the_string_word, start_line, start_column)
            elif char in quotes and has_space == True:
                self.add_error(start_line,start_column,"this word contain spaces")
                return None
            else:
                the_string_word = the_string_word + char
        self.add_error(start_line,start_column,"Unterminated string literal")
        return None
    def isdigit(self,char):
        if char < "0" or char > "9":
            return False
        return True
    def isletter(self,char):
        if char >= "a" and char <= "z":
            return True
        elif char >= "A" and char <= "Z":
                    return True
        
        return False
    
    def isidentifier(self,word,line,column):

        if(self.isdigit(word[0])):
            only_digits_and_dots = True
            position = 0
            while position < len(word):
                if self.isdigit(word[position]) == False and word[position] != ".":
                    only_digits_and_dots = False
                position += 1
            if only_digits_and_dots:
                self.add_error(line,column,"Malformed number: " + word)
            else:
                self.add_error(line,column,"identifier cant start with a digit: " + word)
            return False
        elif(self.isletter(word[0]) == False):
            if word[0] == "!":
                self.add_error(line,column,"! must be followed by =")
            else:
                self.add_error(line,column,"Illegal character '" + word[0] + "'")
            return False
        position = 0
        while position < len(word):
            if (self.isdigit(word[position])== False and self.isletter(word[position])== False):
                self.add_error(line,column+position,"Illegal character("+word[position]+ ")in the identifier")
                return False
            position += 1

        return True
    