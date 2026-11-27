import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from compiler.lexer.lexer import Lexer
sourcecode = "PROGRAMME test; FIN"

lexer = Lexer(sourcecode)
tokens = lexer.readalltokens()

for token in tokens:
    print(token.type, repr(token.value))