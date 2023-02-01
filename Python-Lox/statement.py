import scanner

class Stmt:
	pass

class Expression(Stmt):
	def __init__(self, expression):
		self.expression = expression

	def accept(self, visitor):
		return visitor.visitExpression(self)

class Print(Stmt):
	def __init__(self, expression):
		self.expression = expression

	def accept(self, visitor):
		return visitor.visitPrint(self)

class VariableStmt(Stmt):
	def __init__(self, name, initializer):
		self.name = name
		self.initializer = initializer

	def accept(self, visitor):
		return visitor.visitVariableStmt(self)
