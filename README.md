# Compiler Construction Project
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
# Lexer1:  
#### Keywords: "int", "float", "return", "if", "else", "for", "while", "do", "break", "continue", "void", "char", "double", "switch", "case", "default", "struct", "typedef", "enum", "union", "const", "volatile"
#### Operators: '+', '-', '*', '/', '=', '>', '<', '!', '%'
#### MULTI_CHAR_OPERATORS :"==", "!=", "<=", ">=", "--", "++", "&&", "<<", ">>", "*=", "%=", "+=", "-=", "&="
#### PUNCTUATION : '.', ',', ';', '(', ')', '{', '}','[',']',':'}

# Lexer3 
### The project relies on the re (regular expressions) module, which is part of the Python Standard Library.
### Features
#### Supports keywords, operators, punctuation, identifiers, and string literals.
#### Handles multi-line and single-line comments.
#### Tracks line numbers for each token, useful for error reporting.
#### Identifies invalid tokens, such as invalid number literals (4a) and unsupported symbols.
#### Handles multi-character operators like ++, ==, ,+= . 
#### Includes basic preprocessor directive tokenization (#define).

### Error Handling
The lexer will print an error message whenever it encounters an invalid token. For example, if you have the invalid token in the code, the lexer will output:
Error: Invalid token 'token' at line 'line No.'

# Parser
This parser is designed to analyze and construct the Abstract Syntax Tree (AST) for a simple programming language that includes features such as function definitions,
variable declarations, statements, and expressions. The parser processes the program in a hierarchical manner, breaking it down into manageable components, each of which is
associated with a corresponding node type in the AST.

## Overview of the Parsing Process
The entry point of the parsing process is the `parse()` method, which loops through the tokens in the source code and distinguishes between function declarations and variable declarations. Functions and declarations are parsed separately, and each creates an appropriate node in the AST. A function is identified by its return type and name, followed by parentheses and a block of code. Variable declarations can either be standalone or part of a function.
