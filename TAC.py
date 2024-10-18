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
        #lables and counter will keep increasing
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
        self.generate(node.body)
        self.code.append("End of function")

    def BlockNode(self, node):
        for statement in node.statements:
            self.generate(statement)

    def VariableDeclarationNode(self, node):
        if node.init_value is not None:
            temp_var = self.temp_variable() 
            init_value = self.generate(node.init_value)  

            # assign the temp variable to the actual variable
            #self.code.append(f"{node.name} = {temp_var}")
            # store the init_value in the temp variable
            self.code.append(f"{temp_var} = {init_value}")

        else:
            # declare the variable
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
        loop_start = self.create_lable()  
        loop_end = self.create_lable()  
        
        self.generate(node.init_stmt)
        
        # Start of the loop (create lable)
        self.code.append(f"{loop_start}:")

        # Condition check
        condition = self.generate(node.condition_expr)
        self.code.append(f"if {condition} goto {loop_end}")

        # Loop body
        self.generate(node.loop_body)

        # increment expression
        self.generate(node.increment_expr)

        # the start of the loop
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

    def print_code(self):
        # print the 3 address code
        print("Generated Three Address Code (TAC):")
        for tac in self.code:
            print(tac)




# constant folding
# dead code elimination
