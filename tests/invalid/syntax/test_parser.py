
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser


tests = [

    # ==============================
    # VALID PROGRAMS
    # ==============================

    (
        "Valid: Empty program",
        """
PROGRAMME school;
FIN
""",
        True
    ),

    (
        "Valid: Create table",
        """
PROGRAMME school;
CREATE TABLE users (
    id INTEGER,
    name String[20],
    age REAL
);
FIN
""",
        True
    ),

    (
        "Valid: Insert values",
        """
PROGRAMME school;
INSERT INTO users VALUES (1, 'Ali', 20.5);
FIN
""",
        True
    ),

    (
        "Valid: Select all",
        """
PROGRAMME school;
SELECT * FROM users;
FIN
""",
        True
    ),

    (
        "Valid: Select attributes",
        """
PROGRAMME school;
SELECT id, name, age FROM users;
FIN
""",
        True
    ),

    (
        "Valid: Select with WHERE",
        """
PROGRAMME school;
SELECT * FROM users WHERE age > 18;
FIN
""",
        True
    ),

    (
        "Valid: Multiple statements",
        """
PROGRAMME school;
CREATE TABLE users (
    id INTEGER,
    name String[20],
    age REAL
);
INSERT INTO users VALUES (1, 'Ali', 20.5);
SELECT * FROM users;
FIN
""",
        True
    ),

    (
        "Valid: All relational operators",
        """
PROGRAMME school;
SELECT * FROM users WHERE id = 1;
SELECT * FROM users WHERE id != 2;
SELECT * FROM users WHERE age < 20;
SELECT * FROM users WHERE age > 18;
SELECT * FROM users WHERE age <= 30;
SELECT * FROM users WHERE age >= 10;
FIN
""",
        True
    ),

    # ==============================
    # INVALID PROGRAMS
    # ==============================

    (
        "Invalid: Missing PROGRAMME",
        """
school;
FIN
""",
        False
    ),

    (
        "Invalid: Missing program identifier",
        """
PROGRAMME ;
FIN
""",
        False
    ),

    (
        "Invalid: Missing semicolon",
        """
PROGRAMME school
FIN
""",
        False
    ),

    (
        "Invalid: Missing FIN",
        """
PROGRAMME school;
""",
        False
    ),

    (
        "Invalid: Incomplete CREATE",
        """
PROGRAMME school;
CREATE
FIN
""",
        False
    ),

    (
        "Invalid: Missing TABLE",
        """
PROGRAMME school;
CREATE users (id INTEGER);
FIN
""",
        False
    ),

    (
        "Invalid: Missing table identifier",
        """
PROGRAMME school;
CREATE TABLE (id INTEGER);
FIN
""",
        False
    ),

    (
        "Invalid: Missing left parenthesis",
        """
PROGRAMME school;
CREATE TABLE users id INTEGER);
FIN
""",
        False
    ),

    (
        "Invalid: Missing attribute type",
        """
PROGRAMME school;
CREATE TABLE users (id);
FIN
""",
        False
    ),

    (
        "Invalid: Missing right parenthesis",
        """
PROGRAMME school;
CREATE TABLE users (id INTEGER;
FIN
""",
        False
    ),

    (
        "Invalid: Missing string size number",
        """
PROGRAMME school;
CREATE TABLE users (name String[]);
FIN
""",
        False
    ),

    (
        "Invalid: Missing right bracket",
        """
PROGRAMME school;
CREATE TABLE users (name String[20);
FIN
""",
        False
    ),

    (
        "Invalid: Missing attribute after comma",
        """
PROGRAMME school;
CREATE TABLE users (id INTEGER,);
FIN
""",
        False
    ),

    (
        "Invalid: Missing INSERT INTO",
        """
PROGRAMME school;
INSERT users VALUES (1);
FIN
""",
        False
    ),

    (
        "Invalid: Missing table name in INSERT",
        """
PROGRAMME school;
INSERT INTO VALUES (1);
FIN
""",
        False
    ),

    (
        "Invalid: Missing VALUES",
        """
PROGRAMME school;
INSERT INTO users (1);
FIN
""",
        False
    ),

    (
        "Invalid: Missing value",
        """
PROGRAMME school;
INSERT INTO users VALUES (1, , 20);
FIN
""",
        False
    ),

    (
        "Invalid: Missing right parenthesis in INSERT",
        """
PROGRAMME school;
INSERT INTO users VALUES (1, 20;
FIN
""",
        False
    ),

    (
        "Invalid: Missing semicolon in INSERT",
        """
PROGRAMME school;
INSERT INTO users VALUES (1, 20)
FIN
""",
        False
    ),

    (
        "Invalid: Missing SELECT list",
        """
PROGRAMME school;
SELECT FROM users;
FIN
""",
        False
    ),

    (
        "Invalid: Missing FROM",
        """
PROGRAMME school;
SELECT * users;
FIN
""",
        False
    ),

    (
        "Invalid: Missing table name in SELECT",
        """
PROGRAMME school;
SELECT * FROM;
FIN
""",
        False
    ),

    (
        "Invalid: Missing identifier after comma in SELECT",
        """
PROGRAMME school;
SELECT id, FROM users;
FIN
""",
        False
    ),

    (
        "Invalid: Missing condition value",
        """
PROGRAMME school;
SELECT * FROM users WHERE age > ;
FIN
""",
        False
    ),

    (
        "Invalid: Missing relational operator",
        """
PROGRAMME school;
SELECT * FROM users WHERE age 20;
FIN
""",
        False
    ),

    (
        "Invalid: Missing semicolon in SELECT",
        """
PROGRAMME school;
SELECT * FROM users
FIN
""",
        False
    ),

    (
        "Invalid: Extra token after FIN",
        """
PROGRAMME school;
FIN
SELECT * FROM users;
""",
        False
    ),
]


passed = 0
failed = 0

print("=" * 60)
print("STRUCTSQL PARSER TESTS")
print("=" * 60)

for name, source, expected in tests:

    lexer = Lexer(source)
    tokens = lexer.readalltokens()

    parser = Parser(tokens)
    result = parser.program()

    success = result == expected

    if success:
        passed += 1
        status = "PASS"
    else:
        failed += 1
        status = "FAIL"

    print("\n" + "-" * 60)
    print(f"{status}: {name}")
    print(f"Expected: {expected}")
    print(f"Actual:   {result}")

    if parser.reporter.has_errors():
        for error in parser.reporter.table_of_errors:
            print(error)

    if not success:
        print("Position:", parser.position)
        print("Current token:", parser.currenttoken())


print("\n" + "=" * 60)
print("FINAL RESULTS")
print("=" * 60)

print(f"Total tests: {len(tests)}")
print(f"Passed:      {passed}")
print(f"Failed:      {failed}")

if failed == 0:
    print("\nALL TESTS PASSED!")
else:
    print("\nSOME TESTS FAILED!")
