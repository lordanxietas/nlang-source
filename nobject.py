from type import *
from nobject import *
import json
# import hacky


# def nlangset(self, value):
    # self.nlangval = value
    # self.__dict__.update(value.__dict__)
    # self.__set__(self, value)

# class NLangString(str):
#     def __init__(self, value):
#         self.value = value
#     def __get__(self):
#         return self.value
#     def __set__(self, value):
#         self.value = value
# hacky.set_class(str, type('NLangString', (str,), dict(NLangString.__dict__)))

# objdict = hacky.fetch_dict(object)
# objdict['nlangval'] = None
# objdict['nlangset'] = nlangset
# objdict['__get__'] = lambda self, *args, **kwargs: self.nlangval if self.nlangval != None else self


def times(f, fn):
    for i in range(0, f):
        func = fn[0]
        func({0: f})

def foreach(d, fn):
    fn = fn[0]
    for key, value in d.items():
        fn({"key": NObject(key), "value": NObject(value)})

class NObject(object):
    def __init__(self, value=None, isinstance=False, varname=None, _type=None, this={}, static=False, access='private', parents=['object']):
        self._this = this
        
        self._functionargs = {}
        self._varname = varname
        self._value = value
        if type(self._value) == list:
            self._this['pop'] = NObject(self._value.pop)
            self._this['append'] = NObject(self._value.append)
            self._this['remove'] = NObject(self._value.remove)
        elif type(self._value) == dict:
            self._this['get'] = NObject(self._value.get)
            self._this['items'] = NObject(self._value.items)
            self._this['foreach'] = lambda fn: foreach(self._value, fn)
        elif type(self._value) == str:
            self._this['replace'] = NObject(self._value.replace)
            self._this['strip'] = NObject(self._value.strip)
        elif type(self._value) == int:
            self._this['times'] = lambda fn: times(self._value, fn)
            self._this['str'] = lambda *a, **k: str(self._value)

        self._type = _type
        self._static = static
        self._access = access
        self._parents = parents
        self.isinstance = isinstance
    
    def __getitem__(self, name):
        if type(name) == NObject:
            name = name.nval()
        try:
            return self._value[name]
        except:
            self._value[name] = NObject()
            return self._value[name]
    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def nval(self):
        if self._value == None:
            return None
        elif type(self._value) == dict or type(self._value) == list:
            def _iter(dictionary):
                if type(dictionary) == dict:
                    res = {}
                    for key, value in dictionary.items():
                        try:
                            res[key] = value.nval()
                        except:
                            res[key] = value
                elif type(dictionary) == list:
                    res = []
                    for key, value in enumerate(dictionary):
                        try:
                            res.append(value.nval())
                        except:
                            res.append(value)
                else:
                    return dictionary.nval()
                return res
            return _iter(self._value)
        return self._value
    def __repr__(self):
        return str(self._value)

    def __call__(self, args, this=None):
        if not callable(self._value):
            return self._value
        newargs = []
        kwargs = {}
        for key, arg in args.items():
            if type(key) == int:
                try:
                    res = arg
                    if type(res) == NObject:
                        res = res.nval()
                    newargs.append(res)
                except Exception as e:
                    import traceback
                    print(traceback.format_exc())
                    kwargs[key] = arg
            else:
                try:kwargs[key] = arg.nval()
                except:kwargs[key] = arg
        if 'FunctionDeclaration' in repr(self) or 'FunctionExpression' in repr(self):
            return NObject(self._value(args))
        if 'ClassFunction' in repr(self):
            return NObject(self._value(this, args))
        if 'staticmethod' in repr(self):
            func = self._value.__func__
            return func(*newargs, **kwargs)

        return NObject(self._value(*newargs, **kwargs))
    def assign(self, another):
        for key, prop in another.__dict__.items():
            self.__dict__[key] = prop

    @property
    def __functionargs(self):
        if self.__type == CUSTOM:
            return self._this.get('__init', {}).args # Возвращаем аргументы класса
        else:
            return self._function.args # Возвращаем аргументы функции

class NewNObject(NObject):
    def __init__(self):
        NObject.__init__(self)

def ispyobject(value):
    # return str(type(value)) in [None, int, str, object]
    for tp in ["None", 'class', 'function']:
        if tp in str(type(value)):
            return False