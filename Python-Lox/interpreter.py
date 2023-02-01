import grammar
import scanner
import numbers
import statement
from environment import Environment

class LoxRuntimeError(Exception):
    """
    Raised to denote runtime errors
    """
    def __init__(self, token: scanner.Token, message: str):
        self._message = message
        self._token = token

def stringify(obj: object) -> str:
    if obj is None:
        return "nil"

    if isinstance(obj, numbers.Number):
        text = str(obj)
        if text.endswith(".0"):
            text = text[0:len(text)-2]
        return text

    return str(obj)

def concatOrAdd(left, right, operator):
    """
    Checks the types of the left and right operands
    Adds them if they are numbers
    Concatenates them if they are strings
    """
    if isinstance(left.value, numbers.Number) and isinstance(right.value, numbers.Number):
        return float(left.value) + float(right.value)
    elif isinstance(left.value, str) and isinstance(right.value, str):
        return str(left.value) + str(right.value)
    else:
        raise LoxRuntimeError(operator, "Operands must both be either strings or numbers")

def isEqual(left, right) -> bool:
    """
    Checks if two values are equal
    """
    if left is None and right is None:
        return True
    elif left is None:
        return False
    
    return left == right

def isTrue(obj):
    """
    Returns False if obj is None or False, True otherwise
    """
    if obj is None:
        return False
    elif isinstance(obj, bool):
        return bool(obj)
    else:
        return True

def checkNumberOperand(operator: scanner.Token, right: grammar.Expression):
    if isinstance(right.value, numbers.Number):
        return
    raise LoxRuntimeError(operator, "Operand must be a number")

def checkNumberOperands(left, operator, right):
    if isinstance(left.value, numbers.Number) and isinstance(right.value, numbers.Number):
        return
    else:
        raise LoxRuntimeError(operator, "Operands must both be numbers")

class Interpreter():
    def __init__(self, interpreter) -> None:
        """
        Must pass Lox instance as interpreter argument
        Lox instance is required for error handling
        """
        self._interpreter = interpreter
        self.environment = Environment()

    def interpret(self, stmts: list[statement.Stmt]):
        try:
            for stmt in stmts:
                self._execute(stmt)
        except LoxRuntimeError as error:
            self._interpreter.runtime_error(error)

    def _evaluate(self, expr: grammar.Expression):
        return expr.accept(self)

    def _execute(self, stmt: statement.Stmt):
        stmt.accept(self)

    def visitExpression(self, stmt: statement.Expression) -> None:
        self._evaluate(stmt.expression)
        return None

    def visitPrint(self, stmt: statement.Print) -> None:
        value = self._evaluate(stmt.expression)
        print(stringify(value))
        return None

    def visitLiteral(self, expr: grammar.Literal):
        return expr.value

    def visitGrouping(self, expr: grammar.Grouping):
        return self._evaluate(expr.expression)

    def visitUnary(self, expr: grammar.Unary):
        right = self._evaluate(expr.right)
        
        match expr.operator.type:
            case scanner.TokenType.MINUS:
                checkNumberOperand(expr.operator)
                return -float(right)
            case scanner.TokenType.BANG:
                return isTrue(right)

        return None

    def visitBinary(self, expr: grammar.Binary):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        match expr.operator.type:
            case scanner.TokenType.MINUS:
                checkNumberOperands(expr.left, expr.operator, expr.right)
                return float(left) - float(right)
            case scanner.TokenType.SLASH:
                checkNumberOperands(expr.left, expr.operator, expr.right)
                return float(left)/float(right)
            case scanner.TokenType.STAR:
                checkNumberOperands(expr.left, expr.operator, expr.right)
                return float(left)*float(right)
            # Lox comparison operators only accept numbers
            case scanner.TokenType.GREATER:
                checkNumberOperands(expr.left, expr.operator, expr.right)
                return float(left) > float(right)
            case scanner.TokenType.GREATER_EQUAL:
                checkNumberOperands(expr.left, expr.operator, expr.right)
                return float(left) >= float(right)
            case scanner.TokenType.LESS:
                checkNumberOperands(expr.left, expr.operator, expr.right)
                return float(left) < float(right)
            case scanner.TokenType.LESS_EQUAL:
                checkNumberOperands(expr.left, expr.operator, expr.right)
                return float(left) <= float(right)
            case scanner.TokenType.EQUAL_EQUAL:
                return isEqual(left, right)
            case scanner.TokenType.BANG_EQUAL:
                return left != right
            case scanner.TokenType.PLUS:
                return concatOrAdd(expr.left, expr.right, expr.operator)

        return None

    def visitVariableStmt(self, stmt: statement.VariableStmt) -> None:
        value = None
        if stmt.initializer is not None:
            value = self._evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)
        return None

    def visitVariableExpr(self, expr: grammar.VariableExpr) -> None:
        return self.environment.get(expr.name)

    def visitAssignExpr(self, expr: grammar.Assign) -> object:
        value = self._evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value