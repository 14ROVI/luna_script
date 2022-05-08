from . import Lexer, Parser, Interpreter, Context

class Runner:
    @staticmethod
    def run(fn, text):
        from luna_script.global_symbol_table import global_symbol_table
        
        # Generate tokens
        lexer = Lexer(fn, text)
        tokens, error = lexer.make_tokens()
        if error: return None, error
        
        # Generate AST
        parser = Parser(tokens)
        ast = parser.parse()
        if ast.error: return None, ast.error

        # Run program
        interpreter = Interpreter()
        context = Context('<program>')
        context.symbol_table = global_symbol_table
        result = interpreter.visit(ast.node, context)
        return result.value, result.error