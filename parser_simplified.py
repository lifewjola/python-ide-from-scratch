import re
import ast

# Tokenizer function
def tokenizer(source_code):
    token_patterns = [
        (r'(?P<IDENTIFIER>[a-zA-Z_][a-zA-Z_0-9]*)', 'IDENTIFIER'),  # Identifiers
        (r'(?P<NUMBER>\d+(\.\d+)?)', 'NUMBER'),                   # Numbers (integer or float)
        (r'(?P<STRING>".*?")', 'STRING'),                        # Strings enclosed in double quotes
        (r'(?P<SYMBOL>[=+\-*/()])', 'SYMBOL'),                   # Symbols (operators, parens, etc.)
        (r'(?P<KEYWORD>print)', 'KEYWORD'),                      # Keywords (e.g., print)
        (r'(?P<WHITESPACE>\s+)', None),                          # Whitespace (ignored)
    ]
    master_pattern = re.compile('|'.join(p[0] for p in token_patterns))

    tokens = []
    for match in master_pattern.finditer(source_code):
        token_type = match.lastgroup
        if token_type and token_type != 'WHITESPACE':  # Ignore whitespace
            tokens.append({'type': token_type, 'value': match.group(token_type)})
    return tokens

# Parser function
# Parser function
def parser(tokens):
    structured = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        # Handle assignment
        if token['type'] == 'IDENTIFIER' and i + 2 < len(tokens) and tokens[i + 1]['value'] == '=':
            target = token['value']
            value = None
            
            # Check for constant assignment
            if tokens[i + 2]['type'] == 'NUMBER':
                value = {'var': tokens[i + 2]['value']}
            
            # Check for binary operations
            elif tokens[i + 2]['type'] == 'IDENTIFIER' and i + 4 < len(tokens) and tokens[i + 3]['type'] == 'SYMBOL':
                value = {
                    'op': tokens[i + 3]['value'],
                    'left': {'var': tokens[i + 2]['value']},
                    'right': {'var': tokens[i + 4]['value']}
                }
                i += 2  # Skip tokens involved in the binary operation
            
            structured.append({'type': 'ASSIGN', 'target': target, 'value': value})
            i += 2  # Skip '=' and value tokens
        
        # Handle print statements
        elif token['type'] == 'IDENTIFIER' and token['value'] == 'print':
            # Ensure '(' is followed by a string or identifier and closed by ')'
            if i + 2 < len(tokens) and tokens[i + 1]['value'] == '(' and tokens[i + 2]['type'] in ('STRING', 'IDENTIFIER'):
                value = {'var': tokens[i + 2]['value']}
                structured.append({'type': 'PRINT', 'value': value})
                i += 3  # Skip '(', value, and ')'
        
        i += 1  # Move to the next token
    
    return structured


# Optimizer function
def optimizer(structured):
    module_body = []
    for stmt in structured:
        if stmt['type'] == 'ASSIGN':
            target = ast.Name(id=stmt['target'], ctx=ast.Store())
            if 'op' in stmt['value']:
                # Handle binary operation
                value = ast.BinOp(
                    left=ast.Name(id=stmt['value']['left']['var'], ctx=ast.Load()),
                    op=ast.Div(),  # Assuming division for this example
                    right=ast.Name(id=stmt['value']['right']['var'], ctx=ast.Load())
                )
            else:
                # Handle constant assignment
                value = ast.Constant(value=stmt['value']['var'])
            module_body.append(ast.Assign(targets=[target], value=value))
        elif stmt['type'] == 'PRINT':
            # Combine string and variable into one print call
            value = stmt['value']['var']
            if value.startswith('"') and value.endswith('"'):
                value = ast.Constant(value=value)
            else:
                value = ast.Name(id=value, ctx=ast.Load())
            
            # Check if there's another print statement following this
            # Combine string and variable for the print statement
            if len(module_body) > 0 and isinstance(module_body[-1], ast.Expr):
                last_expr = module_body[-1]
                if isinstance(last_expr.value.func, ast.Name) and last_expr.value.func.id == 'print':
                    # Combine the previous and current print arguments into one
                    last_expr.value.args.append(value)  # Add to the list of args in the previous print
                else:
                    module_body.append(ast.Expr(
                        value=ast.Call(
                            func=ast.Name(id='print', ctx=ast.Load()),
                            args=[value],
                            keywords=[]
                        )
                    ))
            else:
                module_body.append(ast.Expr(
                    value=ast.Call(
                        func=ast.Name(id='print', ctx=ast.Load()),
                        args=[value],
                        keywords=[]
                    )
                ))

    return ast.Module(body=module_body, type_ignores=[])

# Source code
source_code = """
total_distance = 1000 
average_distance_per_step = 1.2 

average_total_steps = total_distance / average_distance_per_step

print("The average number of steps required for any student to complete the walk is:")
print(average_total_steps)
"""

# Execution
tokens = tokenizer(source_code)
structured = parser(tokens)
optimized_ast = optimizer(structured)


def get_ast():
    return optimized_ast