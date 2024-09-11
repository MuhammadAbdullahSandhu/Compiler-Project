import re
import Token

# Define token rules without preprocessors initially
token_rules = [
    ('KEYWORD', r'\b(?:auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|inline|int|long|register|restrict|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|_Alignas|_Alignof|_Atomic|_Bool|_Complex|_Generic|_Imaginary|_Noreturn|_Static_assert|_Thread_local)\b'),
    ('IDENTIFIER', r'\b[A-Za-z_]\w*\b'),
    ('OPERATOR', r'[+\-*/%=!<>&|^~]'),
    ('MULTI_CHAR_OPERATOR', r'(==|!=|<=|>=|\+\+|--|&&|\|\||<<|>>|->|/=|\*=|%=|\+=|-=|&=|\|=|\^=|<<=|>>=)'),
    ('NUMBER', r'\b0[xX][0-9a-fA-F]+|0[0-7]*|[1-9][0-9]*\b'),
    ('PUNCTUATION', r'[.,;(){}[\]:]'),
    ('STRING', r'"(?:\\.|[^"\\])*"'),
    ('CHAR', r"'(?:\\.|[^'\\])'"),
    ('COMMENT_SINGLE', r'//.*$'),
    ('FLOAT', r'\b\d+\.\d+([eE][+-]?\d+)?|\.\d+([eE][+-]?\d+)?|\d+\.[eE][+-]?\d+\b'),
    ('COMMENT_MULTI', r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/'),
]

# Combine the token rules to regex patteren 
pattern = []
for pair in token_rules:
    token_type, token_regex = pair
    pattern.append(f"(?P<{token_type}>{token_regex})")

# Join the patterns into the final master pattern
token_pattern = '|'.join(pattern)

# preprocessors will be seprated 
pre_p_pattern = r'#\s*(include|define|ifdef|ifndef|endif|undef|pragma)[^\n]*'

# Tokenizer class
class Lexer:
    def __init__(self, code):
        self.code = code
        # Compile the regex patterns
        self.regex = re.compile(token_pattern, re.DOTALL) 
        self.preprocessor_regex = re.compile(pre_p_pattern, re.DOTALL)

    # Tokenize regular code (excluding preprocessors)
    def tokenize(self):
        tokens = []
        ignored_tokens = {'WHITESPACE', 'NEWLINE', 'COMMENT', 'COMMENT_SINGLE', 'COMMENT_MULTI'}
        
        # Remove preprocessor
        regular_tokens = re.sub(self.preprocessor_regex, '', self.code)
        for match in self.regex.finditer(regular_tokens):
            token_type = match.lastgroup
            token_value = match.group(token_type)
                
            if token_type in ignored_tokens:
                continue
            
            tokens.append(Token.Token(token_type, token_value))
        return tokens

    # Tokenize preprocessors after normal code tokenization
    def tokenize_preprocessors(self):
        preprocessors = []
        for match in self.preprocessor_regex.finditer(self.code):
            # Find the full match 
            token_value = match.group(0)  
            preprocessors.append(Token.Token("PREPROCESSOR", token_value))
        return preprocessors
