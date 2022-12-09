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
Adding booleans is equivalent to the OR function, and in this
case subtraction will be the same as the AND function
```
M_e( <l_term> {<operator> <r_term>}, s) ==>
    if M_rt( <r_term>, s ) == error
        return error
    if M_lt( <l_term>, s ) == error
        return error
    if <operator> == '-'
        return M_lt( <l_term>, s ) and M_rt( <r_term>, s)
    if <operator> == '+'
        return M_lt( <l_term>, s ) or M_rt( <r_term>, s)
```

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
The grammar rules for assignment are changed to be readable between  
Syntax Rules and Semantic Rules, the meaning of the Grammar rule is  
still the same.  
```
<assignment>     -->  <var> '=' <bool_relation>
<bool_relation>  -->  <bool_expr> {'!=='|'==' <bool_expr>}
<bool_expr>      -->  <expr> {'<=='|'>=='|'<'|'>' <expr>}
<expr>           -->  <term> {'+'|'-' <term>}
<term>           -->  <exp> {'*'|'/'|'%' <exp>}
<exp>            -->  <logical> {'^' <logical>}
<logical>        -->  <factor> {'~'|'&'|'|' <factor>}
<factor>         -->  <var>
```
Becomes:
```
<assignment>     -->  <var> '=' <bool_relation>
<bool_relation>  -->  <bool_expr> ('!=='|'==') <bool_expr> | <bool_expr>
<bool_expr>      -->  <expr> ('<=='|'>=='|'<'|'>') <expr>  | <expr>
<expr>           -->  <term> ('+'|'-') <term>              | <term>
<term>           -->  <exp> ('*'|'/'|'%') <exp>            | <exp>
<exp>            -->  <logical> '^' <logical>              | <logical>
<logical>        -->  <factor> ('~'|'&'|'|') <factor>      | <factor>
<factor>         -->  <var>
```

``` 
Syntax Rule:   <assignment> --> <var> '=' <bool_relation>
Semantic Rule: <bool_relation>.actual_type <-- 
                    if <var>.actual_type == int and
                    <bool_relation>.actual_type == bool
                        then bool
                    if <var>.actual_type == bool and
                    <bool_relation>.actual_type == int
                        then int
                    if <var>.actual_type == int and
                    <bool_relation>.actual_type == char
                        then char
                    if <var>.actual_type == char and
                    <bool_relation>.actual_type == int
                        then int
                    if <var>.actual_type == float and
                    <bool_relation>.actual_type == int
                        then int
Predicate:     <var>.actual_type == <var>.expected_type

Syntax Rule:   <bool_relation> --> <bool_expr>[2] ('!=='|'==') <bool_expr>[3]
Semantic Rule: <bool_relation>.actual_type <-- bool
Predicate:     <bool_relation>.actual_type == <bool_relation>.expected_type

Syntax Rule:   <bool_relation> --> <bool_expr>
Semantic Rule: <bool_relation>.actual_type <-- <bool_expr>.actual_type
Predicate:     <bool_relation>.actual_type == <bool_relation>.expected_type

Syntax Rule:   <bool_expr> --> <expr>[2] ('<=='|'>=='|'<'|'>') <expr>[3]
Semantic Rule: <bool_expr>.actual_type <-- bool
Predicate:     <bool_expr>.actual_type == <bool_expr>.expected_type

Syntax Rule:   <bool_expr> --> <expr>
Semantic Rule: <bool_expr>.actual_type <-- <expr>.actual_type
Predicate:     <bool_expr>.actual_type == <bool_expr>.expected_type

Syntax Rule:   <expr> --> <term>[2] '+' <term>[3]
Semantic Rule: <expr>.actual_type <--
                    if <term>[2].actual_type == String and
                    <term>[3].actual_type == String
                        then String
                    if <term>[2].actual_type == int and
                    <term>[3].actual_type == int
                        then int
                    else float
                    end if
Predicate:     <expr>.actual_type == <expr>.expected_type

Syntax Rule:   <expr> --> <term>[2] '-' <term>[3]
Semantic Rule: <expr>.actual_type <--
                    if <term>[2].actual_type == int and
                    <term>[3].actual_type == int
                        then int
                    else float
                    end if
Predicate:     <expr>.actual_type == <expr>.expected_type

Syntax Rule:   <expr> --> <term>
Semantic Rule: <expr>.actual_type <-- <term>.actual_type
Predicate:     <expr>.actual_type == <expr>.expected_type

Syntax Rule:   <term> --> <exp>[2] '*' <exp>[3]
Semantic Rule: <term>.actual_type <--
                    if <exp>[2].actual_type == String and
                    <exp>[3].actual_type == int
                        then String
                    if <exp>[2].actual_type == int and
                    <exp>[3].actual_type == int
                        then int
                    else float
                    end if
Predicate:     <term>.actual_type == <term>.expected_type

Syntax Rule:   <term> --> <exp>[2] '/'|'%' <exp>[3]
Semantic Rule: <term>.actual_type <--
                    if <exp>[2].actual_type == int and
                    <exp>[3].actual_type == int and
                    lookup(<exp>[3].value) != 0
                        then float
                    if <exp>[2].actual_type == float and
                    <exp>[3].actual_type == float and
                    lookup(<exp>[3].value) != 0.0
                        then float
                    end if
Predicate:     <term>.actual_type == <term>.expected_type

Syntax Rule:   <term> --> <exp>
Semantic Rule: <term>.actual_type <-- <exp>.actual_type
Predicate:     <term>.actual_type == <term>.expected_type

Syntax Rule:   <exp> --> <logical>[2] '^' <logical>[3]
Semantic Rule: <exp>.actual_type <-- float
Predicate:     <exp>.actual_type == <exp>.expected_type

Syntax Rule:   <logical> --> <factor>[2] '~'|'&'|'|' <factor>[3]
Semantic Rule: <logical>.actual_type <-- bool
Predicate:     <logical>.actual_type == <logical>.expected_type

Syntax Rule:   <factor> --> <var>
Semantic Rule: <factor>.actual_type <-- lookup(<var>.string)
```
# Question 10 #
### Assignment Statements passing syntax, but failing or passing semantics ###
### 1 ###
This assignment statement successfully passes syntax analysis
``` a = 5.0 ^ False - '\n' ```
However, we can trace the semantic analysis to where the '^' is checked.
```
<assignment> -> <bool_relation> -> <bool_expr> -> <expr> -> <term> -> <exp>
```
Here 5.0 and False arent both floats, and this statement gets rejected by  
semantic analysis.  
### 2 ###
This assignment statement successfully passes syntax analysis
``` a = 6 * 'str' + 1 ```
However, we can trace the semantic analysis to where the '\*' is checked.  
```
<assignment> -> <bool_relation> -> <bool_expr> -> <expr> -> <term> 
```
Then here we can see that while the type of the first portion of the  
problem is int, the second portion is String, and doesnt have a type  
that can be returned, failing the semantic analysis.
### 3 ###
This assignment statement successfully passes syntax analysis
``` a = 'str' * 2 + 'ing' ```
This assignment statement also passes the semantic analysis because  
Strings can be multiplied by integers, and then the resulting String can  
be added to another String.

# Question 11 #
### Find Weakest Precondition ###   
```
a = 2 * (b - 1) - 1 {a > 0}
```
 - plug in a = 0, b = 1.5  
 - b = 1.5, weakest precondition: {b > 1.5}  
```
if (x < y)
	x = x + 1
else
	x = 3 * x
{x < 0}
```  
 - Two conditions need to be met:
    - x = x + 1 {x < 0}
    - x = 3 * x {x < 0}
 - x = x + 1 {x < 0}
    - 0 = x + 1
    - {x < -1}
 - x = 3 * x {x < 0}
    - 0 = 3 * x
    - {x < 0}
 - Weakest precondition: {x < 0}
```
y = a * 2 * (b - 1) - 1
if (x < y)
	x = y + 1
else
	x = 3 * x
{x < 0}
```
 - Two conditions need to be met:
    - x = x + 1 {x < 0}
    - x = 3 * x {x < 0}  
 - x = y + 1 {x < 0}
    - 0 = y + 1
    - 0 = a * 2 * (b - 1)
    - {ab - a < 0}
 - x = 3 * x
    - {x < 0}
```
a = 3 * (2 * b + a)
b = 2 * a - 1
{b > 5}
```
 - 5 < 2 * a - 1
 - 6 < 2 * a
 - 3 < a
 - this becomes post-condition for: a = 3 * (2 * b + a)
 - 3 < 3 * (2 * b + a)
 - 1 < 2 * b + a
 - 1 - a < 2 * b
 - weakest precondition: {(1 - a) / 2 < b}