from typing import List
from enum import Enum
from Token import TokenType

KEYWORDS = {"if", "else", "while", "for", "return"}  # Example keywords
OPERATORS = {'+', '-', '*', '/', '=', '==', '!=', '<', '>'}  # Example operators
PUNCTUATION = {'.', ',', ';', '(', ')', '{', '}'}  # Example punctuation

class Token:
    def __init__(self, type: TokenType, value: str):
        self.t_type = type
        self.t_vale = value

    def __str__(self) -> str:
          return f"Token{{type={self.t_type}, value='{self.t_vale}'}}"
    
    

# Keywords 
def keyword(s_string: str) -> bool:
    return s_string in KEYWORDS
# Operators
def operator(o_ch: str) -> bool:
    return o_ch in OPERATORS
# Punctuation
def punctuation(p_ch: str) -> bool:
    return p_ch in PUNCTUATION


def lexer(input: str) -> List[Token]:
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
            current_token.clear()  # Reset token
            while i < len(input) and '0' <= input[i] <= '9':
                current_token.append(input[i])
                i += 1
            tokens.append(Token(TokenType.NUMBER, ''.join(current_token)))
            continue

      

    return tokens
