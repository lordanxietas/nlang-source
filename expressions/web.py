from nobject import *
import pypugjs

class HtmlExpression(object):
    def __init__(self, text):
        self.text = text
    def eval(self, vm):
        vm['result']._value += self.text

class EchoExpression(object):
    def __init__(self, getter):
        self.getter = getter
    
    def eval(self, vm):
        result = self.getter.eval(vm)
        if type(result) == NObject:
            result = result.nval()
        vm['result']._value += str(result)