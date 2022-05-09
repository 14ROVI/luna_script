from . import SymbolTable

from .types import Number
from .types import BuiltInFunction


global_symbol_table = SymbolTable()
global_symbol_table.set("null",     Number.null)
global_symbol_table.set("false",    Number.false)
global_symbol_table.set("true",     Number.true)
global_symbol_table.set("pi",       Number.math_PI)
global_symbol_table.set("is_num",   BuiltInFunction.is_number)
global_symbol_table.set("is_str",   BuiltInFunction.is_string)
global_symbol_table.set("is_lst",   BuiltInFunction.is_list)
global_symbol_table.set("is_fun",   BuiltInFunction.is_function)
global_symbol_table.set("len",      BuiltInFunction.len)
global_symbol_table.set("str",      BuiltInFunction.str)
global_symbol_table.set("Embed",    BuiltInFunction.embed)