from tabulate import tabulate
from optimizer import optimizer_constant_folding
from AST import BlockNode, AssignmentNode, IdentifierNode, ReturnNode, BinaryOperationNode

class op_Three_address_code:
    
    def __init__(self):
        self.temp_counter = 0  
        self.label_counter = 0  
        self.code = [] 

        # track variable values for constant propagation 
        self.constants = {} 
        
        # track temporary variables 
        self.temp_values = {} 
        self.function_definitions = {} 

    def temp_variable(self):
        self.temp_counter += 1
        temp_var = f"t{self.temp_counter}"
        # Initialize with None
        self.temp_values[temp_var] = None  
        return temp_var

    def create_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def generate(self, node):
        class_name = f"{node.__class__.__name__}"
        class_attr = getattr(self, class_name)
        if class_attr:
            return class_attr(node)
        else:
            raise Exception(f"Node type {node.__class__.__name__} not found.")
        
    def resolve_value(self, operand):
        if isinstance(operand, str) and operand in self.temp_values:
            # Use stored value if available
            return self.temp_values[operand]  
        try:
            # Try converting to a number
            return float(operand)  
        except ValueError:
            return operand 

    def ProgramNode(self, node):
        for function in node.functions:
            self.function_definitions[function.name] = function
            #y = self.function_definitions[function.name] = function
            #print(y)
        for function in node.functions:
            self.generate(function)
        

    def FunctionNode(self, node):
        #self.code.append(f"function {node.name}:")
        #self.code.append("Start of function")
        self.generate(node.body)
        #self.code.append("End of function")

    def BlockNode(self, node):
        for statement in node.statements:
            self.generate(statement)

    def VariableDeclarationNode(self, node):
        if node.init_value is not None:
            init_value = self.generate(node.init_value)

            # Store constant value
            self.constants[node.name] = init_value  
            #print(f'constant{init_value}')
            self.code.append(f"{node.name} = {init_value}")
        else:
            self.constants[node.name] = None  
            self.code.append(f"variable {node.name}")

    def AssignmentNode(self, node):
        value = self.generate(node.value)

        # Update constant value
        self.constants[node.name] = value  
        self.code.append(f"{node.name} = {value}")

    def ReturnNode(self, node):
        value = self.generate(node.value)
        self.code.append(f"return {value}")

    def IfNode(self, node):
        condition = self.generate(node.condition)
        
        # Evaluate condition at compile time
        if isinstance(condition, bool):
            # If the condition is a constant boolean, decide at compile time
            if condition:
                # Only generate the "then" block if condition is True
                self.generate(node.then_block)
            elif node.else_block:
                # Only generate the "else" block if condition is False
                self.generate(node.else_block)
        else:
            # Proceed with normal if statement generation if condition cannot be folded
            then_label = self.create_label()
            end_label = self.create_label()
            else_label = self.create_label() if node.else_block else end_label

            # Conditional jump to the then label if the condition is true
            self.code.append(f"if {condition} goto {then_label}")
            
            # If there's an else block, add a jump to it, otherwise jump to end
            if node.else_block:
                self.code.append(f"goto {else_label}")
            
            # Then block
            self.code.append(f"{then_label}:")
            self.generate(node.then_block)
            
            # Unconditionally jump to the end label to avoid fall-through
            self.code.append(f"goto {end_label}")
            
            # Else block, if it exists
            if node.else_block:
                self.code.append(f"{else_label}:")
                self.generate(node.else_block)
            
            # End of if-else
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
        left_value = self.resolve_value(left)
        right_value = self.resolve_value(right)
        
        # Perform constant folding if possible
        result = optimizer_constant_folding(left_value, node.operator, right_value)
        
        if result is not None:
            temp_var = self.temp_variable()

            # Store the result in temp_values
            self.temp_values[temp_var] = result  
            self.code.append(f"{temp_var} = {result}")
            
            return temp_var
        else:
            temp_var = self.temp_variable()
            self.code.append(f"{temp_var} = {left} {node.operator} {right}")
            return temp_var

    def NumberNode(self, node):
        return str(node.value)

    def IdentifierNode(self, node):
        # Use the constant value if available for propagation
        if node.name in self.constants and self.constants[node.name] is not None:
            return self.constants[node.name]
        else:
            return node.name
        
    
    def FunctionCallNode(self, node):
        function_def = self.function_definitions.get(node.func_name)
        if not function_def:
            raise Exception(f"Function '{node.func_name}' not defined.")

        # Generate argument values
        arg_values = [self.generate(arg) for arg in node.arguments]
        print(f'argument values {arg_values}')

        # Create parameter-to-argument mapping
        #zip pairs elements from the list of parameter names and the list of argument values together.
        #dict converts the list of paired values into a dictionary.
        param_mapping = dict(zip([param[1].t_vale for param in function_def.parameters], arg_values))
        print (param_mapping)

        # Generate the inlined function body with substituted parameters
        #[(int, IdentifierNode("x")), (int, IdentifierNode("y"))]
        return_value = self.inline_function_body(function_def.body, param_mapping)
        
        print (f'function call return values {return_value}')

        return return_value
    
    def inline_function_body(self, body_node, param_mapping):
        inlined_code = []

        # create copy of code
        original_code = self.code 
        self.code = inlined_code 
        print(f'this is original code {original_code}')
        # Generate the function body with parameter substitution
        #traverses the function body and applies substitutions so that each parameter is replaced by its corresponding argument
        self.substituted_body(body_node, param_mapping)

        # Restore original code buffer
        inlined_code = self.code
        #print(f'this is inline code {inlined_code}')
        self.code = original_code 

        # Add the inlined code to the original code buffer
        x = self.code.extend(inlined_code)
        #print(x)
        
        # Return the last temporary variable as the function's result
        #etrieves the last line of inlined code, which should contain the function’s return value.
        
        results = inlined_code[-1].split(' = ')[0] 
        #temp = t1
        #print(f'this is value = {results}')
        return results

    def substituted_body(self, body_node, param_mapping):
        if isinstance(body_node, BlockNode):
            for statement in body_node.statements:
                self.substituted_body(statement, param_mapping)
        elif isinstance(body_node, AssignmentNode):
            value = self.replace_parameters(body_node.value, param_mapping)
            self.code.append(f"{body_node.name} = {value}")
        elif isinstance(body_node, ReturnNode):
            value = self.replace_parameters(body_node.value, param_mapping)
            self.code.append(f"{value}")

    def replace_parameters(self, value_node, param_mapping):
        if isinstance(value_node, IdentifierNode) and value_node.name in param_mapping:
            return param_mapping[value_node.name]
        elif isinstance(value_node, BinaryOperationNode):
            left = self.replace_parameters(value_node.left, param_mapping)
            right = self.replace_parameters(value_node.right, param_mapping)
            result = optimizer_constant_folding(left, value_node.operator, right)
            return f"{result}"
        else:
            return self.generate(value_node)


    def print_code(self):
        print("Generated Optimized Three Address Code (TAC):")
        tac_table = [[i + 1, line] for i, line in enumerate(self.code)]
        print(tabulate(tac_table, headers=["Line", "Code"], tablefmt="fancy_grid"))
        print(self.function_definitions)
        print(self.temp_values)
        print(self.constants)

        # print("\nTemporary Variables:")
        # temp_table = [[name, value] for name, value in self.temp_values.items()]
        # print(tabulate(temp_table, headers=["Temporary Variable", "Value"], tablefmt="fancy_grid"))
