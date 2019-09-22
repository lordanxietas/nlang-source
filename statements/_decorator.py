from nobject import *
class DecoratorStatement(object):

    def __init__(self, getter, statement):
        self.getter = getter
        self.statement = statement
    
    def eval(self, vm):
        variable = self.getter.eval(vm)
        args = {}
        self.statement.decorated = True
        args[0] = self.statement.eval(vm)
        if 'FunctionDeclaration' in str(variable.nval()):
            return variable.nval()(args)
        if 'builtin_function_or_method' in str(type(variable.nval())):
            return variable(args)
        return variable(args)