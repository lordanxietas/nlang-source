from nobject import *
class DictExpression(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary
    def eval(self, vm):
        array = dict()
        for key, value in self.dictionary.items():
            array[key.eval(vm).nval()] = value.eval(vm)
        return NObject(array, type="Dict")