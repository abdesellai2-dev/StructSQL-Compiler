import sys
from pathlib import Path
import inspect

sys.path.append(str(Path(__file__).resolve().parents[3]))

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser

sourcecode = """
PROGRAMME school;

CREATE TABLE users (
    id INTEGER,
    name String[20],
    age REAL
);

INSERT INTO users VALUES (1, 'Ali', 20.5);

SELECT * FROM users;

FIN
"""

lexer = Lexer(sourcecode)
tokens = lexer.readalltokens()

print("TOKENS:")
for i, token in enumerate(tokens):
    print(i, token.type, repr(token.value))

parser = Parser(tokens)

print("\nPROGRAM FUNCTION:")
print(inspect.getsource(Parser.program))

print("\nRESULT:")
result = parser.program()

print("Program result:", result)
print("Position:", parser.position)
print("Current token:", parser.currenttoken())