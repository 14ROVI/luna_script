from discord import VoiceChannel as DiscordVoiceChannel

from . import Value, String, Number


class VoiceChannel(Value):
    def __init__(self, value):
        super().__init__()
        self.value: DiscordVoiceChannel = value
        
        from . import Guild
        
        self.symbol_table.set("id", Number(self.value.id))
        self.symbol_table.set("guild", Guild(self.value.guild))
        self.symbol_table.set("mention", String(self.value.mention))
        self.symbol_table.set("name", String(self.value.name))
        
    def is_true(self):
        return True
        
    def copy(self):
        copy = VoiceChannel(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.value.name

    def __repr__(self):
        return f"<VoiceChannel id={self.value.id}>"