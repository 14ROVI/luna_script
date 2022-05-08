from discord import Embed as DiscordEmbed

from . import Value


class Embed(Value):
    def __init__(self, value):
        super().__init__()
        self.value: DiscordEmbed = value

        
    def is_true(self):
        return True
        
    def copy(self):
        copy = Embed(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"<Embed id={self.value.id}>"