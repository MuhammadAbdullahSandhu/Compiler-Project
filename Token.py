
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

class Token:
    def __init__(self, type: TokenType, value: str):
        self.t_type = type
        self.t_vale = value

    def __str__(self):
          return f"Token{{type={self.t_type:<20} value='{self.t_vale}'}}"
    
    
    
    

    