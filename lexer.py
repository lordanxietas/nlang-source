# from enum import Enum
from type import *
import re

class Lexer(object):
    def __init__(self):
        self.position = 0
    def tokenize(self, text):
        self.text = text + '\0'
        self.tokens = []
        while self.position < len(self.text):
            current = self.peek()
            if current.isdigit():
                self.tokenizeNumber()
            # elif re.match('\s{4}', self.text[(self.position - 1):(self.position - 1) + 4]):
            #     self.addToken(INDENT, 'tab')
            #     for i in range(0, 4):
            #         self.next()
            elif re.match('\t', current):
                self.addToken(INDENT, 'tab')
                self.next()
            elif current in ['"', '`', "'"]:
                self.next()
                self.tokenizeString(current)
            elif re.match('\w|_', current):
                self.tokenizeVariable(current)
            elif current in OPERATOR_CHARS:
                self.tokenizeOperator()
            else:
                self.next()
        return self.tokens
    def tokenizeNumber(self):
        number = str()
        current = self.peek(0)
        while current.isdigit() or (current == '.' and self.peek(1).isdigit()):
            number += current
            current = self.next()
        self.addToken(NUM, number)
    def tokenizeString(self, first):
        strval = str()
        current = self.peek()
        while current != first:
            strval += current
            current = self.next()
        self.next()
        self.addToken(STRING, strval)
    def tokenizeVariable(self, first):
        variable = str()
        current = self.peek()
        while re.match('\w|_', current):
            variable += current
            current = self.next()
        kwd = self.keyword(variable)
        if not kwd:
            self.addToken(VARIABLE, variable)
        else:
            self.addToken(kwd, str(variable))
    def tokenizeOperator(self):
        op = self.peek()
        self.next()
        self.addToken(operator(op), op)
    def keyword(self, name):
        return KEYWORDS.get(name, False)
    def addToken(self, type, text):
        self.tokens.append(Token(type, text))
    def peek(self, relativePosition=0):
        position = int(self.position + relativePosition)
        if not (position < len(self.text)):
            return None
        return self.text[position]
    def next(self):
        self.position += 1
        return self.peek(0)