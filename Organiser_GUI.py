import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from shutil import copy2
from Sort_by_date import Test_PartA
from copy_all_VI import copy_media_files

def select_input_path():
    input_path = filedialog.askdirectory(title="Input Path")
    input_path_entry.delete(0, tk.END)
    input_path_entry.insert(0, input_path)

def select_output_path():
    output_path = filedialog.askdirectory(title="Output Path")
    output_path_entry.delete(0, tk.END)
    output_path_entry.insert(0, output_path)

def execute_program():
    input_path = input_path_entry.get()
    output_path = output_path_entry.get()
    
    # Copy media files
    copy_media_files(input_path, output_path)
    
    # Run Test_PartA function
    Test_PartA(output_path)

    # Show success message
    messagebox.showinfo("Success", "Organized successfully!!")

# Create the main window
root = tk.Tk()
root.title("Path Selector")

# Input path button and entry
input_path_button = tk.Button(root, text="Select Input Path", command=select_input_path)
input_path_button.pack(pady=5)

input_path_entry = tk.Entry(root, width=50)
input_path_entry.pack()

# Output path button and entry
output_path_button = tk.Button(root, text="Select Output Path", command=select_output_path)
output_path_button.pack(pady=5)

output_path_entry = tk.Entry(root, width=50)
output_path_entry.pack()

# Execute button
execute_button = tk.Button(root, text="Execute Program", command=execute_program, height=2, width=20)
execute_button.pack(pady=20)

# Run the main event loop
root.mainloop()