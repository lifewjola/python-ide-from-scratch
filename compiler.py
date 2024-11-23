import dis
import types
import ast
from parser_simplified import get_ast
import dis
import types

def generate_bytecode_from_ast(node):
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
            process_node(node.func)
            for arg in node.args:
                process_node(arg)
            bytecode_instructions.append(f"CALL_FUNCTION {len(node.args)}")

    # Start processing the root node
    process_node(node)
    
    return bytecode_instructions

# The AST you provided as input
ast_tree = get_ast()

# Generate bytecode instructions
bytecode_instructions = generate_bytecode_from_ast(ast_tree)
print(bytecode_instructions)

def get_bytecode():
    instructions = []
    for instruction in bytecode_instructions:
        instructions.append(instruction)

    return instructions

# def get_bytecodes():


    
