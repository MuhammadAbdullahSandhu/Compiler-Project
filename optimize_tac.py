from tabulate import tabulate
from optimizer import optimizer_constant_folding

class op_Three_address_code:
    
    def __init__(self):
        self.temp_counter = 0  
        self.label_counter = 0  
        self.code = []
        self.variables = {}  # Store variable values
        self.temp_values = {}  # Store temporary variable values

    def temp_variable(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def create_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def generate(self, node):
        class_name = f"{node.__class__.__name__}" 
        class_attr = getattr(self, class_name, None)  
        if class_attr:
            return class_attr(node)
        else:
            raise Exception(f"Not found: {node.__class__.__name__}")

    def ProgramNode(self, node):
        for function in node.functions:
            self.generate(function)

    def FunctionNode(self, node):
        self.code.append(f"function {node.name}:")
        self.code.append("Start of function")
        self.generate(node.body)
        self.code.append("End of function")

    def BlockNode(self, node):
        for statement in node.statements:
            self.generate(statement)

    def VariableDeclarationNode(self, node):
        init_value = self.generate(node.init_value) if node.init_value else None
        # Store the variable and its value
        self.variables[node.name] = init_value  
        if init_value is not None:
            self.code.append(f"{node.name} = {init_value}")
        else:
            self.code.append(f"variable {node.name}")

    def AssignmentNode(self, node):
        value = self.generate(node.value)

        # Update the stored value
        self.variables[node.name] = value 
        self.code.append(f"{node.name} = {value}")

    def ReturnNode(self, node):
        value = self.generate(node.value)
        self.code.append(f"return {value}")

    def IfNode(self, node):
        condition = self.generate(node.condition)
        if isinstance(condition, bool):
            if condition:
                self.generate(node.then_block)
            elif node.else_block:
                self.generate(node.else_block)
        else:
            then_label = self.create_label()
            else_label = self.create_label() if node.else_block else None
            end_label = self.create_label() if else_label else None

            self.code.append(f"if {condition} goto {then_label}")
            if else_label:
                self.code.append(f"goto {else_label}")

            self.code.append(f"{then_label}:")
            self.generate(node.then_block)

            if end_label:
                self.code.append(f"goto {end_label}")

            if else_label:
                self.code.append(f"{else_label}:")
                self.generate(node.else_block)

            if end_label:
                self.code.append(f"{end_label}:")


    def ForStatementNode(self, node):
        loop_start = self.create_label()
        loop_end = self.create_label()

        self.generate(node.init_stmt)
        self.code.append(f"{loop_start}:")

        condition = self.generate(node.condition_expr)
        self.code.append(f"if not {condition} goto {loop_end}")

        self.generate(node.loop_body)
        self.generate(node.increment_expr)
        self.code.append(f"goto {loop_start}")
        self.code.append(f"{loop_end}:")

    def BinaryOperationNode(self, node):
        left = self.generate(node.left)
        right = self.generate(node.right)

        # Resolve temporary variables to their values if available
        left_value = self.update_value(left)
        right_value = self.update_value(right)

        # Perform constant folding if possible
        result = optimizer_constant_folding(left_value, node.operator, right_value)
        
        if result is not None:
            temp_var = self.temp_variable()
            self.temp_values[temp_var] = result  # Store the result in temp_values
            self.code.append(f"{temp_var} = {result}")
            return temp_var
        else:
            temp_var = self.temp_variable()
            self.code.append(f"{temp_var} = {left} {node.operator} {right}")
            return temp_var

    def NumberNode(self, node):
        return str(node.value)

    def IdentifierNode(self, node):
        # Return the stored value of the identifier, if available
        return self.variables.get(node.name, node.name)

    def FunctionCallNode(self, node):
        arguments = [self.generate(arg) for arg in node.arguments]
        temp_var = self.temp_variable()
        self.code.append(f"{temp_var} = call {node.func_name}({', '.join(arguments)})")
        return temp_var

    def update_value(self, operand):
        
        #Resolve the value of an operand
        if isinstance(operand, str) and operand in self.temp_values:
            # Use stored value if available
            return self.temp_values[operand]  
        try:
            # Try converting to a number it will raise error if operand is not a number
            return float(operand)  
        except ValueError:
            return operand 

    def print_code(self):
        print("Generated Optimized Three Address Code (TAC):")
        tac_table = [[i + 1, line] for i, line in enumerate(self.code)]
        print(tabulate(tac_table, headers=["Line", "Code"], tablefmt="fancy_grid"))
        print("\nVariables:")
        var_table = [[name, value] for name, value in self.variables.items()]
        print(tabulate(var_table, headers=["Variable", "Value"], tablefmt="fancy_grid"))

        print("\nTemporary Variables:")
        temp_table = [[name, value] for name, value in self.temp_values.items()]
        print(tabulate(temp_table, headers=["Temporary Variable", "Value"], tablefmt="fancy_grid"))
