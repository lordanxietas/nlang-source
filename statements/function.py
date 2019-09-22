from nobject import *
from type import *
from exceptions import *
class FunctionStatement(object):
    pass

class FunctionDeclaration(object):
    def __init__(self, typeofret, name, args, statements):
        self.type = typeofret
        self.name = name
        self.args = args
        self.statements = statements
        self.decorated = False
    
    def eval(self, vm):
        def call(args={}, **kwargs):
            vm.lock()
            i = 0
            for funcargname, argtype in self.args.items():
                if args.get(funcargname) == None:
                    try:
                        args[funcargname] = args[i]
                    except Exception as e:
                        if len(kwargs) == 0:
                            raise e
                i += 1
            newargs = {}
            for key, arg in kwargs.items():
                if type(key) != int:
                    newargs[key] = NObject(arg)
            for key, arg in args.items():
                if type(key) != int:
                    newargs[key] = arg
            args = newargs
            for key, arg in newargs.items():
                vm[key] = arg
            for statement in self.statements:
                try:
                    statement.eval(vm)
                except ReturnException as e:
                    res = e.get()
                    return res._value
            vm.unlock()
            return NObject()
        nobject = NObject()
        nobject._value = call
        nobject._functionargs = self.args
        vm[self.name] = nobject
        return nobject

    def __repr__(self):
        st = f'def {self.name}()' + ' {'
        for state in self.statements:
            st += ' ' + str(state) + ';'
        st += '}'
        return st