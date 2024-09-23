from Token import TokenType
import Lexer
from AST import ProgramNode, FunctionNode, BlockNode, VariableDeclarationNode, ReturnNode, AssignmentNode, NumberNode, IdentifierNode
from MyGrammar import TokenKind
from Lexer import KEYWORDS
from token_kind import keyword_kinds
from SymbolTable import SymbolTable



class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_pos = 0
        self.global_symbol_table = SymbolTable(is_global=True)  
        self.local_symbol_table = self.global_symbol_table 
        self.symbol_table = SymbolTable()
        

    def current_token(self):
        if self.current_token_pos < len(self.tokens):
            return self.tokens[self.current_token_pos]
        return None

    def consume_token(self, token_type, values=None):
        token = self.current_token()
        
        # Check if the token type matches
        if token and token.t_type == token_type:
            # Check if values is a list/tuple and if the token's value matches any of the values
            if values is None or token.t_vale in values:
                self.current_token_pos += 1
                return token
            else:
                expected = f"{token_type} with value in {values}"
                raise SyntaxError(f"Unexpected token: {token}. Expected {expected}.")
        else:
            expected = token_type if values is None else f"{token_type} with value in {values}"
            raise SyntaxError(f"Unexpected token: {token}. Expected {expected}.")


    def parse(self):
        global_declarations = []
        functions = []
        print("Parsing program")

        while self.current_token() is not None:
            token = self.current_token()

            if token.t_type == TokenType.KEYWORD and token.t_vale in [TokenType.int_kw, TokenType.void_kw, TokenType.long_kw]:
                next_token = self.tokens[self.current_token_pos + 1]

                if next_token.t_type == TokenType.IDENTIFIER and (self.tokens[self.current_token_pos + 2].t_type != TokenType.PUNCTUATION or self.tokens[self.current_token_pos + 2].t_vale != TokenKind.open_paren):
                    global_declarations.append(self.parse_declaration())
                else:
                    functions.append(self.parse_function())
            else:
                raise SyntaxError(f"Unexpected token {token} before function or declaration")
       
        program = ProgramNode(functions)
        st = self.symbol_table
        print(f"AST:  {program}")
        print(f"{st}")
        print(self.symbol_table.lookup('i'))

        return global_declarations, functions

    def parse_function(self):
        print("Parsing function declaration")
        return_type = self.consume_token(TokenType.KEYWORD, [TokenType.int_kw, TokenType.void_kw, TokenType.long_kw])
        func_name = self.consume_token(TokenType.IDENTIFIER)

        # Define the function in the symbol table
        self.global_symbol_table.define(func_name.t_vale, return_type.t_vale)
        self.symbol_table.define(func_name.t_vale, return_type.t_vale)

        self.consume_token(TokenType.PUNCTUATION, TokenType.open_paren)
        self.consume_token(TokenType.PUNCTUATION, TokenType.close_paren)
        self.consume_token(TokenType.PUNCTUATION, TokenKind.open_brack)

        # Push a new scope for the function
        self.local_symbol_table = self.global_symbol_table.push_scope() 
        body = self.parse_block()  # parse_block will handle local variables
        self.global_symbol_table.pop_scope()  # Pop the function scope
        self.local_symbol_table = self.global_symbol_table 

        self.consume_token(TokenType.PUNCTUATION, TokenType.close_brack)
        if return_type.t_vale != TokenType.void_kw:
            if not any(isinstance(stmt, ReturnNode) for stmt in body.statements):
                raise SyntaxError(f"Function '{func_name.t_vale}' of type '{return_type.t_vale}' must return a value.")

        return FunctionNode(func_name.t_vale, body)

        
        
    def parse_block(self):
        statements = []
        print("Parsing block: statements")
        token = self.current_token()
        while token is not None and token.t_vale != TokenType.close_brack:
            token = self.current_token()
            if token.t_type == TokenType.KEYWORD and token.t_vale == TokenType.int_kw:
                # Parsing variable declaration
                statements.append(self.parse_declaration())
            else:
                # Parsing statement
                statements.append(self.parse_statement())
            token = self.current_token()  # Update token after each statement
        
        return BlockNode(statements)

    def parse_declaration(self):
        token = self.current_token()
        print("Parsing variable declaration")

        if token.t_type == TokenType.KEYWORD and token.t_vale in [TokenType.int_kw, TokenType.long_kw, TokenType.void_kw]:
            var_type = self.consume_token(TokenType.KEYWORD, [TokenType.int_kw, TokenType.long_kw, TokenType.void_kw])
            vari_name = self.consume_token(TokenType.IDENTIFIER)
            var_name = vari_name.t_vale

            # Define the variable in the symbol table
            self.symbol_table.define(var_name, var_type.t_vale)

            init_value = None
            token = self.current_token()
            if token and token.t_type == TokenType.OPERATOR and token.t_vale == TokenKind.equals:
                self.consume_token(TokenType.OPERATOR, TokenKind.equals)
                init_value = self.parse_expression()
            
            self.consume_token(TokenType.PUNCTUATION, TokenKind.semicolon)

            return VariableDeclarationNode(vari_name.t_vale, init_value)


    def parse_statement(self):
        print("Parsing statement")
        token = self.current_token()

        if token and token.t_type == TokenType.KEYWORD and token.t_vale == TokenType.return_kw:
            return self.parse_return_statement()

        elif token and token.t_type == TokenType.IDENTIFIER:
            return self.parse_assignment_statement()

        
    def parse_return_statement(self):
        print("Parsing return statement")
        self.consume_token(TokenType.KEYWORD, 'return') 
        value = self.parse_expression()  
        self.consume_token(TokenType.PUNCTUATION, ';')  
        return ReturnNode(value)

    def parse_assignment_statement(self):
        print("Parsing assignment statement")
        var_name = self.consume_token(TokenType.IDENTIFIER)  
        self.consume_token(TokenType.OPERATOR, TokenKind.equals)  
        value = self.parse_expression()  
        self.consume_token(TokenType.PUNCTUATION, TokenKind.semicolon)  
        
        return AssignmentNode(var_name.t_vale, value)

    def parse_expression(self):
        token = self.current_token()
        
        if token.t_type == TokenType.NUMBER:
            self.consume_token(TokenType.NUMBER)  
            return NumberNode(token.t_vale)
        
        elif token.t_type == TokenType.IDENTIFIER:
            var_name = token.t_vale
            self.consume_token(TokenType.IDENTIFIER)
            return IdentifierNode(var_name)

        else:
            raise SyntaxError(f"Unexpected token in expression: {token}")
