import tkinter as tk
from tkinter import scrolledtext
from tokenizer import tokenize
from parser import parse
from optimizer import optimize
from compiler import generate_bytecode
from execute import execute

# Function to process and link the code
def run_code():
    try:
        # Clear previous output
        output_area.delete(1.0, tk.END)
        
        # Get the code from the editor
        code = editor.get("1.0", "end-1c")
        
        # Tokenize the code
        tokens = tokenize(code)
        
        # Parse the tokens
        structured = parse(tokens)
        
        # Optimize the structured code into an AST
        optimized_ast = optimize(structured)
        
        # Generate bytecode from the AST
        bytecode = generate_bytecode(optimized_ast)
        
        # Execute the bytecode and capture the output
        result = execute(bytecode)
        
        # Display the result in the output area
        output_area.insert(tk.END, f"Output:\n{result}\n")
    
    except Exception as e:
        # Display the error message in the output area
        output_area.insert(tk.END, f"Error:\n{e}\n")




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
