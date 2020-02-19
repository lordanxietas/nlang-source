from nobject import *
from exceptions import *
class ClassStatement(object):
    
    def __init__(self, name, parents, fields):
        self.name = name
        self.parents = parents
        self.fields = fields
    def eval(self, vm):
        this = {}
        for field in self.fields:
            obj = field.eval(vm)
            this[obj._varname] = obj
        new = NObject(this=this, varname=self.name, _type=self.name, parents=self.parents)
        vm[self.name] = new

class ClassFunction(object):
    def __init__(self, classname, access, static, type, name, args, block):
        self.classname = classname
        self.access = access
        self.static = static
        self.type = type
        self.name = name
        self.args = args
        self.statements = block
    
    def __repr__(self):
        return '(class method {} {} ({}))'.format(self.type, self.name, self.args)
    
    def eval(self, vm):
        def call(this, args):
            vm.lock()
            if not self.static:
                vm['this'] = this
            i = 0
            for funcargname, argtype in self.args.items():
                if args.get(funcargname) == None:
                    try:
                        if type(args[i]) != NObject:
                            args[i] = args[i].eval(vm)
                        args[funcargname] = args[i]
                    except:
                        args[funcargname] = self.args[funcargname]['base'].eval(vm)
                i += 1
            newargs = {}
            for key, arg in args.items():
                if type(key) != int:
                    if type(arg) != NObject:
                        arg = arg.eval(vm)
                    newargs[key] = arg
            args = newargs
            for key, arg in newargs.items():
                vm[key] = arg
            for statement in self.statements:
                try:
                    statement.eval(vm)
                except ReturnException as e:
                    return e.get()
            vm.unlock()
            return NObject()
        return NObject(access=self.access, static=self.static, _type=self.type, varname=self.name, value=call)

class ClassField(object):
    def __init__(self, access, static, type, name, value):
        self.access = access
        self.static = static
        self.type = type
        self.name = name
        self.value = value
    def __repr__(self):
        return '(field {} {} = {})'.format(self.type, self.name, self.value)
    def eval(self, vm):
        return NObject(
            access=self.access,
            static=self.static,
            _type=self.type,
            varname=self.name,
            value=self.value.eval(vm)
        )