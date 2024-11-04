from tabulate import tabulate
# ProgramNode
# FunctionNode
# BlockNode
# VariableDeclarationNode
# AssignmentNode
# IfNode
# ForStatementNode
# ReturnNode
# BinaryOperationNode
# IdentifierNode
# NumberNode

#Recursive AST Traversal
#recursive traversal 

# start from the nodes as in AST

class Three_address_code:
    
    def __init__(self):
        self.temp_counter = 0  
        self.label_counter = 0  
        self.code = []
        

    def temp_variable(self):
        # temporary veriables
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def create_lable(self):
        #lables and counter 
        self.label_counter += 1
        return f"L{self.label_counter}"

    def generate(self, node):
        # class name from the node class
        class_name = f"{node.__class__.__name__}" 
        #print (class_name)
        # get the method dynamically
        class_attr = getattr(self, class_name)  
        #print(class_attr)
        if class_attr:
            return class_attr(node)
        else:
            raise Exception(f"not found {node.__class__.__name__}")

    def ProgramNode(self, node):
        for function in node.functions:
            self.generate(function)

    def FunctionNode(self, node):
        self.code.append(f"function {node.name}:")
        self.code.append("Start of function")
        # if node.parameters is not None:
        #     self.code.append(node.parameters)
        self.generate(node.body)
        self.code.append("End of function")

    def BlockNode(self, node):
        for statement in node.statements:
            self.generate(statement)

    def VariableDeclarationNode(self, node):
        if node.init_value is not None:
            init_value = self.generate(node.init_value)
            self.code.append(f"{node.name} = {init_value}")
        else:
            self.code.append(f"variable {node.name}")

    def AssignmentNode(self, node):
        value = self.generate(node.value)
        self.code.append(f"{node.name} = {value}")

    def ReturnNode(self, node):
        value = self.generate(node.value)
        self.code.append(f"return {value}")


    def IfNode(self, node):
        # Generate the condition expression
        condition = self.generate(node.condition)

        # creating Labels
        then_label = self.create_lable()  
        else_label = self.create_lable() if node.else_block else None

        # create an end label  
        end_label = self.create_lable() if else_label or self.code else None  

        # conditional jump to then block
        self.code.append(f"if {condition} goto {then_label}")
        if else_label:
            self.code.append(f"goto {else_label}")

        # generate the then block code
        self.code.append(f"{then_label}:")
        self.generate(node.then_block)

        # jump to the end 
        if end_label:
            self.code.append(f"goto {end_label}")

        # Generate the 'else' block code (if it exists)
        if else_label:
            self.code.append(f"{else_label}:")
            self.generate(node.else_block)

        # End label (only if required)
        if end_label:
            self.code.append(f"{end_label}:")

    def ForStatementNode(self, node):
        loop_start = self.create_lable()  # Start of the loop
        loop_end = self.create_lable()  # End of the loop

        # Initialize the loop variable
        self.generate(node.init_stmt)
        
        # Start of the loop (label)
        self.code.append(f"{loop_start}:")

        # Condition check
        condition = self.generate(node.condition_expr)
        self.code.append(f"if not {condition} goto {loop_end}")

        # Loop body
        self.generate(node.loop_body)

        # Increment expression
        self.generate(node.increment_expr)

        # Jump back to the start of the loop
        self.code.append(f"goto {loop_start}")

        # End of the loop
        self.code.append(f"{loop_end}:")


    def BinaryOperationNode(self, node):
        left = self.generate(node.left)
        right = self.generate(node.right)
        temp_vari = self.temp_variable()
        self.code.append(f"{temp_vari} = {left} {node.operator} {right}")
        return temp_vari

    def NumberNode(self, node):
        return str(node.value)

    def IdentifierNode(self, node):
        return node.name

    def FunctionCallNode(self, node):
        # Generate code for the function arguments
        arguments = [self.generate(arg) for arg in node.arguments]

        # Create a temporary variable to store the result
        temp_var = self.temp_variable()

        # Generate TAC for the function call
        self.code.append(f"{temp_var} = call {node.func_name}({', '.join(arguments)})")

        return temp_var
    
    def print_code(self):
        print("Generated Three Address Code (TAC):")
        tac_table = [[i + 1, line] for i, line in enumerate(self.code)]
        print(tabulate(tac_table, headers=["Line", "Code"], tablefmt="fancy_grid"))

