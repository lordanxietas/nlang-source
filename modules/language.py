from nobject import *


def ToString(value):
    return str(value)
def ToInt(value):
    return int(value)
def ToDict(value):
    try:return dict(value)
    except:return value.__dict__

def AddPyMod(vm, _import=None, _from=None):
    from pymodules import pymods
    if _import != None:
        if _from != None:
            module = __import__(_import, fromlist=[_from])
        else:
            module = __import__(_import)
    vm[_import] = NObject(module)
    pymods += [_import]

def language(vm):
    from pymodules import pymods
    vm['null'] = NObject(0)
    vm['undefined'] = NObject()
    vm['io'] = NObject(this={
        "ToInt": NObject(ToInt, static=True),
        "ToString": NObject(ToString, static=True),
        "ToDict": NObject(ToDict, static=True)
    })
    vm['true'] = NObject(True)
    vm['false'] = NObject(False)
    vm['pyimport'] = NObject(lambda _import, _from=None: AddPyMod(vm, _import, _from))
    vm['pymod'] = NObject(lambda name: pymods.append(name))
    return vm
from pymodules import mods
mods += ["language"]