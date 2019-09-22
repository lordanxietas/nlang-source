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
            print('Ты не можешь создать экземпляр не класса')
        constructor = variable._this.get(variable._type)
        if constructor == None:
            raise ConstructorDoesNotExists(f'Конструктора {str(self.getter.list[0])} не существует')
        if constructor._type != 'void':
            print('Конструктор не может что то возвращать')
        vm.lock()
        new = NObject(this={})
        new._type = variable._type
        
        for name, field in variable._this.items():
            if name != variable._varname:
                new._this[name] = field
        vm['this'] = new
        if 'ClassFunction' in repr(constructor):
            if 'None' not in str(constructor._value(new, self.getter.list[0].args).nval()):
                print('Конструктор не может что то возвращать')
        vm.unlock()
        return new
        
    def __repr__(self):
        return f'{self.getter}'