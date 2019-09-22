from type import *
from nobject import *
class CallingExpression(object):
    def __init__(self, getter, args):
        self.getter = getter
        self.args = args

    def eval(self, vm):
        '''
        1. Берём аргументы функции
        2. Сравниваем их с аргументами
        '''
        variable = self.getter.eval(vm)
        args = {}
        for key, arg in self.args.items():
            args[key] = arg.eval(vm)
            if type(args[key]) != NObject:
                try:
                    args[key] = args[key].eval(vm)
                except:
                    args[key] = NObject(args[key])
        if 'FunctionDeclaration' in str(variable.nval()):
            return variable.nval()(args)
        if 'builtin_function_or_method' in str(type(variable.nval())):
            return variable(args)
        return variable(args)

    def __str__(self):
        return repr(self.getter)

    def __repr__(self):
        return repr(self.getter) + f'({self.args})'
