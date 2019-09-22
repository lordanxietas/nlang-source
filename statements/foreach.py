from nobject import *
class ForeachStatement(object):
    
    def __init__(self, key, value, expr, block):
        self.key = key
        self.value = value
        self.expr = expr
        self.block = block
    
    def eval(self, vm):
        res = self.expr.eval(vm).nval()
        if type(res) == dict:
            res = res.items()
        elif type(res) == list:
            res = enumerate(res)
        for key, value in res:
            vm[self.key] = NObject(key)
            vm[self.value] = NObject(value)
            self.block.eval(vm)