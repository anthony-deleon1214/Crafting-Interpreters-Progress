import scanner
import grammar

class ParseError(Exception):
    """Raised for unexpected token"""

class Parser:
    def __init__(self, token_list: list[scanner.Token]) -> None:
        self.tokens = token_list
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