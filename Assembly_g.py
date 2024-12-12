from tabulate import tabulate

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
instruction_size = 4

registers = ['eax', 'ebx', 'ecx', 'edx']

class AssemblyGenerator:
    assembly_code = []
    local_vars_offset = 0
    local_vars_at = {}
    stack_pointer = 0
    available_registers = registers
    used_registers = {}
    old_locals_vars = {}
    compare_operator = None
    stack = []
    local_variable = 0

    def __init__(self, tac_code):
        self.tac_code = tac_code
        print(self.tac_code )

    def add_instruction(self, assembly_instruction): 
            self.assembly_code.append(assembly_instruction)


# Register functions
    def allocate_register(self):
        if self.available_registers:
            reg = self.available_registers.pop(0)  # Take the first available register
            return reg
        else:
            # Spill to the stack if no registers are available
            reg = self.spill_to_stack()
            return reg

    def free_register(self, reg):
        if reg in self.used_registers:
            del self.used_registers[reg]
            self.available_registers.append(reg)

    def spill_to_stack(self):
        # Spill the last used register to the stack
        reg = self.used_registers.popitem()[0]  # Pop last used register and get its value
        self.stack.append(reg)  # Push value to the stack
        return reg

    def load_from_stack(self, reg):
        if self.stack:
            value = self.stack.pop()  # Pop from the stack
            self.used_registers[reg] = value
            return value

# Helper functions
    def push_to_stack(self, value):
        # Push value to stack
        self.add_instruction(["push", value])
        #self.allocate_to_stack()

    def pop_from_stack(self, value):
        # Remove value from stack
        self.add_instruction(["pop", value])
        #self.remove_from_stack()

    def move(self, to, what):
        self.add_instruction(["mov", to, what])

    def calculate_local_variables(self):
        """
        Analyze the TAC code to calculate the number of unique local variables.
        """
        local_variables = set()

        for line in self.tac_code:
            parts = line.split()
            
            # Skip non-assignment lines
            if len(parts) >= 3 and parts[1] == "=":
                variable = parts[0]
                
                # Exclude temporary variables (e.g., t1, t2) and constants
                if not variable.startswith("t") and not variable.isdigit():
                    local_variables.add(variable)

        return len(local_variables)

    # Parse functions
    def function_prologue(self, instruction):
        # Used at the start of every function to make space
        self.old_locals_vars = self.local_vars_at
        
        #print(f'xxxxxx{self.old_locals_vars}')
        self.add_instruction([instruction[1]])
        #print(f'xxxxx{instruction[-1]}')
        self.push_to_stack("ebp")
        self.move("ebp", "esp")
        #print ( f'local_vars_at {self.local_vars_offset}')
        # self.calculate_local_variables()
        # # Calculate local variable space
        # num_local_vars = self.calculate_local_variables()
        # self.local_variable = num_local_vars
        # total_local_size = num_local_vars * instruction_size

        # if total_local_size > 0:
        #     self.add_instruction(['sub ', 'esp', f'{total_local_size}'])  

        

    def resolve_param(self, instruction):
        # Not same as resolve_var because parameters may not have a default value
        var = instruction[-1]
        #print(f'ID', iD)
        if f"{var}" not in self.local_vars_at:
            self.local_vars_at[f"{var}"] = f"[ebp+{(1 + 1 + len(self.local_vars_at)) * instruction_size}]"
        return self.local_vars_at[f"{var}"]

    def resolve_value(self, token):
        # Compare types first, else run resolve_var
        if not (
                isinstance(token, int)
        ):
            #print("To resolve: ", token)
            return self.resolve_variable(token)
        else:
            return token

    def resolve_variable(self, var):
        # If its a temporary variable assign resgister or else push to stack
        
        #print(f'local variable {self.local_vars_at}')
        if var not in self.local_vars_at:
            #print(f'local{self.local_vars_at}')
            if var.startswith('t'):
                reg = self.allocate_register()
                self.used_registers[reg] = var
                self.local_vars_at[var] = reg
                #print(f'{self.local_vars_at[iD]} = {reg}')
                #print (f'register     {reg}')
            else:
                #print(f'local var offset', self.local_vars_offset)
                self.local_vars_at[var] = f"[ebp-{(1 + self.local_vars_offset) * instruction_size}]"
                self.local_vars_offset += 1

                #print(f'this is the value = {self.local_vars_at[iD]}')

        return self.local_vars_at[var]

    def function_epilogue(self, instruction):
        # Used at closing of every function to clear space
        return_var = instruction[-1]
        #print(f'return_var {return_var}')
        return_value = self.resolve_variable(return_var)
        self.move("eax", return_value)
        self.move("ebp", "esp")
        self.pop_from_stack("ebp")
        self.add_instruction(["ret"])

        self.restore_state()

    def restore_state(self):
        # Restore stack as it was before we made space for a function
        self.local_vars_at = self.old_locals_vars
        self.local_vars_offset = 0
        self.available_registers = registers
        self.used_registers = {}

    def handle_call(self, instruction):

        func_name = instruction[3]
        args = instruction[4:]

        #print(f'arguments', args)
        return_addr = instruction[-1]
        #print (f'return {return_addr}')

        # Parse the arguments and make space for them
        for arg in reversed(args):
            self.push_to_stack(self.resolve_value(arg))

        # Parse the call function
        self.add_instruction(["call", func_name])

        # Decrease the stack, len = num_args * instruction size
        self.add_instruction(["add", "esp", len(args) * instruction_size])
        self.resolve_variable(return_addr)

    def handle_assignment(self, instruction):
        
        var = instruction[0]
        #print(f'to {to}')
        value = instruction[2]

        print(f'assignemnt', var , value)
        #print(f'what {what}')
        value = int(value) if value.isdigit() else value
        to_value = self.resolve_variable(var)
        what_value = self.resolve_value(value)
        #print (f'to value  {to_value}   what value {what_value}')
        self.move(to_value, what_value)
        #print (f'moving ', to_value, what_value)

    def handle_arithmetic(self, target,left,operator,right):
        
        self.handle_assignment([target, '=', left])
        #print(f'to ' ,to)
        left = target
        #print("Changed to", to)
        #print( f'change the value {to}')
        to_value = self.resolve_variable(left)
        
        right = int(right) if right.isdigit() else right
        
        what_value = self.resolve_value(right)
        
        self.add_instruction([mappings[operator], to_value, what_value])

    def handle_new_block(self, instruction):
        block_name = instruction
        #print(f'block name ', block_name)
        self.add_instruction([block_name])

    def handle_comparison(self, target,left,operator,right):
        print (f'target',target,'left', left, 'operator', operator, 'right', right)
        self.handle_assignment([target, '=', left])
        left = target

        right = int(right) if right.isdigit() else right
        to_value = self.resolve_variable(left)
        what_value = self.resolve_value(right)
        self.add_instruction(['cmp', to_value, what_value])
        self.compare_operator = mappings[operator]

    def handle_jump(self, instruction):
        #print(instruction)
        block_name = instruction[-1]
        #print(f'block name : ',  block_name)
        self.add_instruction(['jmp', block_name])

    def handle_conditional_jump(self, instruction):
        block_to_go_to = instruction[-1]
        #print( f'jump ' , block_to_go_to)
        self.add_instruction([self.compare_operator, block_to_go_to])
        self.compare_operator = None

    def parse(self):
        for line in self.tac_code:
            parts = line.split()
            # Handle function prologue (function definitions)
            if parts[0] == 'function':
                self.function_prologue(parts)
                #print(f'Function Prologue: {instruction_parts}')

            # Handle new blocks (labels)
            elif parts[-1] == ':':
                self.handle_new_block(parts)
                print(f'New Block yes: {parts}')
            
            elif parts[0] == 'param':
                self.resolve_param(parts)
                print(f'param {parts}')

             # Handle function calls
            elif 'call' in parts:
                self.handle_call(parts)
                print(f'Function Call: {parts}')

            # Handle assignments
            elif len(parts) == 3 and parts[1] == '=':
                self.handle_assignment(parts)
                #print(f'Assignment {instruction_parts}')
            
            # Handle arithmetic operations 
            elif any(op in parts for op in ['+', '-', '*', '/']):
                target = parts[0] 
                left = parts[2] 
                operator = parts[3]
                right = parts[4]
                self.handle_arithmetic(target,left,operator,right)
                # print(f'arithmentic {instruction_parts}')

            # Handle boolean/comparison operations
            elif any(op in parts for op in ['==', '!=', '<', '>', '<=', '>=']):
                target = parts[0] 
                left = parts[2] 
                operator = parts[3]
                right = parts[4]
                self.handle_comparison(target,left,operator,right)
                #print(f'boolean {instruction_parts}')
            
            # Handle conditional jumps (e.g., if statements)
            elif parts[0] == 'if':
                self.handle_conditional_jump(parts)
                #print(f'if statement {instruction_parts}')
            
            # Handle unconditional jumps (e.g., goto)
            elif parts[0] == 'goto':
                self.handle_jump(parts)
                #print(f'goto {instruction_parts}')

            
            # Handle return statements
            elif parts[0] == 'return':
                self.function_epilogue(parts)
                print(f'return {parts}')
            
           
           
        
        return self.assembly_code

            
    def print_asm(self):
        # Format the assembly_code for tabular display
        table = [[" ".join(map(str, instruction))] for instruction in self.assembly_code]
        print(tabulate(table, headers=["Assembly Code"], tablefmt="fancy_grid"))

                

        
