import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import os
from tkcalendar import Calendar  # Import the Calendar widget

# Create the main window
root = tk.Tk()
root.title("Bee Inspection and To-Do List")

# Set window to fullscreen
root.state('zoomed')  # Maximize window but not fully fullscreen
root.configure(bg="#FFF4A3")

# Close button functionality
def close_app():
    """Gracefully close the app when the close button is clicked."""
    root.quit()

# Create a custom close button in the top-right corner
close_button = ttk.Button(root, text="X", command=close_app)
close_button.place(x=root.winfo_screenwidth() - 50, y=10)  # Positioning the button in the top-right corner

# Create a notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Function to save inspection data (Placeholder for demonstration)
def save_inspection_data():
    messagebox.showinfo("Save", "Inspection data saved successfully!")

# --- Inspection Form Tab ---
inspection_tab = ttk.Frame(notebook)
notebook.add(inspection_tab, text="Inspection Form")

# Add content to the Inspection Form tab
inspection_frame = ttk.Frame(inspection_tab)
inspection_frame.pack(fill="both", expand=True, padx=10, pady=10)

scrollbar = ttk.Scrollbar(inspection_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas = tk.Canvas(inspection_frame, yscrollcommand=scrollbar.set, bg="#FFF4A3")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=canvas.yview)

form_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=form_frame, anchor="nw")

# Populate inspection form fields
fields = [
    "Date of Inspection",
    "Queen Status",
    "Colony Population",
    "Presence of Brood",
    "Hive Condition",
    "Honey Harvested",
    "Hive Weight",
    "Honey Stores",
    "Mite Count",
    "Disease Symptoms",
    "Treatment Applied",
    "Pest Control Efforts",
    "Feed Type",
    "Feed Amount",
    "Swarm Warnings",
    "Swarm Actions",
    "Hive Location",
    "Flowering Plants",
    "Equipment Inventory",
    "Equipment Maintenance"
]

entries = {}
for i, field in enumerate(fields):
    label = ttk.Label(form_frame, text=field, background="#FFF4A3")
    label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
    
    # If the field is "Date of Inspection", use the calendar widget
    if field == "Date of Inspection":
        date_entry = Calendar(form_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        date_entry.grid(row=i, column=1, padx=10, pady=5)
        entries[field] = date_entry
    else:
        entry = ttk.Entry(form_frame, width=40)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[field] = entry

# Hive Chart - Create frames for each hive frame
hive_chart_label = ttk.Label(form_frame, text="Hive Chart", background="#FFF4A3", font=("Arial", 14, "bold"))
hive_chart_label.grid(row=len(fields), column=0, columnspan=2, pady=10)

# Frame options for dropdown
frame_options = ["Honey", "Pollen", "Bee Bread", "Brood", "Empty"]

# Dictionary to store frame content
frame_contents = {}

# Create the frame grid for the hive (Horizontal Layout)
num_frames = 10  # Assume 10 frames in the hive
frame_grid_frame = ttk.Frame(form_frame)
frame_grid_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

# Place the frames horizontally
for i in range(num_frames):
    frame_label = ttk.Label(frame_grid_frame, text=f"Frame {i+1}", background="#FFF4A3", font=("Arial", 10))
    frame_label.grid(row=0, column=i, padx=10, pady=5, sticky="w")
    
    # Create a Combobox for selecting the frame content
    frame_combobox = ttk.Combobox(frame_grid_frame, values=frame_options, width=15)
    frame_combobox.grid(row=1, column=i, padx=10, pady=5)
    
    # Store the combobox in the dictionary with the frame number as key
    frame_contents[f"Frame {i+1}"] = frame_combobox

# Save button for inspection form
save_button = ttk.Button(form_frame, text="Save Inspection Data", command=save_inspection_data)
save_button.grid(row=len(fields)+num_frames+2, column=0, columnspan=2, pady=10)

# Update canvas scroll region
form_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# --- To-Do List Tab ---
todo_tab = ttk.Frame(notebook)
notebook.add(todo_tab, text="To-Do List")

# Frame for to-do list
todo_frame = ttk.Frame(todo_tab)
todo_frame.pack(fill="both", expand=True, padx=10, pady=10)

scrollbar_todo = ttk.Scrollbar(todo_frame)
scrollbar_todo.pack(side=tk.RIGHT, fill=tk.Y)

canvas_todo = tk.Canvas(todo_frame, yscrollcommand=scrollbar_todo.set, bg="#FFF4A3")
canvas_todo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_todo.config(command=canvas_todo.yview)

list_frame = ttk.Frame(canvas_todo)
canvas_todo.create_window((0, 0), window=list_frame, anchor="nw")

# To-do list functionality
TODO_FILE = "todo_list.txt"

def load_tasks():
    """Load tasks from file."""
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as file:
            for line in file:
                task, completed = line.strip().split("|", 1)
                add_task(task, completed == "True")

def save_tasks():
    """Save tasks to file."""
    with open(TODO_FILE, "w") as file:
        for widget in list_frame.winfo_children():
            if isinstance(widget, tk.Checkbutton):
                task_text = widget.cget("text")
                completed = task_vars[widget].get()
                file.write(f"{task_text}|{completed}\n")

def add_task(task_text="", completed=False):
    """Add a task to the to-do list."""
    var = tk.BooleanVar(value=completed)
    cb = tk.Checkbutton(
        list_frame,
        text=task_text,
        variable=var,
        font=("Arial", 12),
        onvalue=True,
        offvalue=False,
        command=lambda: toggle_task(cb, var),
        anchor="w",
        bg="#FFF4A3"
    )
    cb.pack(fill="x", pady=2)
    task_vars[cb] = var
    if completed:
        cb.config(fg="gray", font=("Arial", 12, "overstrike"))

    list_frame.update_idletasks()
    canvas_todo.config(scrollregion=canvas_todo.bbox("all"))

def toggle_task(cb, var):
    """Toggle the appearance of a task when checked or unchecked."""
    if var.get():
        cb.config(fg="gray", font=("Arial", 12, "overstrike"))
    else:
        cb.config(fg="black", font=("Arial", 12))
    save_tasks()

def add_new_task():
    """Add a new task from the input box."""
    task_text = task_entry.get()
    if task_text.strip():
        add_task(task_text)
        task_entry.delete(0, tk.END)
        save_tasks()

# Dictionary to hold task variables
task_vars = {}

# Input and button for adding new tasks
task_entry = ttk.Entry(todo_tab, width=50)
task_entry.pack(pady=10)

add_button = ttk.Button(todo_tab, text="Add Task", command=add_new_task)
add_button.pack(pady=5)

# Load tasks from file
load_tasks()

# Update canvas scroll region
list_frame.update_idletasks()
canvas_todo.config(scrollregion=canvas_todo.bbox("all"))

# Run the main loop
root.mainloop()

