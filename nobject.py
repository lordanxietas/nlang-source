from type import *

class NObject(object):
    def __init__(self, value=None, isinstance=False, varname=None, type=None, this={}, static=False, access='private', parents=['object']):
        self._this = this
        self._functionargs = {}
        self._varname = varname
        self._value = value
        self._type = type
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
                    res = arg.nval()
                    newargs.append(res)
                except Exception as e:
                    import traceback
                    print(traceback.format_exc())
                    kwargs[key] = arg
            else:
                try:kwargs[key] = arg.nval()
                except:kwargs[key] = arg
        if 'FunctionDeclaration' in repr(self):
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
        