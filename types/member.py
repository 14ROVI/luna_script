from discord import (
    Member as DiscordMember,
    Permissions as DiscordPermissions,
)

from .. import RTError, RTResult

from . import Value, String, Number, ClassFunction


class Member(Value):
    def __init__(self, value):
        super().__init__()
        self.value: DiscordMember = value
        
        from . import Guild
        
        self.symbol_table.set("id", Number(self.value.id))
        self.symbol_table.set("guild", Guild(self.value.guild))
        self.symbol_table.set("discriminator", String(self.value.discriminator))
        self.symbol_table.set("nickname", String(self.value.nick or self.value.name))
        self.symbol_table.set("mention", String(self.value.mention))
        self.symbol_table.set("avatar_url", String(self.value.display_avatar.url))
        self.symbol_table.set("bot", Number.true if self.value.bot else Number.false)
        self.symbol_table.set("joined_at", Number(self.value.joined_at.timestamp))
        self.symbol_table.set("created_at", Number(self.value.created_at.timestamp))
        
        self.symbol_table.set("add_role", ClassFunction(self, self.add_role))
        self.symbol_table.set("remove_role", ClassFunction(self, self.remove_role))
        self.symbol_table.set("has_role", ClassFunction(self, self.has_role))
        self.symbol_table.set("has_permissions", ClassFunction(self, self.has_permissions))
        self.symbol_table.set("ban", ClassFunction(self, self.ban))
        self.symbol_table.set("kick", ClassFunction(self, self.kick))
        
        
    def is_true(self):
        return True
        
    def copy(self):
        copy = Member(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"<Member id={self.value.id}>"
    
    #####################
        
    async def add_role(self, exec_ctx):
        from . import Role
        role = exec_ctx.symbol_table.get("role")

        if not isinstance(role, Role):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a Role",
                exec_ctx
            ))
            
        if not exec_ctx.register_api_interaction():
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Can't use more than 6 API interactions in a command!",
                exec_ctx
            ))

        await self.value.add_roles(*role.value, reason="Custom command")
        return RTResult().success(Number.null)
    add_role.arg_names = ["role"]
    
    
    async def remove_role(self, exec_ctx):
        from . import Role
        role = exec_ctx.symbol_table.get("role")

        if not isinstance(role, Role):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a Role",
                exec_ctx
            ))
            
        if not exec_ctx.register_api_interaction():
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Can't use more than 6 API interactions in a command!",
                exec_ctx
            ))

        await self.value.remove_roles(*role.value, reason="Custom command")
        return RTResult().success(Number.null)
    remove_role.arg_names = ["role"]
    
    
    async def has_role(self, exec_ctx):
        from . import Role
        role = exec_ctx.symbol_table.get("role")

        if not isinstance(role, Role):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a Role",
                exec_ctx
            ))

        for member_role in self.value.roles:
            if member_role.id == role.value.id:
                return RTResult().success(Number.true)
        return RTResult().success(Number.false)
    has_role.arg_names = ["role"]
    
    
    async def has_permissions(self, exec_ctx):
        perms = exec_ctx.symbol_table.get("perms")

        if not isinstance(perms, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a Number",
                exec_ctx
            ))

        member_perms = dict([p for p in iter(self.value.guild_permissions)])
        has_perms = True
        for (perm, value) in DiscordPermissions(permissions=perms.value):
            if value:
                has_perms = has_perms and member_perms[perm]

        if has_perms:
            return RTResult().success(Number.true)
        return RTResult().success(Number.false)
    has_permissions.arg_names = ["perms"]
    
    
    async def kick(self, exec_ctx):
        if not exec_ctx.register_api_interaction():
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Can't use more than 6 API interactions in a command!",
                exec_ctx
            ))
            
        await self.value.kick(reason="Custom command")
        return RTResult().success(Number.null)
    kick.arg_names = []
    
    
    async def ban(self, exec_ctx):
        if not exec_ctx.register_api_interaction():
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Can't use more than 6 API interactions in a command!",
                exec_ctx
            ))
            
        await self.value.ban(reason="Custom command")
        return RTResult().success(Number.null)
    ban.arg_names = []