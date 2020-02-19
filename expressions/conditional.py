from type import *
from nobject import *
class ConditionalExpression(object):
    
    def __init__(self, type, first, second):
        self.type = type
        self.first = first
        self.second = second
    
    def eval(self, vm):
        first = self.first.eval(vm)
        if type(first) == NObject:
            first = first.nval()
        
        second = self.second.eval(vm)
        if type(second) == NObject:
            second = second.nval()

        if self.type == LT:
            return NObject(first < second)
        elif self.type == GT:
            return NObject(first > second)
        elif self.type == GTEQ:
            return NObject(first >= second)
        elif self.type == LTEQ:
            return NObject(first <= second)
        elif self.type == EXCLEQ:
            return NObject(first != second)
        elif self.type == EQEQ:
            return NObject(first == second)
        elif self.type == AMPAMP:
            return NObject(bool(first and second))
        elif self.type == BARBAR:
            return NObject(bool(first or second))

class ExcludeExpression(object):
    def __init__(self, expr):
        self.expr = expr
    def eval(self, vm):
        res = self.expr.eval(vm)
        if type(res) == NObject:
            res = res.nval()
        return bool(res == False)