import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Function to save link to database with timestamp
def save_to_database():
    link = link_entry.get()
    position = position_entry.get()
    notes = notes_entry.get("1.0", tk.END).strip()  # Get notes from Text widget
    source = source_var.get()  # Get selected source
    upload_resume = upload_resume_var.get()  # Get upload resume boolean
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("INSERT INTO links (link, position, notes, source, upload_resume, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                       (link, position, notes, source, upload_resume, timestamp))
        conn.commit()
        messagebox.showinfo("Success", "Link saved to database.")
        # Clear entry fields after saving
        link_entry.delete(0, tk.END)
        position_entry.delete(0, tk.END)
        notes_entry.delete("1.0", tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save link to database: {e}")

# Function to handle right-click context menu
def copy_text():
    root.clipboard_clear()
    root.clipboard_append(root.focus_get().get())

def cut_text():
    copy_text()
    root.focus_get().delete(0, tk.END)

def paste_text():
    root.focus_get().insert(tk.END, root.clipboard_get())

# Create SQLite database
conn = sqlite3.connect('links.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS links 
                  (id INTEGER PRIMARY KEY, link TEXT, position TEXT, notes TEXT, 
                  source TEXT, upload_resume BOOLEAN, timestamp TIMESTAMP)''')

# Create main window
root = tk.Tk()
root.title("Link and Position Saver")

# Link entry field
link_label = tk.Label(root, text="Link:")
link_label.grid(row=0, column=0, padx=5, pady=5)
link_entry = tk.Entry(root, width=50)
link_entry.grid(row=0, column=1, padx=5, pady=5)
# Enable right-click copy and paste
link_entry.bind("<Button-3>", lambda e: link_entry_copy_paste_menu.post(e.x_root, e.y_root))
link_entry_copy_paste_menu = tk.Menu(link_entry, tearoff=0)
link_entry_copy_paste_menu.add_command(label="Cut", command=cut_text)
link_entry_copy_paste_menu.add_command(label="Copy", command=copy_text)
link_entry_copy_paste_menu.add_command(label="Paste", command=paste_text)

# Position entry field
position_label = tk.Label(root, text="Position:")
position_label.grid(row=1, column=0, padx=5, pady=5)
position_entry = tk.Entry(root, width=50)
position_entry.grid(row=1, column=1, padx=5, pady=5)
# Enable right-click copy and paste
position_entry.bind("<Button-3>", lambda e: position_entry_copy_paste_menu.post(e.x_root, e.y_root))
position_entry_copy_paste_menu = tk.Menu(position_entry, tearoff=0)
position_entry_copy_paste_menu.add_command(label="Cut", command=cut_text)
position_entry_copy_paste_menu.add_command(label="Copy", command=copy_text)
position_entry_copy_paste_menu.add_command(label="Paste", command=paste_text)

# Notes entry field
notes_label = tk.Label(root, text="Notes:")
notes_label.grid(row=2, column=0, padx=5, pady=5)
notes_entry = tk.Text(root, width=50, height=5)
notes_entry.grid(row=2, column=1, padx=5, pady=5)
# Enable right-click copy and paste
notes_entry.bind("<Button-3>", lambda e: notes_entry_copy_paste_menu.post(e.x_root, e.y_root))
notes_entry_copy_paste_menu = tk.Menu(notes_entry, tearoff=0)
notes_entry_copy_paste_menu.add_command(label="Cut", command=cut_text)
notes_entry_copy_paste_menu.add_command(label="Copy", command=copy_text)
notes_entry_copy_paste_menu.add_command(label="Paste", command=paste_text)

# Source selection dropdown
source_label = tk.Label(root, text="Source:")
source_label.grid(row=3, column=0, padx=5, pady=5)
source_var = tk.StringVar(root)
source_choices = ["LinkedIn", "Indeed", "Other"]
source_dropdown = tk.OptionMenu(root, source_var, *source_choices)
source_dropdown.grid(row=3, column=1, padx=5, pady=5)

# Checkbox for uploading custom resume
upload_resume_var = tk.BooleanVar(root)
upload_resume_checkbox = tk.Checkbutton(root, text="Upload Custom Resume", variable=upload_resume_var)
upload_resume_checkbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Save button
save_button = tk.Button(root, text="Save", command=save_to_database)
save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
