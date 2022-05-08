from discord import Message as DiscordMessage

from .. import RTResult, RTError

from . import Value, String, Embed


class Message(Value):
    def __init__(self, value):
        super().__init__()
        self.value: DiscordMessage = value
        
        from . import Number, TextChannel, Guild, Member, Embed, List, ClassFunction
        
        self.symbol_table.set("id", Number(self.value.id))
        self.symbol_table.set("content", String(self.value.content))
        self.symbol_table.set("channel", TextChannel(self.value.channel))
        self.symbol_table.set("guild", Guild(self.value.guild))
        self.symbol_table.set("url", String(self.value.jump_url))
        self.symbol_table.set("author", Member(self.value.author))
        self.symbol_table.set("embeds", List(Embed(embed) for embed in self.value.embeds))
        self.symbol_table.set("reply", ClassFunction(self, self.reply))
        
    def is_true(self):
        return True
        
    def copy(self):
        copy = Message(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.value.content

    def __repr__(self):
        return f"<Message author={self.value.user}>"
    
    #####################
        
    async def reply(self, exec_ctx):
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
                text = arg
            elif isinstance(arg, Embed):
                embed = arg
            else:
                return RTResult().failure(RTError(
                    self.pos_start, self.pos_end,
                    "Arguments must be Strings or Embeds",
                    exec_ctx
                ))

        new_message = await self.value.reply(text.value)
        new_message = Message(new_message)
        return RTResult().success(new_message)
    reply.arg_names = ["args"]