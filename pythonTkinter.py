import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk  
from datetime import datetime

# ==========================================
# 1. DATABASE SETUP LOGIC
# ==========================================
def initialize_database():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root123456"
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS student_db;")
        cursor.execute("USE student_db;")
        
        # Active Records Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books_issued (
                book_id INT PRIMARY KEY,
                student_id VARCHAR(50) NOT NULL,
                student_name VARCHAR(100) NOT NULL,
                date_of_issue DATE NOT NULL,
                book_name VARCHAR(150) NOT NULL,
                fine INT DEFAULT 0
            );
        """)

        # Permanent Historical Archive Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS archived_books (
                archive_id INT AUTO_INCREMENT PRIMARY KEY,
                book_id INT NOT NULL,
                student_id VARCHAR(50) NOT NULL,
                student_name VARCHAR(100) NOT NULL,
                date_of_issue DATE NOT NULL,
                book_name VARCHAR(150) NOT NULL,
                date_of_return TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        try:
            cursor.execute("ALTER TABLE books_issued ADD COLUMN fine INT DEFAULT 0;")
        except Error:
            pass # Column already exists
            
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Database initialization error: {e}")

# Run setup immediately when script boots up
initialize_database()


# ==========================================
# 2. WINDOW OPENING FUNCTIONS
# ==========================================

def open_register_window():
    reg_window = tk.Toplevel(root)
    reg_window.title("Register Student Book Issue")
    reg_window.geometry("600x550")
    reg_window.configure(bg="#1c1c1c")
    
    tk.Label(reg_window, text="Book Registration Form", font=("Segoe UI", 24, "bold"), bg="#1c1c1c", fg="#FFFCC6").pack(pady=25)

    form_frame = tk.Frame(reg_window, bg="#1c1c1c")
    form_frame.pack(padx=50, fill="x")

    lbl_opts = {"font": ("Segoe UI", 13), "bg": "#1c1c1c", "fg": "#E1E1E1", "anchor": "w"}
    ent_opts = {"font": ("Segoe UI", 13), "width": 30, "bg": "#2d2d2d", "fg": "white", "insertbackground": "white", "relief": "flat"}

    tk.Label(form_frame, text="Book ID :", **lbl_opts).grid(row=0, column=0, sticky="w", pady=8)
    book_id_entry = tk.Entry(form_frame, **ent_opts)
    book_id_entry.grid(row=0, column=1, pady=8, padx=10)

    tk.Label(form_frame, text="Book Name:", **lbl_opts).grid(row=1, column=0, sticky="w", pady=8)
    book_name_entry = tk.Entry(form_frame, **ent_opts)
    book_name_entry.grid(row=1, column=1, pady=8, padx=10)

    tk.Label(form_frame, text="Student ID:", **lbl_opts).grid(row=2, column=0, sticky="w", pady=8)
    student_id_entry = tk.Entry(form_frame, **ent_opts)
    student_id_entry.grid(row=2, column=1, pady=8, padx=10)

    tk.Label(form_frame, text="Student Name:", **lbl_opts).grid(row=3, column=0, sticky="w", pady=8)
    student_name_entry = tk.Entry(form_frame, **ent_opts)
    student_name_entry.grid(row=3, column=1, pady=8, padx=10)

    tk.Label(form_frame, text="Date (YYYY-MM-DD):", **lbl_opts).grid(row=4, column=0, sticky="w", pady=8)
    date_entry = tk.Entry(form_frame, **ent_opts)
    date_entry.grid(row=4, column=1, pady=8, padx=10)
    
    date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

    def submit_action():
        b_id = book_id_entry.get().strip()
        s_id = student_id_entry.get().strip()
        s_name = student_name_entry.get().strip()
        b_name = book_name_entry.get().strip()
        d_issue = date_entry.get().strip()
        
        if not b_id or not s_id or not s_name or not d_issue or not b_name:
            messagebox.showwarning("Missing Information", "Please fill out all fields before submitting!")
            return
        
        if not b_id.isdigit():
            messagebox.showerror("Input Error", "Book ID must be a valid integer number!")
            return
            
        try:
            datetime.strptime(d_issue, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Format Error", "Date must strictly use the YYYY-MM-DD format!")
            return

        try:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="root123456", database="student_db")
            cursor = conn.cursor()
            query = "INSERT INTO books_issued (book_id, student_id, student_name, date_of_issue, book_name, fine) VALUES (%s, %s, %s, %s, %s, 0);"
            cursor.execute(query, (int(b_id), s_id, s_name, d_issue, b_name))
            conn.commit()
            
            messagebox.showinfo("Success", f"Successfully registered record for {s_name}!")
            clear_action()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to save record: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def clear_action():
        book_id_entry.delete(0, tk.END)
        student_id_entry.delete(0, tk.END)
        student_name_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        book_name_entry.delete(0, tk.END)
        date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

    btn_frame = tk.Frame(reg_window, bg="#1c1c1c")
    btn_frame.pack(pady=40)

    submit_btn = tk.Button(btn_frame, text="Submit Data", font=("Segoe UI", 13, "bold"), bg="#4CAF50", fg="black", activeforeground="#0022FF", width=15, relief="flat", command=submit_action)
    submit_btn.pack(side="left", padx=15)

    clear_btn = tk.Button(btn_frame, text="Clear Fields", font=("Segoe UI", 13, "bold"), bg="#f44336", fg="black", activeforeground="#0929F9", width=15, relief="flat", command=clear_action)
    clear_btn.pack(side="left", padx=15)


def open_search_window():
    search_window = tk.Toplevel(root)
    search_window.title("Search Library Database")
    search_window.geometry("650x450")
    search_window.configure(bg="#1c1c1c")
    
    books_dict = {
        101: "Lord of the rings",
        102: "The great gatsby",
        103: "To Kill a Mockingbird",
        104: "1984",
        105: "Pride and Prejudice",
        106: "The Catcher in the Rye",
        107: "The Hobbit",
        108: "Fahrenheit 451"
    }
    
    tk.Label(search_window, text="Search Book Inventory", font=("Segoe UI", 22, "bold"), bg="#1c1c1c", fg="#FFFCC6").pack(pady=20)
    
    search_frame = tk.Frame(search_window, bg="#1c1c1c")
    search_frame.pack(pady=10)
    
    tk.Label(search_frame, text="Enter Book Name:", font=("Segoe UI", 12), bg="#1c1c1c", fg="#E1E1E1").grid(row=0, column=0, padx=10, sticky="w")
    search_entry = tk.Entry(search_frame, font=("Segoe UI", 12), width=25, bg="#2d2d2d", fg="white", insertbackground="white", relief="flat")
    search_entry.grid(row=0, column=1, padx=10)
    
    result_frame = tk.LabelFrame(search_window, text=" Search Results ", font=("Segoe UI", 11, "bold"), bg="#1c1c1c", fg="#FFFCC6", bd=2, relief="groove")
    result_frame.pack(pady=30, padx=40, fill="both", expand=True)
    
    lbl_res_opts = {"font": ("Segoe UI", 13), "bg": "#1c1c1c", "anchor": "w"}
    
    id_result_lbl = tk.Label(result_frame, text="Book ID: --", fg="white", **lbl_res_opts)
    id_result_lbl.pack(fill="x", padx=20, pady=5)
    
    name_result_lbl = tk.Label(result_frame, text="Book Name: --", fg="white", **lbl_res_opts)
    name_result_lbl.pack(fill="x", padx=20, pady=5)
    
    status_result_lbl = tk.Label(result_frame, text="Availability Status: --", fg="white", **lbl_res_opts)
    status_result_lbl.pack(fill="x", padx=20, pady=5)

    def perform_search():
        query_name = search_entry.get().strip().lower()
        
        if not query_name:
            messagebox.showwarning("Search Warning", "Please enter a book name to search!")
            return
        
        found_id = None
        found_name = None
        
        for b_id, b_name in books_dict.items():
            if b_name.lower() == query_name:
                found_id = b_id
                found_name = b_name
                break
        
        if found_id is None:
            id_result_lbl.config(text="Book ID: Not Found", fg="#f44336")
            name_result_lbl.config(text=f"Book Name: '{search_entry.get()}' missing from catalog", fg="#f44336")
            status_result_lbl.config(text="Availability Status: Unknown", fg="#f44336")
            return
        
        is_issued = False
        try:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="root123456", database="student_db")
            cursor = conn.cursor()
            cursor.execute("SELECT book_id FROM books_issued WHERE book_id = %s;", (found_id,))
            record = cursor.fetchone()
            
            if record:
                is_issued = True
                
        except Error as e:
            print(f"Database read error during check: {e}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
                
        id_result_lbl.config(text=f"Book ID: {found_id}", fg="white")
        name_result_lbl.config(text=f"Book Name: {found_name}", fg="white")
        
        if is_issued:
            status_result_lbl.config(text="Availability Status: NOT AVAILABLE (Already Registered/Issued)", fg="#ff6b6b")
        else:
            status_result_lbl.config(text="Availability Status: AVAILABLE", fg="#4caf50")

    search_btn = tk.Button(search_frame, text="Search", font=("Segoe UI", 11, "bold"), bg="#FFFCC6", fg="black", command=perform_search, relief="flat", width=10)
    search_btn.grid(row=0, column=2, padx=10)


def open_tables_window():
    tables_window = tk.Toplevel(root)
    tables_window.title("Database Tables")
    tables_window.geometry("1000x550") 
    tables_window.configure(bg="#1c1c1c")
    
    tk.Label(tables_window, text="Issued Books Table Records", font=("Segoe UI", 20, "bold"), bg="#1c1c1c", fg="#FFFCC6").pack(pady=15)

    columns = ("book_id", "student_id", "student_name", "date_of_issue", "book_name", "fine")
    tree = ttk.Treeview(tables_window, columns=columns, show="headings", height=12)
    
    tree.heading("book_id", text="Book ID")
    tree.heading("student_id", text="Student ID")
    tree.heading("student_name", text="Student Name")
    tree.heading("date_of_issue", text="Date of Issue")
    tree.heading("book_name", text="Book Name")
    tree.heading("fine", text="Accumulated Fine")
    
    tree.column("book_id", width=80, anchor="center")
    tree.column("student_id", width=100, anchor="center")
    tree.column("student_name", width=150, anchor="w")
    tree.column("date_of_issue", width=120, anchor="center")
    tree.column("book_name", width=180, anchor="w")
    tree.column("fine", width=160, anchor="center")
    
    scrollbar = ttk.Scrollbar(tables_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="top", fill="both", expand=True, padx=20, pady=10)
    scrollbar.pack(side="right", fill="y")

    def load_table_records():
        for item in tree.get_children():
            tree.delete(item)
            
        try:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="root123456", database="student_db")
            cursor = conn.cursor()
            cursor.execute("SELECT book_id, student_id, student_name, date_of_issue, book_name, fine FROM books_issued;")
            rows = cursor.fetchall()
            
            for row in rows:
                b_id, s_id, s_name, issue_date, b_name, stored_fine = row
                
                if isinstance(issue_date, str):
                    issue_date_obj = datetime.strptime(issue_date, "%Y-%m-%d").date()
                else:
                    issue_date_obj = issue_date

                fine_str = f"₹{stored_fine}"
                
                tree.insert("", tk.END, values=(b_id, s_id, s_name, issue_date_obj.strftime('%Y-%m-%d'), b_name, fine_str))
        except Error as e:
            messagebox.showerror("Fetch Error", f"Could not retrieve database rows: {e}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def clear_selected_record():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Warning", "Please click on a record row from the table list first to clear it!")
            return
            
        record_values = tree.item(selected_item)['values']
        target_book_id = record_values[0]
        student_id_target = record_values[1]
        student_target = record_values[2] 
        date_issued_target = record_values[3]
        book_name_target = record_values[4]
        
        confirm = messagebox.askyesno("Confirm Return", f"Are you sure you want to mark Book ID {target_book_id} as returned by {student_target}?\nThis moves the record to permanent history logs.")
        if not confirm:
            return

        try:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="root123456", database="student_db")
            cursor = conn.cursor()
            
            archive_query = """
                INSERT INTO archived_books (book_id, student_id, student_name, date_of_issue, book_name)
                VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(archive_query, (int(target_book_id), student_id_target, student_target, date_issued_target, book_name_target))
            
            cursor.execute("DELETE FROM books_issued WHERE book_id = %s;", (int(target_book_id),))
            conn.commit()
            
            messagebox.showinfo("Returned Successfully", "Record archived safely! Book available in active inventory once again.")
            load_table_records()  
        except Error as e:
            messagebox.showerror("Database Execution Error", f"Could not finalize automated history migration tracking details: {e}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    btn_control_frame = tk.Frame(tables_window, bg="#1c1c1c")
    btn_control_frame.pack(pady=15)
    
    return_btn = tk.Button(btn_control_frame, text="Mark Selected as Returned / Clear Record", font=("Segoe UI", 12, "bold"), bg="#4CAF50", fg="black", relief="flat", padx=15, pady=5, command=clear_selected_record)
    return_btn.pack()

    load_table_records()


def open_update_window():
    update_window = tk.Toplevel(root)
    update_window.title("Update Library Records")
    update_window.geometry("600x620") 
    update_window.configure(bg="#1c1c1c")
    
    tk.Label(update_window, text="Modify Record Fields", font=("Segoe UI", 24, "bold"), bg="#1c1c1c", fg="#FFFCC6").pack(pady=20)
    
    fetch_frame = tk.LabelFrame(update_window, text=" Find Record by Book ID ", font=("Segoe UI", 11, "bold"), bg="#1c1c1c", fg="#FFFCC6", bd=2, relief="groove")
    fetch_frame.pack(padx=40, fill="x", pady=10)
    
    tk.Label(fetch_frame, text="Enter Book ID to Modify:", font=("Segoe UI", 12), bg="#1c1c1c", fg="#E1E1E1").grid(row=0, column=0, padx=10, pady=15, sticky="w")
    search_id_entry = tk.Entry(fetch_frame, font=("Segoe UI", 12), width=15, bg="#2d2d2d", fg="white", insertbackground="white", relief="flat")
    search_id_entry.grid(row=0, column=1, padx=10, pady=15)
    
    fields_frame = tk.Frame(update_window, bg="#1c1c1c")
    fields_frame.pack(padx=50, fill="x", pady=15)
    
    lbl_opts = {"font": ("Segoe UI", 13), "bg": "#1c1c1c", "fg": "#E1E1E1", "anchor": "w"}
    ent_opts = {"font": ("Segoe UI", 13), "width": 30, "bg": "#2d2d2d", "fg": "white", "insertbackground": "white", "relief": "flat"}
    
    tk.Label(fields_frame, text="Book Name:", **lbl_opts).grid(row=0, column=0, sticky="w", pady=8)
    up_book_name = tk.Entry(fields_frame, **ent_opts)
    up_book_name.grid(row=0, column=1, pady=8, padx=10)
    
    tk.Label(fields_frame, text="Student ID:", **lbl_opts).grid(row=1, column=0, sticky="w", pady=8)
    up_student_id = tk.Entry(fields_frame, **ent_opts)
    up_student_id.grid(row=1, column=1, pady=8, padx=10)
    
    tk.Label(fields_frame, text="Student Name:", **lbl_opts).grid(row=2, column=0, sticky="w", pady=8)
    up_student_name = tk.Entry(fields_frame, **ent_opts)
    up_student_name.grid(row=2, column=1, pady=8, padx=10)
    
    tk.Label(fields_frame, text="Date (YYYY-MM-DD):", **lbl_opts).grid(row=3, column=0, sticky="w", pady=8)
    up_date_issue = tk.Entry(fields_frame, **ent_opts)
    up_date_issue.grid(row=3, column=1, pady=8, padx=10)

    tk.Label(fields_frame, text="Accumulated Fine (₹):", **lbl_opts).grid(row=4, column=0, sticky="w", pady=8)
    up_fine = tk.Entry(fields_frame, **ent_opts)
    up_fine.grid(row=4, column=1, pady=8, padx=10)

    def fetch_target_record():
        b_id = search_id_entry.get().strip()
        if not b_id or not b_id.isdigit():
            messagebox.showwarning("Input Missing", "Please enter a valid numeric Book ID!")
            return
            
        try:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="root123456", database="student_db")
            cursor = conn.cursor()
            cursor.execute("SELECT book_name, student_id, student_name, date_of_issue, fine FROM books_issued WHERE book_id = %s;", (int(b_id),))
            record = cursor.fetchone()
            
            if not record:
                messagebox.showerror("Not Found", f"No active issue records discovered matching Book ID: {b_id}")
                return
                
            up_book_name.delete(0, tk.END)
            up_student_id.delete(0, tk.END)
            up_student_name.delete(0, tk.END)
            up_date_issue.delete(0, tk.END)
            up_fine.delete(0, tk.END)
            
            up_book_name.insert(0, record[0])
            up_student_id.insert(0, record[1])
            up_student_name.insert(0, record[2])
            
            date_val = record[3].strftime('%Y-%m-%d') if isinstance(record[3], datetime) or hasattr(record[3], 'strftime') else str(record[3])
            up_date_issue.insert(0, date_val)
            up_fine.insert(0, str(record[4]))
            
            messagebox.showinfo("Loaded", "Record fetched successfully! You can now make changes.")
            
        except Error as e:
            messagebox.showerror("Error", f"Could not read row: {e}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def commit_updates():
        b_id = search_id_entry.get().strip()
        b_name = up_book_name.get().strip()
        s_id = up_student_id.get().strip()
        s_name = up_student_name.get().strip()
        d_issue = up_date_issue.get().strip()
        f_amt = up_fine.get().strip()
        
        if not b_id or not b_name or not s_id or not s_name or not d_issue or f_amt == "":
            messagebox.showwarning("Validation Error", "All fields must be completely filled out before saving updates!")
            return
            
        if not f_amt.isdigit():
            messagebox.showerror("Input Error", "Fine layout value structure must be a valid whole number integer string!")
            return

        try:
            datetime.strptime(d_issue, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Format Error", "Date must strictly use the YYYY-MM-DD format structure!")
            return
            
        try:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="root123456", database="student_db")
            cursor = conn.cursor()
            query = """
                UPDATE books_issued 
                SET book_name = %s, student_id = %s, student_name = %s, date_of_issue = %s, fine = %s 
                WHERE book_id = %s;
            """
            cursor.execute(query, (b_name, s_id, s_name, d_issue, int(f_amt), int(b_id)))
            conn.commit()
            
            messagebox.showinfo("Success", "Library schema modifications saved successfully!")
            update_window.destroy() 
        except Error as e:
            messagebox.showerror("Database Execution Error", f"Could not update fields: {e}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    fetch_btn = tk.Button(fetch_frame, text="Find/Load", font=("Segoe UI", 10, "bold"), bg="#FFFCC6", fg="black", command=fetch_target_record, relief="flat", width=10)
    fetch_btn.grid(row=0, column=2, padx=15, pady=15)
    
    save_btn = tk.Button(update_window, text="Save Updates", font=("Segoe UI", 13, "bold"), bg="#4CAF50", fg="black", relief="flat", width=18, command=commit_updates)
    save_btn.pack(pady=10)


def open_archive_history_view():
    arch_win = tk.Toplevel(root)
    arch_win.title("Permanent History Returns Log Archive")
    arch_win.geometry("950x500")
    arch_win.configure(bg="#111111")
    
    tk.Label(arch_win, text="📚 Permanent Historical Book Logs Archive", font=("Segoe UI", 18, "bold"), bg="#111111", fg="#007AFF").pack(pady=15)
    
    columns = ("arc_id", "b_id", "s_id", "s_name", "iss_date", "b_name", "ret_date")
    a_tree = ttk.Treeview(arch_win, columns=columns, show="headings", height=14)
    
    a_tree.heading("arc_id", text="Log ID")
    a_tree.heading("b_id", text="Book ID")
    a_tree.heading("s_id", text="Student ID")
    a_tree.heading("s_name", text="Student Name")
    a_tree.heading("iss_date", text="Issue Date")
    a_tree.heading("b_name", text="Book Name")
    a_tree.heading("ret_date", text="Returned Timestamp")
    
    a_tree.column("arc_id", width=60, anchor="center")
    a_tree.column("b_id", width=70, anchor="center")
    a_tree.column("s_id", width=90, anchor="center")
    a_tree.column("s_name", width=140, anchor="w")
    a_tree.column("iss_date", width=110, anchor="center")
    a_tree.column("b_name", width=160, anchor="w")
    a_tree.column("ret_date", width=180, anchor="center")
    
    scroll = ttk.Scrollbar(arch_win, orient="vertical", command=a_tree.yview)
    a_tree.configure(yscrollcommand=scroll.set)
    
    a_tree.pack(side="left", fill="both", expand=True, padx=(20,0), pady=15)
    scroll.pack(side="right", fill="y", padx=(0,20), pady=15)
    
    try:
        conn = mysql.connector.connect(host="127.0.0.1", user="root", password="root123456", database="student_db")
        cursor = conn.cursor()
        cursor.execute("SELECT archive_id, book_id, student_id, student_name, date_of_issue, book_name, date_of_return FROM archived_books ORDER BY date_of_return DESC;")
        records = cursor.fetchall()
        
        for item in records:
            iss_str = item[4].strftime('%Y-%m-%d') if hasattr(item[4], 'strftime') else str(item[4])
            ret_str = item[6].strftime('%Y-%m-%d %H:%M:%S') if hasattr(item[6], 'strftime') else str(item[6])
            a_tree.insert("", tk.END, values=(item[0], item[1], item[2], item[3], iss_str, item[5], ret_str))
    except Error as e:
        messagebox.showerror("Error Loading Archive", f"Could not sync with structural storage history rows: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


# ==========================================
# 3. SECURE AUTHENTICATION SYSTEM
# ==========================================
def open_login_screen():
    login_win = tk.Toplevel(root)
    login_win.title("Secure Gatekeeper System")
    login_win.geometry("400x320")
    login_win.configure(bg="#121212")
    
    def on_login_close():
        root.destroy()
    login_win.protocol("WM_DELETE_WINDOW", on_login_close)

    tk.Label(login_win, text="SECURITY ACCESS", font=("Segoe UI", 18, "bold"), bg="#121212", fg="#FFFCC6").pack(pady=(25, 15))

    lbl_opts = {"font": ("Segoe UI", 11), "bg": "#121212", "fg": "#E1E1E1"}
    ent_opts = {"font": ("Segoe UI", 11), "bg": "#2d2d2d", "fg": "white", "insertbackground": "white", "relief": "flat"}

    tk.Label(login_win, text="Administrator Identity ID:", **lbl_opts).pack(pady=(10, 2))
    username_entry = tk.Entry(login_win, width=28, **ent_opts)
    username_entry.pack(pady=2)
    username_entry.focus()

    tk.Label(login_win, text="System Verification Token:", **lbl_opts).pack(pady=(10, 2))
    
    password_frame = tk.Frame(login_win, bg="#121212")
    password_frame.pack(pady=2)

    password_entry = tk.Entry(password_frame, show="*", width=20, **ent_opts)
    password_entry.pack(side=tk.LEFT)

    def toggle_password():
        if password_entry.cget("show") == "*":
            password_entry.config(show="")
            toggle_btn.config(text="Hide", bg="#494949")
        else:
            password_entry.config(show="*")
            toggle_btn.config(text="Show", bg="#333333")

    toggle_btn = tk.Button(password_frame, text="Show", font=("Segoe UI", 9, "bold"), command=toggle_password, width=6, bg="black", fg="black", relief="flat")
    toggle_btn.pack(side=tk.LEFT, padx=(6, 0))

    def check_login():
        username = username_entry.get().strip()
        password = password_entry.get()
        
        if username == "admin" and password == "secret123":
            messagebox.showinfo("Success", "Authorisation Token verified successfully!")
            login_win.destroy()
            root.deiconify() 
        else:
            messagebox.showerror("Access Denied", "Invalid administrative identity mapping arrays.")

    login_win.bind('<Return>', lambda event: check_login())

    login_button = tk.Button(login_win, text="Authenticate System", font=("Segoe UI", 12, "bold"), command=check_login, bg="black", fg="black", relief="flat", width=20)
    login_button.pack(pady=30)


# ==========================================
# 4. TKINTER MAIN INTERFACE AND LAYOUT
# ==========================================

root = tk.Tk()
root.title("Library Unified Network Database")
root.geometry("1080x640")
root.configure(bg="#121212")

# Hide main loop layout safely immediately until login clears
root.withdraw()

title_label = tk.Label(root, text="HOME", font=("Segoe UI", 63, "bold"), bg="#121212", fg="#E1E1E1")
title_label.pack(pady=15)

style = ttk.Style()
style.theme_use('clam')

# Configures the default layout state
style.configure(
    "Custom.TButton",
    font=("Segoe UI", 31, "bold"), 
    background="#FFFCC6",
    foreground="black",
    borderwidth=0,
    cursor="hand2"
)

# Enforces permanent black font configuration state during hovering/clicking actions
style.map(
    "Custom.TButton",
    foreground=[('pressed', 'black'), ('active', 'black')],
    background=[('pressed', '#E6E3B3'), ('active', '#FFFCC6')]
)

# --- Sidebar Configuration Layout ---
archive_btn = tk.Button(
    root, 
    text="Archive", 
    font=("Segoe UI", 14, "bold"), 
    background="#59F604",
    relief="flat", 
    padx=20, 
    pady=10,
    command=open_archive_history_view
)
archive_btn.place(relx=0.96, rely=0.94, anchor="se")

# Reconfigured as highly-styled ttk Elements safely packed without layout crashing tags
regst = ttk.Button(root, text="Book Issue", style="Custom.TButton", width=15, command=open_register_window)
srch = ttk.Button(root, text="Search", style="Custom.TButton", width=15, command=open_search_window)
updt = ttk.Button(root, text="Update", style="Custom.TButton", width=15, command=open_update_window)
shtbl = ttk.Button(root, text="Record", style="Custom.TButton", width=15, command=open_tables_window)
exit_btn = ttk.Button(root, text="Exit", style="Custom.TButton", width=15, command=root.destroy)

regst.pack(side="top", anchor="w", padx=(100, 0), pady=(40, 45))
srch.pack(side="top", anchor="w", padx=(100, 0), pady=(0, 45))
updt.pack(side="top", anchor="w", padx=(100, 0), pady=(0, 45))
shtbl.pack(side="top", anchor="w", padx=(100, 0), pady=(0, 45))
exit_btn.pack(side="top", anchor="w", padx=(100, 0), pady=(0, 45))

vertical_line = tk.Frame(root, width=6, bg='#007AFF') 
vertical_line.place(relx=0.5, rely=0.2, relheight=0.9, anchor="n")

# --- IMAGE 1 ---
try:
    pil_img1 = Image.open("img1.png")
    pil_img1 = pil_img1.resize((120, 90), Image.Resampling.LANCZOS) 
    home_image = ImageTk.PhotoImage(pil_img1)

    image_label = tk.Label(root, image=home_image, bg="#121212")
    image_label.place(relx=0.71, rely=0.024, anchor="ne")
    image_label.image = home_image
except Exception as e:
    print(f"Error loading img1.png: {e}") 

# --- IMAGE 2 ---
try:
    pil_lib = Image.open("lib.png")
    pil_lib = pil_lib.resize((400, 300), Image.Resampling.LANCZOS)
    lib_image = ImageTk.PhotoImage(pil_lib)

    lib_image_label = tk.Label(root, image=lib_image, bg="#121212")
    lib_image_label.place(relx=0.75, rely=0.55, anchor="center")
    lib_image_label.image = lib_image
except Exception as e:
    print(f"Error loading lib.png: {e}") 

# Launch secure authorization gatekeeper module
open_login_screen()

root.mainloop()
