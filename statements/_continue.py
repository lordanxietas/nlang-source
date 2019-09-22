from exceptions import ContinueException
class ContinueStatement(object):
    def __init__(self):
        pass
    def eval(self, vm):
        raise ContinueException()