import argparse
import scanner
import io
import sys

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
        scanner = Scanner(args)
        tokens = scanner.scanTokens()

        for token in tokens:
            print(token)