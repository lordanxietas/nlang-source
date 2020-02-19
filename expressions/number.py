from nobject import *
class NumberExpression(object):
    def __init__(self, value):
        if '.' in str(value):
            self.value = float(value)
        else:
            self.value = int(value)
    def eval(self, vm):
        return NObject(self.value)
    
    def __repr__(self):
        return str(self.value)