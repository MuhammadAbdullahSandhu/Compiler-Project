from Token import TokenKind



keyword_kinds = []
symbol_kinds = []
punctuator_kinds =[]

bool_kw = TokenKind("_Bool", keyword_kinds)
char_kw = TokenKind("char", keyword_kinds)
int_kw = TokenKind("int", keyword_kinds)
long_kw = TokenKind("long", keyword_kinds)
void_kw = TokenKind("void", keyword_kinds)

return_kw = TokenKind("return", keyword_kinds)
if_kw = TokenKind("if", keyword_kinds)
else_kw = TokenKind("else", keyword_kinds)
while_kw = TokenKind("while", keyword_kinds)
for_kw = TokenKind("for", keyword_kinds)
break_kw = TokenKind("break", keyword_kinds)
continue_kw = TokenKind("continue", keyword_kinds)

auto_kw = TokenKind("auto", keyword_kinds)
static_kw = TokenKind("static", keyword_kinds)
extern_kw = TokenKind("extern", keyword_kinds)
struct_kw = TokenKind("struct", keyword_kinds)
union_kw = TokenKind("union", keyword_kinds)
const_kw = TokenKind("const", keyword_kinds)
typedef_kw = TokenKind("typedef", keyword_kinds)
sizeof_kw = TokenKind("sizeof", keyword_kinds)

plus = TokenKind("+", symbol_kinds)
minus = TokenKind("-", symbol_kinds)
star = TokenKind("*", symbol_kinds)
slash = TokenKind("/", symbol_kinds)
mod = TokenKind("%", symbol_kinds)
equals = TokenKind("=", symbol_kinds)
incr = TokenKind("++", symbol_kinds)
decr = TokenKind("--", symbol_kinds)
plusequals = TokenKind("+=", symbol_kinds)
minusequals = TokenKind("-=", symbol_kinds)
starequals = TokenKind("*=", symbol_kinds)
divequals = TokenKind("/=", symbol_kinds)
modequals = TokenKind("%=", symbol_kinds)
twoequals = TokenKind("==", symbol_kinds)
notequal = TokenKind("!=", symbol_kinds)
bool_and = TokenKind("&&", symbol_kinds)
bool_or = TokenKind("||", symbol_kinds)
bool_not = TokenKind("!", symbol_kinds)
lt = TokenKind("<", symbol_kinds)
gt = TokenKind(">", symbol_kinds)
ltoe = TokenKind("<=", symbol_kinds)
gtoe = TokenKind(">=", symbol_kinds)
amp = TokenKind("&", symbol_kinds)
pound = TokenKind("#", symbol_kinds)
lbitshift = TokenKind("<<", symbol_kinds)
rbitshift = TokenKind(">>", symbol_kinds)
compl = TokenKind("~", symbol_kinds)

dquote = TokenKind('"', punctuator_kinds)
squote = TokenKind("'", punctuator_kinds)

open_paren = TokenKind("(", punctuator_kinds)
close_paren = TokenKind(")", punctuator_kinds)
open_brack = TokenKind("{", punctuator_kinds)
close_brack = TokenKind("}", punctuator_kinds)
open_sq_brack = TokenKind("[", punctuator_kinds)
close_sq_brack = TokenKind("]", punctuator_kinds)

comma = TokenKind(",", punctuator_kinds)
semicolon = TokenKind(";", punctuator_kinds)
dot = TokenKind(".", punctuator_kinds)
arrow = TokenKind("->", punctuator_kinds)
