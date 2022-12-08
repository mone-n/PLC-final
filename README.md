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
into Token objects. Stops when an invalid token is detected.  
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
regex for comments:
 - matches any whitespace or non whitespace characters  
 between triple apostrophes. (Multiline comments)
 - also matches any single characters an unlimited number  
 of times on a single line, preceded by a #
```
('''[\s\S]*''')|(#.*)
```
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
 - any number of non apostrophe or unescaped characters enclosed  
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
regex for any reserved symbol:  
 - pretty simple, each reserved symbol is its own regex, all  
 of them are escaped so I dont have to worry if regex can read them.  
 - symbols include: \+, \-, \*, \/, \^, \(, \), \>\=\=, \<\=\=,  
  \>, \<, \=\=, \!\=\=, \=, \~, \!, \&, \|, \{, \}, \,
```
(SYMBOL)
```
regex for identifying variable or function names:  
 - can be any number of alphanumeric or underscore characters  
 cant start with a number however.
```
([a-zA-Z_][a-zA-Z0-9_]*)
```

# Question 4 #
![parser.py](./parser.py) attempts to parse through a given list  
of Token objects, making sure it is syntactically correct. Gets  
called only if the Lexer succedes

### Parse Tree ###
Example parse tree for a small program:  
```
String hi
hi = 'hello world\n'
```
```
func: ()
 func: start()
  func: statement()
   func: declaration()
    func: var_declare() - tokens validated: String, hi
  func: statement()
   func: assignment() - tokens validated: hi, =
    func: bool_relation()
     func: bool_expr()
      func: expr()
       func: term()
        func: exp()
         func: logical()
          func: factor() - tokens validated: 'hello world\n'
```
The parse tree reads kind of like a file system, where nodes  
without spaces ahead of them are root nodes, and the nodes  
directly underneath are its children.  
  
The parse tree lets the user know which function has validated  
which tokens, and what chain of functions was called to  
validated each token.

### Grammar Rules ###
```
<start>          -->  {<statement>}
<statment>       -->  <block> | <selection> | <while_loop> | <declaration> | <assignment>
<block>          -->  '{' <start> '}'
<selection>      -->  'if' '(' <bool_relation> ')' '{' <start> '}' [<else_statement>|<elif_statement>]
<while_loop>     -->  'while' '(' <bool_relation> ')' '{' <start> '}'
<declaration>    -->  <var_declare> | <func_declare>
<assignment>     -->  [a-zA-Z_][a-zA-Z0-9_]* '=' <bool_relation>
<bool_relation>  -->  <bool_expr> {'!=='|'==' <bool_expr>}
<else_statement> -->  'else' '{' <start> '}'
<elif_statement> -->  'elif' '(' <bool_relation> ')' '{' <start> '}' [<else_statement>|<elif_statement>]
<var_declare>    -->  ('String'|'int'|'char'|'float'|'bool') [a-zA-Z_][a-zA-Z0-9_]*
<func_declare>   -->  'def' [a-zA-Z_][a-zA-Z0-9_]* '(' {[a-zA-Z_][a-zA-Z0-9_]* ','} ')'
                      '{' <start> '}'
<bool_expr>      -->  <expr> {'<=='|'>=='|'<'|'>' <expr>}
<expr>           -->  <term> {'+'|'-' <term>}
<term>           -->  <exp> {'*'|'/'|'%' <exp>}
<exp>            -->  <logical> {'^' <logical>}
<logical>        -->  <factor> {'~'|'&'|'|' <factor>}
<factor>         -->  [a-zA-Z_][a-zA-Z0-9_]* | [-+]?[0-9]*[.][0-9]+ | [-+]?[0-9]+ | 
                      ((?<![a-zA-Z0-9_])True(?![a-zA-Z0-9_])|(?<![a-zA-Z0-9_])False(?![a-zA-Z0-9_]))
                      | '[ -~]' | \'(\\\\.|[^\'\\\\])*\' | '(' <bool_relation> ')'
                      | [a-zA-Z_][a-zA-Z0-9_]* '(' {[a-zA-Z_][a-zA-Z0-9_]* ','} ')'
```

# Question 5 #
### Denotational semantics to define selection statement ###  
Grammar for my selection statement  
```
<selection>  -->  'if' '(' <bool_relation> ')' '{' <start> '}'
```
converts to:  
```
M_sel( if ( <bool_relation> ) { <start> }, s) ==>
    if M_br( <bool_relation>, s) == error
        return error
    if M_br( <bool_relation>, s) == False
        return s
    else
        if M_st( <start>, s) == error
            return error
        return M_st( <start>, s)
```
# Question 6 #
### Denotational semantics to define loop statement ###  
Grammar for my loop statement  
```
<while_loop>  -->  'while' '(' <bool_relation> ')' '{' <start> '}'
```
converts to:  
```
M_w( 'while' '(' <bool_relation> ')' '{' <start> '}', s) ==>
    if M_br( <bool_relation>, s) == error
        return error
    if M_br( <bool_relation>, s) == False
        return s
    else
        if M_s( <start>, s) == error
            return error
        M_w( 'while' '(' <bool_relation> ')' '{' <start> '}', M_s(LS, s))
```
# Question 7 #
### Denotational semantics to define expr statement ###  
The function (edited to reflect the RDA part without the ParseTree  
generation part) for my expr statement.
```
# <expr>  -->  <term> {'+'|'-' <term>}
def expr(self):
        self.term()
        while self.curr_token.lexeme in ['+', '-']:
            self.next_token()
            self.term()
```
Converts to:
```
M_e( <l_term> {<operator> <r_term>}, s) ==>
	if M_rt( <r_term>, s ) == error
		return error
	if M_lt( <l_term>, s ) == error
		return error
    if <operator> == '-'
        return M_lt( <l_term>, s ) - M_rt( <r_term>, s)
    if <operator> == '+'
    	return M_lt( <l_term>, s ) + M_rt( <r_term>, s)
```
# Question 8 #
### redefine Expr statement so it can return a boolean solution ###  

# Question 9 #
### Attribute grammar for assignment statement ###
 - ##### String + String does concatenation #####  
 - ##### String * Natural repeats the String #####  
 - ##### Assign bool to natural is allowed #####  
 - ##### Assign natural to bool is allowed #####  
 - ##### Assign char to natural is allowed #####  
 - ##### Assign natural to char is allowed #####  
 - ##### Assign natural to real is allowed #####  
 - ##### No other types are allowed to be assigned to others outside of their own #####  
 - ##### Dividing by zero is an error #####  
 - ##### Modulo operating by zero is an error #####  
```
Syntax Rule:   <assignment> --> <var> '=' <bool_relation>
Semantic Rule: <bool_relation>.expected_type <-- <var>.actual_type

Syntax Rule:   <bool_relation> --> <bool_expr> {'!=='|'==' <bool_expr>}
Semantic Rule: <
```
# Question 10 #
### 3 syntactically valid assignment statements ###

# Question 11 #
### Find Weakest Precondition ###  
- a. 
```C
a = 2 * (b - 1) - 1 {a > 0}
```
    - plug in a = 0, b = 1.5  
    - b = 1.5, weakest precondition: {b > 1.5}  
- b. 
```C
if (x < y)
	x = x + 1
else
	x = 3 * x
{x < 0}
```  