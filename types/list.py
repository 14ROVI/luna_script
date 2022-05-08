from .. import RTError, RTResult

from . import Value, Number, ClassFunction




class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.symbol_table.set("extend", ClassFunction(self, self.extend))
        self.symbol_table.set("append", ClassFunction(self, self.append))
        self.symbol_table.set("pop",    ClassFunction(self, self.pop))
        self.symbol_table.set("get",    ClassFunction(self, self.get))
        
        self.elements = elements
        
    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return "[" + ", ".join(repr(x) for x in self.elements) + "]"

    def __repr__(self):
        return "[" + ", ".join(repr(x) for x in self.elements) + "]"
    
    #####################
        
    def extend(self, exec_ctx):
        other = exec_ctx.symbol_table.get("other")

        if not isinstance(other, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be list",
                exec_ctx
            ))

        new_list = self.copy()
        new_list.elements.extend(other.elements)
        return RTResult().success(new_list)
    extend.arg_names = ["other"]
    
    def append(self, exec_ctx):
        other = exec_ctx.symbol_table.get("other")
        new_list = self.copy()
        new_list.elements.append(other)
        return RTResult().success(new_list)
    append.arg_names = ["other"]
    
    def pop(self, exec_ctx):
        other = exec_ctx.symbol_table.get("other")
        
        if not isinstance(other, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be integer",
                exec_ctx
            ))
        
        new_list = self.copy()
        try:
            new_list.elements.pop(round(other.value))
            return RTResult().success(new_list)
        except:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Index out of bounds of list",
                exec_ctx
            ))
    pop.arg_names = ["other"]
    
    def get(self, exec_ctx):
        other = exec_ctx.symbol_table.get("other")
        
        if not isinstance(other, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be integer",
                exec_ctx
            ))
        
        try:
            element = self.elements[round(other.value)]
            return RTResult().success(element)
        except:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Index out of bounds of list",
                exec_ctx
            ))
    get.arg_names = ["other"]
    
    
    def contains(self, exec_ctx):
        element = exec_ctx.symbol_table.get("element")
        
        if element in self.elements:
            return RTResult().success(Number.true)
        else:
            return RTResult().success(Number.false)
    contains.arg_names = ["element"]
