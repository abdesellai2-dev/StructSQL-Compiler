import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from compiler.lexer.lexer import Lexer
source = """SELECT
    * FROM users
    WHERE age >= 18;"""

lexer = Lexer(source)
tokens = lexer.readalltokens()

for token in tokens:
    print(token.type, token.value, token.line, token.column)