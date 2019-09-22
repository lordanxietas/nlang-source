from exceptions import ReturnException
class ReturnStatement(object):
    def __init__(self, expr):
        self.expr = expr
    def eval(self, vm):
        raise ReturnException(self.expr.eval(vm))