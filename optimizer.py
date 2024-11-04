

def optimizer_constant_folding(left, operator, right):
    try:
        if operator in ['++', '--']:
            # Convert the operand to float
            left = float(left)  
            
            if operator == '++':
                result = left + 1
            elif operator == '--':
                result = left - 1

            # Return as int if the result is an integer, otherwise as float
            return int(result) if result.is_integer() else result
        
        # Attempt to convert both operands to float (to support both int and float)
        left = float(left)
        right = float(right)

        # Perform the operation based on the operator
        if operator == '+':
            result = left + right
        elif operator == '-':
            result = left - right
        elif operator == '*':
            result = left * right
        elif operator == '/':
            if right == 0:
                assert("Division by zero")
            result = left / right 
        elif operator == '%':
            if right == 0:
                raise ("Modulo by zero")
            result = left % right
        elif operator == ">=":
            return left >= right
        elif operator == "<=":
            return left <= right
        elif operator == "==":
            return left == right
        elif operator == "!=":
            return left != right
        elif operator == ">":
            return left > right
        elif operator == "<":
            return left < right
        else:
            raise ValueError(f"Unsupported operator: {operator}")

        return int(result) if result.is_integer() else result

    except ValueError:
        # If operands are not numbers or cannot be converted, return None
        return None
      
