from Token import TokenType
import Lexer
from AST import FunctionNode, BlockNode, VariableDeclarationNode, ReturnNode, AssignmentNode, NumberNode, IdentifierNode

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_pos = 0

    def current_token(self):
        if self.current_token_pos < len(self.tokens):
            return self.tokens[self.current_token_pos]
        return None

    def consume_token(self, token_type, value=None):
        token = self.current_token()
        if token and token.t_type == token_type and (value is None or token.t_vale == value):
            print(f"Consuming token: {token}")
            self.current_token_pos += 1
            return token
        else:
            expected = token_type if value is None else f"{token_type} with value '{value}'"
            raise SyntaxError(f"Unexpected token: {token}. Expected {expected}.")

    def parse(self):
        functions = []
        print("Parsing program")
        while self.current_token() is not None:
            functions.append(self.parse_function())
        # Test printing AST
        print("AST:", functions)  
        return functions

    def parse_function(self):
        print("Parsing function :- statement")
        token = self.current_token()
        fun_name = self.current_token()

        # For 'int'
        return_type = self.consume_token(TokenType.KEYWORD ) 
        # For 'main' 
        func_name = self.consume_token(TokenType.IDENTIFIER)  
        # For '('
        self.consume_token(TokenType.PUNCTUATION)  
        # For ')'
        self.consume_token(TokenType.PUNCTUATION) 
        # For '{' 
        self.consume_token(TokenType.PUNCTUATION)  
         # Parse the function block
        body = self.parse_block() 
        # For '}'
        self.consume_token(TokenType.PUNCTUATION)  
            
        print(f"Function name: {fun_name.t_vale}")
        print(f"Function name: {return_type.t_vale}")
        return FunctionNode(return_type.t_vale, func_name.t_vale, body)
        
        

    def parse_block(self):
        statements = []
        print("Parsing block :- statements")
        while self.current_token() is not None and self.current_token().t_vale != '}':
            if self.current_token().t_type == TokenType.KEYWORD and self.current_token().t_vale == 'int':
                # parsing variable declaration
                statements.append(self.parse_declaration())  
            else:
                 # Parsing statement
                statements.append(self.parse_statement()) 
        return BlockNode(statements)

    def parse_declaration(self):
        print("Parsing variable declaration")
        # parsing keywords like 'int' 'void'
        var_type = self.consume_token(TokenType.KEYWORD)  
        # parsing variable name
        vari_name = self.consume_token(TokenType.IDENTIFIER)  
        init_value = None
        var_name = self.current_token().t_vale
        
        # chech = expression
        if self.current_token() and self.current_token().t_type == TokenType.OPERATOR and self.current_token().t_vale == '=':
            # Parse '='
            self.consume_token(TokenType.OPERATOR, '=')  
            # Parse the expression after '='
            init_value = self.parse_expression()  
        # parsing ';'
        self.consume_token(TokenType.PUNCTUATION, ';')  
        
        print(f"Declared variable: {var_name}")
        return VariableDeclarationNode(var_type.t_vale, vari_name.t_vale, init_value)
        

    def parse_statement(self):
        print("Parsing statement :- expression or return statement")
        token = self.current_token()

        if token and token.t_type == TokenType.KEYWORD and token.t_vale == 'return':
             # parsing 'return'
            self.consume_token(TokenType.KEYWORD, 'return') 
            # parsing expression after return
            value = self.parse_expression()  
            # parsing ';'
            self.consume_token(TokenType.PUNCTUATION, ';')  
            return ReturnNode(value)

        elif token and self.current_token().t_type == TokenType.IDENTIFIER:
            var_name = self.consume_token(TokenType.IDENTIFIER)  
            # parsing variable name
            self.consume_token(TokenType.OPERATOR, '=')  
            # parsing the expression after '='
            value = self.parse_expression()  
            self.consume_token(TokenType.PUNCTUATION, ';')  
            return AssignmentNode(var_name.t_vale, value)

    def parse_expression(self):
        token = self.current_token()
        # parsing number
        if token.t_type == TokenType.NUMBER:
            self.consume_token(TokenType.NUMBER)  
            return NumberNode(token.t_vale)
        # parsing identifier
        elif token.t_type == TokenType.IDENTIFIER:
            self.consume_token(TokenType.IDENTIFIER)  
            return IdentifierNode(token.t_vale)

        else:
            raise SyntaxError(f"Unexpected token in expression: {token}")
