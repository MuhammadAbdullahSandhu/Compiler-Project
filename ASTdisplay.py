# ast_nodes.py
from graphviz import Digraph

class ASTNode:
    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def to_graph(self, dot=None):
        if dot is None:
            dot = Digraph()

        node_name = f"{id(self)}"
        dot.node(node_name, self.__class__.__name__)

        for attr_name, attr_value in self.__dict__.items():
            if isinstance(attr_value, list):
                for index, item in enumerate(attr_value):
                    item_node_name = f"{id(item)}"
                    dot.node(item_node_name, repr(item))
                    dot.edge(node_name, item_node_name)
                    item.to_graph(dot)
            elif isinstance(attr_value, ASTNode):
                item_node_name = f"{id(attr_value)}"
                dot.node(item_node_name, repr(attr_value))
                dot.edge(node_name, item_node_name)
                attr_value.to_graph(dot)

        return dot

class ProgramNode(ASTNode):
    def __init__(self, functions):
        self.functions = functions

class FunctionNode(ASTNode):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

class FunctionCallNode(ASTNode):
    def __init__(self, func_name, arguments):
        self.func_name = func_name
        self.arguments = arguments

class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class VariableDeclarationNode(ASTNode):
    def __init__(self, name, init_value=None):
        self.name = name if isinstance(name, str) else ', '.join(name)
        self.init_value = init_value

class AssignmentNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class ReturnNode(ASTNode):
    def __init__(self, value):
        self.value = value

class IfNode(ASTNode):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class ForStatementNode(ASTNode):
    def __init__(self, init_stmt, condition_expr, increment_expr, loop_body):
        self.init_stmt = init_stmt
        self.condition_expr = condition_expr
        self.increment_expr = increment_expr
        self.loop_body = loop_body

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class BinaryOperationNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class IdentifierNode(ASTNode):
    def __init__(self, name):
        if isinstance(name, list):
            self.name = name[0]
        else:
            self.name = name
