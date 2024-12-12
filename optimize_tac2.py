from tabulate import tabulate

class Optimizer:
    def __init__(self, tac_code, debugging=True):
        self.tac_code = tac_code
        print(f'Code before optimization {tac_code}')

        # To track variables with constant values
        self.constants = {}  
        
        self.code = tac_code

        # Enable or disable debug messages
        self.debugging = debugging  

    def debug(self, message):
        if self.debugging:
            print(message)

    def optimize(self):
        self.debug("Starting optimization")
        
        self.constant_propagation()
        self.constant_folding()
        self.condition_folding()
        self.dead_code_elimination()
        self.update_return()
    

    def update_return(self):
        self.debug("Updating return statements with constant values")
        optimized_code = []

        for line in self.code:
            parts = line.split()
            
            if line.startswith("function"):
                optimized_code.append(line)
                continue

            # Check for return statement
            if parts[0] == "return" and len(parts) == 2:
                return_var = parts[1]

                # Replace the return variable with its constant value if available
                if return_var in self.constants:
                    constant_value = self.constants[return_var]

                    self.debug(f"Replacing return {return_var} with return {constant_value}")
                    line = f"return {constant_value}"

            optimized_code.append(line)

        self.code = optimized_code
        self.debug(f"Code after updating return values: {self.code}")

        

    def constant_propagation(self):
        self.debug("Performing constant propagation")
        optimized_code = []

        for line in self.code:
            parts = line.split()
            
            # if retuen statement , for now keep it same , return statement will be updated later 
            if parts[0] == "return":
                optimized_code.append(line)
                continue

            if len(parts) == 5 and parts[1] == 'not':
                optimized_code.append(line)
                continue

            if len(parts) == 3 and parts[1] == '=': 
                variable, value = parts[0], parts[2]
                if value.isdigit():
                    self.constants[variable] = value

                    self.debug(f"Tracking constant: {variable} = {value}")
                    
                else:
                    # Replace constants in the value
                    value = self.replace_constants(value)
                    line = f"{variable} = {value}"
            
            else:
                # Replace constants in the whole line
                line = self.replace_constants(line)

            optimized_code.append(line)
    
        self.code = optimized_code
        self.debug(f"Code after constant propagation: {self.code}")

    # this will handle the value that manually come from tac like i++ will be converted to i + 1 or i - 1
    def replace_constants(self, line):
        parts = line.split()

        # Handle z++
        if len(parts) == 5 and parts[3] in ['+', '-']:  
            variable, operator, operand = parts[0], parts[3], parts[4]
            if variable in self.constants and operand.isdigit():
                # Perform folding
                result = self.optimizer_constant_folding(int(self.constants[variable]), operator, int(operand))
                self.constants[variable] = str(result)
                return f"{variable} = {result}"

        # Replace constants in the entire line
        for variable, value in self.constants.items():
            line = line.replace(variable, value)
        return line

    def constant_folding(self):
        self.debug("Performing constant folding")
        optimized_code = []

        for line in self.code:
            parts = line.split()
            # Binary operation
            if len(parts) == 5 and parts[1] == '=':  
                label, left, operator, right = parts[0], parts[2], parts[3], parts[4]

                # Replace with constant values if available
                left = int(left) if left.isdigit() else self.constants.get(left, left)
                right = int(right) if right.isdigit() else self.constants.get(right, right)

                
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):  
                    result = self.optimizer_constant_folding(left, operator, right)
                    self.debug(f"Folding result: {label} = {result}")
                    line = f"{label} = {result}"
                    self.constants[label] = str(result)

            optimized_code.append(line)

        self.code = optimized_code
        self.debug(f"Code after constant folding: {self.code}")


    def condition_folding(self):
        self.debug("Performing condition folding")
        optimized_code = []

        # default for not skipping block
        skip_block = False

        for line in self.code:
            parts = line.split()

            # Handle conditional branch with negation
            # if x goto L1
            if parts[0] == "if" and parts[2] == "goto":  
                condition_variable, label = parts[1], parts[3]
                condition_value = self.constants.get(condition_variable, condition_variable)

                # Evaluate condition and fold
                if condition_value == "True":
                    optimized_code.append(f"goto {label}")
                    skip_block = True

                elif condition_value == "False":
                    
                    skip_block = False  
                else:
                    optimized_code.append(line)

            # Handle conditions (if not goto)
            elif parts[0] == "if" and parts[1] == "not" and parts[3] == "goto":
                condition_variable, label = parts[3], parts[4]
                condition_value = self.constants.get(condition_variable, condition_variable)

                #print(f'condition value ',condition_value)

                # Negate condition and fold
                if condition_value == "True":
                    # If True, do not skip the block
                    skip_block = False  
                elif condition_value == "False":
                    optimized_code.append(f"goto {label}")
                    skip_block = True
                else:
                    optimized_code.append(line)

            elif line.strip().endswith(":"):  # Process labels
                skip_block = False
                optimized_code.append(line)

            elif not skip_block:  # Only process reachable code
                optimized_code.append(line)

        self.code = optimized_code
        self.debug(f"Code after condition folding: {self.code}")

    
    
    def dead_code_elimination(self):
        self.debug("Performing dead code elimination...")
        optimized_code = []
        active_labels = set()

        # Mark active labels
        for line in self.code:
            
            parts = line.split()
            
            if parts[0] == "goto" and len(parts) == 2:
                active_labels.add(parts[1] + ":")
                
            elif parts[0] == "if" and parts[2] == "goto" and len(parts) == 4:
                active_labels.add(parts[3] + ":")
            
            elif parts[0] == "if" and parts[3] == "goto" and len(parts) == 5:
                active_labels.add(parts[3] + ":")

             # function names as active
            elif parts[0] == "function": 
                active_labels.add(line.strip())

        self.debug(f"Active labels: {active_labels}")

        # Remove unreachable code
        skip = False
        for line in self.code:
            
            if line.endswith(":"):
                skip = line not in active_labels
                
            if not skip:
                # Update constants for reachable assignments
                parts = line.split()
                if len(parts) == 3 and parts[1] == "=":
                    variable, value = parts[0], self.replace_constants(parts[2])
                    if value.isdigit():
                        self.constants[variable] = value
                        self.debug(f"Revalidating constant: {variable} = {value}")
                optimized_code.append(line)

        self.code = optimized_code
        self.debug(f"Code after dead code elimination: {self.code}")


    def optimizer_constant_folding(self, left, operator, right):
        try:
            # Arithmetic operators
            if operator == '+': 
                return left + right
            if operator == '-': 
                return left - right
            if operator == '*': 
                return left * right
            if operator == '/': 
                return left / right if right != 0 else "undefined"
            if operator == '%': 
                return left % right if right != 0 else "undefined"
            if operator == '++': return left + right

            # Comparison operators
            if operator == '>=': 
                return "True" if left >= right else "False"
            if operator == '<=': 
                return "True" if left <= right else "False"
            if operator == '==': 
                return "True" if left == right else "False"
            if operator == '!=': 
                return "True" if left != right else "False"
            if operator == '>': 
                return "True" if left > right else "False"
            if operator == '<': 
                return "True" if left < right else "False"

            raise ValueError(f"Unsupported operator: {operator}")
        
        
        except Exception as e:
            self.debug(f"Error during folding: {e}")
            return "undefined"
        

    #print the optimized Three address code
    def print_optimized_code(self):
        print("Optimized Three Address Code (TAC):")
        tac_table = [[i + 1, line] for i, line in enumerate(self.code)]
        print(tabulate(tac_table, headers=["Line", "Code"], tablefmt="fancy_grid"))
        


