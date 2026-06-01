import tkinter as tk
from tkinter import messagebox
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
            host="",
            user="",
            password="",
            database="" # Safe to specify now since initialization step created it
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


# ==========================================
# 3. TKINTER INTERFACE AND LAYOUT
# ==========================================
root = tk.Tk()
root.title("Student Database Portal")
root.geometry("350x280")
root.configure(bg="#f0f0f0") # Light grey structural theme context

# Title Screen Banner
title_label = tk.Label(root, text="Student Data Registry", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333333")
title_label.pack(pady=15)

# --- Name Field Container ---
name_label = tk.Label(root, text="Student Name:", font=("Arial", 11), bg="#f0f0f0")
name_label.pack(anchor="w", padx=40)
name_entry = tk.Entry(root, width=30, font=("Arial", 11))
name_entry.pack(pady=5)

# --- Grade Field Container ---
grade_label = tk.Label(root, text="Assigned Grade:", font=("Arial", 11), bg="#f0f0f0")
grade_label.pack(anchor="w", padx=40, pady=(5, 0))
grade_entry = tk.Entry(root, width=30, font=("Arial", 11))
grade_entry.pack(pady=5)

# --- Action Buttons Layout Container ---
# Save Submission Button
save_btn = tk.Button(
    root, 
    text="Save Student Info", 
    command=submit_student_data, # Maps to our database write function
    bg="#4CAF50", 
    fg="black", 
    font=("Arial", 11, "bold"),
    padx=10,
    pady=5
)
save_btn.pack(pady=(20, 5))

# Reset/Clear Field Box Button
clear_btn = tk.Button(
    root, 
    text="Clear Fields", 
    command=clear_entry_fields, # Maps to interface cleaner function
    bg="#f44336", 
    fg="black", 
    font=("Arial", 10),
    padx=5
)
clear_btn.pack()

# Start application interaction engine tracking loops
root.mainloop()
