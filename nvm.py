from nobject import *

class Nvm(dict):
    def __init__(self):
        dict.__init__({})
    
    def lock(self):
        self.copy = dict(self)
    
    def __setitem__(self, nm, value):
        if type(value) != NObject or 'Expression' in str(type(value.nval())):
            raise Exception('Помещение в виртуальную машину не NObject')
        dict.__setitem__(self, nm, value)

    def unlock(self):
        for item, value in self.copy.items():
            self[item] = value

    def get(self, nm):
        pymod = None
        try:
            pymod = eval(nm)
        except:
            pass
        if pymod == None:
            try:
                return self[nm]
            except Exception as e:
                return None
        else:
            return NObject(pymod)