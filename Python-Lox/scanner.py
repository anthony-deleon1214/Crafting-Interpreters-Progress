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
        while not self._is_at_eof():
            self._start = self._current
            self._scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, len(self._line)))
        return self.tokens

    def _scanToken(self) -> None:
        """
        Arguments are stored in Scanner class instance
        Switch statement to add each token to self.tokens
        """
        char = self._advance()
        match char:
            # Handling single character lexemes
            case '(':
                self._addToken(TokenType.LEFT_PAREN)
            case ')':
                self._addToken(TokenType.RIGHT_PAREN)
            case '{':
                self._addToken(TokenType.LEFT_BRACE)
            case '}':
                self._addToken(TokenType.RIGHT_BRACE)
            case ',':
                self._addToken(TokenType.COMMA)
            case '.':
                self._addToken(TokenType.DOT)
            case '-':
                self._addToken(TokenType.MINUS)
            case '+':
                self._addToken(TokenType.PLUS)
            case ';':
                self._addToken(TokenType.SEMICOLON)
            case '*':
                self._addToken(TokenType.STAR)

            # Handling potentially double character lexemes
            case '!':
                self._addToken(TokenType.BANG_EQUAL if self._match('=') else TokenType.BANG)
            case '=':
                self._addToken(TokenType.EQUAL_EQUAL if self._match('=') else TokenType.EQUAL)
            case '<':
                self._addToken(TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS)
            case '>':
                self._addToken(TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER)

            # Logic for ignoring parsing of comments
            case '/':
                if self._match('/'):
                    while self._peek() != '\n' and not self._is_at_eof():
                        self._advance()
                else:
                    self._addToken(TokenType.SLASH)
            
            # Handling whitespace characters
            case ' ':
                None
            case '\r':
                None
            case '\t':
                None
            case '\n':
                self._line += 1

            # Processing literals
            case '"':
                self._addToken(TokenType.STRING)

            # Error in default case
            case _:
                Lox.error(self._line, "Unexpected character")
            

    def _advance(self) -> str:
        self._current += 1
        return self.source[self._current-1]

    def _peek(self) -> str:
        """
        Checks the current character without advancing
        """
        if self._is_at_eof():
            return '\0'
        return self.source[self._current]

    def _addToken(self, tokenType: TokenType, literal:str = None) -> None:
        text = self.source[self._start:self._current]
        self.tokens.append(Token(tokenType, text, literal, self._line))

    def _match(self, expected):
        """
        Checks if the current character matches an expected character
        Returns False if at end of file or if character does not match
        Consumes current character and returns True otherwise
        """
        if self._is_at_eof():
            return False        
        elif self.source[self._current] != expected:
            return False
        
        self._current += 1
        return True
        
    def _is_at_eof(self):
        """
        Checks whether whole source file has been parsed
        """
        return (self._current >= len(self.source))