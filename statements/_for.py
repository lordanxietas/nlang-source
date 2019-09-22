class ForStatement(object):
    def __init__(self, decl, _while, _do, block):
        self.decl = decl
        self._while = _while
        self._do = _do
        self.block = block
    
    def eval(self, vm):
        self.decl.eval(vm)
        while self._while.eval(vm).nval():
            self.block.eval(vm)
            self._do.eval(vm)