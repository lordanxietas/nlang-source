from nobject import *
from exceptions import *
class AssignmentStatement(object):
    def __init__(self, getter, value):
        self.getter = getter
        self.value = value
    def eval(self, vm):
        '''Присваиваем по геттеру'''
        variable = self.getter.eval(vm)
        # if 'this' in self.getter.list and variable.nval() == None:
        #     variable = NObject()
        # print(self.getter)
        iter = []
        for exp in self.getter.list:
            iter.append(str(exp))
        if variable == None:
            if str(self.getter.list[0]) != 'this':
                raise VariableNotExists(f'Переменной {".".join(iter)} не существует')
            else:
                # variable = NObject()
                value = self.value.eval(vm)
                self.getter.list[0].eval(vm)._this[str(exp)] = value
                return
        # присваиваем если например f = 123
        if len(self.getter.list) == 1:
            res = self.value.eval(vm)
            variable.assign(res)
            vm[self.getter.list[0].text] = res
        else:
            value = self.value.eval(vm)
            if type(value) == NObject:
                variable.assign(value)
            else:
                # variable.nlangset(value)
                pass
                # hacky.write_memory_in(id(variable)+24, value)

                # print(thedict)
                # print(thedict)
            
    def __repr__(self):
        return f'{self.getter} = {self.value}'

class DeclarationStatement(object):
    def __init__(self, type, name, value):
        self.type = type
        self.name = name
        self.value = value
    def eval(self, vm):
        '''Присваиваем по геттеру'''
        result = self.value.eval(vm)
        if type(result) == NObject:
            result._type = self.type
            vm[self.name] = result
        else:
            vm[self.name] = NObject(result, _type=self.type)
    def __repr__(self):
        return f'{self._type} {self.name} = {self.value}'