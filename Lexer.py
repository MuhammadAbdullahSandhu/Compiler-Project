import Token
from Token import TokenType
from token_kind import keyword_kinds, symbol_kinds, punctuator_kinds
from errors import Errors

# Define Grammar
KEYWORDS = {keyword.value for keyword in keyword_kinds}
OPERATORS = {keyword.value for keyword in symbol_kinds}
MULTI_CHAR_OPERATORS = {keyword.value for keyword in symbol_kinds}
PUNCTUATION = {keyword.value for keyword in punctuator_kinds}

# Check if a string is a keyword
def is_Keyword(keyword):
    return keyword in KEYWORDS

# Check if a character is a single-character operator
def is_Operator(operator):
    return operator in OPERATORS

# Check if a string is a multi-character operator
def is_Multi_C_operator(multi_operator):
    return multi_operator in MULTI_CHAR_OPERATORS

# Check if a character is a punctuation mark
def is_Punctuation(punctuation):
    return punctuation in PUNCTUATION

# Lexical Analysis with Line Numbers and Error Handling for invalid tokens
def Lexer(input_string):
    tokens = []
    length = len(input_string)
    i = 0 
    line_number = 1  # Track the current line number
    
    while i < length:
        current_char = input_string[i]
        
        # Skip whitespace and track newlines
        if current_char in ' \t':
            i += 1
            continue
        if current_char == '\n':
            line_number += 1
            i += 1
            continue

        # Handle single-line comments
        if current_char == '/' and i + 1 < length and input_string[i + 1] == '/':
            start = i
            while i < length and input_string[i] != '\n':
                i += 1
            continue

        # Handle multi-line comments
        if current_char == '/' and i + 1 < length and input_string[i + 1] == '*':
            start = i
            i += 2
            while i + 1 < length and not (input_string[i] == '*' and input_string[i + 1] == '/'):
                if input_string[i] == '\n':
                    line_number += 1
                i += 1
            i += 2  # Skip closing */
            continue
         
            
        if current_char.isdigit():
            start = i
            is_decimal = False
            # Scan for numbers and handle decimals separately
            while i < length and (input_string[i].isdigit() or (input_string[i] == '.' and not is_decimal)):
                if input_string[i] == '.':
                    is_decimal = True  # We have encountered a decimal point
                i += 1

            # Handle the invalid case 
            if i < length and input_string[i].isalpha():
                print(f"Error: Invalid token '{input_string[start:i + 1]}' at line {line_number}")
                tokens.append(Token.Token(TokenType.UNKNOWN, input_string[start:i + 1], line_number))
                i += 1  # Skip the invalid character
            else:
                # Separate handling for decimals and integers
                if is_decimal:
                    # Decimal number case
                    tokens.append(Token.Token(TokenType.DECIMAL, input_string[start:i], line_number))
                else:
                    # Integer number case
                    tokens.append(Token.Token(TokenType.NUMBER, input_string[start:i], line_number))
            continue

        # Handle identifiers and keywords
        if current_char.isalpha() or current_char == '_':
            start = i
            while i < length and (input_string[i].isalnum() or input_string[i] == '_'):
                i += 1
            token_value = input_string[start:i]
            if is_Keyword(token_value):
                tokens.append(Token.Token(TokenType.KEYWORD, token_value, line_number))
            else:
                tokens.append(Token.Token(TokenType.IDENTIFIER, token_value, line_number))
            continue
        
        #  Handle multi-character operators including '++'
        if i + 1 < length and is_Multi_C_operator(input_string[i:i + 2]):
            tokens.append(Token.Token(TokenType.OPERATOR, input_string[i:i + 2], line_number))
            i += 2
            continue

        # Handle multi-character operators
        if i + 1 < length and is_Multi_C_operator(input_string[i:i + 2]):
            tokens.append(Token.Token(TokenType.OPERATOR, input_string[i:i + 2], line_number))
            i += 2
            continue

        # Handle single-character operators
        if is_Operator(current_char):
            tokens.append(Token.Token(TokenType.OPERATOR, current_char, line_number))
            i += 1
            continue
        
        # Handle punctuation
        if is_Punctuation(current_char):
            tokens.append(Token.Token(TokenType.PUNCTUATION, current_char, line_number))
            i += 1
            continue
        
        # Handle preprocessor directives
        if current_char == '#':
            start = i
            i += 1
            while i < length and input_string[i] != '\n':
                if input_string[i] == '\\':  
                    i += 1  # Skip continuation lines
                    continue
                i += 1
            tokens.append(Token.Token(TokenType.PREPROCESSOR, input_string[start:i], line_number))
            line_number += 1
            i += 1  # Skip the newline
            continue

        # Handle string literals
        if current_char == '"':
            start = i
            i += 1
            while i < length and (input_string[i] != '"' or input_string[i - 1] == '\\'):
                if input_string[i] == '\n':
                    line_number += 1
                i += 1
            i += 1  # Skip the closing quote
            tokens.append(Token.Token(TokenType.STRING_LITERAL, input_string[start:i], line_number))
            continue
        
        # Handle unknown characters (Invalid token)
        Errors.invalid_token(current_char,line_number)
        tokens.append(Token.Token(TokenType.UNKNOWN, current_char, line_number))
        i += 1

    return tokens
