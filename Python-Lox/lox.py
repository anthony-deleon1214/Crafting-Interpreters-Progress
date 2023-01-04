import argparse
import io
import sys

class Lox:
    def __init__(self, args) -> None:
        if len(args) > 1:
            print("Error: too many arguments")
        elif len(args) == 1:
            self.runFile(args[0])
        else:
            self.runPrompt()

    def runFile(self, path):
        with open(path, 'rb') as file:
            contents = file.read()
        self.run(contents)

    def error(self, line, message):
        pass

    def runPrompt(self):
        input = io.BufferedReader

        while True:
            print("> ")
            line = input()
            if line == None:
                break
            self.run(line)

    def run(self, *args):
        scanner = Scanner(args)
        tokens = scanner.scanTokens()

class Scanner:
    def __init__(self, source):
        self.source = source

    def scanTokens(self) -> list:
        