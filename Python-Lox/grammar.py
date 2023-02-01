import scanner

class Expression:
	pass

class Chain(Expression):
	def __init__(self, left, Expression, right):
		self.left = left
		self.Expression, right = Expression, right

	def accept(self, visitor):
		return visitor.visitChain(self)

class Unary(Expression):
	def __init__(self, operator, right):
		self.operator = operator
		self.right = right

	def accept(self, visitor):
		return visitor.visitUnary(self)

class Binary(Expression):
	def __init__(self, left, operator, right):
		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor):
		return visitor.visitBinary(self)

class Grouping(Expression):
	def __init__(self, expression):
		self.expression = expression

	def accept(self, visitor):
		return visitor.visitGrouping(self)

class Literal(Expression):
	def __init__(self, value):
		self.value = value

	def accept(self, visitor):
		return visitor.visitLiteral(self)

class VariableExpr(Expression):
	def __init__(self, name):
		self.name = name

	def accept(self, visitor):
		return visitor.visitVariableExpr(self)

class Assign(Expression):
	def __init__(self, name, value):
		self.name = name
		self.value = value

	def accept(self, visitor):
		return visitor.visitAssign(self)
