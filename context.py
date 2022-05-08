from typing_extensions import Self
from discord.ext.commands import Bot
from discord import Interaction

from . import Position


class Context:
    def __init__(self, display_name: str, parent: Self | None = None, parent_entry_pos: Position | None = None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None
        self.bot = None
        self.invoker = None
        self.interaction = None
        self.api_interactions = 0
        self.max_api_interactions = 6
        self.is_code_block = True
        

    def get_bot(self) -> Bot:
        if not self.bot:
            return self.parent.get_bot()
        return self.bot

    def get_interaction(self) -> Interaction:
        if not self.interaction:
            return self.parent.get_interaction()
        return self.interaction

    def get_invoker(self):
        if not self.invoker:
            return self.parent.get_invoker()
        return self.invoker

    def register_api_interaction(self):
        root = self
        while root.parent:
            root = root.parent
        root.api_interactions += 1
        if root.api_interactions > self.max_api_interactions:
            return False
        return True
    
    def get_code_block_context(self):
        root = self
        while root.parent and not root.is_code_block:
            root = root.parent
        return root