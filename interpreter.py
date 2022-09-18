from . import RTResult, RTError, Context, TokenType, Keywords, SymbolTable

from .types import Number, String, List, Function



class Interpreter:
    @classmethod
    async def visit(cls, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(cls, method_name, cls.no_visit_method)
        res = await method(node, context)

        if node.child:
            new_context = Context(type(res.value).__name__, context, node.child.pos_start)
            if res.value:
                new_context.symbol_table = res.value.symbol_table
            else:
                new_context.symbol_table = SymbolTable()
            new_context.is_code_block = False
            res.value = res.register(await cls.visit(node.child, new_context))

        return res

    @classmethod
    async def no_visit_method(cls, node, _):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ###################################

    @classmethod
    async def visit_NumberNode(cls, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(
                node.pos_start, node.pos_end))

    @classmethod
    async def visit_StringNode(cls, node, context):
        return RTResult().success(
            String(node.tok.value).set_context(context).set_pos(
                node.pos_start, node.pos_end))

    @classmethod
    async def visit_ListNode(cls, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(await cls.visit(element_node, context)))
            if res.should_return(): return res

        return res.success(
            List(elements)
                .set_context(context)
                .set_pos(node.pos_start, node.pos_end)
        )

    @classmethod
    async def visit_VarAccessNode(cls, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)

    @classmethod
    async def visit_VarAssignNode(cls, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(await cls.visit(node.value_node, context))
        if res.should_return(): return res
        
        if node.extra_names != []:
            nd = context.symbol_table.get(var_name)
            prev = None

            if not nd:
                return res.failure(RTError(
                    node.pos_start, node.pos_end,
                    f"'{name}' not defined",
                    context
                ))

            for index, name_tok in enumerate(node.extra_names):
                name = name_tok.value
                prev = nd
                nd = nd.symbol_table.symbols[name] if name in nd.symbol_table.symbols else None

                if not nd and index != len(node.extra_names)-1:
                    return res.failure(RTError(
                        node.pos_start, node.pos_end,
                        f"'{name}' not defined",
                        context
                    ))
            
            prev.symbol_table.set(name, value)
            return res.success(value)

        context.symbol_table.set(var_name, value)
        return res.success(value)

    @classmethod
    async def visit_BinOpNode(cls, node, context):
        res = RTResult()
        left = res.register(await cls.visit(node.left_node, context))
        if res.should_return(): return res
        right = res.register(await cls.visit(node.right_node, context))
        if res.should_return(): return res

        if node.op_tok.type == TokenType.TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TokenType.TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TokenType.TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TokenType.TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TokenType.TT_POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == TokenType.TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TokenType.TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TokenType.TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TokenType.TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TokenType.TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TokenType.TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TokenType.TT_KEYWORD, Keywords.KW_AND):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TokenType.TT_KEYWORD, Keywords.KW_OR):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    @classmethod
    async def visit_UnaryOpNode(cls, node, context):
        res = RTResult()
        number = res.register(await cls.visit(node.node, context))
        if res.should_return(): return res

        error = None

        if node.op_tok.type == TokenType.TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.matches(TokenType.TT_KEYWORD, Keywords.KW_NOT):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    @classmethod
    async def visit_IfNode(cls, node, context):
        res = RTResult()

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(await cls.visit(condition, context))
            if res.should_return(): return res

            if condition_value.is_true():
                expr_value = res.register(await cls.visit(expr, context))
                if res.should_return(): return res
                return res.success(
                    Number.null if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            expr_value = res.register(await cls.visit(expr, context))
            if res.should_return(): return res
            return res.success(
                Number.null if should_return_null else expr_value)

        return res.success(Number.null)

    @classmethod
    async def visit_ForNode(cls, node, context):
        res = RTResult()
        elements = []

        start_value = res.register(await cls.visit(node.start_value_node, context))
        if res.should_return(): return res

        end_value = res.register(await cls.visit(node.end_value_node, context))
        if res.should_return(): return res

        if node.step_value_node:
            step_value = res.register(await cls.visit(node.step_value_node,
                                                 context))
            if res.should_return(): return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            value = res.register(await cls.visit(node.body_node, context))
            if res.should_return(
            ) and res.loop_should_continue == False and res.loop_should_break == False:
                return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Number.null if node.should_return_null else List(elements).
            set_context(context).set_pos(node.pos_start, node.pos_end))

    @classmethod
    async def visit_WhileNode(cls, node, context):
        res = RTResult()
        elements = []

        while True:
            condition = res.register(await cls.visit(node.condition_node, context))
            if res.should_return(): return res

            if not condition.is_true():
                break

            value = res.register(await cls.visit(node.body_node, context))
            if res.should_return(
            ) and res.loop_should_continue == False and res.loop_should_break == False:
                return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Number.null if node.should_return_null else List(elements).
            set_context(context).set_pos(node.pos_start, node.pos_end))

    @classmethod
    async def visit_FuncDefNode(cls, node, context):
        
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(
            func_name, body_node, arg_names,
            node.should_auto_return).set_context(context).set_pos(
                node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    @classmethod
    async def visit_CallNode(cls, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(await cls.visit(node.node_to_call, context))
        if res.should_return(): return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            new_context = context.get_code_block_context()
            args.append(res.register(await cls.visit(arg_node, new_context)))
            if res.should_return(): return res

        return_value = res.register(await value_to_call.execute(args))
        if res.should_return(): return res
        return_value = return_value.copy().set_pos(
            node.pos_start, node.pos_end).set_context(context)
        return res.success(return_value)

    @classmethod
    async def visit_ReturnNode(cls, node, context):
        res = RTResult()

        if node.node_to_return:
            value = res.register(await cls.visit(node.node_to_return, context))
            if res.should_return(): return res
        else:
            value = Number.null

        return res.success_return(value)

    @classmethod
    async def visit_ContinueNode(cls, node, context):
        return RTResult().success_continue()

    @classmethod
    async def visit_BreakNode(cls, node, context):
        return RTResult().success_break()
