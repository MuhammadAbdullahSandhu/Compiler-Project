import re
import Token
from errors import Errors

# Define token rules without preprocessors initially
token_rules = [
    ('COMMENT_SINGLE', r'//.*$'),  # Single-line comment
    ('COMMENT_MULTI', r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/'),  # Multi-line comment
    ('STRING', r'"(?:\\.|[^"\\])*"'),  # String literal
    ('CHAR', r"'(?:\\.|[^'\\])'"),  # Character literal
    ('KEYWORD', r'\b(?:auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|inline|int|long|register|restrict|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|_Alignas|_Alignof|_Atomic|_Bool|_Complex|_Generic|_Imaginary|_Noreturn|_Static_assert|_Thread_local)\b'),  # Keywords
    ('MULTI_CHAR_OPERATOR', r'(==|!=|<=|>=|\+\+|--|&&|\|\||<<|>>|->|/=|\*=|%=|\+=|-=|&=|\|=|\^=|<<=|>>=)'),  # Multi-character operators
    ('IDENTIFIER', r'\b[A-Za-z_]\w*\b'),  # Identifiers
    ('NUMBER',  r'\b[0-9]*\.[0-9]+|' + \
               r'0[0-7]*|' + \
               r'\b[1-9][0-9]*\b|' + \
               r'\b0\b' ),  # Numbers (hex, octal, decimal)
    ('OPERATOR', r'[+\-*/%=!<>&|^~]'),  # Single-character operators
    ('PUNCTUATION', r'[.,;(){}[\]:]'),  # Punctuation
    ('WHITESPACE', r'\s+'),  # Ignore spaces and tabs
    ('INVALID_NUMBER', r'\b0[bB][^01]+|0[bB]$|0[xX][^0-9a-fA-F]+|0[xX]$|\b\d+[A-Za-z]+\b'),  # Invalid numbers (e.g., 0b2, 123abc)
    ('INVALID', r'[^\s]+'),  # Invalid token (catch-all)
]

# Combine the token rules to a regex pattern
pattern = []
for pair in token_rules:
    token_type, token_regex = pair
    pattern.append(f"(?P<{token_type}>{token_regex})")

# Join the patterns into the final master pattern
token_pattern = '|'.join(pattern)

# Preprocessors will be separated 
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
        ignored_tokens = {'WHITESPACE', 'NEWLINE', 'COMMENT_SINGLE', 'COMMENT_MULTI'}
        
        # Remove preprocessors
        regular_tokens = re.sub(self.preprocessor_regex, '', self.code)
        
        # Track line numbers
        current_line = 1
        line_start = 0
        
        for match in self.regex.finditer(regular_tokens):
            token_type = match.lastgroup
            token_value = match.group(token_type)
            token_start = match.start()
            
            # Debugging output for tracking tokens
            print(f"Matched token: Type={token_type}, Value={token_value}, Line={current_line}")
            
            # Update line number
            line_increment = regular_tokens.count('\n', line_start, token_start)
            current_line += line_increment
            
            # Update line_start to the start of the current token's line
            line_start = token_start
            
            if token_type in ignored_tokens:
                if token_type == 'COMMENT_MULTI':
                    current_line += token_value.count('\n')
                continue
            
            if token_type == 'INVALID_NUMBER':
                Errors.invalid_token(token_value, current_line)
                tokens.append(Token.Token('INVALID', token_value, current_line))
                continue
            
            tokens.append(Token.Token(token_type, token_value, current_line))
        
        return tokens

    
    # Tokenize preprocessors after normal code tokenization
    def tokenize_preprocessors(self):
        preprocessors = []
        current_line = 1  # Track line numbers for preprocessors
        for match in self.preprocessor_regex.finditer(self.code):
            # Find the full match 
            token_value = match.group(0)  
            token_start = match.start()

            # Update line number for preprocessors
            line_increment = self.code.count('\n', 0, token_start)
            current_line += line_increment

            preprocessors.append(Token.Token("PREPROCESSOR", token_value, current_line))
        
        return preprocessors


