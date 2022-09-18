from secrets import choice
from . import Value


class Choice(Value):
    def __init__(self, choice_value):
        super().__init__()
        class innerChoice:
            value = choice_value
        self.value: int = innerChoice()
        
    def copy(self):
        return self

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"<Choice>"