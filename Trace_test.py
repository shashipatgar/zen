import tkinter as tk
from tkinter import ttk, messagebox
from database_functions import insert_test_result, query_test_result,create_connection
from connect_create_Database import verify_connection

# Function to change the tab highlight when clicked
def on_tab_change(event):
    notebook = event.widget
    current_tab = notebook.index("current")
    
    for i in range(notebook.index("end")):
        if i == current_tab:
            notebook.tab(i, padding=[1, 1, 1, 1])
        else:
            notebook.tab(i, padding=[1, 1,1,1])
    
    style.configure("TNotebook.Tab", background="#B9DCD4")
    style.configure("TNotebook.Tab", background="blue", padding=[5, 5, 5, 5])
    
# Function to handle submission of test results
def on_submit():
    serial_number = serial_number_entry.get()
    pcba_number=PCBA_Number_entry.get()
    status = status_var.get()
    pc_name = pc_name_entry.get()
    problem = problem_selection.get()
    Failure_stage=Stage_selection.get()
    #failure_reason = failure_reason_entry.get()
    
    if serial_number and status and pc_name:
        insert_test_result(serial_number,pcba_number, status, pc_name, problem,Failure_stage)
        messagebox.showinfo("Success", "Test result saved.")
        
        # Clear all fields after submission
        serial_number_entry.delete(0, tk.END)
        PCBA_Number_entry.delete(0, tk.END)
        status_var.set("Failed")
        pc_name_entry.delete(0, tk.END)
        problem_selection.set("")
        Stage_selection.set("")
    else:
        messagebox.showwarning("Missing Information", "Please fill in all required fields.")

# Function to handle searching for test results
def on_search():
    serial_number = search_serial_number_entry.get()
    pcba_number=PCBA_Number_entry.get()
    
    if serial_number or pcba_number:
        results = query_test_result(serial_number,pcba_number)
        if results:
            display_results(results)
        else:
            clear_results()
            messagebox.showwarning("Not Found", "No records found for the given serial number.")
    else:
        messagebox.showwarning("Missing Information", "Please enter a serial number to search.")

def display_results(results):
    clear_results()  # Clear any existing results first

    headers = ["Serial Number","PCBA_number", "Status", "Failure Reason", "Problem", "PC Name", "Date & Time"]
    
    for col, header in enumerate(headers):
        tk.Label(result_frame, text=header, bg="#fff",font=('Helvetica', 12, 'bold')).grid(row=0, column=col, padx=10, pady=5)
    
    for row, result in enumerate(results, start=1):
        for col, value in enumerate(result):
            tk.Label(result_frame, text=value, bg="#fff",font=('Helvetica', 10)).grid(row=row, column=col, padx=10, pady=5)

def clear_results():
    # Remove all widgets in the result_frame
    for widget in result_frame.winfo_children():
        widget.destroy()

# Create main window
root = tk.Tk()
root.title("ZenTrace")
root.geometry("1300x720+5+5")  # Position at top-left corner
root.maxsize(1800, 800)
root.minsize(1000, 600)

# Set the background color for frames
bg_color = "#DEF3EE"

# Create a style for the notebook tabs
style = ttk.Style()
style.configure("TNotebook", background="#A2C9C1")
style.configure("TNotebook.Tab", background="darkgreen", foreground="Black")

# Create a notebook (tabs container)
notebook = ttk.Notebook(root)

# Create the frames for the main tabs with the background color
operation_history_frame = ttk.Frame(notebook)
rework_debug_frame = tk.Frame(notebook, bg=bg_color)
module_status_frame = tk.Frame(notebook, bg=bg_color)
seal_scanning_frame = tk.Frame(notebook, bg=bg_color)

# Add the frames as tabs in the notebook
notebook.add(operation_history_frame, text="Operation History")
notebook.add(rework_debug_frame, text="Rework & Debug")
notebook.add(module_status_frame, text="Module Status")
notebook.add(seal_scanning_frame, text="Seal Scanning")

# Add a nested notebook inside "Operation History" for the sub-tabs
operation_history_notebook = ttk.Notebook(operation_history_frame)

# Create frames for the sub-tabs
meters_frame = tk.Frame(operation_history_notebook, bg=bg_color)
Failure_History_frame = ttk.Frame(operation_history_notebook)

# Add the sub-tabs to the operation history notebook
operation_history_notebook.add(meters_frame, text="Meters")
operation_history_notebook.add(Failure_History_frame, text="Failure History")

# Add search section inside the "Failure History" tab
tk.Label(Failure_History_frame, text="Search Serial Number:", font="lucida 8 bold", bg=meters_frame.cget("bg"), fg="Black").grid(row=0, column=0, padx=10, pady=10)
search_serial_number_entry = tk.Entry(Failure_History_frame)
search_serial_number_entry.grid(row=0, column=1, padx=(20, 20), pady=(10, 10))

search_button = tk.Button(Failure_History_frame, text="Search", command=on_search)
search_button.grid(row=0, column=2, padx=10, pady=10)

# Result frame inside the "Failure History" tab
result_frame = tk.Frame(Failure_History_frame, bg="#f0f0f0")
result_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nw")

# Add dummy tabs for additional functionality
dummy_tab1_frame = ttk.Frame(operation_history_notebook)
operation_history_notebook.add(dummy_tab1_frame, text="Low Voltage")
dummy_tab2_frame = ttk.Frame(operation_history_notebook)
operation_history_notebook.add(dummy_tab2_frame, text="High Voltage")

# Rework & Debug section
# Serial Number
tk.Label(meters_frame, text="Serial Number:", anchor='w', width=20, font="lucida 8 bold", bg="light grey").grid(row=0, column=0, padx=10, pady=10, sticky='w')
serial_number_entry = tk.Entry(meters_frame, width=30)
serial_number_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

# PCBA Number
tk.Label(meters_frame, text="PCBA Number:", anchor='w', width=20, font="lucida 8 bold", bg="light grey").grid(row=0, column=3, padx=2, pady=10, sticky='w')
PCBA_Number_entry = tk.Entry(meters_frame, width=30)
PCBA_Number_entry.grid(row=0, column=4, padx=10, pady=10, sticky='w')

# Status radio buttons
tk.Label(meters_frame, text="Status:", anchor='w', width=20, font="lucida 8 bold", bg="light grey").grid(row=1, column=0, padx=10, pady=10, sticky='w')
status_var = tk.StringVar(value="Failed")
tk.Radiobutton(meters_frame, text="Passed", variable=status_var, value="Passed", bg=meters_frame.cget("bg")).grid(row=1, column=1, padx=0, pady=10, sticky='w')
tk.Radiobutton(meters_frame, text="Failed", variable=status_var, value="Failed", bg=meters_frame.cget("bg")).grid(row=1, column=2, padx=0, pady=10, sticky='w')

# PC Name
tk.Label(meters_frame, text="PC Name:", anchor='w', width=20, font="lucida 8 bold", bg="light grey").grid(row=2, column=0, padx=10, pady=10, sticky='w')
pc_name_entry = tk.Entry(meters_frame, width=30)
pc_name_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

# Failure Stage dropdown
tk.Label(meters_frame, text="Failure Stage:", anchor='w', width=20, font="lucida 8 bold", bg="light grey").grid(row=2, column=3, padx=2, pady=10, sticky='w')
choices = ("Product Integration","Firmware", "TCPIP", "Calibration", "Accuracy", "Parameter testing", "Final Verification")
Stage_selection = ttk.Combobox(meters_frame, values=choices, width=27)
Stage_selection.grid(row=2, column=4, padx=10, pady=10, sticky='w')



# Problem selection dropdown
tk.Label(meters_frame, text="Select Problem:", anchor='w', width=20,  font="lucida 8 bold",bg="light grey").grid(row=3, column=0, padx=10, pady=10, sticky='w')
choices = ("Not getting power On", "LED Blinking", "Mag fail", "Relay Disconnect fail", "Relay Open fail")
problem_selection = ttk.Combobox(meters_frame, values=choices, width=27)
problem_selection.grid(row=3, column=1, padx=10, pady=10, sticky='w')

# Submit button
submit_button = tk.Button(meters_frame, text="Submit", command=on_submit)
submit_button.grid(row=4, column=1, padx=10, pady=10, sticky='w')

# Clear all fields button
clear_button = tk.Button(operation_history_notebook,bg="dark green", fg="white",text="check database", command= verify_connection)
clear_button.pack(side="right",anchor="ne",padx=5,pady=5)

# Place the tab containers on the main window
notebook.pack(expand=True, fill='both')
operation_history_notebook.pack(expand=True, fill='both')

# Bind the tab change event to the highlighting function
notebook.bind("<<NotebookTabChanged>>", on_tab_change)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the application
root.mainloop()