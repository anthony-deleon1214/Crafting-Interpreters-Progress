from scanner import *

class Environment:
    def __init__(self) -> None:
        """
        Initialize an empty dictionary for variable bindings
        """
        self.values = {}

    def define(self, name: str, value) -> None:
        """
        Creates a variable binding in self.values
        Does not check for existing bindings to allow redefining variables
        """
        self.values[name] = value

    def get(self, name: Token):
        """
        Checks self.values for a given identifier
        Returns bound value if found
        Raises RuntimeError otherwise
        """
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)

        raise RuntimeError(name, "Undefined variable '" + name.lexeme + "'.")

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        raise RuntimeError(name, "Undefined variable '" + name.lexeme + "'.")