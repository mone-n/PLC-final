from lexer import Lexer
from parser import Parser


class Compiler:
	def __init__(self, file):

		# take given FILE object and convert it to one string
		self.code_raw = file.read()

		# create a lexer with our file_string
		lexer = Lexer(self.code_raw)

		# attempt to tokenize the file_string
		if lexer.tokenize():
			tokens = lexer.tokens

			# if a file has tokens, attempt to parse it
			if tokens != []:
				parser = Parser(tokens)
				parser.start(parser.parse_tree)

				# print the parse tree to console
				parser.parse_tree.print_tree()

		# failed tokenization, print the location of the failed lexeme
		else:
			print("lexeme at index {:2d} is invalid\n".format(len(lexer.tokens)))


if __name__ == "__main__":
	file = open("test_file.txt", "r")
	compiler = Compiler(file)