from type import *
from nobject import *
class BinaryExpression:
    def __init__(self, _type, expr1, expr2):
        self._type = _type
        self.expr1 = expr1
        self.expr2 = expr2
    def eval(self, vm):
        res1 = self.expr1.eval(vm)
        if type(res1) == NObject:
            res1 = res1.nval()
        
        res2 = self.expr2.eval(vm)
        if type(res2) == NObject:
            res2 = res2.nval()

        if self._type == PLUS:
            return NObject(res1 + res2)
        elif self._type == MINUS:
            return NObject(res1 - res2)
        elif self._type == STAR:
            return NObject(res1 * res2)
        elif self._type == SLASH:
            result = res1 / res2
            if "." in str(result):
                splitted = str(result).split(".")
                for letter in splitted[1]:
                    if letter != "0":
                        return NObject(float(result))
                return NObject(int(result))
            else:
                return NObject(int(result))