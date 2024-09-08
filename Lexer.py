from Token import TokenType

KEYWORDS = {"if", "else", "while", "for", "return"}  
OPERATORS = {'+', '-', '*', '/', '=', '==', '!=', '<', '>'}  
PUNCTUATION = {'.', ',', ';', '(', ')', '{', '}'} 

class Token:
    def __init__(self, type: TokenType, value: str):
        self.t_type = type
        self.t_vale = value

    def __str__(self):
            return f"Token   <type={self.t_type}, value'{self.t_vale}'>"
    
# Keywords 
def check_keyword(s_string: str):
    return s_string in KEYWORDS
# Operators
def check_operator(o_ch: chr):
    return o_ch in OPERATORS
# Punctuation
def check_punctuation(p_ch: chr):
    return p_ch in PUNCTUATION

def lexer(input: str):
    tokens = []
    current_token = []

    i = 0
    while i < len(input):
        current_char = input[i]

    # check if its whitespace
        if current_char in ' \t\n\r':
            i += 1
            continue

    # check if its numbers
        if '0' <= current_char <= '9':
            current_token.clear()  
            while i < len(input) and '0' <= input[i] <= '9':
                current_token.append(input[i])
                i += 1
            tokens.append(Token(TokenType.NUMBER, ''.join(current_token)))
            continue

        # check if its identifiers and keywords
        elif ('A' <= current_char <= 'Z') or ('a' <= current_char <= 'z') or current_char == '_':
            current_token.clear() 
            while i < len(input) and (('A' <= input[i] <= 'Z') or 
                                      ('a' <= input[i] <= 'z') or 
                                      ('0' <= input[i] <= '9') or 
                                      input[i] == '_'):
                current_token.append(input[i])
                i += 1
            token_value = ''.join(current_token)
            if check_keyword(token_value):
                tokens.append(Token(TokenType.KEYWORD, token_value))
            else:
                tokens.append(Token(TokenType.IDENTIFIER, token_value))
            continue

        
        elif check_operator(current_char):
            tokens.append(Token(TokenType.OPERATOR, current_char))
            i += 1
            continue

        
        elif check_punctuation(current_char):
            tokens.append(Token(TokenType.PUNCTUATION, current_char))
            i += 1
            continue

        
        tokens.append(Token(TokenType.UNKNOWN, current_char))
        i += 1

    return tokens
