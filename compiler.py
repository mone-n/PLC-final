from token import Token
from lexer import Lexer
# from syntax_analyzer import RDA

class Compiler:
	def __init__(self, code_raw):
		lexer = Lexer(code_raw)



if __name__ == "__main__":
	file = open("test_file.txt", "r")
	code_raw = file.read()
	compiler = Compiler(code_raw)