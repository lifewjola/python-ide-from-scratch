import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
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

# Function to open a file
def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                code = file.read()
                editor.delete(1.0, tk.END)  # Clear the current editor content
                editor.insert(tk.END, code)  # Load the file content into the editor
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

# Function to save the file
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, "w") as file:
                code = editor.get("1.0", tk.END)
                file.write(code)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

# Setup the Tkinter GUI
root = tk.Tk()
root.title("Python IDE")

# Maximize window on startup and make it resizeable
root.geometry("800x600")  # Default window size
root.state('zoomed')  # Maximize window on startup

# Create a frame for the editor and buttons
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill="both", expand=True)

# Create a text editor for code input
editor = scrolledtext.ScrolledText(frame, width=80, height=20)
editor.grid(row=0, column=0, padx=5, pady=5, columnspan=3, sticky="nsew")

# Create buttons for file operations and running the code
open_button = tk.Button(frame, text="Open File", command=open_file)
open_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

save_button = tk.Button(frame, text="Save File", command=save_file)
save_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

run_button = tk.Button(frame, text="Run Code", command=run_code)
run_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

# Create an output area to display results
output_area = scrolledtext.ScrolledText(root, width=80, height=10)
output_area.pack(padx=10, pady=10, fill="both", expand=True)

# Make sure the grid rows/columns expand properly
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)

# Run the application
root.mainloop()
