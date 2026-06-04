import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from mysql.connector import Error

# ==========================================
# 1. DATABASE SETUP LOGIC
# ==========================================
def initialize_database():
    try:
        # Connect to the general server landing pad using your working password
        conn = mysql.connector.connect(
            host="",
            user="",
            password=""
        )
        cursor = conn.cursor()
        
        # Create and select the database room
        cursor.execute("CREATE DATABASE IF NOT EXISTS student_db;")
        cursor.execute("USE student_db;")
        
        # Build the physical storage table layout
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                grade VARCHAR(10) NOT NULL
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Database initialization error: {e}")

# Run setup immediately when script boots up to ensure DB exists
initialize_database()


# ==========================================
# 2. BUTTON CLICK ACTION FUNCTIONS
# ==========================================
'''
def submit_student_data():
    """Triggered when user clicks 'Save Student Info'"""
    student_name = name_entry.get().strip()
    student_grade = grade_entry.get().strip()
    
    # Validation checklist guard rail
    if not student_name or not student_grade:
        messagebox.showwarning("Missing Information", "Please fill out both Name and Grade fields!")
        return

    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root123456",
            database="student_db" # Safe to specify now since initialization step created it
        )
        cursor = conn.cursor()
        
        # Parameterized insertion for security tracking
        query = "INSERT INTO students (name, grade) VALUES (%s, %s);"
        cursor.execute(query, (student_name, student_grade))
        conn.commit()
        
        messagebox.showinfo("Success", f"🎉 Saved {student_name} (Grade: {student_grade}) to the database!")
        
        # Clear interface data slots
        name_entry.delete(0, tk.END)
        grade_entry.delete(0, tk.END)
        
    except Error as e:
        messagebox.showerror("Database Error", f"Failed to push data: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def clear_entry_fields():
    """Triggered when user clicks 'Clear Fields'"""
    name_entry.delete(0, tk.END)
    grade_entry.delete(0, tk.END)
'''

# ==========================================
# 3. TKINTER INTERFACE AND LAYOUT
# ==========================================

root = tk.Tk()
root.title("Library Unified Network Database")
root.geometry("1080x640")
root.configure(bg="#121212") # Light grey structural theme context

# Title Screen Banner
title_label = tk.Label(root, text="HOME", font=("Segoe UI", 63, "bold"), bg="#121212", fg="#E1E1E1")
title_label.pack(pady=15)
style = ttk.Style()
style.theme_use('clam')  # 'clam' theme allows color changes on Mac

style.configure(
    "Custom.TButton",
    font=("Segoe UI", 31, "bold"),
    background="#FFFCC6",       # Your custom pink hex background
    foreground="black",         # Text color
    borderwidth=0,
             # Darker shade for hover/click feel
    activeforeground="black"
    ,cursor="hand2"
)
# --- Name Field Container ---
#name_label = tk.Label(root, text="Student Name:", font=("Arial", 11), bg="#f0f0f0")
#name_label.pack(anchor="w", padx=40)
#name_entry = tk.Entry(root, width=30, font=("Arial", 11))
#name_entry.pack(pady=5)

# --- Grade Field Container ---
#grade_label = tk.Label(root, text="Assigned Grade:", font=("Arial", 11), bg="#f0f0f0")
#grade_label.pack(anchor="w", padx=40, pady=(5, 0))
#grade_entry = tk.Entry(root, width=30, font=("Arial", 11))
#grade_entry.pack(pady=5)
# --- Action Buttons Layout Container ---
# Save Submission Button
regst = ttk.Button(root, text="Register", style="Custom.TButton",width=15)
srch= ttk.Button(root, text="Search", style="Custom.TButton",width=15)
shtbl = ttk.Button(root, text="Show Tables", style="Custom.TButton",width=15)
exit = ttk.Button(root, text="Exit", style="Custom.TButton",width=15)
#func call
regst.pack(anchor="w", padx=(40, 0), pady=(40, 70))
srch.pack(anchor="w", padx=(40, 0), pady=(0, 70))
shtbl.pack(anchor="w", padx=(40, 0), pady=(0, 70))
exit.pack(anchor="w", padx=(40, 0), pady=(0, 70))

vertical_line = tk.Frame(root, width=6, bg='#007AFF' ) 
#vertical_line.pack(fill="y", expand=True,side="left", padx=530, pady=0)
vertical_line.place(
    relx=0.5,
    rely=0.2,
    relheight=0.9,
    anchor="n")


# Start application interaction engine tracking loops
root.mainloop()
