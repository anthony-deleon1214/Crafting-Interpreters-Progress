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

    def _match(self, *token_types: list[scanner.TokenType]) -> bool:
        for token in token_types:
            if self._check(token):
                self._advance()
                return True

        return False

    def _check(self, token_type: scanner.TokenType) -> bool:
        if self.tokens[self._current+1] == token_type:
            return True

    def _advance(self) -> int:
        self._current += 1
        return self._current

    def _expression(self):
        return self._equality()

    def _equality(self):
        expr = self._comparison()

        while self._match()