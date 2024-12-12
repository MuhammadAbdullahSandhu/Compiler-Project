mappings = {
    '+': 'add',
    '-': 'sub',
    '*': 'mul',
    '/': 'div',
    '<': 'jl',
    '>': 'jg',
    '<=': 'jle',
    '>=': 'jge',
    '==': 'je',
}

class TACToAssemblyConverter:
    def __init__(self):
        self.assembly_code = []  # List to store generated assembly instructions
        self.local_vars_at = {}  # Tracks variable locations on the stack
        self.stack_offset = 0    # Tracks stack frame size
        self.instruction_size = 4

    def add_instruction(self, instruction):
        """
        Add an instruction to the assembly code.
        """
        self.assembly_code.append(instruction)

    def allocate_stack(self):
        """
        Allocate space on the stack for a variable and update the stack offset.
        """
        self.stack_offset += 4  # Assuming 4 bytes per variable
        return f"[ebp-{self.stack_offset}]"

    def resolve_var(self, var):
        """
        Resolve the stack location of a variable, allocating if necessary.
        """
        if var not in self.local_vars_at:
            self.local_vars_at[var] = self.allocate_stack()
        return self.local_vars_at[var]

    def handle_function_prologue(self, function_name):
        """
        Handle the function prologue (setup stack frame).
        """
        self.add_instruction(f"{function_name}")     # Function label
        self.add_instruction("push ebp")             # Save caller's base pointer
        self.add_instruction("mov ebp, esp")         # Set up the stack frame

    def handle_function_parameters(self, params):
        """
        Handle function parameters by mapping them to stack locations.
        Parameters are passed via `[ebp+offset]`.
        """
        for index, param in enumerate(params):
            # Parameter offset starts at `[ebp+8]`
            offset = (index + 2) * self.instruction_size  
            self.local_vars_at[param] = f"[ebp+{offset}]"
            self.add_instruction(f"; Parameter {param} is located at {self.local_vars_at[param]}")
            

    def handle_function_epilogue(self):
        """
        Handle the function epilogue (cleanup stack frame).
        """
        self.add_instruction("mov esp, ebp")  # Restore stack pointer
        self.add_instruction("pop ebp")      # Restore caller's base pointer
        self.add_instruction("ret")          # Return to the caller

    def handle_arithmetic(self, target, left, operator, right):
        """
        Handle arithmetic operations like `a = b + c`.
        """
        # Resolve locations for the operands
        left_location = self.resolve_var(left)    # Get the location of the left operand (register/stack)
        right_location = self.resolve_var(right)  # Get the location of the right operand (register/stack)

        # Allocate a location for the target variable
        target_location = self.resolve_var(target)

        # Load the left operand into the target location
        self.add_instruction(f"mov {target_location}, {left_location}")

        # Perform the arithmetic operation
        self.add_instruction(f"{mappings[operator]} {target_location}, {right_location}")

    def handle_assignment(self, parts):
        """
        Handle assignments like `a = b` or `a = 5`.
        """
        target, value = parts  # Extract `a`, `=`, and `b` or `5`
        target_location = self.resolve_var(target)  # Resolve stack location for `a`

        # If the value is numeric, move it directly to the target
        if value.isdigit():
            self.add_instruction(f"mov {target_location}, {value}")
        else:
            # Resolve the location of the source variable
            value_location = self.resolve_var(value)
            self.add_instruction(f"mov {target_location}, {value_location}")

    def convert(self, tac_code):
        """
        Convert a list of TAC instructions to assembly.
        """
        for line in tac_code:
            parts = line.split()

            if parts[0] == "function":  # Function definition
                function_name = parts[1]
                params = parts[2:]      # Remaining parts are function parameters
                self.handle_function_prologue(function_name)
                #self.handle_function_parameters(params)

            elif parts[0] == "param":  # Parameter declaration
                self.handle_function_parameters(parts)

            
            # Handle arithmetic operations 
            elif any(op in parts for op in ['+', '-', '*', '/']):
                target = parts[0] 
                left = parts[2] 
                operator = parts[3]
                right = parts[4]
                self.handle_arithmetic(target,left,operator,right)
                # print(f'arithmentic {instruction_parts}')

            elif parts[0] == "end":    # Function end marker
                self.handle_function_epilogue()

    def print_assembly(self):
        """
        Print the generated assembly code.
        """
        print("\nGenerated Assembly Code:")
        for instruction in self.assembly_code:
            print(instruction)



