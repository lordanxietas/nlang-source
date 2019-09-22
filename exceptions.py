class BreakException(Exception):
    pass
class ReturnException(Exception):
    def __init__(self, value):
        self.value = value
    def get(self):
        return self.value

class ContinueException(Exception):
    pass
class WrongSyntaxException(Exception):
    pass
class WrongExpressionException(Exception):
    pass
class VariableNotExists(Exception):
    pass
class NotStatic(Exception):
    pass
class ConstructorDoesNotExists(Exception):
    pass
class LexerError(Exception):
    pass