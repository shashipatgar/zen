import tkinter as tk
from tkinter import ttk, messagebox
from database_functions import insert_test_result, query_test_result

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
    style.configure("TNotebook.Tab", background="lightblue", padding=[5, 5, 5, 5])


    # Function to handle searching for test results
def on_search():
    serial_number = search_serial_number_entry.get()
    if serial_number:
        results = query_test_result(serial_number)
        if results:
            # Clear previous search results
            for widget in result_frame.winfo_children():
                widget.destroy()

            for i, column in enumerate(results):
                result_text = f"Serial Number: {column[0]}\nStatus: {column[1]}\nFailure Reason: {column[2]}\nFailed as: {column[3]}\nPC Name: {column[4]}\nTime: {column[5]}"
                label = tk.Label(result_frame, text=result_text, justify="left", anchor="w", bg="#f0f0f0", padx=10, pady=5)
                label.grid(row=i, column=0, sticky='w')
        else:
            messagebox.showwarning("Not Found", "No records found for the given serial number.")
    else:
        messagebox.showwarning("Missing Information", "Please enter a serial number to search.")

# Function to handle submission of test results
def on_submit():
    serial_number = serial_number_entry.get()
    status = status_var.get()
    pc_name = Stage_selection.get()
    problem = problem_selection.get()
    #failure_reason = failure_reason_entry.get()

    if serial_number and status and pc_name:
        insert_test_result(serial_number, status, pc_name, problem)
        messagebox.showinfo("Success", "Test result saved.")
        # Clear the fields after submission
        clear_fields()
    else:
        messagebox.showwarning("Missing Information", "Please fill in all required fields.")

# Function to clear form fields after submission
def clear_fields():
    serial_number_entry.delete(0, tk.END)
    status_var.set("Passed")
    Stage_selection.set("")
    problem_selection.set("")
    #failure_reason_entry.delete(0, tk.END)

# Create main window
root = tk.Tk()
root.title("ZenTrace")
root.geometry("1000x600+5+5")  # Position at top-left corner (0,0)
root.config(bg="black")

# Set the background color you want for the frames
bg_color = "#DEF3EE"

# Create a style for the notebook tabs
style = ttk.Style()
style.configure("TNotebook", background="#A2C9C1")
style.configure("TNotebook.Tab", background="darkgreen", foreground="Black")

# Create a notebook (tabs container)
notebook = ttk.Notebook(root)

# Create the frames for the main tabs with the background color
operation_history_frame = ttk.Frame(notebook)
rework_debug_frame = tk.Frame(notebook, bg=bg_color)  # Set background color
module_status_frame = tk.Frame(notebook, bg=bg_color)  # Set background color
seal_scanning_frame = tk.Frame(notebook, bg=bg_color)  # Set background color

# Add the frames as tabs in the notebook
notebook.add(operation_history_frame, text="Operation History")
notebook.add(rework_debug_frame, text="Rework & Debug")
notebook.add(module_status_frame, text="Module Status")
notebook.add(seal_scanning_frame, text="Seal Scanning")

# Add a nested notebook inside "Operation History" for the sub-tabs
operation_history_notebook = ttk.Notebook(operation_history_frame)

# Create frames for the sub-tabs with the background color
meters_frame = tk.Frame(operation_history_notebook, bg=bg_color)  # Set background color
modules_frame = tk.Frame(operation_history_notebook, bg=bg_color)  # Set background color

# Add the sub-tabs to the operation history notebook
operation_history_notebook.add(meters_frame, text="Meters")
operation_history_notebook.add(modules_frame, text="Modules")

# Add search section inside the "Meters" tab (meters_frame)
tk.Label(meters_frame, text="Search Serial Number:", font="bold", bg=bg_color, fg="Black").grid(row=0, column=0, padx=10, pady=10)
search_serial_number_entry = tk.Entry(meters_frame)
search_serial_number_entry.grid(row=0, column=1, padx=(20, 20), pady=(10,10))
search_button = tk.Button(meters_frame, text="Search", command=on_search)
search_button.grid(row=0, column=2, padx=10, pady=10)

# Result frame inside the "Meters" tab to display search results
result_frame = tk.Frame(meters_frame, bg="#f0f0f0")
result_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nw")

# Rework & Debug section
# Serial Number
tk.Label(rework_debug_frame, text="Serial Number:", anchor='w', width=20, bg=rework_debug_frame.cget("bg")).grid(row=0, column=0, padx=10, pady=10, sticky='w')
serial_number_entry = tk.Entry(rework_debug_frame, width=30)
serial_number_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

# Status radio buttons
tk.Label(rework_debug_frame, text="Status:", anchor='w', width=20, bg=rework_debug_frame.cget("bg")).grid(row=1, column=0, padx=10, pady=10, sticky='w')
status_var = tk.StringVar(value="Passed")
tk.Radiobutton(rework_debug_frame, text="Passed", variable=status_var, value="Passed", bg=rework_debug_frame.cget("bg")).grid(row=1, column=1, padx=0, pady=10, sticky='w')
tk.Radiobutton(rework_debug_frame, text="Failed", variable=status_var, value="Failed", bg=rework_debug_frame.cget("bg")).grid(row=1, column=2, padx=0, pady=10, sticky='w')

# Problem selection dropdown
tk.Label(rework_debug_frame, text="Select Problem:", anchor='w', width=20, bg=rework_debug_frame.cget("bg")).grid(row=2, column=0, padx=10, pady=10, sticky='w')
choices = ("Not getting power On", "LED Blinking", "Mag fail", "Relay Disconnect fail", "Relay Open fail")
problem_selection = ttk.Combobox(rework_debug_frame, values=choices, width=27)
problem_selection.grid(row=2, column=1, padx=10, pady=10, sticky='w')

# PC Name entry
tk.Label(rework_debug_frame, text="Stage:", anchor='w', width=20, bg=rework_debug_frame.cget("bg")).grid(row=3, column=0, padx=10, pady=10, sticky='w')
choices = ("Product Integration","Firmware", "TCPIP", "Calibration", "Accuracy", "Parameter testing", "Final Verification")
Stage_selection = ttk.Combobox(rework_debug_frame, values=choices, width=27)
Stage_selection.grid(row=3, column=1, padx=10, pady=10, sticky='w')

'''# Failure Reason entry
tk.Label(rework_debug_frame, text="Failure Reason (if any):", anchor='w', width=20, bg=rework_debug_frame.cget("bg")).grid(row=4, column=0, padx=10, pady=10, sticky='w')
failure_reason_entry = tk.Entry(rework_debug_frame, width=30)
failure_reason_entry.grid(row=4, column=1, padx=10, pady=10, sticky='w')'''


# Submit button
submit_button = tk.Button(rework_debug_frame, text="Submit",bg=rework_debug_frame.cget("bg"), command=on_submit)
submit_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Pack the operation history notebook inside the operation history tab
operation_history_notebook.pack(expand=1, fill="both")

# Pack the main notebook
notebook.pack(expand=1, fill="both")

# Bind the tab change event to highlight the selected tab
notebook.bind("<<NotebookTabChanged>>", on_tab_change)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the Tkinter main loop
root.mainloop()