KEYWORDS = {
    "PROGRAMME": "PROGRAMME",
    "FIN": "FIN",
    "CREATE": "CREATE",
    "TABLE": "TABLE",
    "INSERT": "INSERT",
    "INTO": "INTO",
    "VALUES": "VALUES",
    "SELECT": "SELECT",
    "FROM": "FROM",
    "WHERE": "WHERE",
    "INTEGER": "TYPE_INTEGER",
    "REAL": "TYPE_REAL",
    "String": "TYPE_STRING",
    "string": "TYPE_STRING",
    
}
OPERATORS = {
    "=": "EQUALS",
    "<": "LESS_THAN",
    ">": "GREATER_THAN",
    "<=": "LESS_THAN_EQUAL",
    ">=": "GREATER_THAN_EQUAL",
    "!=": "DIFFERENT",
}
SEPERATORS = {
#    "_": "UNDERSCORE",
    "*": "NEDJMA",
    "(": "LEFT_PARENTEZ",
    ")": "RIGHT_PARENTEZ",
    "[": "LEFT_BRACKET",
    "]": "RIGHT_BRACKET",
#    ".": "POINT",
    ",": "COMMA",
    ";": "SEMICOLON",
}





class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    def __str__(self):
        return f"{self.type:<20} {self.value!r:<18} line {self.line}, col {self.column}"


