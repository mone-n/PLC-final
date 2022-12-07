import re
from token import Token
from parse_tree import Parse_Tree

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.index = 0

		self.parse_tree = Parse_Tree()
		self.curr_parse = self.parse_tree

		self.validated_tokens = []
		self.curr_token = self.tokens[self.index]
		

	# raises an error giving the token at fault
	# and the index of the token at fault
	def error(self):
		raise Exception('error with token: (' + self.curr_token.lexeme + ") at token index: " + str(self.index))


	# adds the previous token to a list of validated tokens
	# then increments the current token index
	# and sets the current token to the next token
	def next_token(self, parse_tree_node):
		self.validated_tokens.append(self.curr_token)
		parse_tree_node.tokens.append(self.curr_token.lexeme)

		if self.index < len(self.tokens) - 1:
			self.index += 1

		self.curr_token = self.tokens[self.index]


	# returns true the current token integer is valid variable name
	# or valid function name returns false otherwise
	def validate_var(self):
		if re.findall('[a-zA-Z_][a-zA-Z0-9_]*', self.curr_token.lexeme) != []:
			return re.findall('[a-zA-Z_][a-zA-Z0-9_]*', self.curr_token.lexeme)[0] == self.curr_token.lexeme
		return False


	# returns true the current token integer is a real_literal
	# returns false otherwise
	def validate_real(self):
		if re.findall('[-+]?[0-9]*[.][0-9]+', self.curr_token.lexeme) != []:
			return re.findall('[-+]?[0-9]*[.][0-9]+', self.curr_token.lexeme)[0] == self.curr_token.lexeme
		return False


	# returns true the current token integer is a natural_literal
	# returns false otherwise
	def validate_natural(self):
		if re.findall('[-+]?[0-9]+', self.curr_token.lexeme) != []:
			return re.findall('[-+]?[0-9]+', self.curr_token.lexeme)[0] == self.curr_token.lexeme
		return False


	# returns true the current token integer is a bool_literal
	# returns false otherwise
	def validate_bool(self):

		# match either True or False case sensitive that does
		# not have an alphanumeric character or underscore in front
		# or behind it
		bool_literal_regex = "((?<![a-zA-Z0-9_])True(?![a-zA-Z0-9_])|" +\
		 "(?<![a-zA-Z0-9_])False(?![a-zA-Z0-9_]))"

		if re.findall(bool_literal_regex, self.curr_token.lexeme) != []:
			return re.findall(bool_literal_regex, self.curr_token.lexeme)[0] == self.curr_token.lexeme
		return False


	# returns true the current token integer is a char_literal
	# returns false otherwise
	def validate_char(self):
		if re.findall("'\\\\?[ -~]'", self.curr_token.lexeme) != []:
			return re.findall("'\\\\?[ -~]'", self.curr_token.lexeme)[0] == self.curr_token.lexeme
		return False


	# returns true the current token integer is a String_literal
	# returns false otherwise
	def validate_string(self):
		if re.findall("\'(\\\\.|[^\'\\\\])*\'", self.curr_token.lexeme) != []:
			return re.search("\'(\\\\.|[^\'\\\\])*\'", self.curr_token.lexeme)[0] == self.curr_token.lexeme
		return False



	'''
	- GRAMMAR RULES -

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
	<term>           -->  <exp> {'*'|'/' <exp>}
	<exp>            -->  <logical> {'^' <logical>}
	<logical>        -->  <factor> {'~'|'&'|'|' <factor>}
	<factor>         -->  [a-zA-Z_][a-zA-Z0-9_]* | [-+]?[0-9]*[.][0-9]+ | [-+]?[0-9]+ | 
	                      ((?<![a-zA-Z0-9_])True(?![a-zA-Z0-9_])|(?<![a-zA-Z0-9_])False(?![a-zA-Z0-9_]))
						  | '[ -~]' | \'(\\\\.|[^\'\\\\])*\' | '(' <bool_relation> ')'
						  | [a-zA-Z_][a-zA-Z0-9_]* '(' {[a-zA-Z_][a-zA-Z0-9_]* ','} ')'

	'''


	#<start>  -->  {<statement>}
	def start(self, parent):

		this_parse = Parse_Tree("start", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		while self.curr_token.lexeme in ['{', 'if', 'while', 'String', 'int', 'char', \
		'float', 'bool', 'def'] or self.validate_var() and self.index < len(self.tokens) -1:
			self.statement(this_parse)


	# <statment>  -->  <block> | <selection> | <while_loop> | <declaration> | <assignment>
	def statement(self, parent):

		this_parse = Parse_Tree("statement", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		# test for block statement
		if self.curr_token.lexeme == "{":
			self.block(this_parse)

		# test for if statement
		elif self.curr_token.lexeme == "if":
			self.selection(this_parse)

		# test for while loop
		elif self.curr_token.lexeme == "while":
			self.while_loop(this_parse)

		# test for String
		elif self.curr_token.lexeme in ['String', 'int', 'char', \
		'float', 'bool', 'def']:
			self.declaration(this_parse)

		# test for a valid variable name
		elif self.validate_var():
			self.assignment(this_parse)

		# throw error
		else:
			self.error()


	# <block>  -->  '{' <start> '}'
	def block(self, parent):

		this_parse = Parse_Tree("block", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		if self.curr_token.lexeme == "{":
			self.next_token(this_parse)
			self.start(this_parse)

			if self.curr_token.lexeme == '}':
				self.next_token(this_parse)

			else:
				self.error()
		else:
			self.error()


	# <selection>  -->  'if' '(' <bool_relation> ')' '{' <start> '}' [<else_statement>|<elif_statement>]
	def selection(self, parent):

		this_parse = Parse_Tree("selection", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		if self.curr_token.lexeme == 'if':
			self.next_token(this_parse)

			if self.curr_token.lexeme == "(":
				self.next_token(this_parse)
				self.bool_relation(this_parse)

				if self.curr_token.lexeme == ")":
					self.next_token(this_parse)

					if self.curr_token.lexeme == "{":
						self.next_token(this_parse)
						self.start(this_parse)

						if self.curr_token.lexeme == "}":
							self.next_token(this_parse)

							if self.curr_token.lexeme == "else":
								self.else_statement(this_parse)

							elif self.curr_token.lexeme == "elif":
								self.elif_statement(this_parse)

						else:
							self.error()
					else:
						self.error()
				else:
					self.error()
			else:
				self.error()
		else:
			self.error()


	# <while_loop>  -->  'while' '(' <bool_relation> ')' '{' <start> '}'
	def while_loop(self, parent):

		this_parse = Parse_Tree("while_loop", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		if self.curr_token.lexeme == "while":
			self.next_token(this_parse)

			if self.curr_token.lexeme == "(":
				self.next_token(this_parse)
				self.bool_relation(this_parse)

				if self.curr_token.lexeme == ")":
					self.next_token(this_parse)

					if self.curr_token.lexeme == "{":
						self.next_token(this_parse)
						self.start(this_parse)

						if self.curr_token.lexeme == "}":
							self.next_token(this_parse)

						else:
							self.error()
					else:
						self.error()
				else:
					self.error()
			else:
				self.error()
		else:
			self.error()


	# <declaration>  -->  <var_declare> | <func_declare>
	def declaration(self, parent):

		this_parse = Parse_Tree("declaration", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		# test for var declaration
		if self.curr_token.lexeme in ['String', 'int', 'char', \
		'float', 'bool']:
			self.var_declare(this_parse)

		# test for func declaration
		elif self.curr_token.lexeme == "def":
			self.func_declare(this_parse)

		# throw error
		else:
			self.error()


	# <assignment>  -->  [a-zA-Z_][a-zA-Z0-9_]* '=' <bool_relation>
	def assignment(self, parent):

		this_parse = Parse_Tree("assignment", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		if self.validate_var():
			self.next_token(this_parse)

			if self.curr_token.lexeme == '=':
				self.next_token(this_parse)
				self.bool_relation(this_parse)

			else:
				self.error()
		else:
			self.error()


	# <bool_relation>  -->  <bool_expr> {'!=='|'==' <bool_expr>}
	def bool_relation(self, parent):

		this_parse = Parse_Tree("bool_relation", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		self.bool_expr(this_parse)
		while self.curr_token.lexeme in ['!==', '==']:
			self.next_token(this_parse)
			self.bool_expr(this_parse)


	# <else_statement>  -->  'else' '{' <start> '}'
	def else_statement(self, parent):

		this_parse = Parse_Tree("else_statement", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		if self.curr_token.lexeme == "else":
			self.next_token(this_parse)

			if self.curr_token.lexeme == "{":
				self.next_token(this_parse)
				self.start(this_parse)

				if self.curr_token.lexeme == "}":
					self.next_token(this_parse)

				else:
					self.error()
			else:
				self.error()
		else:
			self.error()


	# <elif_statement>  -->  'elif' '(' <bool_relation> ')' '{' <start> '}' [<else_statement>|<elif_statement>]
	def elif_statement(self, parent):

		this_parse = Parse_Tree("elif_statement", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		if self.curr_token.lexeme == "elif":
			self.next_token(this_parse)

			if self.curr_token.lexeme == "(":
				self.next_token(this_parse)
				self.bool_relation(this_parse)

				if self.curr_token.lexeme == ")":
					self.next_token(this_parse)

					if self.curr_token.lexeme == "{":
						self.next_token(this_parse)
						self.start(this_parse)

						if self.curr_token.lexeme == "}":
							self.next_token(this_parse)

							if self.curr_token.lexeme == "else":
								self.else_statement(this_parse)

							elif self.curr_token.lexeme == "elif":
								self.elif_statement(this_parse)

						else:
							self.error()
					else:
						self.error()
				else:
					self.error()
			else:
				self.error()
		else:
			self.error()


	# <var_declare>  -->  ('String'|'int'|'char'|'float'|'bool') [a-zA-Z_][a-zA-Z0-9_]*
	def var_declare(self, parent):

		this_parse = Parse_Tree("var_declare", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		if self.curr_token.lexeme in ['String', 'int', 'char', \
		'float', 'bool']:
			self.next_token(this_parse)

			if self.validate_var():
				self.next_token(this_parse)

			else:
				self.error()
		else:
			self.error()


	# <func_declare>  -->  'def' [a-zA-Z_][a-zA-Z0-9_]* '(' {[a-zA-Z_][a-zA-Z0-9_]* ','} ')'
	# 				       '{' <start> '}'
	def func_declare(self, parent):

		this_parse = Parse_Tree("func_declare", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		if self.curr_token.lexeme == "def":
			self.next_token(this_parse)

			if self.validate_var():
				self.next_token(this_parse)

				if self.curr_token.lexeme == "(":
					self.next_token(this_parse)

					while self.validate_var():
						self.next_token(this_parse)

						if self.curr_token.lexeme == ',':
							self.next_token(this_parse)

						else:
							self.error()

					if self.curr_token.lexeme == ')':
						self.next_token(this_parse)

						if self.curr_token.lexeme == "{":
							self.next_token(this_parse)
							self.start(this_parse)

							if self.curr_token.lexeme == "}":
								self.next_token(this_parse)

							else:
								self.error()
						else:
							self.error()
					else:
						self.error()
				else:
					self.error()
			else:
				self.error()
		else:
			self.error()


	# <bool_expr>  -->  <expr> {'<=='|'>=='|'<'|'>' <expr>}
	def bool_expr(self, parent):

		this_parse = Parse_Tree("bool_expr", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		self.expr(this_parse)
		while self.curr_token.lexeme in ['<==', '>==', '<', '>']:
			self.next_token(this_parse)
			self.expr(this_parse)


	# <expr>  -->  <term> {'+'|'-' <term>}
	def expr(self, parent):

		this_parse = Parse_Tree("expr", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		self.term(this_parse)
		while self.curr_token.lexeme in ['+', '-']:
			self.next_token(this_parse)
			self.term(this_parse)

			
	# <term>  -->  <exp> {'*'|'/' <exp>}
	def term(self, parent):

		this_parse = Parse_Tree("term", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		self.exp(this_parse)
		while self.curr_token.lexeme in ['*', '/']:
			self.next_token(this_parse)
			self.exp(this_parse)

			
	# <exp>  -->  <logical> {'^' <logical>}
	def exp(self, parent):

		this_parse = Parse_Tree("exp", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		self.logical(this_parse)
		while self.curr_token.lexeme == '^':
			self.next_token(this_parse)
			self.logical(this_parse)

			
	# <logical>  -->  <factor> {'~'|'&'|'|' <factor>}
	def logical(self, parent):

		this_parse = Parse_Tree("logical", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		self.factor(this_parse)
		while self.curr_token.lexeme in ['~', '&', '|']:
			self.next_token(this_parse)
			self.factor(this_parse)


	# <factor>  -->  [-+]?[a-zA-Z_][a-zA-Z0-9_]* | [-+]?[0-9]*[.][0-9]+ | [-+]?[0-9]+ | 
	#                ((?<![a-zA-Z0-9_])True(?![a-zA-Z0-9_])|(?<![a-zA-Z0-9_])False(?![a-zA-Z0-9_]))
	#                | '[ -~]' | \'(\\\\.|[^\'\\\\])*\' | '(' <bool_relation> ')'
	#                | [-+]?[a-zA-Z_][a-zA-Z0-9_]* '(' {[-+]?[a-zA-Z_][a-zA-Z0-9_]* ','} ')'
	def factor(self, parent):

		this_parse = Parse_Tree("factor", [self.curr_token.lexeme])
		parent.add_child(this_parse)
		self.curr_parse = this_parse

		if self.validate_real() or self.validate_natural() \
		or self.validate_bool() or self.validate_char()	or self.validate_string()\
		or self.curr_token.lexeme in ['!', '~']:

			if self.curr_token.lexeme in ['!', '~']:
				self.next_token(this_parse)
			self.next_token(this_parse)

		elif self.curr_token.lexeme == "(":
			self.next_token(this_parse)
			self.bool_relation(this_parse)

			if self.curr_token.lexeme == ")":
				self.next_token(this_parse)

			else:
				self.error()

		elif self.validate_var() or self.curr_token.lexeme in ['-','+']:
			if self.curr_token.lexeme in ['-','+']:
				self.next_token(this_parse)
			self.next_token(this_parse)

			if self.curr_token.lexeme == "(":
				self.next_token(this_parse)

				while self.validate_var():
					self.next_token(this_parse)

					if self.curr_token.lexeme == ',':
						self.next_token(this_parse)

					else:
						self.error()

				if self.curr_token.lexeme == ")":
					self.next_token(this_parse)

				else:
					self.error()
		else:
			self.error()

			