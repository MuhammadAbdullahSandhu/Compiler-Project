class ASTNode:
    pass

class FunctionNode(ASTNode):
    def __init__(self, return_type, name, body):
        self.return_type = return_type
        self.name = name
        self.body = body

    def __repr__(self):
        return f"FunctionNode{{returnType='{self.return_type}', name='{self.name}', body={self.body}}}"


class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"

class VariableDeclarationNode(ASTNode):
    def __init__(self, var_type, name, init_value=None):
        self.var_type = var_type
        self.name = name
        self.init_value = init_value

    def __repr__(self):
        return f"VariableDeclaration(name={self.name}, type={self.init_value})"

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

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"

