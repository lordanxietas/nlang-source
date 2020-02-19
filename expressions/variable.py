from nobject import *
class VariableExpression(object):
    def __init__(self, text):
        self.text = text

    def eval(self, vm):
        # if self.text == 'None':
        #     return None
        variable = vm.get(self.text)
        if variable == None: 
            return vm['undefined']
        return variable
    
    def __repr__(self):
        return self.text

class ArrayAccessExpression(object):
    def __init__(self, access):
        self.variable = None
        self.access = access
    def eval(self, vm):
        res = self.variable

        for ac in self.access:
            result = ac.eval(vm).nval()
            res = res[result]
        return res