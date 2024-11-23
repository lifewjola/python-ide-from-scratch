from compiler import get_bytecode
def execute_bytecode(bytecode_instructions):
    # Simulated environment to store variables and manage the stack
    variables = {}
    stack = []
    
    # Function to handle operations on the stack
    def binary_op(op):
        right = stack.pop()
        left = stack.pop()
        if op == 'DIV':
            stack.append(left / right)  # Perform division
        else:
            raise ValueError(f"Unknown binary operation: {op}")
    
    # To capture all print outputs
    print_output = []

    # Loop through the bytecode instructions
    for instruction in bytecode_instructions:
        parts = instruction.split()
        op = parts[0]
        
        if op == 'LOAD_CONST':
            # Load a constant value onto the stack
            value = ' '.join(parts[1:])
            
            # Check if the constant is numeric (either float or int)
            if value.replace('.', '', 1).isdigit():  # Check for float or int
                stack.append(float(value) if '.' in value else int(value))
            else:
                # Otherwise, it's a string (e.g., print message)
                stack.append(value.strip('"'))  # Strip quotes from string constants
        
        elif op == 'STORE_NAME':
            # Store the value from the stack into a variable
            var_name = parts[1]
            value = stack.pop()
            variables[var_name] = value
        
        elif op == 'LOAD_NAME':
            # Load a variable onto the stack
            var_name = parts[1]
            stack.append(variables.get(var_name, None))
        
        elif op == 'BINARY_OP':
            # Perform a binary operation (e.g., division)
            binary_op(parts[1])
        
        elif op == 'CALL_FUNCTION':
            # Handle function calls (e.g., print)
            num_args = int(parts[1])
            args = [stack.pop() for _ in range(num_args)][::-1]  # Reverse args to maintain order
            
            # Handle multiple arguments to print correctly
            if args:
                # Check if any of the arguments are strings or variables
                output_str = ' '.join(map(str, args))  # Combine arguments to a string
                print_output.append(output_str)  # Add the combined output to the list

    # Collect all the results
    output_str = "\n".join(print_output)  # Combine all output into a single string, each on a new line
    return output_str


# Updated Bytecode
bytecode_instructions = get_bytecode()

# Execute the bytecode and get the output
result = execute_bytecode(bytecode_instructions)

print(result)
