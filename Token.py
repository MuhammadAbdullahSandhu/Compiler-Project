
class TokenType:
    NUMBER = 'NUMBER'
    KEYWORD = 'KEYWORD'
    IDENTIFIER = 'IDENTIFIER'
    OPERATOR = 'OPERATOR'
    PUNCTUATION = 'PUNCTUATION'
    A_OPERATOR = 'A_OPERATOR'
    PREPROCESSOR = 'PREPROCESSOR'
    UNKNOWN = 'UNKNOWN'
    COMMENT ='COMMENT'
    STRING_LITERAL = 'STRING_LITERAL'
    bool_kw = "_Bool"
    char_kw = "char"
    short_kw = "short"
    int_kw = 'int'
    long_kw = "long"
    signed_kw = "signed"
    unsigned_kw = "unsigned"
    void_kw = "void"

    return_kw = "return"
    if_kw = "if"
    else_kw = "else"
    while_kw = "while"
    for_kw = "for"
    break_kw = "break"
    continue_kw = "continue"

    auto_kw = "auto"
    static_kw = "static"
    extern_kw = "extern"
    struct_kw = "struct"
    union_kw = "union"
    const_kw = "const"
    typedef_kw = "typedef"
    sizeof_kw = "sizeof"

    plus = "+"
    minus = "-"
    star = "*"
    slash = "/"
    mod = "%"
    incr = "++"
    decr = "--"
    equals = "="
    plusequals = "+="
    minusequals = "-="
    starequals = "*="
    divequals = "/="
    modequals = "%="
    twoequals = "=="
    notequal = "!="
    bool_and = "&&"
    bool_or = "||"
    bool_not = "!"
    lt = "<"
    gt = ">"
    ltoe = "<="
    gtoe = ">="
    amp = "&"
    pound = "#"
    lbitshift = "<<"
    rbitshift = ">>"
    compl = "~"

    dquote = '"'
    squote = "'"

    open_paren = '('
    close_paren = ")"
    open_brack = "{"
    close_brack = "}"
    open_sq_brack = "["
    close_sq_brack = "]"
    comma = ","
    semicolon = ";"
    dot = "."
    arrow = "->"

class Token:
    def __init__(self, type: TokenType, value: str, line_no: int):
        self.t_type = type
        self.t_vale = value
        self.line_number = line_no

    def __str__(self):
          return f"Token{{type = {self.t_type:<20} value = {self.t_vale:<10} line = {self.line_number}}}"


class TokenKind:
    def __init__(self, name, category):
        self.name = name
        self.category = category

    def __repr__(self):
        return f"TokenKind(name={self.name}, category={self.category})"
    