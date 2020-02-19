from nobject import *
from exceptions import *
class NewExpression(object):
    def __init__(self, getter, args):
        self.getter = getter
        self.args = args
    def eval(self, vm):
        # variable = self.getter.list[0].eval(vm)
        from expressions import CallingExpression
        if type(self.getter.list[0]) == CallingExpression:
            variable = self.getter.list[0].getter.eval(vm)
        else:
            variable = self.getter.list[0].eval(vm)
        for i, expr in enumerate(self.getter.list):
            if i == 0:continue
            variable = variable._this.get(str(expr))
        if variable._varname != variable._type:
            print('You cant create not from class')
        constructor = variable._this.get(variable._type)
        if constructor == None:
            raise ConstructorDoesNotExists(f'Конструктора {str(self.getter.list[0])} не существует')
        if constructor._type != 'void':
            print('Constructor cant return anything')
        vm.lock()
        new = NObject(this={})
        new._type = variable._type
        
        for name, field in variable._this.items():
            if name != variable._varname:
                new._this[name] = field
        
        def inherit(new, variable):
            for parent in variable._parents:
                _parent = vm[parent]
                for name, field in _parent._this.items():
                    if name != _parent._varname:
                        new._this[name] = field
                if len(_parent._parents) != 0:
                    inherit(new, _parent)
        inherit(new, variable)
        vm['this'] = new
        if 'ClassFunction' in repr(constructor):
            if 'None' not in str(constructor._value(new, self.getter.list[0].args).nval()):
                print('Конструктор не может что то возвращать')
        vm.unlock()
        return new
        
    def __repr__(self):
        return f'{self.getter}'