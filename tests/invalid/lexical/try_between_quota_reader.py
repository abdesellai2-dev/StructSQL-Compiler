import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from compiler.lexer.lexer import Lexer
src = "x = ‘brahmi’; y = 'a\tb';"
for t in Lexer(src).readalltokens():
    print(t.type, repr(t.value), t.line, t.column)