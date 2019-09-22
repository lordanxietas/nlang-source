class ConditionalStatement(object):
    def __init__(self, cond, _if, _else):
        self.cond = cond
        self._if = _if
        self._else = _else
    def eval(self, vm):
        if self.cond.eval(vm).nval():
            self._if.eval(vm)
        else:
            if self._else != None:
                self._else.eval(vm)