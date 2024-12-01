class SymbolTable:
    def __init__(self, is_global=False, parent=None):
         # Store symbols as {name: (type, value)}
        self.symbols = {} 

        # Keep track of child scopes
        self.children = []  

        # Track if this is the global scope
        self.is_global = is_global  

        # Reference to the parent scope
        self.parent = parent  

    def define(self, name, var_type, value=None):
        if name in self.symbols:
            raise Exception(f"Variable '{name}' is already defined in this scope.")
        self.symbols[name] = (var_type, value)

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        if self.parent is not None:
            return self.parent.lookup(name)
        raise NameError(f"Variable '{name}' is not declared.")

    def set_value(self, name, value):
        #print(f"Setting value of '{name}' to: {value}")
        if name in self.symbols:
            var_type, _ = self.symbols[name]
            self.symbols[name] = (var_type, value)
        elif self.parent:
            self.parent.set_value(name, value)
        else:
            raise NameError(f"Variable '{name}' is not declared.")
    

    def check_type(self, name, expected_type):
        symbol_type, _ = self.lookup(name)
        if symbol_type != expected_type:
            raise TypeError(f"Type mismatch for variable '{name}': expected '{expected_type}', got '{symbol_type}'.")
        

    def push_scope(self):
        # Create new scope with current scope as parent
        new_scope = SymbolTable(parent=self)
        # Add new scope to the list of child scopes
        self.children.append(new_scope)
        return new_scope
    
    
    def __repr__(self, level=0):
        #print Symbol table
        indent = "  " * level
        scope_type = "\nGlobal" if self.is_global else "Local"
        result = f"{indent}{scope_type} Scope:\n"
        for name, (var_type, value) in self.symbols.items():
            result += f"{indent}  {name}: {var_type}\n"  
        for child in self.children:
            result += child.__repr__(level + 1)
        return result
    
    
