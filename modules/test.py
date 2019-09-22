from nobject import NObject
from threading import Thread
def thread(target):
    Thread(target=lambda: target({})).start()
def test(vm):
    vm['thread'] = NObject(thread)
    return vm
from pymodules import mods
mods += ["test"]