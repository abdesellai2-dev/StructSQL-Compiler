import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from compiler.lexer.lexer import Lexer
source = input("Enter SQL code: ")

lexer = Lexer(source)
tokens = lexer.readalltokens()
print("tokens :")
for token in tokens:
    print(token.type, end=" ")