import ast

def generate_bytecode(node):
    bytecode_instructions = []

    def process_node(node):
        if isinstance(node, ast.Module):
            # Process the body of the module (which contains statements like assignments, print, etc.)
            for stmt in node.body:
                process_node(stmt)

        elif isinstance(node, ast.Assign):
            # Handle assignment (target = value)
            for target in node.targets:
                if isinstance(target, ast.Name) and isinstance(node.value, ast.Constant):
                    # Store the value in a local variable (store operation)
                    bytecode_instructions.append(f"LOAD_CONST {node.value.value}")
                    bytecode_instructions.append(f"STORE_NAME {target.id}")
                elif isinstance(target, ast.Name) and isinstance(node.value, ast.BinOp):
                    # Handle binary operation assignment
                    process_node(node.value)  # Process the operation (left, right)
                    bytecode_instructions.append(f"STORE_NAME {target.id}")

        elif isinstance(node, ast.BinOp):
            # Handle binary operations like division, addition, etc.
            process_node(node.left)  # Process the left operand
            process_node(node.right)  # Process the right operand
            bytecode_instructions.append(f"BINARY_OP {type(node.op).__name__.upper()}")

        elif isinstance(node, ast.Name):
            # Load a variable (either for reading or writing)
            bytecode_instructions.append(f"LOAD_NAME {node.id}")

        elif isinstance(node, ast.Constant):
            # Load a constant value
            bytecode_instructions.append(f"LOAD_CONST {node.value}")

        elif isinstance(node, ast.Expr):
            # Handle expression (like print)
            process_node(node.value)
            
        elif isinstance(node, ast.Call):
            # Process function calls (like print)
            if isinstance(node.func, ast.Name) and node.func.id == 'print':
                # For the print function, load the arguments onto the stack
                for arg in node.args:
                    process_node(arg)
                # Append the call to print
                bytecode_instructions.append(f"CALL_FUNCTION {len(node.args)}")
            else:
                # Handle other function calls (if needed)
                process_node(node.func)
                for arg in node.args:
                    process_node(arg)
                bytecode_instructions.append(f"CALL_FUNCTION {len(node.args)}")

    # Start processing the root node
    process_node(node)
    
    return bytecode_instructions
