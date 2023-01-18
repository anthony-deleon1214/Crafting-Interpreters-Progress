import argparse
import scanner
import io
import sys
import lox_parser

class Lox:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False        

    def runFile(self, path):
        with open(path, 'rb') as file:
            contents = file.read()
        self.run(contents)
        if self.hadError:
            sys.exit(1)

    def error(self, line, message):
        self.report(line, "", message)

    def parse_error(self, token: scanner.Token, msg: str):
        if token.token_type == scanner.TokenType.EOF:
            self.report(token.line, "at end", msg)
        else:
            self.report(token.line, " at '" + token.lexeme + "'", msg)

    def report(self, line, where, message):
        self.hadError = True
        sys.stderr.write("[line " + line + "] Error" + where + ": " + message)

    def runPrompt(self):
        input = io.BufferedReader

        while True:
            print("> ")
            line = input()
            if line == None:
                break
            self.run(line)
            self.hadError = False

    def run(self, *args):
        scanner = scanner(args)
        tokens = scanner.scanTokens()
        parser = lox_parser.Parser(tokens)
        expression = parser.parse()

        # Need to finish interpreter functionality

        for token in tokens:
            print(token)

    def runtime_error(self, error):
        pass