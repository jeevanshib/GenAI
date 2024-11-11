import tkinter as tk  
from tkinter import ttk  
from tkinter import filedialog  
from langchain_community.llms import Ollama  
 
ollama = Ollama(base_url="http://127.0.0.1:11434", model="llama3")  
 
# Create main window  
root = tk.Tk()  
root.title("Code Converter")  
root.geometry("500x400")  
root.configure(bg="light blue")  
file_path=""
# Load and resize the logo  
logo = tk.PhotoImage(file="logo.png")  
resized_logo = logo.subsample(2, 2)  # Change the subsample values to adjust the size  
logo_label = tk.Label(root, image=resized_logo, bg="light blue")  
logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")  
 
# Function to handle file upload  
def upload_file():
    global file_path  
    input_language = input_language_var.get()  
    filetypes = (("Text files", f"*.{input_language.lower()}"), ("All files", "*.*"))  
    file_path = filedialog.askopenfilename(filetypes=filetypes)  
           
           
def doc_generate(file_path):
    with open(file_path, 'r') as file:  
        source_code = file.read()  
    prompt = f'''You are a highly skilled and accurate documentation specialist. Your task is to create detailed documentation for a piece of code written in {input_language_dropdown.get()} . The documentation should include:  
   
- A high-level overview of what the code does.  
- Detailed explanations of each section of the code.  
- Descriptions of all variables, data structures, and their purposes.  
- Explanations of any logic or calculations performed in the code.  
- Annotations about any external libraries or modules used in the code.  
- Any assumptions or prerequisites needed to understand the code.  
 
Here is a piece of code written in {input_language_dropdown.get()}:  
 
{source_code}  
 
Please create comprehensive documentation based on the provided code.  
'''  
 
    SAS_doc = ollama.invoke(prompt)  
    return SAS_doc  
 
 
def generate_documentation():
    print(file_path)
    if file_path:  
        documentation = doc_generate(file_path)  
        text_box1.delete("1.0", tk.END)  
        text_box1.insert("1.0", documentation)
        convert_code(file_path)
 
 
# Function to convert code  
def convert_code(file_path):  
    with open(file_path, 'r') as file:  
        source_code = file.read()  
    output_language = convert_language_var.get()  
    prompt = f'''You are a highly skilled and accurate code converter.  
                Your task is to translate code from one programming language to another,  
                ensuring that the converted code is functionally equivalent to the original, free of syntax and logical errors, and  
                adheres to best practices of the target language.  
                Additionally, please ensure that: All variable names and data structures are appropriately translated to the conventions of the target language.  
                Any necessary libraries or modules required in the target language are properly imported. The syntax of the target language is strictly followed, including proper indentation, use of semicolons, and other language-specific rules.  
                The converted code is well-documented with comments to explain the logic and any changes made during the conversion.  
                Here is a piece of code written in {input_language_dropdown.get()}:\n{source_code}\n  
                Please convert the above code to {output_language}. Provide only {output_language} code as the final output, can include comments but no other information.  
                The output should have only {output_language} code, no notes or descriptions needed.'''  
    converted_code = ollama.invoke(prompt)  
    text_box2.delete("1.0", tk.END)  
    text_box2.insert("1.0", converted_code)  
 
# Input language selection dropdown  
input_language_label = tk.Label(root, text="Select Input Language:", font=("Arial", 12), bg="light blue")  
input_language_label.grid(row=1, column=0, columnspan=2, pady=10)  
 
input_languages = ["SAS", "Pyspark", "Python", "C", "cpp", "Java"]  
input_language_var = tk.StringVar(value="SAS")  # Set default value to "SAS"  
input_language_dropdown = ttk.Combobox(root, textvariable=input_language_var, values=input_languages)  
input_language_dropdown.grid(row=2, column=0, columnspan=2, pady=10)  
 
# Source code file upload button  
upload_button = ttk.Button(root, text="Upload Source Code File", padding=10, command=upload_file)  
upload_button.grid(row=3, column=0, columnspan=2, pady=10)  
 
# Convert language selection dropdown  
convert_language_label = tk.Label(root, text="Select Convert Language:", font=("Arial", 12), bg="light blue")  
convert_language_label.grid(row=4, column=0, columnspan=2, pady=10)  
 
convert_languages = ["Python", "Pyspark", "C", "C++", "Java"]  
convert_language_var = tk.StringVar(value="Python")  # Set default value to "Python"  
convert_language_dropdown = ttk.Combobox(root, textvariable=convert_language_var, values=convert_languages)  
convert_language_dropdown.grid(row=5, column=0, columnspan=2, pady=10)  
 
# Submit button  
submit_button = ttk.Button(root, text="Submit", padding=10, command=generate_documentation)  
submit_button.grid(row=6, column=0, columnspan=2, pady=10)  
 
# Text box 1 (Source file document)  
text_box1_label = tk.Label(root, text="Document of Source File:", font=("Arial", 12), bg="light blue")  
text_box1_label.grid(row=7, column=0, padx=10)  
 
text_box1 = tk.Text(root, height=10, width=50)  
text_box1.grid(row=8, column=0, padx=10, pady=(0, 10))  
 
# Text box 2 (Output code)  
text_box2_label = tk.Label(root, text="Output Code:", font=("Arial", 12), bg="light blue")  
text_box2_label.grid(row=7, column=1, padx=10)  
 
text_box2 = tk.Text(root, height=10, width=45)  
text_box2.grid(row=8, column=1, pady=(0, 7))  
 
# Download buttons  
def download_file2():  
    extension=convert_language_dropdown.get()
    file_path = filedialog.asksaveasfilename(defaultextension=extension, filetypes=(("Text files", "*.txt"), ("All files", "*.*")))  
    if file_path:  
        content = text_box2.get("1.0", tk.END) if download_button1 in root.focus_get() else text_box1.get("1.0", tk.END)  
        with open(file_path, "w") as file:  
            file.write(content)    
           
def download_file1():  
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))  
    if file_path:  
        content = text_box1.get("1.0", tk.END) if download_button1 in root.focus_get() else text_box2.get("1.0", tk.END)  
        with open(file_path, "w") as file:  
            file.write(content)  
 
download_button1 = ttk.Button(root, text="Download", padding=10,command=download_file1)  
download_button1.grid(row=9, column=0, padx=(10, 5), pady=10)
 
 
download_button2 = ttk.Button(root, text="Download", padding=10, command=download_file2)  
download_button2.grid(row=9, column=1, padx=(5, 10), pady=10)  
 
# Configure column and row weights  
root.grid_columnconfigure(0, weight=1)  
root.grid_columnconfigure(1, weight=1)  
root.grid_rowconfigure(8, weight=1)  
 
# Run main loop  
root.mainloop()  