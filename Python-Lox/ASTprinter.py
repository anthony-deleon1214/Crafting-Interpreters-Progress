import scanner
import grammar

class AstPrinter():
    def printast(self, expression: grammar.Expression):
        return expression.accept(self)

    def parenthesize(self, name: str, *expressions: grammar.Expression) -> str:
        output_str = "(" + name

        for expression in expressions:
            output_str += " "
            output_str += expression.accept(self)

        output_str += ")"

        return output_str

    def visitChain(self, expression: grammar.Expression) -> str:
        return self.parenthesize("chain", expression.left, expression.right)

    def visitBinary(self, expression: grammar.Expression) -> str:
        return self.parenthesize(expression.operator.lexeme, expression.left, expression.right)

    def visitUnary(self, expression: grammar.Expression) -> str:
        return self.parenthesize(expression.operator.lexeme, expression.right)

    def visitGrouping(self, expression: grammar.Expression) -> str:
        return self.parenthesize("group", expression.expression)

    def visitLiteral(self, expression: grammar.Expression) -> str:
        return str(expression.value)

if __name__ == "__main__":
    expression = grammar.Binary(
        grammar.Unary(
            scanner.Token(scanner.TokenType.MINUS, "-", None, 1),
            grammar.Literal(123)),
        scanner.Token(scanner.TokenType.STAR, "*", None, 1),
        grammar.Grouping(
            grammar.Literal(45.67)
        )
    )
    print(AstPrinter().printast(expression))