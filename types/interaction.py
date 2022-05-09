from discord import Interaction as DiscordInteraction

from .. import RTError, RTResult

from . import Value, String, Number, ClassFunction


class Interaction(Value):
    def __init__(self, value):
        super().__init__()
        self.value: DiscordInteraction = value
        
        from . import TextChannel, Guild, Member
        
        self.symbol_table.set("channel", TextChannel(self.value.channel))
        self.symbol_table.set("guild", Guild(self.value.guild))
        self.symbol_table.set("author", Member(self.value.user))
        
        self.symbol_table.set("respond", ClassFunction(self, self.respond))
        
    def is_true(self):
        return True
        
    def copy(self):
        copy = Interaction(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return f"Interaction by {self.value.user}"

    def __repr__(self):
        return f"<Interaction user={self.value.user}>"
    
    #####################
        
    async def respond(self, exec_ctx):
        from . import Embed
        args = exec_ctx.symbol_table.get("args").elements
        
        if not exec_ctx.register_api_interaction():
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Can't use more than 6 API interactions in a command!",
                exec_ctx
            ))
        
        if len(args) == 0:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a string",
                exec_ctx
            ))
    
        text = None
        embed = None
    
        for arg in args:
            if isinstance(arg, String):
                text = arg.value
            elif isinstance(arg, Embed):
                embed = arg.value
            else:
                return RTResult().failure(RTError(
                    self.pos_start, self.pos_end,
                    "Arguments must be Strings or Embeds",
                    exec_ctx
                ))
                
        await self.value.send(content=text, embed=embed)
        return RTResult().success(Number.null)
    respond.arg_names = ["args"]