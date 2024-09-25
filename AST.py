class ASTNode:
    def __repr__(self):
        return self.__class__.__name__
    
class ProgramNode(ASTNode):
    def __init__(self, functions):
        self.functions = functions
    def __repr__(self):
        return f"{self.__class__.__name__}(functions={self.functions})"


class FunctionNode(ASTNode):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def __repr__(self):
        return "FunctionDeclaration{\n" + \
           "  \t  name='" + self.name + "',\n" + \
           "  \t  body=" + str(self.body) + "\n" + \
           "}"

class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"

class VariableDeclarationNode(ASTNode):
    def __init__(self, name, init_value=None):
        self.name = name
        self.init_value = init_value

    def __repr__(self):
        if self.init_value is not None:
            return f"VariableDeclaration(name -> {self.name}, initializer -> {self.init_value})"
        else:
            return f"VariableDeclaration(name -> {self.name})"

class AssignmentNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Assignment({self.name}, {self.value})"

class ReturnNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Return({self.value})"

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"
    
class BinaryOperationNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"

