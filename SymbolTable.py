from AST import NumberNode,IdentifierNode,BinaryOperationNode

class SymbolTable:
    def __init__(self, is_global=False, parent=None):
        self.symbols = {}  
        self.children = []  
        self.is_global = is_global  
        self.parent = parent 
        

    def define(self, name, var_type):
        if name in self.symbols:
            raise Exception(f"Variable '{name}' is already defined in this scope.")
        self.symbols[name] = var_type
        
    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        if self.parent is not None:
            return self.parent.lookup(name)
        
        raise NameError(f"Variable '{name}' is not declared.")

    def check_type(self, name, expected_type):
        # Look up the type of the symbol (variable or function) in the symbol table
        symbol_type = self.lookup(name)
        if symbol_type is None:
            raise NameError(f"Variable '{name}' is not declared.")
        if symbol_type != expected_type:
            raise TypeError(f"Type mismatch for variable '{name}': expected {expected_type}, got {symbol_type}")


    def push_scope(self):
        new_scope = SymbolTable(parent=self)  
        self.children.append(new_scope)
        return new_scope

    def pop_scope(self):
        if self.children:
            self.children.pop()

    def __repr__(self, level=0):
        indent = "  " * level
        scope_type = "Global" if self.is_global else "Local"
        result = f"{indent}{scope_type} Scope:\n"
        for name, var_type in self.symbols.items():
            result += f"{indent}  {name}: {var_type}\n"
        for child in self.children:
            result += child.__repr__(level + 1)  
        return result
    

