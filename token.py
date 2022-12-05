class Token:
	def __init__(self, lexeme, code):
		self.lexeme = lexeme or ""
		self.code = code or -1
