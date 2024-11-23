import tkinter as tk
from tkinter import scrolledtext
from parser_simplified import tokenizer, parser, optimizer
from compiler import generate_bytecode_from_ast, get_bytecode
from execute import execute_bytecode

# Function to process and link the code
# Function to process and link the code
def run_code():
    # Get the code from the editor
    code = editor.get("1.0", "end-1c")
    
    # Tokenize the code
    tokens = tokenizer(code)
    
    # Parse the tokens
    structured = parser(tokens)
    
    # Optimize the structured code into an AST
    optimized_ast = optimizer(structured)
    
    # Generate bytecode from the AST
    bytecode = generate_bytecode_from_ast(optimized_ast)
    
    # Execute the bytecode and capture the output
    result = execute_bytecode(bytecode)
    
    # Output the result in the output area
    output_area.delete(1.0, tk.END)  # Clear previous output
    output_area.insert(tk.END, f"Output:\n{result}\n")



# Setup the Tkinter GUI
root = tk.Tk()
root.title("Simple Python IDE")

# Create a text editor for code input
editor = scrolledtext.ScrolledText(root, width=80, height=20)
editor.pack(padx=10, pady=10)

# Create a button to run the code
run_button = tk.Button(root, text="Run Code", command=run_code)
run_button.pack(pady=5)

# Create an output area to display results
output_area = scrolledtext.ScrolledText(root, width=80, height=10)
output_area.pack(padx=10, pady=10)

# Run the application
root.mainloop()
