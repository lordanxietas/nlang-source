from nobject import *
from pymodules import pymods
from exceptions import *
class GetterExpression(object):
    def __init__(self, lst):
        self.list = lst
    
    def eval(self, vm):
        from expressions import CallingExpression, ArrayAccessExpression
        res = self.list[0].eval(vm)
        
        for i, expr in enumerate(self.list):
            if i == 0:
                continue
            copy = res
            res1 = res._this.get(str(expr))
            if self.list[0].text == 'this':
                if res1 == None:
                    return None
            if type(expr) == ArrayAccessExpression:
                expr.variable = res
                res = expr.eval(vm)
            elif 'None' in str(res1):
                try:
                    if str(expr) in res._value.__dict__:
                        res = NObject(res._value.__dict__.get(str(expr)))
                    else:
                        at = getattr(res._value, str(expr))
                        res = NObject(at)
                except AttributeError:
                    raise AttributeError(f'У класса {res._type} нет поля {str(expr)}')
            else:
                res = res1
            
            if type(expr) == CallingExpression:
                newargs = {}
                for key, arg in expr.args.items():
                    newargs[key] = arg.eval(vm)
                if type(res) == NObject:
                    if 'Class' in repr(res):
                        if not res._static:
                            exc = False
                            try:
                                res = res._value(self.list[i - 1].eval(vm), newargs)
                                
                            except:
                                exc = True
                            if exc:
                                raise NotStatic(f'Функция {str(expr)} не статическая')
                        else:
                            res = res(newargs)
                    else:
                        res = res(newargs)
                else:
                    res = res(newargs)

        return res

    def __repr__(self):
        return f'{self.list[0]}'