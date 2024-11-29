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
