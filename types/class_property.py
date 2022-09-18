from .. import RTResult

from . import Value


class ClassProperty(Value):
    def __init__(self, function):
        self.function = function

    def copy(self):
        return RTResult().success(self.function())

    def __repr__(self):
        return f"<{type(self.object).__name__} property {self.name}>"