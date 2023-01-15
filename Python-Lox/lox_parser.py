import scanner
import grammar
import lox

class ParseError(Exception):
    """Raised for unexpected token"""

class Parser:
    def __init__(self, token_list: list[scanner.Token]) -> None:
        self.tokens = token_list
        self._interpreter = lox.Lox
        self._current = 0

    def parse(self):
        try:
            return self._expression()
        except ParseError as error:
            return None

    def is_at_end(self) -> bool:
        """Checks if next token is EOF"""
        return self._peek().type == scanner.TokenType.EOF

    def _match(self, *token_types: scanner.TokenType) -> bool:
        for token in token_types:
            if self._check(token):
                self._advance()
                return True

        return False

    def _check(self, token_type: scanner.TokenType) -> bool:
        """
        Checks if current token matches a given type
        Does not consume the current token
        """
        if self.is_at_end():
            return False
        return self._peek(token_type) == token_type

    def _peek(self) -> scanner.Token:
        """
        Checks token at next position without incrementing self._current
        """
        return self.tokens[self._current]

    def _previous(self) -> scanner.Token:
        """
        Returns previous token from self.tokens
        """
        return self.tokens[self._current - 1]

    def _advance(self) -> int:
        """
        Increments self._current
        Returns token at position before advancing
        """
        self._current += 1
        return self.tokens[self._current - 1]

    def _expression(self):
        return self._equality()

    # Binary operator methods
    def _equality(self):
        """
        Matches based on the grammar rule
        equality -> comparison ( ( "!=" |  "==" ) )*
        """
        expr = self._comparison()

        # Checking for equality operators
        while self._match(scanner.TokenType.BANG_EQUAL, scanner.TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = grammar.Binary(expr, operator, right)

        return expr

    def _comparison(self):
        expr = self._term()

        # Matching for any comparison operator
        while self._match(scanner.TokenType.GREATER, scanner.TokenType.GREATER_EQUAL, scanner.TokenType.LESS, scanner.TokenType.LESS_EQUAL):
            operator = self._previous()
            right = self._term()
            expr = grammar.Binary(expr, operator, right)

        return expr

    def _term(self):
        expr = self._factor()

        # Matching for addition and subtraction tokens
        while self._match(scanner.TokenType.PLUS, scanner.TokenType.MINUS):
            operator = self._previous()
            right = self._factor()
            expr = grammar.Binary(expr, operator, right)

        return expr

    def _factor(self):
        expr = self._unary()

        # Matching for multiplication and division
        while self._match(scanner.TokenType.SLASH, scanner.TokenType.STAR):
            operator = self._previous()
            right = self._unary()
            expr = grammar.Binary(expr, operator, right)

        return expr

    # Unary operator methods
    def _unary(self):
        """
        Check for unary operators (negations here)
        Return Unary syntax tree if found
        Call self._primary otherwise
        """
        if self._match(scanner.TokenType.BANG, scanner.TokenType.MINUS):
            operator = self._previous()
            right = self._unary()
            return grammar.Unary(operator, right)
        
        return self._primary()

    def _primary(self):
        """
        Checking for terminal expressions
        Returns Literal syntax tree node with corresponding Python type
        """
        # Check for boolean and null types
        if self._match(scanner.TokenType.FALSE):
            return grammar.Literal(False)
        if self._match(scanner.TokenType.TRUE):
            return grammar.Literal(True)
        if self._match(scanner.TokenType.NIL):
            return grammar.Literal(None)

        # Checking for string or number literals
        if self._match(scanner.TokenType.NUMBER, scanner.TokenType.STRING):
            return grammar.Literal(self._previous().literal)

        # Checking for parenthesized expressions
        if self._match(scanner.TokenType.LEFT_PAREN):
            expr = self._expression()
            # Consume tokens until finding right parenthesis
            self._consume(scanner.TokenType.RIGHT_PAREN, "Expected ')' after expression")
            return grammar.Grouping(expr)

    def _consume(self, token_type: scanner.TokenType, msg: str):
        """
        Consumes next token if it is the provided type
        Raises an error otherwise
        """
        if self._check(token_type):
            return self._advance()

        raise self._error(self._peek(), msg)

    def _error(self, token: scanner.Token, msg: str) -> ParseError:
        self._interpreter.error()
        return ParseError()

    def _synchronize(self):
        self._advance()

        while not self.is_at_end():
            if self._previous().type == scanner.TokenType.SEMICOLON:
                return None

            token_type = self._peek().type
            match token_type:
                case scanner.TokenType.CLASS:
                    return None
                case scanner.TokenType.FUN:
                    return None
                case scanner.TokenType.VAR:
                    return None
                case scanner.TokenType.FOR:
                    return None
                case scanner.TokenType.IF:
                    return None
                case scanner.TokenType.WHILE:
                    return None
                case scanner.TokenType.PRINT:
                    return None
                case scanner.TokenType.RETURN:
                    return None
            
            self._advance()