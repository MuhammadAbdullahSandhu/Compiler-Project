class Optimizer:
    def __init__(self, tac_code):
        self.tac_code = tac_code
        print(f"Code before optimization: {tac_code}")

        # To track variables with constant values
        self.constants = {}
        self.code = tac_code

    def constant_propagation(self):
        """Perform constant propagation on the code."""
        opt_tac = []  # List to store the optimized TAC

        for line in self.code:
            # Check if the line is an assignment
            if '=' in line and 'goto' not in line:
                variable, expression = map(str.strip, line.split('=', 1))
                

                # Propagate constants in the expression
                for const_var, const_value in self.constants.items():
                    expression = expression.replace(const_var, str(const_value))

                # If the expression is a comparison, do not store it as a constant
                if any(op in expression for op in ['>=', '<=', '>', '<', '==', '!=']):
                    opt_tac.append(f"{variable} = {expression}")
                else:
                    # Treat it as a constant and store in the constants dictionary
                    self.constants[variable] = expression
                    opt_tac.append(f"{variable} = {expression}")

            else:
                # Append lines that are not assignments unchanged
                opt_tac.append(line)

        # Update the code with optimized TAC
        self.code = opt_tac




    def constant_folding(self):
        opt_tac = []  # List to store the TAC after folding

        for line in self.code:
            parts = line.split()
            # Binary operation
            if len(parts) == 5 and parts[1] == '=':  
                variable, left, operator, right = parts[0], parts[2], parts[3], parts[4]


                print(f'operator {operator}')
                # Replace variables with constants if available
                left = int(left) if left.isdigit() else self.constants.get(left, left)
                right = int(right) if right.isdigit() else self.constants.get(right, right)

                # Apply constant folding if both operands are constants
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):

                    folded_value = self.optimizer_constant_folding(left, operator, right)

                    opt_tac.append(f"{variable} = {folded_value}")

                    self.constants[variable] = folded_value  # Update constants
                    continue  # Skip appending the original line
                # If not foldable, keep the line as-is
                opt_tac.append(line)

            elif len(parts) == 7 and parts[1] == '=':  
                variable, left, operator, right, operator, right  = parts[0], parts[2], parts[3], parts[4], parts[5], parts[6] 


                print(f'operator {operator}')
                # Replace variables with constants if available
                left = int(left) if left.isdigit() else self.constants.get(left, left)
                right = int(right) if right.isdigit() else self.constants.get(right, right)

                # Apply constant folding if both operands are constants
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):

                    folded_value = self.optimizer_constant_folding(left, operator, right)

                    opt_tac.append(f"{variable} = {folded_value}")

                    self.constants[variable] = folded_value  
                    continue  
               
                opt_tac.append(line)
            else:

                opt_tac.append(line)

        self.code = opt_tac 

    def condition_folding(self):
       
        opt_tac = [] 

        for line in self.code:
            if line.strip().startswith("if"):  

                # Split the conditional line: "if x > y goto L1"
                condition, label = line.split("goto")
                condition = condition.strip().replace("if", "").strip()
                label = label.strip()

                # Replace constants in the condition
                for const_var, const_value in self.constants.items():
                    condition = condition.replace(const_var, str(const_value))

                
                try:
                    result = eval(condition)
                    if result:

                        # Condition is True keep the goto
                        opt_tac.append(f"goto {label}")
                    else:
                        # Condition is False; skip this line
                        pass
                except Exception:
                    opt_tac.append(line)

            else:
                opt_tac.append(line)

        self.code = opt_tac



    def dead_code_elimination(self):
        
        live_variables = set()
        opt_tac = []

        for line in reversed(self.code):
            if '=' in line and 'goto' not in line:
                variable, expression = map(str.strip, line.split('=', 1))
                if variable not in live_variables:
                    continue
                for part in expression.split():
                    if part.isalnum() and not part.isdigit():
                        live_variables.add(part)
                opt_tac.append(line)
                live_variables.discard(variable)
            elif 'goto' in line or ':' in line or line.startswith('if'):
                opt_tac.append(line)
                if line.startswith('if'):
                    condition = line.split('goto')[0].replace('if', '').strip()
                    for part in condition.split():
                        if part.isalnum() and not part.isdigit():
                            live_variables.add(part)
            elif line.startswith('return'):
                return_value = line.replace('return', '').strip()
                if return_value.isalnum() and not return_value.isdigit():
                    live_variables.add(return_value)
                opt_tac.append(line)
            else:
                opt_tac.append(line)

        self.code = opt_tac[::-1]


    def update_return(self):
        optimized_code = []

        for line in self.code:
            parts = line.split()

            # Check for return statement
            if parts[0] == "return" and len(parts) == 2:
                return_var = parts[1]

                # Replace the return variable with its constant value if available
                if return_var in self.constants:
                    constant_value = self.constants[return_var]


                    line = f"return {constant_value}"

            optimized_code.append(line)

        self.code = optimized_code

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
            if operator == '--': return left - right

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
            print(f"Error during folding: {e}")
            return "undefined"

    def print_optimized_code(self, stage="Constant Propagation"):
 
        print(f"Optimized TAC ({stage}):")
        for line in self.code:
            print(line)


