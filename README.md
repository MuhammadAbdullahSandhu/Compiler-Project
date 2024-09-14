### Compiler Construction Project
#### Tokenize .C file 
#### SUPPORTED TOKENS
    NUMBER 
    KEYWORD
    IDENTIFIER 
    OPERATOR 
    PUNCTUATION 
    PREPROCESSOR
    UNKNOWN
    COMMENT
### Lexer for Simple Programming Language (Lexer1)
#### This repository contains a lexer for a simple programming language. The lexer processes an input string of code and breaks it into tokens such as keywords, operators, identifiers, and punctuation. It also includes error handling for invalid tokens and tracks line numbers (Lexer 1).
### Lexer3 The project relies on the re (regular expressions) module, which is part of the Python Standard Library.

### Features
#### Supports keywords, operators, punctuation, identifiers, and string literals.
#### Handles multi-line and single-line comments.
#### Tracks line numbers for each token, useful for error reporting.
#### Identifies invalid tokens, such as invalid number literals (4a) and unsupported symbols.
#### Handles multi-character operators like ++, ==, ,+= . 
#### Includes basic preprocessor directive tokenization (#define).

### Error Handling
#### The lexer will print an error message whenever it encounters an invalid token. For example, if you have the invalid token in the code, the lexer will output:
Error: Invalid token 'token' at line 'line No.'
