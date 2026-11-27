import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from compiler.lexer.lexer import Lexer


folder = ROOT / "tests" / "invalid" / "lexical" 
for file in sorted(folder.glob("*.sql")):
    src = file.read_text(encoding="utf-8")
    l = Lexer(src)
    tokens = l.readalltokens()
    print("==", file.name, "->", len(l.reporter.table_of_errors), "errors")
    for e in l.reporter.table_of_errors:
        print("   ", e)