from .. import RTError, RTResult

from . import Value, Number, ClassFunction


class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value: str = value
        
        self.symbol_table.set("startswith", ClassFunction(self, self.startswith))

    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def is_true(self):
        return len(self.value) > 0

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'"{self.value}"'

    ########################### 
    
    async def startswith(self, exec_ctx):
        text = exec_ctx.symbol_table.get("text")

        if not isinstance(text, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a string",
                exec_ctx
            ))
        
        if self.value.startswith(text.value):
            return RTResult().success(Number.true)
        else:
            return RTResult().success(Number.false)
    startswith.arg_names = ["text"]
    
    
    async def endswith(self, exec_ctx):
        text = exec_ctx.symbol_table.get("text")

        if not isinstance(text, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a string",
                exec_ctx
            ))
        
        if self.value.endswith(text.value):
            return RTResult().success(Number.true)
        else:
            return RTResult().success(Number.false)
    endswith.arg_names = ["text"]
    
    
    async def contains(self, exec_ctx):
        text = exec_ctx.symbol_table.get("text")

        if not isinstance(text, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a string",
                exec_ctx
            ))
        
        if text.value in self.value:
            return RTResult().success(Number.true)
        else:
            return RTResult().success(Number.false)
    contains.arg_names = ["text"]
    
    
    async def upper(self, _):
        return RTResult().success(String(self.value.upper()))
    upper.arg_names = []
    
    
    async def lower(self, _):
        return RTResult().success(String(self.value.lower()))
    lower.arg_names = []