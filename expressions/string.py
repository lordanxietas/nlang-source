from nobject import *
class StringExpression(object):
    def __init__(self, string):
        self.value = string.replace('\\n', '\n').replace('\\r', '\r').replace('\\t', '\t').replace('\\s', '\s')
    
    def eval(self, vm):
        return NObject(self.value)
    
    def __repr__(self):
        return str('"' + self.value + '"')