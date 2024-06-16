import os
import logging
import webbrowser
from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

HISTORY_FILE = "merge_history.txt"
LOG_FILE = "merge_log.txt"

class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.configure(state='disabled')
            self.text_widget.yview(tk.END)
        self.text_widget.after(0, append)

def setup_logging(log_text_widget):
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    handler = TextHandler(log_text_widget)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(handler)

def find_pdfs(directory):
    pdf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

def merge_pdfs(pdf_files, output_path):
    pdf_writer = PdfWriter()
    
    logging.info("Starting Merging Process")
    logging.info("Loading Files")
    logging.info("Files to merge:")
    for pdf_file in pdf_files:
        logging.info(pdf_file)
    
    for pdf_file in pdf_files:
        try:
            logging.info(f"Merging {pdf_file}")
            pdf_reader = PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])
        except Exception as e:
            logging.error(f"Error reading {pdf_file}: {e}")
    
    try:
        with open(output_path, 'wb') as out:
            pdf_writer.write(out)
        log_history(output_path)
        logging.info("Merge complete")
        logging.info(f"Destination of merged file: {output_path}")
    except Exception as e:
        logging.error(f"Error writing to {output_path}: {e}")

def log_history(output_path):
    with open(HISTORY_FILE, 'a') as file:
        file.write(output_path + '\n')

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as file:
            return file.readlines()
    return []

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry_dir.delete(0, tk.END)
        entry_dir.insert(0, directory)

def save_file():
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                               filetypes=[("PDF files", "*.pdf")])
    if output_path:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, output_path)

def open_file_in_explorer(filepath):
    if os.name == 'nt':  # Windows
        os.startfile(filepath)
    elif os.name == 'posix':  # macOS or Linux
        webbrowser.open(filepath)

def start_merge():
    directory = entry_dir.get()
    output_path = entry_output.get()
    
    if not directory or not output_path:
        messagebox.showerror("Error", "Both directory and output file must be specified")
        return
    
    try:
        pdf_files = find_pdfs(directory)
        if not pdf_files:
            messagebox.showinfo("Info", "No PDF files found in the selected directory")
            return
        
        merge_pdfs(pdf_files, output_path)
        update_history_tab()
        messagebox.showinfo("Success", f"Successfully merged {len(pdf_files)} PDFs into {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def update_history_tab():
    history_list.delete(0, tk.END)
    for line in load_history():
        history_list.insert(tk.END, line.strip())

# Create the main window
root = tk.Tk()
root.title("PDF Merger")
root.geometry("800x600")

# Create a tabbed interface
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Configure resizing for the root window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Merge tab
frame_merge = ttk.Frame(notebook)
notebook.add(frame_merge, text="Merge PDFs")

# Directory selection
frame_dir = ttk.Frame(frame_merge)
frame_dir.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
frame_merge.grid_columnconfigure(0, weight=1)

label_dir = ttk.Label(frame_dir, text="Select Directory:", font=("Helvetica", 12))
label_dir.grid(row=0, column=0, sticky="w")

entry_dir = ttk.Entry(frame_dir, width=50, font=("Helvetica", 12))
entry_dir.grid(row=0, column=1, padx=5, sticky="ew")
frame_dir.grid_columnconfigure(1, weight=1)

button_dir = ttk.Button(frame_dir, text="Browse...", command=select_directory)
button_dir.grid(row=0, column=2)

# Output file selection
frame_output = ttk.Frame(frame_merge)
frame_output.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

label_output = ttk.Label(frame_output, text="Output File:", font=("Helvetica", 12))
label_output.grid(row=0, column=0, sticky="w")

entry_output = ttk.Entry(frame_output, width=50, font=("Helvetica", 12))
entry_output.grid(row=0, column=1, padx=5, sticky="ew")
frame_output.grid_columnconfigure(1, weight=1)

button_output = ttk.Button(frame_output, text="Browse...", command=save_file)
button_output.grid(row=0, column=2)

# Merge button
button_merge = ttk.Button(frame_merge, text="Merge PDFs", command=start_merge)
button_merge.grid(row=2, column=0, pady=10)

# Log tab
frame_log = ttk.Frame(notebook)
notebook.add(frame_log, text="Log")

log_text = tk.Text(frame_log, wrap="word", font=("Helvetica", 12), state="disabled")
log_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
frame_log.grid_rowconfigure(0, weight=1)
frame_log.grid_columnconfigure(0, weight=1)

# History tab
frame_history = ttk.Frame(notebook)
notebook.add(frame_history, text="History")

history_list = tk.Listbox(frame_history, font=("Helvetica", 12))
history_list.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
frame_history.grid_rowconfigure(0, weight=1)
frame_history.grid_columnconfigure(0, weight=1)

# Make the output paths clickable
def on_history_click(event):
    selection = history_list.curselection()
    if selection:
        filepath = history_list.get(selection[0])
        open_file_in_explorer(filepath)

history_list.bind('<Double-1>', on_history_click)

# Setup logging
setup_logging(log_text)

# Initial load of history
update_history_tab()

# Run the application
root.mainloop()
