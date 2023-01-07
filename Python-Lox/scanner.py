from lox import Lox
from enum import Enum, auto

# Sum type for all accepted TokenTypes in Lox
class TokenType(Enum):
    # Single character tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    EOF = auto()

class Token():
    def __init__(self, type: TokenType, lexeme: str, literal: str, line: int) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return self.type + " " + self.lexeme + " " + self.literal

class Scanner():
    def __init__(self, source) -> None:
        self.source = source
        self.tokens = []
        self._start = 0
        self._current = 0
        self._line = 1

    def scanTokens(self) -> list:
        """
        Loops through each character in source file passed to Scanner instance at initialization
        Calls private helper method scanToken to parse individual tokens
        Appends an EOF (end of file) token to self.tokens
        Returns self.tokens list
        """
        for char in self.source:
            self._start = self._current
            self._scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self._line))
        return self.tokens

    def _scanToken(self):
        """
        Arguments are stored in Scanner class instance
        Switch statement to add each token to self.tokens
        """
        char = self._advance()
        match char:
            case '(':
                self.tokens.append(Token(TokenType.LEFT_PAREN, '(', '(', self._line))
            case ')':
                self.tokens.append(Token(TokenType.RIGHT_PAREN, ')', ')', self._line))
            case '{':
                self.tokens.append(Token(TokenType.LEFT_BRACE, '{', '{', self._line))
            case '}':
                self.tokens.append(Token(TokenType.RIGHT_BRACE, '}', '}', self._line))
            case ',':
                self.tokens.append(Token(TokenType.COMMA, ',', ',', self._line))
            case '.':
                self.tokens.append(Token(TokenType.DOT, '.', '.', self._line))
            case '-':
                self.tokens.append(Token(TokenType.MINUS, '-', '-', self._line))
            case '+':
                self.tokens.append(Token(TokenType.PLUS, '+', '+', self._line))
            case ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', ';', self._line))
            case '*':
                self.tokens.append(Token(TokenType.STAR, '*', '*', self._line))

            case _:
                Lox.error(self._line, "Unexpected character")
            

    def _advance(self):
        return self.source[self._current+1]