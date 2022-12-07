import re
from token import Token

class Lexer:
	def __init__(self, code_raw):
		self.code_raw = code_raw
		self.tokens = []
		self.token_definitions = {
			0 : "real_literal",
			1 : "natural_literal",
			2 : "bool_literal",
			3 : "char_literal",
			4 : "string_literal",
			5 : "string_literal",
			6 : "if statement",
			7 : "else statement",
			8 : "elif statement",
			9 : "while loop",
			10: "String declaration",
			11: "int declaration",
			12: "char declaration",
			13: "float declaration",
			14: "boolean declaration",
			15: "function declaration",
			16: "addition symbol",
			17: "subtraction symbol",
			18: "multiplication symbol",
			19: "division symbol",
			20: "exponentiation symbol",
			21: "left parentheses",
			22: "right parentheses",
			23: "greater than or equal too symbol",
			24: "less than or equal too symbol",
			25: "greater than symbol",
			26: "less than symbol",
			27: "equal too symbol",
			28: "not equal too symbol",
			29: "assignment symbol",
			30: "unary negation symbol",
			31: "logical not symbol",
			32: "logical and symbol",
			33: "logical or symbol",
			34: "left curly brace",
			35: "right curly brace",
			36: "parameter separator",
			37: "variable or function identifier"
		}


	def remove_comments(self):
		comment_regex = "('''[\\s\\S]*''')|(#.*)"
		self.code_raw = re.sub(comment_regex, '', self.code_raw)


	def tokenize(self):
		self.remove_comments()
		self.code_raw = self.code_raw.strip()

		# optional plus or minus, with an optional number ahead
		# of a decimal point with a number behind.
		real_literal_regex = "([-+]?[0-9]*[.][0-9]+)"

		# optional plus or minus, with a number behind it.
		natural_literal_regex = "([-+]?[0-9]+)"

		# match either True or False case sensitive that does
		# not have an alphanumeric character or underscore in front
		# or behind it
		bool_literal_regex = "((?<![a-zA-Z0-9_])True(?![a-zA-Z0-9_])|" +\
		 "(?<![a-zA-Z0-9_])False(?![a-zA-Z0-9_]))"

		# match a single character from ascii code for space
		# to the ascii code for tilde. between two ' characters
		char_literal_regex = "('\\\\?[ -~]')"

		# match a series of non ' characters while
		# disallowing \ characters without an escaped
		# character after it. between two ' characters
		string_literal_regex = "(\'(\\\\.|[^\'\\\\])*\')"

		# build regex patterns for keywords
		keyword_regex = ["if","else","elif","while",\
		"String","int","char","float","bool", "def"]

		# prepend and append a lookahead and lookbehind
		# to make sure the keyword doesnt have a character
		# before or after it, making it a variable.
		for i in range(len(keyword_regex)):
			keyword_regex[i] = "((?<![a-zA-Z0-9_])" + keyword_regex[i] + "(?![a-zA-Z0-9_]))"
		keyword_regex = "|".join(keyword_regex)

		# special symbols for math, boolean operations, code
		# separation, etc.
		special_symbols_regex = "(\+)|(\-)|(\*)|(\/)|(\^)|(\()|(\))|" +\
		"(\>\=\=)|(\<\=\=)|(\>)|(\<)|(\=\=)|(\!\=\=)|(\=)|(\~)|(\!)|(\&)|" +\
		"(\|)|(\{)|(\})|(\,)"

		# variable or function name without a leading number.
		var_func_identifier_regex = "([a-zA-Z_][a-zA-Z0-9_]*)"

		# combine all patterns into a master pattern
		overall_regex  = real_literal_regex
		overall_regex += "|" + natural_literal_regex
		overall_regex += "|" + bool_literal_regex
		overall_regex += "|" + char_literal_regex
		overall_regex += "|" + string_literal_regex
		overall_regex += "|" + keyword_regex
		overall_regex += "|" + special_symbols_regex
		overall_regex += "|" + var_func_identifier_regex

		# start lexeme indexing at 0
		lexeme_index = 0

		# re.match gets the first match in a string. so this gets
		# the first match
		match = re.match(overall_regex, self.code_raw)

		# individually read the next token and determine if it is a valid
		# token until EOF is reached.
		while match is not None and match[0]:

			self.code_raw = self.code_raw.replace(match[0], '', 1)
			self.code_raw = self.code_raw.lstrip()

			self.tokens.append(
				Token(
					match[0],
					match.groups().index(match[0])
				)
			)

			print("Lexeme at index {:2d} is: {:16s}Token is ({:2d}) {:s}".format(
				lexeme_index,
				match[0],
				match.groups().index(match[0]),
				self.token_definitions[match.groups().index(match[0])]
				)
			)

			lexeme_index += 1

			match = re.match(overall_regex, self.code_raw)

		# since re.match only matches at the beginning of a string
		# it will return null when an invalid token is processed,
		# and break the while loop above.
		# If the while loop condition fails early, a token at the
		# current index is invalid
		if len(self.code_raw) > 0:
			return False
		return True