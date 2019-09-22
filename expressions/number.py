from nobject import *
class NumberExpression(object):
    def __init__(self, value):
        self.value = float(value)
    
    def eval(self, vm):
        return NObject(self.value)
    
    def __repr__(self):
        return str(self.value)