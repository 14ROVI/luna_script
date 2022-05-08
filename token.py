from enum import Enum


DIGITS = '0123456789'
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SKIP_LETTERS = ' \t'
NEW_LINES = ';\n'
COMMENT_SYMBOL = '#'
LETTERS_DIGITS = LETTERS + DIGITS


class TokenType(Enum):
    TT_INT = 'INT'
    TT_FLOAT = 'FLOAT'
    TT_STRING = 'STRING'
    TT_IDENTIFIER = 'IDENTIFIER'
    TT_KEYWORD = 'KEYWORD'
    TT_PLUS = 'PLUS'
    TT_MINUS = 'MINUS'
    TT_MUL = 'MUL'
    TT_DIV = 'DIV'
    TT_POW = 'POW'
    TT_EQ = 'EQ'
    TT_LPAREN = 'LPAREN'
    TT_RPAREN = 'RPAREN'
    TT_LSQUARE = 'LSQUARE'
    TT_RSQUARE = 'RSQUARE'
    TT_EE = 'EE'
    TT_NE = 'NE'
    TT_LT = 'LT'
    TT_GT = 'GT'
    TT_LTE = 'LTE'
    TT_GTE = 'GTE'
    TT_COMMA = 'COMMA'
    TT_ARROW = 'ARROW'
    TT_NEWLINE = 'NEWLINE'
    TT_EOF = 'EOF'
    TT_DOT = 'DOT'

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self)


SYMBOL_TO_TOKENS = {
    '+': TokenType.TT_PLUS,
    '*': TokenType.TT_MUL,
    '/': TokenType.TT_DIV,
    '^': TokenType.TT_POW,
    '(': TokenType.TT_LPAREN,
    ')': TokenType.TT_RPAREN,
    '[': TokenType.TT_LSQUARE,
    ']': TokenType.TT_RSQUARE,
    ',': TokenType.TT_COMMA,
    ';': TokenType.TT_NEWLINE,
    '\n': TokenType.TT_NEWLINE,
    '.': TokenType.TT_DOT,
}


class Keywords(Enum):
    KW_VAR = 'var'
    KW_AND = 'and'
    KW_OR = 'or'
    KW_NOT = 'not'
    KW_IF = 'if'
    KW_ELIF = 'elif'
    KW_ELSE = 'else'
    KW_FOR = 'for'
    KW_TO = 'to'
    KW_STEP = 'step'
    KW_WHILE = 'while'
    KW_FUN = 'fun'
    KW_THEN = 'then'
    KW_END = 'end'
    KW_RETURN = 'return'
    KW_CONTINUE = 'continue'
    KW_BREAK = 'break'

    def __str__(self):
        return str(self.value)


KEYWORDS = {
    Keywords.KW_VAR.value: Keywords.KW_VAR,
    Keywords.KW_AND.value: Keywords.KW_AND,
    Keywords.KW_OR.value: Keywords.KW_OR,
    Keywords.KW_NOT.value: Keywords.KW_NOT,
    Keywords.KW_IF.value: Keywords.KW_IF,
    Keywords.KW_ELIF.value: Keywords.KW_ELIF,
    Keywords.KW_ELSE.value: Keywords.KW_ELSE,
    Keywords.KW_FOR.value: Keywords.KW_FOR,
    Keywords.KW_TO.value: Keywords.KW_TO,
    Keywords.KW_STEP.value: Keywords.KW_STEP,
    Keywords.KW_WHILE.value: Keywords.KW_WHILE,
    Keywords.KW_FUN.value: Keywords.KW_FUN,
    Keywords.KW_THEN.value: Keywords.KW_THEN,
    Keywords.KW_END.value: Keywords.KW_END,
    Keywords.KW_RETURN.value: Keywords.KW_RETURN,
    Keywords.KW_CONTINUE.value: Keywords.KW_CONTINUE,
    Keywords.KW_BREAK.value: Keywords.KW_BREAK,
}


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
