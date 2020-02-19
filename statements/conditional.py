from nobject import *
class ConditionalStatement(object):
    def __init__(self, cond, _if, _else):
        self.cond = cond
        self._if = _if
        self._else = _else
    def eval(self, vm):
        res = self.cond.eval(vm)
        if type(res) == NObject:
            res = res.nval()
        if res:
            self._if.eval(vm)
        else:
            if self._else != None:
                self._else.eval(vm)