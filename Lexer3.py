import re
from Token import Token
import Token

# Define token rules
token_rules = [
    ('NUMBER',    r'\d+(\.\d*)?'),          
    ('IDENTIFIER', r'[A-Za-z_]\w*'),        
    ('STRING',    r'"(?:[^"\\]|\\.)*"'),   
    ('COMMENT',   r'//[^\n]*'),             
    ('MULTICOMMENT', r'/\*[\s\S]*?\*/'),    
    ('OPERATOR',  r'[+\-*/%=&|<>!^~]'),    
    ('PUNCTUATION', r'[.,;(){}[\]]'),       
    ('WHITESPACE', r'\s+'),                 
    ('NEWLINE',   r'\n'),   
    ('KEYWORD', r'\b(int|float|return|if|else|for|while|do|break|continue|void|char|double|switch|case|default)\b'),            
]

# Combine the token specifications into a single regex pattern
pattern_parts = [f"(?P<{pair[0]}>{pair[1]})" for pair in token_rules]
master_pattern = '|'.join(pattern_parts)

# Tokenizer class
class Lexer:
    def __init__(self, code):
        self.code = code
        self.regex = re.compile(master_pattern)
    
    def tokenize(self):
        tokens = []
        for match in self.regex.finditer(self.code):
            token_type = match.lastgroup
            token_value = match.group(token_type)
            if token_type in ('WHITESPACE', 'NEWLINE'):
                continue
            elif token_type in ('COMMENT', 'MULTICOMMENT'):
                continue
            yield token_type, token_value
            tokens.append(Token.Token(token_type, token_value))

# Example usage
if __name__ == '__main__':
    code = '''
    #include <stdio.h>

int main() {
    int arr[3] = {1, 2, 3}; // An array of integers
    int *ptr = arr;         // Pointer to the first element of the array

    // Print array elements using pointer arithmetic
    for (int i = 0; i < 3.5; i++) {
        printf("Element %d: %d\n", i, *(ptr + i));
        if ( a > b)
    '''
    
    lexer = Lexer(code)
    for token_type, token_value in lexer.tokenize():
        print(f"Token{{type={token_type:<15}, value='{token_value}'}}")
