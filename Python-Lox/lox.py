import io
import sys
import scanner
import lox_parser
import interpreter

class Lox:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False
        self.interpreter = interpreter.Interpreter(self)

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
        if token.type == scanner.TokenType.EOF:
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

    def run(self, args: str):
        scan = scanner.Scanner(self, args)
        tokens = scan.scanTokens()
        parser = lox_parser.Parser(self, tokens)
        statements = parser.parse()

        if self.had_error:
            sys.exit(65)
        if self.had_runtime_error:
            sys.exit(70)
        
        self.interpreter.interpret(statements)

    def runtime_error(self, error):
        sys.stderr.write("[line " + error.token.line + "] " + error.message)
        self.had_runtime_error = True

if __name__ == "__main__":
    lox_test = Lox()
    user_input = input(">>>")
    while user_input != "exit":
        lox_test.run(user_input)
        user_input = input(">>>")