from discord import (
    Guild as DiscordGuild,
    TextChannel as DiscordTextChannel,
    VoiceChannel as DiscordVoiceChannel,
)

from luna_script.types.class_property import ClassProperty

from .. import RTError, RTResult

from . import ClassFunction, Value, String, Number, List



class Guild(Value):
    def __init__(self, value):
        super().__init__()
        self.value: DiscordGuild = value
        
        from . import TextChannel, VoiceChannel, Member
        
        self.symbol_table.set("id", Number(self.value.id))
        self.symbol_table.set("name", String(self.value.name))
        if self.value.banner is not None:
            self.symbol_table.set("banner_url", String(self.value.banner.url))
        else:
            self.symbol_table.set("banner_url", Number.null)
        self.symbol_table.set("channels", List(
            TextChannel(channel) if isinstance(channel, DiscordTextChannel) else VoiceChannel(channel)
            for channel in self.value.channels
            if isinstance(channel, (DiscordTextChannel, DiscordVoiceChannel))
        ))
        self.symbol_table.set("owner_id", Number(self.value.owner_id))
        self.symbol_table.set("owner", Number.null)
        if self.value.owner is not None:
            self.symbol_table.set("owner", ClassProperty(lambda _: Member(self.value.owner)))
        self.symbol_table.set("get_member", ClassFunction(self, self.get_member))
        self.symbol_table.set("get_channel", ClassFunction(self, self.get_channel))
        self.symbol_table.set("get_thread", ClassFunction(self, self.get_thread))
        self.symbol_table.set("get_role", ClassFunction(self, self.get_role))
        self.symbol_table.set("ban", ClassFunction(self, self.ban))
        self.symbol_table.set("kick", ClassFunction(self, self.kick))
        
        
    def is_true(self):
        return True
        
    def copy(self):
        copy = Guild(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.value.name

    def __repr__(self):
        return f"<Guild id={self.value.id}>"
        
    #####################
        
    async def get_member(self, exec_ctx):
        from . import Member
        member_id = exec_ctx.symbol_table.get("id")

        if not isinstance(member_id, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a number",
                exec_ctx
            ))

        member = self.value.get_member(member_id.value)
        if not member:
            member = await self.value.query_members(user_ids=[member_id.value])
            member = member[0] if len(member) > 0 else None
        if member:
            return RTResult().success(Member(member))
        else:
            return RTResult().success(Number.null)
    get_member.arg_names = ["id"]
    
    
    async def get_channel(self, exec_ctx):
        from . import TextChannel, VoiceChannel
        channel_id = exec_ctx.symbol_table.get("id")

        if not isinstance(channel_id, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a number",
                exec_ctx
            ))

        channel = self.value.get_channel(channel_id.value)
        if isinstance(channel, DiscordTextChannel):
            return RTResult().success(TextChannel(channel))
        elif isinstance(channel, DiscordVoiceChannel):
            return RTResult().success(VoiceChannel(channel))
        else:
            return RTResult().success(Number.null)
    get_channel.arg_names = ["id"]
    
    
    async def get_thread(self, exec_ctx):
        from . import TextChannel, VoiceChannel
        channel_id = exec_ctx.symbol_table.get("id")

        if not isinstance(channel_id, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a number",
                exec_ctx
            ))

        channel = self.value.get_thread(channel_id.value)
        if channel is not None:
            return RTResult().success(TextChannel(channel))
        else:
            return RTResult().success(Number.null)
    get_thread.arg_names = ["id"]
    
    
    async def get_role(self, exec_ctx):
        from . import Role
        role_id = exec_ctx.symbol_table.get("id")

        if not isinstance(role_id, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a number",
                exec_ctx
            ))

        role = self.value.get_role(role_id.value)
        if role is not None:
            return RTResult().success(Role(role))
        else:
            return RTResult().success(Number.null)
    get_role.arg_names = ["id"]
    
    
    async def ban(self, exec_ctx):
        if not exec_ctx.register_api_interaction():
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Can't use more than 6 API interactions in a command!",
                exec_ctx
            ))
            
        from . import Member
        member = exec_ctx.symbol_table.get("member")

        if not isinstance(member, Member):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a member",
                exec_ctx
            ))

        await member.value.ban(reason="custom command invoked ban")
        return RTResult().success(Number.null)
    ban.arg_names = ["member"]
    
    
    async def kick(self, exec_ctx):
        if not exec_ctx.register_api_interaction():
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Can't use more than 6 API interactions in a command!",
                exec_ctx
            ))
            
        from . import Member
        member = exec_ctx.symbol_table.get("member")

        if not isinstance(member, Member):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a member",
                exec_ctx
            ))

        await member.value.kick(reason="custom command invoked kick")
        return RTResult().success(Number.null)
    kick.arg_names = ["member"]