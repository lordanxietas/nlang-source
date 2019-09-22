class WhileStatement(object):
    def __init__(self, expr, block):
        self.expr = expr
        self.block = block
    
    def eval(self, vm):
        while self.expr.eval(vm).nval():
            self.block.eval(vm)