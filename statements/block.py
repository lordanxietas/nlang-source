class BlockStatement(object):
    def __init__(self, block):
        self.block = block
    
    def eval(self, vm):
        if type(self.block) == list:
            for statement in self.block:
                if statement != None:
                    statement.eval(vm)
        else:
            return self.block.eval(vm)