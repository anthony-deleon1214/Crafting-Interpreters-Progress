import grammar
import scanner
import numbers

class LoxRuntimeError(Exception):
    """
    Raised to denote runtime errors
    """
    def __init__(self, token: scanner.Token, message: str):
        self._message = message
        self._token = token

def concatOrAdd(left, right, operator):
    """
    Checks the types of the left and right operands
    Adds them if they are numbers
    Concatenates them if they are strings
    """
    if left.isinstance(numbers.Number) and right.isinstance(numbers.Number):
        return float(left) + float(right)
    elif left.isinstance(str) and right.isinstance(str):
        return str(left) + str(right)
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
    elif obj.isinstance(bool):
        return bool(obj)
    else:
        return True

class Interpreter():
    def __init__(self, lox) -> None:
        self._lox = lox

    def _evaluate(self, expr: grammar.Expression):
        return expr.accept(self)

    def visitLiteral(self, expr: grammar.Literal):
        return expr.value

    def visitGrouping(self, expr: grammar.Grouping):
        return self._evaluate(expr.expression)

    def visitUnary(self, expr: grammar.Unary):
        right = self._evaluate(expr.right)
        
        match expr.operator.token_type:
            case scanner.TokenType.MINUS:
                return -float(right)
            case scanner.TokenType.BANG:
                return isTrue(right)

        return None

    def visitBinary(self, expr: grammar.Binary):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        match expr.operator.token_type:
            case scanner.TokenType.MINUS:
                return float(left) - float(right)
            case scanner.TokenType.SLASH:
                return float(left)/float(right)
            case scanner.TokenType.STAR:
                return float(left)*float(right)
            # Lox comparison operators only accept numbers
            case scanner.TokenType.GREATER:
                return float(left) > float(right)
            case scanner.TokenType.GREATER_EQUAL:
                return float(left) >= float(right)
            case scanner.TokenType.LESS:
                return float(left) < float(right)
            case scanner.TokenType.LESS_EQUAL:
                return float(left) <= float(right)
            case scanner.TokenType.EQUAL_EQUAL:
                return isEqual(left, right)
            case scanner.TokenType.BANG_EQUAL:
                return left != right

        return None