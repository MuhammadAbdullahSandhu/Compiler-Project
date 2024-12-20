from Token import TokenType
from AST import (
    ProgramNode, FunctionNode, BlockNode, VariableDeclarationNode, 
    ReturnNode, AssignmentNode, NumberNode, IdentifierNode, 
    BinaryOperationNode, IfNode, ForStatementNode, FunctionCallNode, PostDecrementNode, PostIncrementNode
)
from token_kind import symbol_kinds
from SymbolTable import SymbolTable
import token_kind
import TAC
from optimize_tac2 import Optimizer
import Assembly_g


# https://docs.python.org/3/library/ast.html
# https://github.com/ShivamSarodia/ShivyC/tree/master/shivyc/parser

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_pos = 0
        self.global_symbol_table = SymbolTable(is_global=True)  
        self.local_symbol_table = self.global_symbol_table 
        

    def current_token(self):
        if self.current_token_pos < len(self.tokens):
            return self.tokens[self.current_token_pos]
        return None

    def consume_token(self, token_type, values=None):
        token = self.current_token()
        
        # Check if the token type matches
        if token and token.t_type in token_type:
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

#--------------------------------------------------------------------------------------------------------------------------------------------
    # Main parse function to process the entire program
    def parse(self):
        global_declarations = []
        functions = []

        print("Parsing program")

        while self.current_token() is not None:
            token = self.current_token()

            if token.t_type == TokenType.KEYWORD and token.t_vale in [token_kind.int_kw.value, token_kind.void_kw.value]:
                next_token = self.tokens[self.current_token_pos + 1]

                if next_token.t_type == TokenType.IDENTIFIER:
                    # Check if it's a global variable declaration
                    if self.tokens[self.current_token_pos + 2].t_type != TokenType.PUNCTUATION or self.tokens[self.current_token_pos + 2].t_vale != token_kind.open_paren.value:
                        global_declarations.append(self.parse_variable_declaration())
                    else:
                        self.local_symbol_table = self.local_symbol_table.push_scope()
                        functions.append(self.parse_function())
                        self.local_symbol_table = self.local_symbol_table.parent
                else:
                    raise SyntaxError(f"Expected identifier after keyword, found {next_token}.")
            else:
                raise SyntaxError(f"Unexpected token {token} before function or declaration.")
        
        program = ProgramNode(global_declarations, functions)
        symbol_table = self.local_symbol_table
        #AST = program.to_string()
        #print(f"AST:  {AST}")
        #print(f"Symbol Table{symbol_table}") 
        
        # 3 address code
        tac_code = TAC.Three_address_code()  # Pass symbol table
        #tac_code.generate(program)
        #tac_code.print_code()

        #this code will show after optimization
        # tac_code = op_Three_address_code()  # Pass symbol table
        # tac_code.generate(program)
        # tac_code.print_code()
        #optimizer = Optimizer(tac_code.code)
        #optimizer.optimize()

        # Print the optimized TAC
        #optimizer.print_optimized_code()

        #print (tac_code.code)
        #gcc_asm = tac_to_gcc_asm(tac_code.code)
        #for line in gcc_asm:
        #  print(line)
        

        
        
        return global_declarations, functions ,program, symbol_table, tac_code

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def parse_variable_declaration(self):
        print("Parsing variable declaration")
        token = self.current_token()
        
        # Check for the type keyword (like 'int')
        if token.t_type == TokenType.KEYWORD and token.t_vale in [token_kind.int_kw.value,token_kind.float_kw.value]:
            var_type = self.consume_token(TokenType.KEYWORD)
            init_value = None  
            # hold variable names
            var_names = []  

            # Parse the first identifier
            vari_name = self.consume_token(TokenType.IDENTIFIER)
            var_names.append(vari_name.t_vale)

            # Check for multiple variable declarations 
            while True:
                token = self.current_token()
                if token.t_type == TokenType.PUNCTUATION and token.t_vale == token_kind.comma.value:
                    self.consume_token(TokenType.PUNCTUATION, token_kind.comma.value) 
                    vari_name = self.consume_token(TokenType.IDENTIFIER) 
                    var_names.append(vari_name.t_vale)
                else:
                    break

            # Define all variables in the symbol table
            for var_name in var_names:
                self.local_symbol_table.define(var_name, var_type.t_vale)

            # Check for initialization
            token = self.current_token()
            if token and token.t_type == TokenType.OPERATOR and token.t_vale == token_kind.equals.value:
                self.consume_token(TokenType.OPERATOR, token_kind.equals.value) 
                init_value = self.parse_expression()  
                
                # Check types for each variable
                # Type checking
                for var_name in var_names:
                    if isinstance(init_value, NumberNode):
                        if var_type.t_vale == "int" and "." in str(init_value.value):
                            raise TypeError(f"Cannot assign a float value '{init_value.value}' to integer variable '{var_name}'.")
                    self.local_symbol_table.set_value(var_name, init_value)

            self.consume_token(TokenType.PUNCTUATION, token_kind.semicolon.value)  
            return VariableDeclarationNode(var_names, init_value)  
        else:
            raise SyntaxError(f"Expected a variable declaration, found {token}.")



#----------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Parse the function with parameters and without parameters, null if function has no parameter
    def parse_function(self):
        parameters = []
        print("Parsing function declaration")
        fun_type = self.consume_token(TokenType.KEYWORD, [token_kind.int_kw.value, token_kind.void_kw.value])
        func_name = self.consume_token(TokenType.IDENTIFIER)
        
        # Define the function in the global symbol table
        self.global_symbol_table.define(func_name.t_vale, fun_type.t_vale)

        self.consume_token(TokenType.PUNCTUATION, token_kind.open_paren.value)

        # Push a new scope for function parameters and body
        self.local_symbol_table = self.local_symbol_table.push_scope()

        # Parse parameters
        token = self.current_token()
        if token.t_type != TokenType.PUNCTUATION or token.t_vale != token_kind.close_paren.value:
            while True:
                param_type = self.consume_token(TokenType.KEYWORD, [token_kind.int_kw.value])
                param_name = self.consume_token(TokenType.IDENTIFIER)
                
                # Check if there's a default value assignment
                f_value = None
                if self.current_token().t_type == TokenType.OPERATOR and self.current_token().t_vale == token_kind.equals.value:
                    self.consume_token(TokenType.OPERATOR, token_kind.equals.value)

                    # Parse the default value expression
                    f_value = self.parse_expression()  

                # Define parameter in the local scope
                self.local_symbol_table.define(param_name.t_vale, param_type.t_vale,f_value)
                parameters.append((param_type, param_name, f_value))
                
                token = self.current_token()
                if token.t_type == TokenType.PUNCTUATION and token.t_vale == token_kind.comma.value:
                    self.consume_token(TokenType.PUNCTUATION, token_kind.comma.value)
                else:
                    break

        self.consume_token(TokenType.PUNCTUATION, token_kind.close_paren.value)
        self.consume_token(TokenType.PUNCTUATION, token_kind.open_brack.value)

        # Parse the function body
        body = self.parse_block()

        # Pop the function scope
        self.local_symbol_table = self.local_symbol_table.parent

        self.consume_token(TokenType.PUNCTUATION, token_kind.close_brack.value)
        if fun_type.t_vale != token_kind.void_kw.value:

            if not self.return_check(body):
                raise SyntaxError(f"Function '{func_name.t_vale}' of type '{fun_type.t_vale}' must return a value.")

            
        elif fun_type.t_vale == token_kind.void_kw.value:
            if any(isinstance(stmt, ReturnNode) for stmt in body.statements):
                raise SyntaxError(f"Function '{func_name.t_vale}' of type '{fun_type.t_vale}' doesn't return a value.")
    
        return FunctionNode(func_name.t_vale, parameters, body)   
    
    "check the branch of if statment for the return node"
    def return_check(self, node):
        if isinstance(node, ReturnNode):
            return True
        if isinstance(node, BlockNode):
            return any(self.return_check(stmt) for stmt in node.statements)
        if isinstance(node, IfNode):
            then_has_return = self.return_check(node.then_block)
            else_has_return = self.return_check(node.else_block) if node.else_block else False
            return then_has_return and else_has_return
        return False
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Parse Block    
    def parse_block(self):
        print("Parsing block: statements")
        self.local_symbol_table = self.local_symbol_table.push_scope()  # Push a new block scope
        statements = []

        token = self.current_token()
        while token is not None and token.t_vale != token_kind.close_brack.value:
            token = self.current_token()
            if token.t_type == TokenType.KEYWORD and token.t_vale in [token_kind.int_kw.value,token_kind.float_kw.value]:
                statements.append(self.parse_variable_declaration())
            else:
                statements.append(self.parse_statement())
            token = self.current_token()

        # Pop the block scope
        self.local_symbol_table = self.local_symbol_table.parent  
        return BlockNode(statements)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------    
    
    # Parse Statement 
    def parse_statement(self):
        print("Parsing statement")
        token = self.current_token()

        if token and token.t_type == TokenType.KEYWORD and token.t_vale == token_kind.return_kw.value:
            return self.parse_return_statement()

        elif token and token.t_type == TokenType.IDENTIFIER:
            # If the next token is an open parenthesis, it's a function call
            next_token = self.tokens[self.current_token_pos + 1]
            if next_token.t_type == TokenType.PUNCTUATION and next_token.t_vale == token_kind.open_paren.value:
                func_call = self.parse_factor() 
                self.consume_token(TokenType.PUNCTUATION, token_kind.semicolon.value)
                return func_call

            # Otherwise, treat it as an assignment statement
            elif next_token.t_type == TokenType.OPERATOR and next_token.t_vale == token_kind.equals.value:
                return self.parse_assignment_statement()

            elif next_token.t_type == TokenType.OPERATOR and next_token.t_vale in [token_kind.incr.value, token_kind.decr.value]:
                expr = self.parse_factor()
                self.consume_token(TokenType.PUNCTUATION, token_kind.semicolon.value)
                return expr

            else:
                raise SyntaxError(f"Unexpected token {next_token}, expected assignment or function call.")

        elif token and token.t_type in [TokenType.NUMBER, TokenType.IDENTIFIER, token_kind.open_brack.value]:
            expr_value = self.parse_expression()
            self.consume_token(TokenType.PUNCTUATION, token_kind.semicolon.value)
            return expr_value

        elif token and token.t_type == TokenType.KEYWORD and token.t_vale == token_kind.if_kw.value:
            return self.parse_if_statement()

        elif token and token.t_type == TokenType.KEYWORD and token.t_vale == token_kind.for_kw.value:
            return self.parse_for_statement()

        else:
            raise SyntaxError(f"Unexpected Token, found {token}.")

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Parse Return Statment    
    def parse_return_statement(self):
        print("Parsing return statement")
        self.consume_token(TokenType.KEYWORD, token_kind.return_kw.value) 
        value = self.parse_expression()  
        self.consume_token(TokenType.PUNCTUATION, token_kind.semicolon.value)  
        return ReturnNode(value)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Parse Assignment Statement
    def parse_assignment_statement(self):
        print("Parsing assignment statement")
        var_name = self.consume_token(TokenType.IDENTIFIER)  
        # expected_type = self.local_symbol_table.lookup(var_name.t_vale)
        # print(f'expected type = {expected_type}')
        self.consume_token(TokenType.OPERATOR, token_kind.equals.value)  
        value_node = self.parse_expression()
        
        self.local_symbol_table.set_value(var_name.t_vale, value_node)
        self.consume_token(TokenType.PUNCTUATION, token_kind.semicolon.value)  
        return AssignmentNode(var_name.t_vale, value_node)
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Parse If Statement (If else only)
    def parse_if_statement(self):
        print("Parsing if statement")
        self.consume_token(TokenType.KEYWORD, [token_kind.if_kw.value])
        self.consume_token(TokenType.PUNCTUATION, token_kind.open_paren.value)
        # Parse the condition
        token = self.current_token()
        condition = self.parse_expression()
        self.consume_token(TokenType.PUNCTUATION, token_kind.close_paren.value)
        self.consume_token(TokenType.PUNCTUATION, token_kind.open_brack.value)
        then_block = self.parse_block() 
        self.consume_token(TokenType.PUNCTUATION, token_kind.close_brack.value)
        else_block = None
        token = self.current_token()
        if token and token.t_type == TokenType.KEYWORD and token.t_vale == token_kind.else_kw.value:
            self.consume_token(TokenType.KEYWORD, [token_kind.else_kw.value])
            self.consume_token(TokenType.PUNCTUATION, token_kind.open_brack.value)
            else_block = self.parse_block()
            self.consume_token(TokenType.PUNCTUATION, token_kind.close_brack.value)

        return IfNode(condition, then_block, else_block)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Parse Argument 
    def parse_arguments(self):
        print("Parsing function arguments")
        arguments = []

        # Handle case with no arguments
        if self.current_token().t_type == TokenType.PUNCTUATION and self.current_token().t_vale == token_kind.close_paren.value:
            return arguments

        # Parse arguments separated by commas
        while True:
            arg = self.parse_expression()  # Parse each argument as an expression
            arguments.append(arg)

            # If the next token is a comma, continue parsing more arguments
            if self.current_token().t_type == TokenType.PUNCTUATION and self.current_token().t_vale == token_kind.comma.value:
                self.consume_token(TokenType.PUNCTUATION, token_kind.comma.value)
            else:
                break

        return arguments

#----------------------------------------------------------------------------------------------------------------------------------------------------------------   
    # Parse For loop 
    def parse_for_statement(self):
        print("Parsing for loop")
        self.consume_token(TokenType.KEYWORD, token_kind.for_kw.value)
        self.consume_token(TokenType.PUNCTUATION, token_kind.open_paren.value)
        
        # Parse initialization a variable declaration or assignment or empty
        init_stmt = None

        # Get the current token
        token = self.current_token()  
        if token.t_type == TokenType.KEYWORD and token.t_vale == token_kind.int_kw.value:
            init_stmt = self.parse_variable_declaration()  
        elif token.t_type == TokenType.IDENTIFIER:
            init_stmt = self.parse_assignment_statement() 
        #print(f'init_stmt{init_stmt}')
        # Update the token to parse the condition
        token = self.current_token()
        
        # Parse the condition expression leave it empty if it is a null condition
        condition_expr = None
        if token.t_type != TokenType.PUNCTUATION or token.t_vale != token_kind.semicolon.value:
            condition_expr = self.parse_expression()  
        #print(f'condition_expr{condition_expr}')
        self.consume_token(TokenType.PUNCTUATION, token_kind.semicolon.value)
        
        # Update the token to parse the increment expression
        token = self.current_token()
        
        # Parse the increment expression leave it empty if there is no increment)
        increment_expr = None
        if token.t_type != TokenType.PUNCTUATION or token.t_vale != token_kind.close_paren.value:
            increment_expr = self.parse_expression()  

        self.consume_token(TokenType.PUNCTUATION, token_kind.close_paren.value)
        self.consume_token(TokenType.PUNCTUATION, token_kind.open_brack.value)
        # Parse the block of statements for loop body
        loop_body = self.parse_block()
        self.consume_token(TokenType.PUNCTUATION, token_kind.close_brack.value)
        #print(f'loop_body{loop_body}')
        return ForStatementNode(init_stmt, condition_expr, increment_expr, loop_body)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Parse Term setting up AST (left    operator     right)
    # LHS (Left-Hand Side): This is typically the first operand encountered.
    # Operator: This is the operator token that connects LHS and RHS.
    # RHS (Right-Hand Side): This is the operand that comes after the operator.
    def parse_term(self):
        # Parse the first factor
        left = self.parse_factor()  
        while True:
            token = self.current_token()
            if token and token.t_type == TokenType.OPERATOR and token.t_vale in [token_kind.star.value, token_kind.slash.value]:
                operator = self.consume_token(TokenType.OPERATOR, [token_kind.star.value, token_kind.slash.value])
                # Parse the next factor
                right = self.parse_factor()  
                left = BinaryOperationNode(left, operator.t_vale, right)  
            else:
                break

        return left
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Parse Expression
    def parse_expression(self):
         # Parse the left-hand side (a number or identifier)
        left = self.parse_term() 

        token = self.current_token()
        # Handle binary operators and unary operators
        while token and token.t_type == TokenType.OPERATOR and token.t_vale in [keyword.value for keyword in symbol_kinds]:
            operator = self.consume_token(TokenType.OPERATOR, [keyword.value for keyword in symbol_kinds]) 

            # Parse the right-hand side (another number or identifier)
            right = self.parse_term() 

            # Parse the left-hand side
            left = BinaryOperationNode(left, operator.t_vale, right)  

            token = self.current_token()  # Get the next token to check if there are more operators

        return left 

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Parse Factor    
    def parse_factor(self):
        token = self.current_token()

        # Handle numbers
        if token.t_type == TokenType.NUMBER:
            self.consume_token(TokenType.NUMBER)
            return NumberNode(token.t_vale)

        if token.t_type == TokenType.DECIMAL:
            self.consume_token(TokenType.DECIMAL)
            return NumberNode(token.t_vale)

        # Handle identifiers
        elif token.t_type == TokenType.IDENTIFIER:
            var_name = self.consume_token(TokenType.IDENTIFIER)

            # Check if this is a function call
            if self.current_token().t_type == TokenType.PUNCTUATION and self.current_token().t_vale == token_kind.open_paren.value:
                self.consume_token(TokenType.PUNCTUATION, token_kind.open_paren.value)
                arguments = self.parse_arguments()
                self.consume_token(TokenType.PUNCTUATION, token_kind.close_paren.value)
                return FunctionCallNode(var_name.t_vale, arguments)

            # Handle ++ or -- operators
            next_token = self.current_token()
            if next_token and next_token.t_type == TokenType.OPERATOR and next_token.t_vale in [token_kind.incr.value, token_kind.decr.value]:
                operator = self.consume_token(TokenType.OPERATOR, [token_kind.incr.value, token_kind.decr.value])
                if operator.t_vale == token_kind.incr.value:
                    return PostIncrementNode(var_name.t_vale)
                elif operator.t_vale == token_kind.decr.value:
                    return PostDecrementNode(var_name.t_vale)

            # Just an identifier
            return IdentifierNode(var_name.t_vale)

        # Handle parentheses
        elif token.t_type == TokenType.PUNCTUATION and token.t_vale == token_kind.open_paren.value:
            self.consume_token(TokenType.PUNCTUATION, token_kind.open_paren.value)
            expr = self.parse_expression()
            self.consume_token(TokenType.PUNCTUATION, token_kind.close_paren.value)
            return expr

        # Unexpected token
        else:
            raise SyntaxError(f"Unexpected token in factor: {token.t_type} with value '{token.t_vale}'")