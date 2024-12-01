# Compiler Construction Project
#### Tokenize .C file 
#### Lexical Analyzer
#### Overview
This project implements a Lexical Analyzer (Lexer) and a Parser for tokenizing and parsing source code. It is designed to process input code, break it down into tokens, and parse it according to a predefined grammar. Additionally, the lexer handles error detection for invalid tokens and tracks line numbers for each token.
The key components of this project include:
            
        Lexer: Breaks down source code into tokens.
        Token: Represents individual tokens with types and values.
        TokenKind: Categorizes tokens as keywords, symbols, or punctuators.
        Parser: Parses the tokens into meaningful syntax structures.
        Main Program: Coordinates the lexer and parser and provides a command-line interface for users.
        
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
This parser is designed to analyze tokens from a simple programming language, validate their syntax, and construct an Abstract Syntax Tree (AST) for constructs like function definitions, 
variable declarations, statements, expressions, and control flow. In addition to building the AST, the parser manages variable and function scopes using a symbol table, and generates 
three-address code (TAC) for intermediate code representation, facilitating further optimization and code generation steps.

### Overview of the Parsing Process
The primary entry point for parsing is the parse() method. It loops through the tokens of the source code and identifies the different constructs, distinguishing between global declarations (variables) and function definitions. Each recognized construct is represented by a specific node in the AST. Functions are identified by a return type (int or void), followed by an identifier, parameter list, and block of code. Variable declarations can occur globally or within functions, with optional initialization.

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

     ProgramNode: Root node representing the entire program.
     FunctionNode: Represents a function, with its name, parameters, and body.
     BlockNode: Represents a block of statements, with each block introducing a new scope.
     VariableDeclarationNode: Represents variable declarations, with optional initial values.
     AssignmentNode: Represents variable assignments.
     ReturnNode: Represents return statements within functions.
     IfNode: Represents if statements, with optional else blocks.
     ForStatementNode: Represents for loops, handling initialization, condition, and increment.
     FunctionCallNode: Represents function calls within expressions or statements.
     BinaryOperationNode: Represents binary operations, like addition or multiplication, ensuring operator precedence.
     NumberNode and IdentifierNode: Represent literal numbers and variable identifiers in expressions.

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
            
            # Expression Grammar with Precedence Levels
            expression           :- additive_expression
            
            additive_expression  :- multiplicative_expression ( ("+" | "-") multiplicative_expression )*
            
            multiplicative_expression :- primary_expression ( ("*" | "/") primary_expression )*
            
            primary_expression   :- "(" expression ")" 
                                 | NUMBER
                                 | IDENTIFIER
            
            return_type          :- "int" | "void"
            type                 :- "int"

The language grammar defines the structure of the program. A program consists of multiple functions and declarations. Each function consists of a return type, an identifier (function name), and a block of statements. The block can contain various types of statements, such as return statements, assignment statements, and control flow structures like if statements and for loops. Expressions include basic arithmetic and can involve numbers, identifiers, or grouped 
expressions within parentheses. The  grammar supports basic programming constructs with specific types and a order of operation precedence. It allows for function declarations and variable declarations with types limited to integers 
(int) and floating-point numbers (float). Functions can have a return type of either int or void, indicating whether or not they return a value. Within expressions, operations follow a strict precedence hierarchy: parentheses and 
literals (NUMBER or IDENTIFIER) have the highest precedence, allowing specific sub-expressions to be evaluated first. Multiplicative operations (multiplication * and division /) follow, ensuring they are calculated before additive 
operations. Finally, additive operations (addition + and subtraction -) have the lowest precedence. This precedence order is left-associative, meaning that expressions with operators of the same precedence level are evaluated from left 
to right. This design allows the grammar to support complex expressions while ensuring consistent and predictable evaluation order, even in the presence of mixed operators.

### Three Address Code Generation
The Three_address_code class generates three-address code (TAC) from an Abstract Syntax Tree (AST), creating an intermediate representation for easier optimization and code generation. The class manages temporary variables (t1, t2, etc.) and labels (L1, L2, etc.) to represent intermediate values and control flow points. The main method, generate(node), dynamically dispatches to specific methods for each AST node type, such as ProgramNode for the program root, FunctionNode for functions, IfNode for conditionals, and ForStatementNode for loops. These methods append appropriate TAC instructions to self.code.
Statements and expressions within functions are parsed by methods like BlockNode, VariableDeclarationNode, and AssignmentNode. Control flow constructs like IfNode and ForStatementNode generate conditional branches and looping constructs with labels, while BinaryOperationNode handles arithmetic by generating intermediate results. Leaf nodes, NumberNode and IdentifierNode, handle literals and identifiers, ensuring values are properly represented. The class also supports function calls via FunctionCallNode, assigning results to temporary variables. print_code() displays the TAC in a numbered, tabular format, aiding debugging and verification. Overall, Three_address_code converts AST structures into a structured TAC format, making it suitable for further optimization and code generation.

### Optimzations ( Optimized Three address code)
The Three Address Code (TAC) Optimizer is using constant propagation, constant folding, condition folding, dead code elimination, and return value optimization, the optimizer refines the TAC during program execution, making the code more streamlined and efficient. These optimizations are applied together as the program runs, allowing seamless integration and cumulative improvements. 

This optimizer works particularly well with small test cases, especially those involving if-else statements. It simplifies conditions by replacing variables with constant values when available, folding constant expressions, and evaluating static conditional branches. For example, in cases where the outcome of a conditional statement is known at compile time, the optimizer removes the false branch of the code block, leaving only the reachable instructions. This targeted dead code elimination ensures that only unnecessary parts of the conditional blocks are removed, preserving essential logic while eliminating inefficiencies. The code elimination is does not include the unused variable. the unused variables will remains in the optimized three address code.

The optimizer is designed to handle **integer data** types exclusively, ensuring that arithmetic and logical operations are optimized correctly. It tracks constant values throughout the code, updating assignments, conditions, and even return statements to reflect these constants. By combining these optimizations, the TAC optimizer not only improves runtime performance but also creates a cleaner, more maintainable intermediate representation, making it particularly useful for small-scale scenarios and educational purposes.


