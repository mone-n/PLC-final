import re

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
			5 : "if statement",
			6 : "else statement",
			7 : "elif statement",
			8 : "for loop",
			9 : "while loop",
			10: "String loop",
			11: "int loop",
			12: "char loop",
			13: "float loop",
			14: "boolean",
			15: "variable or function identifier"
		}

		self.tokenize()

	def tokenize(self):

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
		char_literal_regex = "('[ -~]')"

		# match a series of non ' characters while
		# disallowing \ characters without an escaped
		# character after it. between two ' characters
		string_literal_regex = "(\'(\\\\.|[^\'\\\\])*\')"

		# build regex patterns for keywords
		keyword_regex = ["if","else","elif","for","while",\
		"String","int","char","float","bool"]

		# prepend and append a lookahead and lookbehind
		# to make sure the keyword doesnt have a character
		# before or after it, making it a variable.
		for i in range(len(keyword_regex)):
			keyword_regex[i] = "((?<![a-zA-Z0-9_])" + keyword_regex[i] + "(?![a-zA-Z0-9_]))"
		keyword_regex = "|".join(keyword_regex)

		special_symbols_regex = "(\+)|(\-)|(\*)|(\/)|(\^)|(\()|(\))|(\>)|" +\
		"(\<)|(\>\=\=)|(\<\=\=)|()"

		# variable or function name without a leading number.
		var_func_identifier_regex = "([a-zA-Z_][a-zA-Z0-9_]*)"



		overall_regex  = real_literal_regex
		overall_regex += "|" + natural_literal_regex
		overall_regex += "|" + char_literal_regex
		overall_regex += "|" + string_literal_regex
		overall_regex += "|" + keyword_regex
		overall_regex += "|" + bool_literal_regex
		overall_regex += "|" + var_func_identifier_regex

		match = re.match(overall_regex, self.code_raw)

		lexeme_index = 0

		while match is not None and match[0]:

			self.code_raw = self.code_raw.replace(match[0], '', 1)

			self.code_raw = self.code_raw.lstrip()

			self.tokens.append(match[0])

			# print(match)
			# print(match.groups())

			print("Lexeme at index {:2d} is: {:10s}Token is ({:2d}) {:s}".format(
				lexeme_index,
				match[0],
				match.groups().index(match[0]),
				self.token_definitions[match.groups().index(match[0])]
				)
			)

			lexeme_index += 1

			match = re.match(overall_regex, self.code_raw)


