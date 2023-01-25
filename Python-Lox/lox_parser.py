from scanner import Token, TokenType
from statement import *
import grammar

class ParseError(Exception):
    """Raised for unexpected token"""

class Parser:
    def __init__(self, token_list: list[Token], interpreter) -> None:
        self.tokens = token_list
        self._interpreter = interpreter
        self._current = 0

    def parse(self):
        try:
            statements = []
            while not self.is_at_end():
                statements.append(Stmt())
            return statements
        except ParseError as error:
            return None

    def is_at_end(self) -> bool:
        """Checks if next token is EOF"""
        return self._peek().type == TokenType.EOF

    def _match(self, *token_types: TokenType) -> bool:
        for token in token_types:
            if self._check(token):
                self._advance()
                return True

        return False

    def _check(self, token_type: TokenType) -> bool:
        """
        Checks if current token matches a given type
        Does not consume the current token
        """
        if self.is_at_end():
            return False
        return self._peek(token_type) == token_type

    def _peek(self) -> Token:
        """
        Checks token at next position without incrementing self._current
        """
        return self.tokens[self._current]

    def _previous(self) -> Token:
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
    
    def _statement(self):
        if self._match(TokenType.PRINT):
            return self._printStatement()

        return self._expressionStatement()

    def _printStatement(self):
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def _expressionStatement(self):
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)
        
    # Binary operator methods
    def _equality(self):
        """
        Matches based on the grammar rule
        equality -> comparison ( ( "!=" |  "==" ) )*
        """
        expr = self._comparison()

        # Checking for equality operators
        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = grammar.Binary(expr, operator, right)

        return expr

    def _comparison(self):
        expr = self._term()

        # Matching for any comparison operator
        while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self._previous()
            right = self._term()
            expr = grammar.Binary(expr, operator, right)

        return expr

    def _term(self):
        expr = self._factor()

        # Matching for addition and subtraction tokens
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous()
            right = self._factor()
            expr = grammar.Binary(expr, operator, right)

        return expr

    def _factor(self):
        expr = self._unary()

        # Matching for multiplication and division
        while self._match(TokenType.SLASH, TokenType.STAR):
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
        if self._match(TokenType.BANG, TokenType.MINUS):
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
        if self._match(TokenType.FALSE):
            return grammar.Literal(False)
        if self._match(TokenType.TRUE):
            return grammar.Literal(True)
        if self._match(TokenType.NIL):
            return grammar.Literal(None)

        # Checking for string or number literals
        if self._match(TokenType.NUMBER, TokenType.STRING):
            return grammar.Literal(self._previous().literal)

        # Checking for parenthesized expressions
        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            # Consume tokens until finding right parenthesis
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
            return grammar.Grouping(expr)

    def _consume(self, token_type: TokenType, msg: str):
        """
        Consumes next token if it is the provided type
        Raises an error otherwise
        """
        if self._check(token_type):
            return self._advance()

        raise self._error(self._peek(), msg)

    def _error(self, token: Token, msg: str) -> ParseError:
        self._interpreter.error()
        return ParseError()

    def _synchronize(self):
        self._advance()

        while not self.is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return None

            token_type = self._peek().type
            match token_type:
                case TokenType.CLASS:
                    return None
                case TokenType.FUN:
                    return None
                case TokenType.VAR:
                    return None
                case TokenType.FOR:
                    return None
                case TokenType.IF:
                    return None
                case TokenType.WHILE:
                    return None
                case TokenType.PRINT:
                    return None
                case TokenType.RETURN:
                    return None
            
            self._advance()