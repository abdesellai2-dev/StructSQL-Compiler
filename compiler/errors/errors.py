

class compilererror:
    def __init__(self,phase,line,column,message):
        self.phase = phase
        self.line = line
        self.column = column
        self.message = message
    def __str__(self):
        return f"[{self.phase}] Line {self.line}, Col {self.column}: {self.message}"
class errorreporter:
    def __init__(self):
        self.table_of_errors=[]
    def add(self,error):
        self.table_of_errors.append(error)
    def has_errors(self):
        if self.table_of_errors:
            return True
        else:
            return False