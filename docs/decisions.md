#	Question	Decision	Reason
1	Compiler language	Python	Fast to write, easy GUI
2	Parsing method	LL(1) predictive, table-driven with a stack	Matches your course (DEBUT/SUIVANT, predictive table, chaine/pile/sorties trace)
3	Target language	Python	Simple file handling, no compile step
4	Keywords case	Case-insensitive (select = SELECT)	The PDF mixes String, string, INTEGER
5	Identifiers case	Case-sensitive (Etudiant ≠ etudiant)	Simple and consistent
6	String type syntax	STRING with optional [n] (string[20])	The PDF uses both forms
7	Meaning of [n]	Maximum length, checked semantically	Gives the size a real use
8	Quote characters	Accept both '...' and ’...’	The PDF uses curly quotes
9	Spaces inside strings	Forbidden	.dat lines are space-separated
10	Numbers	Integer: digits. Real: digits . digits. No negative numbers	Keeps the lexer small
11	INTEGER into REAL	Allowed. REAL into INTEGER is an error	Standard numeric promotion
12	WHERE form	attribute operator literal only	"Simple condition" in the spec
13	Comparisons on STRING	Only = and !=	< and > on text are not meaningful here
14	Comparison type rule	Literal type must match the attribute (INTEGER and REAL together, STRING with STRING)	Matches "validity of conditions"
15	Duplicate CREATE	Semantic error	Avoids silent overwrite
16	CREATE at execution	Create or reset the .dat file on each run	Reproducible demo
17	Comments	Not supported	Not in the spec
18	Whitespace and newlines	Ignored between tokens	Free-form layout
19	Program name	Identifier after PROGRAMME, used only as a label	Per the spec
20	Error recovery	Skip to the next ;	Allows several errors per run