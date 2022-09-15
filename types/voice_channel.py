from datetime import timedelta
from discord import (
    app_commands,
    VoiceChannel as DiscordVoiceChannel
)

from .. import RTResult, RTError

from . import Value, String, Number, ClassFunction, Embed


class VoiceChannel(Value):
    def __init__(self, value):
        super().__init__()
        self.value: DiscordVoiceChannel = value
        
        from . import Guild
        
        self.symbol_table.set("id", Number(self.value.id))
        self.symbol_table.set("guild", Guild(self.value.guild))
        self.symbol_table.set("mention", String(self.value.mention))
        self.symbol_table.set("name", String(self.value.name))
        self.symbol_table.set("send", ClassFunction(self, self.send))
        self.symbol_table.set("run_command", ClassFunction(self, self.run_command))
        
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
    
    
    async def send(self, exec_ctx):
        from . import Message
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

        new_message = await self.value.send(content=text, embed=embed)
        new_message = Message(new_message)
        return RTResult().success(new_message)
    send.arg_names = ["args"]
    
    
    async def run_command(self, exec_ctx):
        bot = exec_ctx.get_bot()
        interaction = exec_ctx.get_interaction()
        args = exec_ctx.symbol_table.get("args").elements
        args = [arg.value for arg in args]
        command_name = args[0]
        args = args[1:]

        if not isinstance(command_name, str):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a string",
                exec_ctx
            ))
        
        invoked_command = None
        for command in bot.tree.walk_commands():
            if isinstance(command, app_commands.Command):
                full_name = command.name
                parent = command.parent
                while parent is not None:
                    full_name = parent.name + " " + full_name
                    parent = parent.parent
                if full_name == command_name:
                    invoked_command = command
                    break
        
        if invoked_command is None:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Command can not be found",
                exec_ctx
            ))
        
        if interaction.channel != self.value:
            interaction.expires_at -= timedelta(minutes=15)
            interaction.channel = self.value
        
        if invoked_command.parent:
            await invoked_command.callback(invoked_command.parent, interaction, *args)
        else:
            await invoked_command.callback(interaction, *args)
        
        return RTResult().success(Number.null)
    run_command.arg_names = ["args"]