class ASTNode:
    def __repr__(self, level=0):
        return self.__class__.__name__

class ProgramNode(ASTNode):
    def __init__(self, functions):
        self.functions = functions
    
    def __repr__(self, level=0):
        indent = "  " * level
        return f"{indent}{self.__class__.__name__}(\n" + \
               f"{indent}  functions=[\n" + \
               ",\n".join([func.__repr__(level + 2) for func in self.functions]) + \
               f"\n{indent}  ]\n{indent})"

class FunctionNode(ASTNode):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self, level=0):
        indent = "  " * level
        parameters_str = ', '.join([f"{param_type.t_vale} {param_name.t_vale}" for param_type, param_name in self.parameters])
        return f"{indent}FunctionNode(\n" + \
               f"{indent}  name='{self.name}',\n" + \
               f"{indent}  parameters=[{parameters_str}],\n" + \
               f"{indent}  body={self.body.__repr__(level + 1)}\n" + \
               f"{indent})"

class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self, level=0):
        indent = "  " * level
        return f"{indent}Block(\n" + \
               ",\n".join([stmt.__repr__(level + 1) for stmt in self.statements]) + \
               f"\n{indent})"

class VariableDeclarationNode(ASTNode):
    def __init__(self, name, init_value=None):
        self.name = name
        self.init_value = init_value

    def __repr__(self, level=0):
        indent = "  " * level
        if self.init_value is not None:
            return f"{indent}VariableDeclarationNode(name='{self.name}', initializer={self.init_value.__repr__(level + 1)})"
        else:
            return f"{indent}VariableDeclarationNode(name='{self.name}')"

class AssignmentNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self, level=0):
        indent = "  " * level
        return f"{indent}AssignmentNode(name='{self.name}', value={self.value.__repr__(level + 1)})"

class ReturnNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self, level=0):
        indent = "  " * level
        return f"{indent}ReturnNode(value={self.value.__repr__(level + 1)})"

class IfNode(ASTNode):
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __repr__(self, level=0):
        indent = "  " * level
        return f"{indent}IfNode(\n" + \
               f"{indent}  condition={self.condition.__repr__(level + 1)},\n" + \
               f"{indent}  then={self.then_block.__repr__(level + 1)},\n" + \
               (f"{indent}  else={self.else_block.__repr__(level + 1)}" if self.else_block else "") + \
               f"\n{indent})"

class ForStatementNode(ASTNode):
    def __init__(self, init_stmt, condition_expr, increment_expr, loop_body):
        self.init_stmt = init_stmt
        self.condition_expr = condition_expr
        self.increment_expr = increment_expr
        self.loop_body = loop_body

    def __repr__(self, level=0):
        indent = "  " * level
        return f"{indent}ForStatementNode(\n" + \
               f"{indent}  init_stmt={self.init_stmt.__repr__(level + 1)},\n" + \
               f"{indent}  condition_expr={self.condition_expr.__repr__(level + 1)},\n" + \
               f"{indent}  increment_expr={self.increment_expr.__repr__(level + 1)},\n" + \
               f"{indent}  loop_body={self.loop_body.__repr__(level + 1)}\n" + \
               f"{indent})"

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self, level=0):
        indent = "  " * level
        return f"{indent}NumberNode(value={self.value})"
    
class BinaryOperationNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self, level=0):
        indent = "  " * level
        return f"{indent}BinaryOperationNode(\n" + \
                f"{indent}  operator='{self.operator}',\n" + \
               f"{indent}  left={self.left.__repr__(level + 1)},\n" + \
               f"{indent}  right={self.right.__repr__(level + 1)}\n" + \
               f"{indent})"

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self, level=0):
        indent = "  " * level
        return f"{indent}IdentifierNode(name='{self.name}')"
