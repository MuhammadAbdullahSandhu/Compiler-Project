class ASTNode:
    def __repr__(self):
        return f"{self.__class__.__name__}()"

class ProgramNode(ASTNode):
    def __init__(self, global_variables, functions):
        self.global_variables = global_variables  # Store global variable declarations
        self.functions = functions  # Store function definitions

    def to_string(self, level=0):
        indent = "  " * level
        globals_str = ",\n".join([var.to_string(level + 2) for var in self.global_variables])
        functions_str = ",\n".join([func.to_string(level + 2) for func in self.functions])
        return (
            f"{indent}ProgramNode(\n"
            f"{indent}  global_variables=[\n{globals_str}\n{indent}  ],\n"
            f"{indent}  functions=[\n{functions_str}\n{indent}  ]\n"
            f"{indent})"
        )

class FunctionNode(ASTNode):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def to_string(self, level=0):
        indent = "  " * level
        t_parameters = ', '.join([
            f"{param_type.t_vale} {param_name.t_vale}" + 
            (f" = {default_value.to_string()}" if default_value else "")
            for param_type, param_name, default_value in self.parameters
        ])
        return f"{indent}FunctionNode(\n" + \
            f"{indent}  name='{self.name}',\n" + \
            f"{indent}  parameters=[{t_parameters}],\n" + \
            f"{indent}  body={self.body.to_string(level + 1)}\n" + \
            f"{indent})"
    
class FunctionCallNode(ASTNode):
    def __init__(self, func_name, arguments):
        self.func_name = func_name
        self.arguments = arguments

    def to_string(self, level=0):
        indent = "  " * level
        args_str = ', '.join([arg.to_string(level + 1) for arg in self.arguments])
        return f"{indent}FunctionCallNode(\n" + \
               f"{indent}  func_name='{self.func_name}',\n" + \
               f"{indent}  arguments=[{args_str}]\n" + \
               f"{indent})"
    
class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def to_string(self, level=0):
        indent = "  " * level
        return f"{indent}BlockNode(\n" + \
               ",\n".join([stmt.to_string(level + 1) for stmt in self.statements]) + \
               f"\n{indent})"

class VariableDeclarationNode(ASTNode):
    def __init__(self, name, init_value=None):
        # Handle both single names and lists of names
        self.name = name if isinstance(name, str) else ', '.join(name)
        self.init_value = init_value

    def to_string(self, level=0):
        indent = "  " * level
        if self.init_value is not None:
            return f"{indent}VariableDeclarationNode(name='{self.name}', initializer={self.init_value.to_string(level + 1)})"
        else:
            return f"{indent}VariableDeclarationNode(name='{self.name}')"

class AssignmentNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def to_string(self, level=0):
        indent = "  " * level
        return f"{indent}AssignmentNode(name='{self.name}', value={self.value.to_string(level + 1)})"

class ReturnNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def to_string(self, level=0):
        indent = "  " * level
        return f"{indent}ReturnNode(value={self.value.to_string(level + 1)})"

class IfNode(ASTNode):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def to_string(self, level=0):
        indent = "  " * level
        return f"{indent}IfNode(\n" + \
               f"{indent}  condition={self.condition.to_string(level + 1)},\n" + \
               f"{indent}  then={self.then_block.to_string(level + 1)},\n" + \
               (f"{indent}  else={self.else_block.to_string(level + 1)}\n" if self.else_block else "") + \
               f"{indent})"

class ForStatementNode(ASTNode):
    def __init__(self, init_stmt, condition_expr, increment_expr, loop_body):
        self.init_stmt = init_stmt
        self.condition_expr = condition_expr
        self.increment_expr = increment_expr
        self.loop_body = loop_body

    def to_string(self, level=0):
        indent = "  " * level
        return f"{indent}ForStatementNode(\n" + \
               f"{indent}  init_stmt={self.init_stmt.to_string(level + 1)},\n" + \
               f"{indent}  condition_expr={self.condition_expr.to_string(level + 1)},\n" + \
               f"{indent}  increment_expr={self.increment_expr.to_string(level + 1)},\n" + \
               f"{indent}  loop_body={self.loop_body.to_string(level + 1)}\n" + \
               f"{indent})"

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def to_string(self, level=0):
        indent = "  " * level
        return f"{indent}NumberNode(value={self.value})"

class BinaryOperationNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def to_string(self, level=0):
        indent = "  " * level
        return f"{indent}BinaryOperationNode(\n" + \
               f"{indent}  operator='{self.operator}',\n" + \
               f"{indent}  left={self.left.to_string(level + 1)},\n" + \
               f"{indent}  right={self.right.to_string(level + 1)}\n" + \
               f"{indent})"
class PostIncrementNode(ASTNode):
    def __init__(self, variable):
        self.variable = variable

    def to_string(self, level=0):
        indent = "  " * level
        return f"{indent}PostIncrementNode(variable='{self.variable}')"

class PostDecrementNode(ASTNode):
    def __init__(self, variable):
        self.variable = variable

    def to_string(self, level=0):
        indent = "  " * level
        return f"{indent}PostDecrementNode(variable='{self.variable}')"
    
class IdentifierNode(ASTNode):
    def __init__(self, name):
        if isinstance(name, list):
            self.name = name[0]
        else:
            self.name = name

    def to_string(self, level=0):
        indent = "  " * level
        return f"{indent}IdentifierNode(name='{self.name}')"
    
    