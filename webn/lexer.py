from enum import Enum
from type import *
from exceptions import *
import re

class Lexer(object):
    def __init__(self):
        self.position = 0
    def tokenize(self, text):
        self.text = text + '\0'
        self.html = ''
        self.tokens = []
        self._started = False
        self._starts = 0
        
        while self.position < len(self.text):
            current = self.peek()
            if current == '<' and self.text[self.position + 1] == '?':
                if self._started:
                    raise LexerError('Парсинг языка N уже был запущен')
                if self.html != '':
                    self.addToken(HTML, self.html)
                    self.html = ''
                self.addToken(NLANGSTART, '<?')
                self.next()
                self.next()
                self._started = True
                self._starts += 1
                continue
            elif current == '?' and self.text[self.position + 1] == '>':
                if not self._started:
                    raise LexerError('Вы забыли закрыть тег')
                self.addToken(NLANGEND, '?>')
                self.next()
                self.next()
                self._started = False
                continue
            if not self._started:
                self.html += current
                self.next()
                continue
            if current.isdigit():
                self.tokenizeNumber()
            elif re.match('==', current + self.text[self.position + 1]):
                self.next();self.next();
                self.addToken(EQEQ, '==')
            elif re.match('>=', current + self.text[self.position + 1]):
                self.next();self.next();
                self.addToken(GTEQ, '>=')
            elif re.match('<=', current + self.text[self.position + 1]):
                self.next();self.next();
                self.addToken(LTEQ, '<=')
            elif re.match('!=', current + self.text[self.position + 1]):
                self.next();self.next();
                self.addToken(EXCLEQ, '!=')
            elif re.match('&&', current + self.text[self.position + 1]):
                self.next();self.next();
                self.addToken(AMPAMP, '&&')
            elif re.match('\|\|', current + self.text[self.position + 1]):
                self.next();self.next();
                self.addToken(BARBAR, '||')
            elif re.match('!=', current + self.text[self.position + 1]):
                self.next();self.next();
                self.addToken(EXCLEQ, '!=')
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
        if self.html != '':
            self.addToken(HTML, self.html)
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
            self.addToken(kwd, f'{variable}')
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