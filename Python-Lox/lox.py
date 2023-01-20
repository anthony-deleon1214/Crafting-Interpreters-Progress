import io
import sys
import scanner
import lox_parser
import interpreter

class Lox:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False
        self.interpreter = interpreter.Interpreter()
        self.scanner = scanner.Scanner()
        self.parser = lox_parser.Parser()

    def runFile(self, path):
        with open(path, 'rb') as file:
            contents = file.read()
        self.run(contents)
        if self.hadError:
            sys.exit(1)

    def error(self, line, message):
        self.report(line, "", message)

    def scan_error(self, line, msg):
        self.report(line, "", msg)

    def parse_error(self, token: scanner.Token, msg: str):
        if token.token_type == scanner.TokenType.EOF:
            self.report(token.line, "at end", msg)
        else:
            self.report(token.line, " at '" + token.lexeme + "'", msg)

    def runtime_error(self, error):
        sys.stderr.write(error.message + "\n[line " + error.token.line + "]")
        self.had_runtime_error = True

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
        scanner = scanner.Scanner(args)
        tokens = scanner.Scanner.scanTokens()
        parser = lox_parser.Parser(tokens)
        expression = parser.parse()

        if self.had_error:
            sys.exit(65)
        if self.had_runtime_error:
            sys.exit(70)
        
        self.interpreter.interpret(expression)

    def runtime_error(self, error):
        sys.stderr.write("[line " + error.token.line + "] " + error.message)
        self.had_runtime_error = True