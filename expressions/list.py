from nobject import *
class ListExpression(object):
    def __init__(self, lst):
        self.list = lst
    
    def eval(self, vm):
        array = []
        for value in self.list:
            array.append(value.eval(vm))
        return NObject(array, _type="List")