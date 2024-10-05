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

### Overview of the Parsing Process
The entry point of the parsing process is the 'parse()' method, which loops through the tokens in the source code and distinguishes between function declarations and variable declarations. Functions and declarations are parsed separately, and each creates an appropriate node in the AST. A function is identified by its return type and name, followed by parentheses and a block of code. Variable declarations can either be standalone or part of a function.

### Function Parsing
Functions in the language consist of a return type ('int' or 'void'), an identifier (function name), a parameter list, and a block of statements. The parser defines each function in the global symbol table and sets up a new scope for the function body. The 'parse_function()' method creates a 'FunctionNode' to represent the function, which includes parameters and the body of the function (a block of statements). After parsing, the function is validated to ensure that if its return type is 'int', it contains a 'return' statement, and if its type is 'void', it doesn’t.

### Variable Declaration
Variable declarations are parsed using the 'parse_variable_declaration()' method. These declarations can be simple, such as 'int a;', or can include an initialization value, such as 'int a = 5;'. The type and identifier are stored in the symbol table for later reference, and the node is added to the AST. Multiple variables can be declared in the same line, separated by commas.

### Statement Parsing
The parser can handle different types of statements: return statements, assignment statements, if statements, for loops, and generic expressions. Each statement type has its dedicated parsing method:
#### Return statements are parsed by 'parse_return_statement()', which ensures that an expression is returned by the function.
#### Assignment statements ('a = 5;') are parsed by 'parse_assignment_statement()', which checks the types of both the variable and the expression to ensure consistency.
#### If statements and for loops are parsed using their respective methods ('parse_if_statement()' and 'parse_for_statement()'), and they handle conditional and loop logic. The parser ensures that conditional expressions evaluate to valid types.
#### Expressions are handled by 'parse_expression()', which can include arithmetic operations, identifiers, or numbers. Expressions are broken down into smaller parts like terms and factors, and are recursively parsed to construct a binary operation tree, if applicable.

### Expression Parsing
Expressions can consist of numbers, identifiers, or more complex arithmetic operations. The parser constructs a hierarchy using the 'BinaryOperationNode' class to represent expressions with operators such as '+', '-', '*', and '/'. 'parse_expression()' breaks down complex expressions into simple terms and factors, which are then combined into binary operation nodes, ensuring correct precedence and associativity.

### Scope Management and Symbol Table
The parser utilizes a symbol table to manage variable declarations and scope handling. Each block of code (such as a function body or loop) introduces a new scope, ensuring that variables are resolved according to their appropriate context. The symbol table supports nested scopes through the use of 'push_scope()' and tracks variable types to ensure consistency across assignments and operations.

### Abstract Syntax Tree (AST) Nodes
The AST is made up of various node types that correspond to different parts of the language:

     ProgramNode: Represents the entire program and holds all the functions.
     FunctionNode: Represents a function, holding the name, parameters, and body.
     BlockNode: Represents a block of statements (enclosed in curly braces '{}').
     VariableDeclarationNode: Represents a variable declaration, with an optional initializer.
     AssignmentNode: Represents an assignment of a value to a variable.
     ReturnNode: Represents a return statement.
     IfNode and ForStatementNode: Represent conditional and loop structures, respectively.
     NumberNode and IdentifierNode: Represent literal numbers and variable identifiers.
     BinaryOperationNode: Represents a binary operation such as 'a + b' or 'x * y'.

### Language Grammar
    program              :- (function | declaration)*
    function             :- return_type identifier "(" ")" block
    declaration          :- variable_declaration
    block                :- "{" (statement | variable_declaration)* "}"
    statement            :- return_statement 
                     | assignment_statement 
                     | if_statement
                     | for_statement
                     | expression ";"
    variable_declaration :- type identifier ";"
                     | type identifier "=" expression ";"
    return_statement     :- "return" expression ";"
    assignment_statement :- identifier "=" expression ";"
    if_statement         :- "if" "(" expression ")" block ( "else" block )?
    for_statement        :- "for" "(" (variable_declaration | assignment_statement)? ";" expression? ";" expression? ")" block
    expression           :- expression ( "+" | "-" | "*" | "/" ) expression
                     | "(" expression ")"
                     | NUMBER
                     | IDENTIFIER
    return_type          :- "int" | "void"
    type                 :- "int"
The language grammar defines the structure of the program. A program consists of multiple functions and declarations. Each function consists of a return type, an identifier (function name), and a block of statements. The block can contain various types of statements, such as return statements, assignment statements, and control flow structures like if statements and for loops. Expressions include basic arithmetic and can involve numbers, identifiers, or grouped expressions within parentheses.


