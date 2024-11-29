def parse(tokens):
    structured = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        # Handle assignment
        if token['type'] == 'IDENTIFIER' and i + 2 < len(tokens) and tokens[i + 1]['value'] == '=':
            target = token['value']
            value = None
            
            if (
                tokens[i + 2]['type'] in ('NUMBER', 'IDENTIFIER') and
                i + 4 < len(tokens) and
                tokens[i + 3]['type'] == 'SYMBOL' and
                tokens[i + 4]['type'] in ('NUMBER', 'IDENTIFIER')
            ):
                left_operand = (
                    {'var': tokens[i + 2]['value']} 
                    if tokens[i + 2]['type'] == 'IDENTIFIER' 
                    else {'const': tokens[i + 2]['value']}
                )
                right_operand = (
                    {'var': tokens[i + 4]['value']} 
                    if tokens[i + 4]['type'] == 'IDENTIFIER' 
                    else {'const': tokens[i + 4]['value']}
                )
                value = {
                    'op': tokens[i + 3]['value'],
                    'left': left_operand,
                    'right': right_operand
                }
                i += 2  # Skip tokens involved in the binary operation

                        # Check for constant assignment or binary operation
            elif tokens[i + 2]['type'] in ('NUMBER', 'IDENTIFIER'):
                value = {'var': tokens[i + 2]['value']}
            else:
                raise ValueError(f"Unexpected token sequence in assignment at position {i}: {tokens[i:i + 5]}")
            
            structured.append({'type': 'ASSIGN', 'target': target, 'value': value})
            i += 2  # Skip '=' and value tokens
        
        # Handle print statements
        elif token['type'] == 'IDENTIFIER' and token['value'] == 'print':
            if i + 3 < len(tokens) and tokens[i + 1]['value'] == '(' and tokens[i + 2]['type'] in ('STRING', 'IDENTIFIER', 'NUMBER') and tokens[i + 3]['value'] == ')':
                value = {'var': tokens[i + 2]['value']}
                structured.append({'type': 'PRINT', 'value': value})
                i += 3  # Skip '(', value, and ')'
            else:
                raise ValueError(f"Invalid print statement syntax at position {i}: {tokens[i:i + 4]}")
        
        i += 1  # Move to the next token
    
    return structured

import ast

def optimize(structured):
    module_body = []
    for stmt in structured:
        if stmt['type'] == 'ASSIGN':
            target = ast.Name(id=stmt['target'], ctx=ast.Store())
            
            if 'op' in stmt['value']:
                # Handle binary operation
                left = stmt['value']['left']
                right = stmt['value']['right']
                
                # Convert left operand
                if 'var' in left:
                    left_operand = ast.Name(id=left['var'], ctx=ast.Load())
                else:  # Constant assignment
                    left_operand = ast.Constant(value=left['const'])
                
                # Convert right operand
                if 'var' in right:
                    right_operand = ast.Name(id=right['var'], ctx=ast.Load())
                else:  # Constant assignment
                    right_operand = ast.Constant(value=right['const'])
                
                # Map operator symbol to corresponding AST operator
                op_map = {
                    '+': ast.Add(),
                    '-': ast.Sub(),
                    '*': ast.Mult(),
                    '/': ast.Div()
                }
                
                # Get the operator from the statement and create the BinOp AST node
                op = op_map.get(stmt['value']['op'])
                if not op:
                    raise ValueError(f"Unsupported operator: {stmt['value']['op']}")
                
                # Create binary operation AST node
                value = ast.BinOp(left=left_operand, op=op, right=right_operand)
            else:
                # Handle constant assignment
                value = ast.Constant(value=stmt['value']['var'])
            
            module_body.append(ast.Assign(targets=[target], value=value))
        
        elif stmt['type'] == 'PRINT':
            # Handle print statement
            value = stmt['value']['var']
            if value.startswith('"') and value.endswith('"'):
                value = ast.Constant(value=value)
            else:
                value = ast.Name(id=value, ctx=ast.Load())
            
            # Combine string and variable into one print call
            if len(module_body) > 0 and isinstance(module_body[-1], ast.Expr):
                last_expr = module_body[-1]
                if isinstance(last_expr.value.func, ast.Name) and last_expr.value.func.id == 'print':
                    # Combine the previous and current print arguments into one
                    last_expr.value.args.append(value)
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
