import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import os
import subprocess
from datetime import datetime

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Tanay@26",
    "database": "parkwatch"
}

# Function to connect to MySQL
def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {err}")
        return None

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("ParkWatch - Admin Dashboard")
        self.root.geometry("1200x700")
        self.root.configure(bg="#2C3E50")
        
        # Configure style for ttk widgets
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TNotebook", background="#2C3E50", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#34495E", foreground="white", padding=[10, 5])
        self.style.map("TNotebook.Tab", background=[("selected", "#2980B9")], foreground=[("selected", "white")])
        self.style.configure("Treeview", background="#ECF0F1", foreground="black", rowheight=25)
        self.style.configure("Treeview.Heading", background="#34495E", foreground="white", font=("Arial", 10, "bold"))
        
        # Main title
        self.title_frame = tk.Frame(root, bg="#2C3E50")
        self.title_frame.pack(fill="x", padx=20, pady=10)
        
        self.title_label = tk.Label(
            self.title_frame, 
            text="ParkWatch Admin Dashboard", 
            font=("Helvetica", 24, "bold"), 
            bg="#2C3E50", 
            fg="white"
        )
        self.title_label.pack(side="left")
        
        self.logout_button = tk.Button(
            self.title_frame, 
            text="Logout", 
            font=("Arial", 12, "bold"), 
            bg="#E74C3C", 
            fg="white",
            command=self.logout
        )
        self.logout_button.pack(side="right", padx=10)
        
        self.refresh_button = tk.Button(
            self.title_frame, 
            text="Refresh Data", 
            font=("Arial", 12, "bold"), 
            bg="#27AE60", 
            fg="white",
            command=self.refresh_data
        )
        self.refresh_button.pack(side="right", padx=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create tabs
        self.shopping_mall_tab = tk.Frame(self.notebook, bg="#ECF0F1")
        self.college_tab = tk.Frame(self.notebook, bg="#ECF0F1")
        self.users_tab = tk.Frame(self.notebook, bg="#ECF0F1")
        
        self.notebook.add(self.shopping_mall_tab, text="Shopping Mall Bookings")
        self.notebook.add(self.college_tab, text="College Bookings")
        self.notebook.add(self.users_tab, text="Registered Users")
        
        # Create treeviews for each tab
        self.create_shopping_mall_view()
        self.create_college_view()
        self.create_users_view()
        
        # Load initial data
        self.refresh_data()
        
    def create_shopping_mall_view(self):
        # Frame for filters
        filter_frame = tk.Frame(self.shopping_mall_tab, bg="#ECF0F1")
        filter_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(filter_frame, text="Filter by date:", bg="#ECF0F1").pack(side="left", padx=5)
        
        # Today's date for default
        today = datetime.now().strftime("%Y-%m-%d")
        
        self.mall_date_var = tk.StringVar(value=today)
        self.mall_date_entry = tk.Entry(filter_frame, textvariable=self.mall_date_var, width=12)
        self.mall_date_entry.pack(side="left", padx=5)
        
        filter_button = tk.Button(
            filter_frame, 
            text="Apply Filter", 
            bg="#3498DB", 
            fg="white",
            command=lambda: self.load_mall_bookings(self.mall_date_var.get())
        )
        filter_button.pack(side="left", padx=5)
        
        clear_button = tk.Button(
            filter_frame, 
            text="Clear Filter", 
            bg="#7F8C8D", 
            fg="white",
            command=lambda: [self.mall_date_var.set(""), self.load_mall_bookings("")]
        )
        clear_button.pack(side="left", padx=5)
        
        # Scrollbar and Treeview
        tree_frame = tk.Frame(self.shopping_mall_tab)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        scroll_y = tk.Scrollbar(tree_frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        
        scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")
        
        self.mall_tree = ttk.Treeview(
            tree_frame,
            columns=("id", "space", "entry_time", "exit_time", "duration", "amount", "transaction_id", "vehicle"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        
        # Configure scrollbars
        scroll_y.config(command=self.mall_tree.yview)
        scroll_x.config(command=self.mall_tree.xview)
        
        # Configure columns
        self.mall_tree.heading("id", text="ID")
        self.mall_tree.heading("space", text="Space")
        self.mall_tree.heading("entry_time", text="Entry Time")
        self.mall_tree.heading("exit_time", text="Exit Time")
        self.mall_tree.heading("duration", text="Hours")
        self.mall_tree.heading("amount", text="Amount (₹)")
        self.mall_tree.heading("transaction_id", text="Transaction ID")
        self.mall_tree.heading("vehicle", text="Vehicle Number")
        
        # Column widths
        self.mall_tree.column("id", width=50)
        self.mall_tree.column("space", width=70)
        self.mall_tree.column("entry_time", width=150)
        self.mall_tree.column("exit_time", width=150)
        self.mall_tree.column("duration", width=70)
        self.mall_tree.column("amount", width=100)
        self.mall_tree.column("transaction_id", width=120)
        self.mall_tree.column("vehicle", width=120)
        
        self.mall_tree.pack(fill="both", expand=True)
        
    def create_college_view(self):
        # Frame for filters
        filter_frame = tk.Frame(self.college_tab, bg="#ECF0F1")
        filter_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(filter_frame, text="Filter by date:", bg="#ECF0F1").pack(side="left", padx=5)
        
        # Today's date for default
        today = datetime.now().strftime("%Y-%m-%d")
        
        self.college_date_var = tk.StringVar(value=today)
        self.college_date_entry = tk.Entry(filter_frame, textvariable=self.college_date_var, width=12)
        self.college_date_entry.pack(side="left", padx=5)
        
        filter_button = tk.Button(
            filter_frame, 
            text="Apply Filter", 
            bg="#3498DB", 
            fg="white",
            command=lambda: self.load_college_bookings(self.college_date_var.get())
        )
        filter_button.pack(side="left", padx=5)
        
        clear_button = tk.Button(
            filter_frame, 
            text="Clear Filter", 
            bg="#7F8C8D", 
            fg="white",
            command=lambda: [self.college_date_var.set(""), self.load_college_bookings("")]
        )
        clear_button.pack(side="left", padx=5)
        
        # Scrollbar and Treeview
        tree_frame = tk.Frame(self.college_tab)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        scroll_y = tk.Scrollbar(tree_frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        
        scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")
        
        self.college_tree = ttk.Treeview(
            tree_frame,
            columns=("id", "space", "entry_time", "exit_time", "duration", "amount", "transaction_id", "vehicle"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        
        # Configure scrollbars
        scroll_y.config(command=self.college_tree.yview)
        scroll_x.config(command=self.college_tree.xview)
        
        # Configure columns
        self.college_tree.heading("id", text="ID")
        self.college_tree.heading("space", text="Space")
        self.college_tree.heading("entry_time", text="Entry Time")
        self.college_tree.heading("exit_time", text="Exit Time")
        self.college_tree.heading("duration", text="Hours")
        self.college_tree.heading("amount", text="Amount (₹)")
        self.college_tree.heading("transaction_id", text="Transaction ID")
        self.college_tree.heading("vehicle", text="Vehicle Number")
        
        # Column widths
        self.college_tree.column("id", width=50)
        self.college_tree.column("space", width=70)
        self.college_tree.column("entry_time", width=150)
        self.college_tree.column("exit_time", width=150)
        self.college_tree.column("duration", width=70)
        self.college_tree.column("amount", width=100)
        self.college_tree.column("transaction_id", width=120)
        self.college_tree.column("vehicle", width=120)
        
        self.college_tree.pack(fill="both", expand=True)
    
    def create_users_view(self):
        # Scrollbar and Treeview
        tree_frame = tk.Frame(self.users_tab)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        scroll_y = tk.Scrollbar(tree_frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        
        scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")
        
        self.users_tree = ttk.Treeview(
            tree_frame,
            columns=("id", "username", "name", "phone", "email", "dl", "vehicle"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        
        # Configure scrollbars
        scroll_y.config(command=self.users_tree.yview)
        scroll_x.config(command=self.users_tree.xview)
        
        # Configure columns
        self.users_tree.heading("id", text="ID")
        self.users_tree.heading("username", text="Username")
        self.users_tree.heading("name", text="Full Name")
        self.users_tree.heading("phone", text="Phone")
        self.users_tree.heading("email", text="Email")
        self.users_tree.heading("dl", text="Driving License")
        self.users_tree.heading("vehicle", text="Vehicle Number")
        
        # Column widths
        self.users_tree.column("id", width=50)
        self.users_tree.column("username", width=100)
        self.users_tree.column("name", width=150)
        self.users_tree.column("phone", width=100)
        self.users_tree.column("email", width=200)
        self.users_tree.column("dl", width=150)
        self.users_tree.column("vehicle", width=120)
        
        self.users_tree.pack(fill="both", expand=True)
    
    def load_mall_bookings(self, date_filter=""):
        conn = connect_db()
        if not conn:
            return
        
        # Clear existing data
        for item in self.mall_tree.get_children():
            self.mall_tree.delete(item)
        
        try:
            cursor = conn.cursor()
            
            if date_filter:
                query = """
                SELECT id, space_number, entry_time, exit_time, duration, amount, 
                       transaction_id, vehicle_number
                FROM shopping_mall
                WHERE DATE(entry_time) = %s
                ORDER BY entry_time DESC
                """
                cursor.execute(query, (date_filter,))
            else:
                query = """
                SELECT id, space_number, entry_time, exit_time, duration, amount, 
                       transaction_id, vehicle_number
                FROM shopping_mall
                ORDER BY entry_time DESC
                """
                cursor.execute(query)
            
            rows = cursor.fetchall()
            
            for row in rows:
                self.mall_tree.insert("", "end", values=row)
            
            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching mall bookings: {err}")
        finally:
            conn.close()
    
    def load_college_bookings(self, date_filter=""):
        conn = connect_db()
        if not conn:
            return
        
        # Clear existing data
        for item in self.college_tree.get_children():
            self.college_tree.delete(item)
        
        try:
            cursor = conn.cursor()
            
            if date_filter:
                query = """
                SELECT id, space_number, entry_time, exit_time, duration, amount, 
                       transaction_id, vehicle_number
                FROM college_parking
                WHERE DATE(entry_time) = %s
                ORDER BY entry_time DESC
                """
                cursor.execute(query, (date_filter,))
            else:
                query = """
                SELECT id, space_number, entry_time, exit_time, duration, amount, 
                       transaction_id, vehicle_number
                FROM college_parking
                ORDER BY entry_time DESC
                """
                cursor.execute(query)
            
            rows = cursor.fetchall()
            
            for row in rows:
                self.college_tree.insert("", "end", values=row)
            
            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching college bookings: {err}")
        finally:
            conn.close()
    
    def load_users(self):
        conn = connect_db()
        if not conn:
            return
        
        # Clear existing data
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        try:
            cursor = conn.cursor()
            
            query = """
            SELECT id, username, name, phone, email, driving_license, vehicle_number
            FROM users
            ORDER BY id
            """
            cursor.execute(query)
            
            rows = cursor.fetchall()
            
            for row in rows:
                self.users_tree.insert("", "end", values=row)
            
            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching users: {err}")
        finally:
            conn.close()
    
    def refresh_data(self):
        """Refresh all data in the dashboard"""
        self.load_mall_bookings(self.mall_date_var.get())
        self.load_college_bookings(self.college_date_var.get())
        self.load_users()
    
    def logout(self):
        """Logout and return to login screen"""
        self.root.destroy()
        
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            login_path = os.path.join(current_dir, "login&signup.py")
            
            if os.path.exists(login_path):
                subprocess.Popen(["python", login_path])
        except Exception as e:
            print(f"Error launching login screen: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()