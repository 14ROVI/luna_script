from discord import Role as DiscordRole

from . import Value, String, Number



class Role(Value):
    def __init__(self, value):
        super().__init__()
        self.value: DiscordRole = value
        
        from . import Guild
        
        self.symbol_table.set("id", Number(self.value.id))
        self.symbol_table.set("name", String(self.value.name))
        self.symbol_table.set("colour", Number(self.value.colour.value))
        self.symbol_table.set("guild", Guild(self.value.guild))
        self.symbol_table.set("permissions", Number(self.value.permissions.value))
        self.symbol_table.set("mention", String(self.value.mention))
        self.symbol_table.set("position", Number(self.value.position))
        
    def is_true(self):
        return True
        
    def copy(self):
        copy = Role(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.value.name

    def __repr__(self):
        return f"<Role id={self.value.id}>"