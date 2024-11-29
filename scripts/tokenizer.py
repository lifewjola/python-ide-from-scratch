import re

def tokenize(source_code):
    # Define token patterns
    token_patterns = [
        (r'(?P<IDENTIFIER>[a-zA-Z_][a-zA-Z_0-9]*)', 'IDENTIFIER'), 
        (r'(?P<NUMBER>\d+(\.\d+)?)', 'NUMBER'), 
        (r'(?P<STRING>".*?")', 'STRING'), 
        (r'(?P<SYMBOL>[=+\-*/()])', 'SYMBOL'),
        (r'(?P<KEYWORD>print)', 'KEYWORD'), 
        (r'(?P<WHITESPACE>\s+)', None),
        (r'(?P<UNKNOWN>.)', 'UNKNOWN')  # Catch-all for unrecognized tokens
    ]

    # Combine patterns
    master_pattern = re.compile('|'.join(p[0] for p in token_patterns))

    tokens = []
    for match in master_pattern.finditer(source_code):
        token_type = match.lastgroup
        token_value = match.group()
        
        # Check token type
        if token_type == 'WHITESPACE':
            continue  # Ignore white space
        elif token_type == 'UNKNOWN':
            raise ValueError(f"Unrecognized token: {token_value}")
        else:
            tokens.append({'type': token_type, 'value': token_value})
    
    return tokens
