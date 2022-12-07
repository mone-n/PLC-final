
class Parse_Tree:
	def __init__(self, name="", tokens=[]):
		self.name = name
		self.tokens = tokens
		self.children = []
		self.parent = None

	# adds a child to the tree
	def add_child(self, child):
		self.child = child
		child.parent = self
		self.children.append(child)

	# get the depth of a node in the tree
	def get_depth(self):
		depth = 0
		p = self.parent
		while p:
			p = p.parent
			depth += 1
		return depth

	# prints tree, each space at the beginning of each
	# line denotes how deep this node is in the tree.
	def print_tree(self):
		print(' ' * self.get_depth(), end='')

		t_list = ""
		if len(self.tokens[1:]) > 0:
			t_list += " - tokens validated: " + ', '.join(self.tokens[1:])

		print("func: " + self.name + "()" + t_list)
		if self.children:
			for child in self.children:
				child.print_tree()