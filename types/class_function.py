from inspect import iscoroutinefunction

from .. import RTResult

from . import BaseFunction



class ClassFunction(BaseFunction):
    def __init__(self, object, function):
        super().__init__(function.__name__)
        self.object = object
        self.function = function

    async def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()

        res.register(self.check_and_populate_args(self.function.arg_names, args, exec_ctx))
        if res.should_return():
            return res

        if iscoroutinefunction(self.function):
            result = await self.function(exec_ctx)
        else:    
            result = self.function(exec_ctx)

        return_value = res.register(result)
        if res.should_return(): return res
        return res.success(return_value)

    def no_visit_method(self, *_):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy = ClassFunction(self.object, self.function)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<{type(self.object).__name__} function {self.name}>"