# Question 1 #

Class for a Token, contains its lexeme as a string  
and its token code as an integer.
```
class Token:
	def __init__(self, lexeme, code):
		self.lexeme = lexeme or ""
		self.code = code or -1
```

# Question 2 #
![compiler.py](./compiler.py) is the 'main' file. Given a file,  
attempts convert the file into a string of tokens using ![lexer.py](./lexer.py).  
Then attempts to parse the file with ![parser.py](./parser.py).

# Question 3 #
![lexer.py](./lexer.py) attempts to convert a given text string  
into tokens. Stops when an invalid token is detected.  
Example valid output:  
```
Lexeme at index  0 is: def             Token is (15) function declaration
Lexeme at index  1 is: func            Token is (37) variable or function identifier
Lexeme at index  2 is: (               Token is (21) left parentheses
Lexeme at index  3 is: )               Token is (22) right parentheses
Lexeme at index  4 is: {               Token is (34) left curly brace
Lexeme at index  5 is: int             Token is (11) int declaration
Lexeme at index  6 is: a               Token is (37) variable or function identifier
Lexeme at index  7 is: }               Token is (35) right curly brace
```
Example invalid output:
```
Lexeme at index  0 is: def             Token is (15) function declaration
Lexeme at index  1 is: func            Token is (37) variable or function identifier
Lexeme at index  2 is: (               Token is (21) left parentheses
Lexeme at index  3 is: )               Token is (22) right parentheses
Lexeme at index  4 is: {               Token is (34) left curly brace
Lexeme at index  5 is: int             Token is (11) int declaration
Lexeme at index  6 is: a               Token is (37) variable or function identifier
lexeme at index  7 is invalid
```
### Regex ###
regex for real literal:  
 - optional - or +, followed by any number of 0-9, a decimal  
 then at least one 0-9
```
([-+]?[0-9]*[.][0-9]+)
```
regex for natural literal:  
 - optional - or +, followed by at least one 0-9
```
([-+]?[0-9]+)
```
regex for bool literal:  
 - The word 'True' or 'False' without a leading or following  
 alphanumeric character or underscore
```
((?<![a-zA-Z0-9_])True(?![a-zA-Z0-9_])|(?<![a-zA-Z0-9_])False(?![a-zA-Z0-9_]))
```
regex for char literal:  
 - any character between space and ~, can be optionally escaped.  
 enclosed in apostrophes.
```
('\\?[ -~]')
```
regex for String literal:  
 - any number of non apostrophe or unescaped characters eclosed  
 in apostrophes.
```
('(\\.|[^'\\])*')
```
regex for any given keyword:
 - matches a keyword exactly without a leading or following  
 alphanumeric character or underscore
 - keywords include "if", "else", "elif", "while", "String",  
 "int", "char", "float", "bool", or "def"
```
(?<![a-zA-Z0-9_])KEYWORD(?![a-zA-Z0-9_])
```