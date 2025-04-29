import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime

class RealEstateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real Estate Management System")
        self.root.geometry("1000x600")
        self.root.configure(bg='#f0f2f5')
        
        # Set theme colors
        self.primary_color = '#3498db'  # Blue
        self.secondary_color = '#2980b9' # Darker blue
        self.accent_color = '#e74c3c'    # Red
        self.light_color = '#ecf0f1'     # Light gray
        self.dark_color = '#2c3e50'      # Dark navy
        self.success_color = '#2ecc71'   # Green
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure button styles
        self.style.configure('TButton', 
                           font=('Arial', 10),
                           padding=6,
                           background=self.primary_color,
                           foreground='white')
        self.style.map('TButton',
                      background=[('active', self.secondary_color)],
                      foreground=[('active', 'white')])
        
        # Configure entry styles
        self.style.configure('TEntry', 
                           fieldbackground=self.light_color,
                           foreground=self.dark_color,
                           padding=5)
        
        # Configure combobox styles
        self.style.configure('TCombobox',
                           fieldbackground=self.light_color,
                           foreground=self.dark_color,
                           selectbackground=self.primary_color)
        
        # Configure treeview styles
        self.style.configure('Treeview',
                           background=self.light_color,
                           foreground=self.dark_color,
                           fieldbackground=self.light_color,
                           rowheight=25)
        self.style.configure('Treeview.Heading',
                            background=self.primary_color,
                            foreground='white',
                            font=('Arial', 10, 'bold'))
        self.style.map('Treeview',
                     background=[('selected', self.secondary_color)])
        
        # Database connection
        self.connection = self.connect_to_database()
        if self.connection:
            self.create_tables()
            self.show_login_page()
        else:
            messagebox.showerror("Error", "Could not connect to database. Application will exit.")
            self.root.destroy()
    
    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='123456',
                database='real_estate_db',
                auth_plugin='mysql_native_password'
            )
            return connection
        except Error as e:
            messagebox.showerror("Database Error", 
                f"Failed to connect to MySQL:\n\n{str(e)}\n\n"
                "Please ensure:\n"
                "1. MySQL server is running\n"
                "2. Database exists\n"
                "3. Credentials are correct")
            return None
    
    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            
            # Users table with proper syntax
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                user_type ENUM('admin', 'agent', 'client') NOT NULL,
                full_name VARCHAR(100)
            )""")
            
            # Properties table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS properties (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                address VARCHAR(200) NOT NULL,
                price DECIMAL(12,2) NOT NULL,
                bedrooms INT,
                bathrooms INT,
                size_sqft INT,
                type ENUM('House', 'Apartment', 'Condo', 'Land') NOT NULL,
                status ENUM('Available', 'Sold', 'Rented') DEFAULT 'Available',
                description TEXT,
                agent_id INT,
                FOREIGN KEY (agent_id) REFERENCES users(id)
            )""")
            
            # Payments table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                property_id INT,
                client_id INT,
                amount DECIMAL(12,2) NOT NULL,
                payment_date DATE NOT NULL,
                payment_method VARCHAR(50),
                FOREIGN KEY (property_id) REFERENCES properties(id),
                FOREIGN KEY (client_id) REFERENCES users(id)
            )""")
            
            # Viewings table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS viewings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                property_id INT,
                client_id INT,
                viewing_date DATETIME NOT NULL,
                status ENUM('Scheduled', 'Completed', 'Cancelled'),
                FOREIGN KEY (property_id) REFERENCES properties(id),
                FOREIGN KEY (client_id) REFERENCES users(id)
            )""")
            
            self.connection.commit()
            cursor.close()
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to create tables: {str(e)}")
            self.root.destroy()
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def show_login_page(self):
        self.clear_window()
        
        # Create header
        self.create_header("Real Estate Login")
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#f0f2f5')
        content_frame.pack(fill='both', expand=True, padx=50, pady=20)
        
        # Login form container
        form_frame = tk.Frame(content_frame, 
                             bg='white',
                             bd=2,
                             relief='groove',
                             padx=20,
                             pady=20)
        form_frame.pack(pady=20)
        
        # Form title
        tk.Label(form_frame, 
                text="Login to Your Account",
                font=('Arial', 14, 'bold'),
                bg='white').pack(pady=(0, 20))
        
        # Username field
        tk.Label(form_frame, 
                text="Username:",
                bg='white',
                font=('Arial', 10)).pack(anchor='w')
        self.login_username = ttk.Entry(form_frame, width=30)
        self.login_username.pack(pady=(0, 10))
        
        # Password field
        tk.Label(form_frame, 
                text="Password:",
                bg='white',
                font=('Arial', 10)).pack(anchor='w')
        self.login_password = ttk.Entry(form_frame, width=30, show="*")
        self.login_password.pack(pady=(0, 20))
        
        # Login button
        login_btn = ttk.Button(form_frame, 
                             text="Login", 
                             command=self.login)
        login_btn.pack(fill='x', pady=5)
        
        # Signup link
        signup_frame = tk.Frame(content_frame, bg='#f0f2f5')
        signup_frame.pack()
        
        tk.Label(signup_frame, 
               text="Don't have an account?",
               bg='#f0f2f5').pack(side='left')
        
        signup_btn = ttk.Button(signup_frame, 
                              text="Sign Up", 
                              command=self.show_signup_page,
                              style='TButton')
        signup_btn.pack(side='left', padx=5)
    
    def create_header(self, title):
        header = tk.Frame(self.root, bg=self.primary_color, height=80)
        header.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(header, 
                             text=title,
                             font=('Arial', 18, 'bold'),
                             bg=self.primary_color,
                             fg='white')
        title_label.pack(side='left', padx=20, pady=20)
        
        if hasattr(self, 'current_user'):
            user_label = tk.Label(header,
                                 text=f"Welcome, {self.get_user_name()}",
                                 font=('Arial', 12),
                                 bg=self.primary_color,
                                 fg='white')
            user_label.pack(side='right', padx=20)
    
    def show_signup_page(self):
        self.clear_window()
        
        # Create header
        self.create_header("Create New Account")
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#f0f2f5')
        content_frame.pack(fill='both', expand=True, padx=50, pady=20)
        
        # Signup form container
        form_frame = tk.Frame(content_frame, 
                             bg='white',
                             bd=2,
                             relief='groove',
                             padx=20,
                             pady=20)
        form_frame.pack(pady=20)
        
        # Form title
        tk.Label(form_frame, 
                text="Create Your Account",
                font=('Arial', 14, 'bold'),
                bg='white').pack(pady=(0, 20))
        
        # Full Name field
        tk.Label(form_frame, 
                text="Full Name:",
                bg='white',
                font=('Arial', 10)).pack(anchor='w')
        self.signup_name = ttk.Entry(form_frame, width=30)
        self.signup_name.pack(pady=(0, 10))
        
        # Email field
        tk.Label(form_frame, 
                text="Email:",
                bg='white',
                font=('Arial', 10)).pack(anchor='w')
        self.signup_email = ttk.Entry(form_frame, width=30)
        self.signup_email.pack(pady=(0, 10))
        
        # Username field
        tk.Label(form_frame, 
                text="Username:",
                bg='white',
                font=('Arial', 10)).pack(anchor='w')
        self.signup_username = ttk.Entry(form_frame, width=30)
        self.signup_username.pack(pady=(0, 10))
        
        # Password field
        tk.Label(form_frame, 
                text="Password:",
                bg='white',
                font=('Arial', 10)).pack(anchor='w')
        self.signup_password = ttk.Entry(form_frame, width=30, show="*")
        self.signup_password.pack(pady=(0, 10))
        
        # User Type field
        tk.Label(form_frame, 
                text="User Type:",
                bg='white',
                font=('Arial', 10)).pack(anchor='w')
        self.signup_type = ttk.Combobox(form_frame, 
                                      values=['client', 'agent'], 
                                      width=27)
        self.signup_type.pack(pady=(0, 20))
        
        # Submit button
        submit_btn = ttk.Button(form_frame, 
                              text="Create Account", 
                              command=self.signup)
        submit_btn.pack(fill='x', pady=5)
        
        # Back to login
        back_btn = ttk.Button(content_frame, 
                            text="Back to Login", 
                            command=self.show_login_page)
        back_btn.pack(pady=10)
        
        # Add Back to Home button if user is logged in
        if hasattr(self, 'current_user') and self.current_user:
            home_btn = ttk.Button(content_frame, 
                                text="Back to Home", 
                                command=self.show_home_page)
            home_btn.pack(pady=10)
    
    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password")
            return
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, password, user_type FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            
            if user and user[1] == self.hash_password(password):
                self.current_user = user[0]
                self.user_type = user[2]
                self.show_home_page()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Error as e:
            messagebox.showerror("Database Error", f"Login failed: {e}")
    
    def signup(self):
        name = self.signup_name.get()
        email = self.signup_email.get()
        username = self.signup_username.get()
        password = self.signup_password.get()
        user_type = self.signup_type.get()
        
        if not all([name, email, username, password, user_type]):
            messagebox.showwarning("Warning", "Please fill all fields")
            return
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, email, user_type, full_name) VALUES (%s, %s, %s, %s, %s)",
                (username, self.hash_password(password), email, user_type, name)
            )
            self.connection.commit()
            cursor.close()
            messagebox.showinfo("Success", "Account created successfully!")
            self.show_login_page()
        except Error as e:
            messagebox.showerror("Error", f"Failed to create account: {e}")
    
    def show_home_page(self):
        self.clear_window()
        
        # Create header
        self.create_header("Dashboard")
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#f0f2f5')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome_frame = tk.Frame(content_frame, bg='white', bd=2, relief='groove', padx=20, pady=20)
        welcome_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(welcome_frame, 
               text=f"Welcome back, {self.get_user_name()}!",
               font=('Arial', 14),
               bg='white').pack(anchor='w')
        
        tk.Label(welcome_frame, 
               text="What would you like to do today?",
               font=('Arial', 10),
               bg='white').pack(anchor='w')
        
        # Navigation buttons
        button_frame = tk.Frame(content_frame, bg='#f0f2f5')
        button_frame.pack(fill='both', expand=True)
        
        # Button configurations
        buttons = [
            ("View Properties", self.show_properties_page, "#3498db"),
            ("Make Payment", self.show_payment_page, "#2ecc71"),
            ("Schedule Viewing", self.show_viewings_page, "#e74c3c"),
            ("Admin Dashboard", self.show_admin_dashboard, "#9b59b6")
        ]
        
        # Only show admin dashboard button for admin users
        if self.user_type != 'admin':
            buttons = buttons[:-1]
        
        # Create buttons in a grid
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(button_frame,
                          text=text,
                          font=('Arial', 12),
                          bg=color,
                          fg='white',
                          activebackground=color,
                          activeforeground='white',
                          relief='flat',
                          bd=0,
                          padx=20,
                          pady=15,
                          command=command)
            
            btn.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='nsew')
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.darken_color(b['bg'])))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
        
        # Configure grid weights
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_rowconfigure(0, weight=1)
        if len(buttons) > 2:
            button_frame.grid_rowconfigure(1, weight=1)
        
        # Logout button
        logout_frame = tk.Frame(content_frame, bg='#f0f2f5')
        logout_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(logout_frame, 
                 text="Logout", 
                 command=self.logout).pack(side='right')
    
    def darken_color(self, color, amount=30):
        """Darken a hex color by the specified amount"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(max(0, x - amount) for x in rgb)
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
    
    def get_user_name(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT full_name FROM users WHERE id = %s", (self.current_user,))
        name = cursor.fetchone()[0]
        cursor.close()
        return name
    
    def show_properties_page(self):
        self.clear_window()
        
        # Create header
        self.create_header("Property Listings")
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#f0f2f5')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Search and filter frame
        search_frame = tk.Frame(content_frame, bg='white', padx=10, pady=10)
        search_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(search_frame, 
               text="Search:",
               bg='white').pack(side='left')
        
        search_entry = ttk.Entry(search_frame, width=40)
        search_entry.pack(side='left', padx=5)
        
        ttk.Button(search_frame, 
                 text="Search",
                 command=lambda: self.search_properties(search_entry.get())).pack(side='left', padx=5)
        
        # Property list treeview with scrollbars
        tree_frame = tk.Frame(content_frame, bg='#f0f2f5')
        tree_frame.pack(fill='both', expand=True)
        
        # Vertical scrollbar
        y_scroll = ttk.Scrollbar(tree_frame)
        y_scroll.pack(side='right', fill='y')
        
        # Horizontal scrollbar
        x_scroll = ttk.Scrollbar(tree_frame, orient='horizontal')
        x_scroll.pack(side='bottom', fill='x')
        
        # Create treeview
        self.property_tree = ttk.Treeview(tree_frame, 
                                        columns=("ID", "Title", "Address", "Price", "Type", "Status"),
                                        show='headings',
                                        yscrollcommand=y_scroll.set,
                                        xscrollcommand=x_scroll.set)
        
        # Configure columns
        self.property_tree.heading("ID", text="ID", anchor='center')
        self.property_tree.heading("Title", text="Title", anchor='center')
        self.property_tree.heading("Address", text="Address", anchor='center')
        self.property_tree.heading("Price", text="Price", anchor='center')
        self.property_tree.heading("Type", text="Type", anchor='center')
        self.property_tree.heading("Status", text="Status", anchor='center')
        
        self.property_tree.column("ID", width=50, anchor='center')
        self.property_tree.column("Title", width=150, anchor='w')
        self.property_tree.column("Address", width=250, anchor='w')
        self.property_tree.column("Price", width=100, anchor='e')
        self.property_tree.column("Type", width=100, anchor='center')
        self.property_tree.column("Status", width=100, anchor='center')
        
        self.property_tree.pack(fill='both', expand=True)
        
        # Configure scrollbars
        y_scroll.config(command=self.property_tree.yview)
        x_scroll.config(command=self.property_tree.xview)
        
        # Load properties
        self.load_properties()
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg='#f0f2f5')
        button_frame.pack(fill='x', pady=(10, 0))
        
        # View details button
        ttk.Button(button_frame, 
                  text="View Details", 
                  command=self.show_property_details).pack(side='left', padx=5)
        
        # Add property button for admin/agent
        if self.user_type in ['admin', 'agent']:
            ttk.Button(button_frame, 
                     text="Add New Property", 
                     command=self.show_add_property_page).pack(side='left', padx=5)
        
        # Back button
        ttk.Button(button_frame, 
                  text="Back to Home", 
                  command=self.show_home_page).pack(side='right')
    
    def search_properties(self, query):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, title, address, price, type, status 
            FROM properties 
            WHERE title LIKE %s OR address LIKE %s
            ORDER BY status, price
        """, (f"%{query}%", f"%{query}%"))
        
        # Clear existing data
        for row in self.property_tree.get_children():
            self.property_tree.delete(row)
        
        # Add new data
        for row in cursor:
            formatted_row = list(row)
            formatted_row[3] = f"${row[3]:,.2f}"
            self.property_tree.insert("", "end", values=formatted_row)
        
        cursor.close()
    
    def load_properties(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, title, address, price, type, status 
            FROM properties 
            ORDER BY status, price
        """)
        
        # Clear existing data
        for row in self.property_tree.get_children():
            self.property_tree.delete(row)
        
        # Add new data
        for row in cursor:
            # Format price with commas
            formatted_row = list(row)
            formatted_row[3] = f"${row[3]:,.2f}"
            self.property_tree.insert("", "end", values=formatted_row)
        
        cursor.close()
    
    def show_property_details(self):
        selected = self.property_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a property")
            return
        
        property_id = self.property_tree.item(selected)['values'][0]
        
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT p.*, u.full_name 
            FROM properties p
            LEFT JOIN users u ON p.agent_id = u.id
            WHERE p.id = %s
        """, (property_id,))
        property_data = cursor.fetchone()
        cursor.close()
        
        if not property_data:
            messagebox.showerror("Error", "Property not found")
            return
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title("Property Details")
        details_window.geometry("600x500")
        details_window.configure(bg='#f0f2f5')
        
        # Header frame
        header_frame = tk.Frame(details_window, bg=self.primary_color, height=60)
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, 
                text=property_data[1],
                font=('Arial', 16, 'bold'),
                bg=self.primary_color,
                fg='white').pack(pady=15)
        
        # Main content frame
        content_frame = tk.Frame(details_window, bg='white', padx=20, pady=20)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Details grid
        details_grid = tk.Frame(content_frame, bg='white')
        details_grid.pack(fill='x', pady=(0, 20))
        
        # Property details
        details = [
            ("Address:", property_data[2]),
            ("Price:", f"${property_data[3]:,.2f}"),
            ("Type:", property_data[7]),
            ("Status:", property_data[8]),
            ("Bedrooms:", property_data[4]),
            ("Bathrooms:", property_data[5]),
            ("Size:", f"{property_data[6]} sqft"),
            ("Agent:", property_data[11] if property_data[11] else "Not assigned")
        ]
        
        for i, (label, value) in enumerate(details):
            tk.Label(details_grid, 
                   text=label,
                   font=('Arial', 10, 'bold'),
                   bg='white').grid(row=i, column=0, sticky='e', padx=5, pady=2)
            
            tk.Label(details_grid, 
                   text=value,
                   bg='white').grid(row=i, column=1, sticky='w', padx=5, pady=2)
        
        # Description
        tk.Label(content_frame, 
               text="Description:",
               font=('Arial', 10, 'bold'),
               bg='white').pack(anchor='w')
        
        desc_frame = tk.Frame(content_frame, bg='white', bd=1, relief='sunken')
        desc_frame.pack(fill='both', expand=True)
        
        desc_text = tk.Text(desc_frame, 
                          height=5,
                          wrap='word',
                          padx=5,
                          pady=5,
                          font=('Arial', 10))
        desc_text.insert('1.0', property_data[9] if property_data[9] else "No description available")
        desc_text.config(state='disabled')
        desc_text.pack(fill='both', expand=True)
        
        # Close button
        button_frame = tk.Frame(details_window, bg='#f0f2f5')
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, 
                 text="Close", 
                 command=details_window.destroy).pack(side='right')
                 
        ttk.Button(button_frame, 
                 text="Back to Home", 
                 command=lambda: [details_window.destroy(), self.show_home_page()]).pack(side='right', padx=5)
    
    def show_add_property_page(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Property")
        add_window.geometry("500x600")
        add_window.configure(bg='#f0f2f5')
        
        # Header frame
        header_frame = tk.Frame(add_window, bg=self.primary_color, height=60)
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, 
                text="Add New Property",
                font=('Arial', 16, 'bold'),
                bg=self.primary_color,
                fg='white').pack(pady=15)
        
        # Main form frame
        form_frame = tk.Frame(add_window, bg='white', padx=20, pady=20)
        form_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollable canvas
        canvas = tk.Canvas(form_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Form fields
        fields = [
            ("Title:", "title_entry"),
            ("Address:", "address_entry"),
            ("Price:", "price_entry"),
            ("Bedrooms:", "bedrooms_entry"),
            ("Bathrooms:", "bathrooms_entry"),
            ("Size (sqft):", "size_entry")
        ]
        
        for i, (label, var_name) in enumerate(fields):
            tk.Label(scrollable_frame, 
                   text=label,
                   bg='white',
                   font=('Arial', 10, 'bold')).grid(row=i, column=0, sticky='e', pady=10, padx=5)
            
            entry = ttk.Entry(scrollable_frame, width=40)
            entry.grid(row=i, column=1, sticky='w', pady=10, padx=5)
            setattr(self, var_name, entry)
        
        # Property type
        tk.Label(scrollable_frame, 
               text="Type:",
               bg='white',
               font=('Arial', 10, 'bold')).grid(row=len(fields), column=0, sticky='e', pady=10, padx=5)
        
        self.type_combobox = ttk.Combobox(scrollable_frame, 
                                        values=['House', 'Apartment', 'Condo', 'Land'],
                                        width=37)
        self.type_combobox.grid(row=len(fields), column=1, sticky='w', pady=10, padx=5)
        
        # Description
        tk.Label(scrollable_frame, 
               text="Description:",
               bg='white',
               font=('Arial', 10, 'bold')).grid(row=len(fields)+1, column=0, sticky='ne', pady=10, padx=5)
        
        self.desc_text = tk.Text(scrollable_frame, 
                               height=5,
                               width=40,
                               wrap='word',
                               padx=5,
                               pady=5)
        self.desc_text.grid(row=len(fields)+1, column=1, sticky='w', pady=10, padx=5)
        
        # Submit button
        def submit_property():
            try:
                cursor = self.connection.cursor()
                cursor.execute("""
                    INSERT INTO properties (
                        title, address, price, bedrooms, bathrooms, 
                        size_sqft, type, description, agent_id, status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Available')
                """, (
                    self.title_entry.get(),
                    self.address_entry.get(),
                    float(self.price_entry.get()),
                    int(self.bedrooms_entry.get()) if self.bedrooms_entry.get() else None,
                    int(self.bathrooms_entry.get()) if self.bathrooms_entry.get() else None,
                    int(self.size_entry.get()) if self.size_entry.get() else None,
                    self.type_combobox.get(),
                    self.desc_text.get("1.0", tk.END).strip(),
                    self.current_user if self.user_type == 'agent' else None
                ))
                self.connection.commit()
                cursor.close()
                messagebox.showinfo("Success", "Property added successfully!")
                add_window.destroy()
                self.load_properties()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for price, bedrooms, bathrooms, and size")
            except Error as e:
                messagebox.showerror("Error", f"Failed to add property: {e}")
        
        # Button frame
        button_frame = tk.Frame(add_window, bg='#f0f2f5', padx=10, pady=10)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, 
                 text="Submit",
                 style='Accent.TButton',
                 command=submit_property).pack(side='left', padx=5)
        
        ttk.Button(button_frame, 
                 text="Cancel", 
                 command=add_window.destroy).pack(side='right')
                 
        ttk.Button(button_frame, 
                 text="Back to Home", 
                 command=lambda: [add_window.destroy(), self.show_home_page()]).pack(side='right', padx=5)
    
    def show_payment_page(self):
        self.clear_window()
        
        # Create header
        self.create_header("Make a Payment")
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#f0f2f5')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Property selection frame
        property_frame = tk.Frame(content_frame, bg='white', padx=10, pady=10)
        property_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(property_frame, 
               text="Select Property:",
               bg='white',
               font=('Arial', 10, 'bold')).pack(anchor='w')
        
        # Property treeview with scrollbars
        tree_frame = tk.Frame(property_frame, bg='white')
        tree_frame.pack(fill='x', pady=5)
        
        y_scroll = ttk.Scrollbar(tree_frame)
        y_scroll.pack(side='right', fill='y')
        
        self.payment_property_tree = ttk.Treeview(tree_frame, 
                                               columns=("ID", "Title", "Price"), 
                                               show='headings',
                                               height=5,
                                               yscrollcommand=y_scroll.set)
        
        self.payment_property_tree.heading("ID", text="ID", anchor='center')
        self.payment_property_tree.heading("Title", text="Title", anchor='center')
        self.payment_property_tree.heading("Price", text="Price", anchor='center')
        
        self.payment_property_tree.column("ID", width=50, anchor='center')
        self.payment_property_tree.column("Title", width=250, anchor='w')
        self.payment_property_tree.column("Price", width=100, anchor='e')
        
        self.payment_property_tree.pack(fill='x')
        y_scroll.config(command=self.payment_property_tree.yview)
        
        # Load properties available for payment
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, title, price 
            FROM properties 
            WHERE status IN ('Available', 'Rented')
            ORDER BY title
        """)
        
        for row in cursor:
            formatted_row = list(row)
            formatted_row[2] = f"${row[2]:,.2f}"
            self.payment_property_tree.insert("", "end", values=formatted_row)
        cursor.close()
        
        # Payment details frame
        payment_frame = tk.Frame(content_frame, bg='white', padx=10, pady=10)
        payment_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(payment_frame, 
               text="Payment Details:",
               bg='white',
               font=('Arial', 10, 'bold')).pack(anchor='w', pady=(0, 10))
        
        # Amount
        details_frame = tk.Frame(payment_frame, bg='white')
        details_frame.pack(fill='x')
        
        tk.Label(details_frame, 
               text="Amount:",
               bg='white').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        
        self.payment_amount = ttk.Entry(details_frame, width=30)
        self.payment_amount.grid(row=1, column=1, sticky='w', pady=5)
        
        # Payment method
        tk.Label(details_frame, 
               text="Payment Method:",
               bg='white').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        
        self.payment_method = ttk.Combobox(details_frame, 
                                        values=['Credit Card', 'Bank Transfer', 'Cash'],
                                        width=27)
        self.payment_method.grid(row=2, column=1, sticky='w', pady=5)
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg='#f0f2f5')
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, 
                 text="Submit Payment",
                 style='Accent.TButton',
                 command=self.process_payment).pack(side='left', padx=5)
        
        ttk.Button(button_frame, 
                 text="Back to Home", 
                 command=self.show_home_page).pack(side='right')
    
    def process_payment(self):
        selected = self.payment_property_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a property")
            return
        
        property_id = self.payment_property_tree.item(selected)['values'][0]
        amount = self.payment_amount.get()
        method = self.payment_method.get()
        
        if not all([property_id, amount, method]):
            messagebox.showwarning("Warning", "Please fill all fields")
            return
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO payments (property_id, client_id, amount, payment_date, payment_method)
                VALUES (%s, %s, %s, CURDATE(), %s)
            """, (property_id, self.current_user, float(amount), method))
            self.connection.commit()
            cursor.close()
            messagebox.showinfo("Success", "Payment processed successfully!")
            self.show_home_page()
        except Error as e:
            messagebox.showerror("Error", f"Payment failed: {e}")
    
    def show_viewings_page(self):
        self.clear_window()
        
        # Create header
        self.create_header("Schedule a Viewing")
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#f0f2f5')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Property selection frame
        property_frame = tk.Frame(content_frame, bg='white', padx=10, pady=10)
        property_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(property_frame, 
               text="Select Property:",
               bg='white',
               font=('Arial', 10, 'bold')).pack(anchor='w')
        
        # Property treeview with scrollbars
        tree_frame = tk.Frame(property_frame, bg='white')
        tree_frame.pack(fill='x', pady=5)
        
        y_scroll = ttk.Scrollbar(tree_frame)
        y_scroll.pack(side='right', fill='y')
        
        self.viewing_property_tree = ttk.Treeview(tree_frame, 
                                               columns=("ID", "Title", "Address"), 
                                               show='headings',
                                               height=5,
                                               yscrollcommand=y_scroll.set)
        
        self.viewing_property_tree.heading("ID", text="ID", anchor='center')
        self.viewing_property_tree.heading("Title", text="Title", anchor='center')
        self.viewing_property_tree.heading("Address", text="Address", anchor='center')
        
        self.viewing_property_tree.column("ID", width=50, anchor='center')
        self.viewing_property_tree.column("Title", width=200, anchor='w')
        self.viewing_property_tree.column("Address", width=300, anchor='w')
        
        self.viewing_property_tree.pack(fill='x')
        y_scroll.config(command=self.viewing_property_tree.yview)
        
        # Load available properties
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, title, address 
            FROM properties 
            WHERE status = 'Available'
            ORDER BY title
        """)
        
        for row in cursor:
            self.viewing_property_tree.insert("", "end", values=row)
        cursor.close()
        
        # Viewing details frame
        viewing_frame = tk.Frame(content_frame, bg='white', padx=10, pady=10)
        viewing_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(viewing_frame, 
               text="Viewing Details:",
               bg='white',
               font=('Arial', 10, 'bold')).pack(anchor='w', pady=(0, 10))
        
        # Viewing date and time
        details_frame = tk.Frame(viewing_frame, bg='white')
        details_frame.pack(fill='x')
        
        # Viewing date
        tk.Label(details_frame, 
               text="Viewing Date (YYYY-MM-DD):",
               bg='white').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        
        self.viewing_date = ttk.Entry(details_frame, width=30)
        self.viewing_date.grid(row=1, column=1, sticky='w', pady=5)
        
        # Viewing time
        tk.Label(details_frame, 
               text="Viewing Time (HH:MM):",
               bg='white').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        
        self.viewing_time = ttk.Entry(details_frame, width=30)
        self.viewing_time.grid(row=2, column=1, sticky='w', pady=5)
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg='#f0f2f5')
        button_frame.pack(fill='x', pady=10)
        
        ttk.Button(button_frame, 
                 text="Schedule Viewing", 
                 style='Accent.TButton',
                 command=self.schedule_viewing).pack(side='left', padx=5)
        
        ttk.Button(button_frame, 
                 text="View My Viewings", 
                 command=self.show_my_viewings).pack(side='left', padx=5)
        
        ttk.Button(button_frame, 
                 text="Back to Home", 
                 command=self.show_home_page).pack(side='right')
    
    def schedule_viewing(self):
        selected = self.viewing_property_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a property")
            return
        
        property_id = self.viewing_property_tree.item(selected)['values'][0]
        date = self.viewing_date.get()
        time = self.viewing_time.get()
        
        if not all([property_id, date, time]):
            messagebox.showwarning("Warning", "Please fill all fields")
            return
        
        try:
            datetime_str = f"{date} {time}:00"
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO viewings (property_id, client_id, viewing_date, status)
                VALUES (%s, %s, %s, 'Scheduled')
            """, (property_id, self.current_user, datetime_str))
            self.connection.commit()
            cursor.close()
            messagebox.showinfo("Success", "Viewing scheduled successfully!")
        except Error as e:
            messagebox.showerror("Error", f"Failed to schedule viewing: {e}")
    
    def show_my_viewings(self):
        viewings_window = tk.Toplevel(self.root)
        viewings_window.title("My Scheduled Viewings")
        viewings_window.geometry("800x500")
        viewings_window.configure(bg='#f0f2f5')
        
        # Header frame
        header_frame = tk.Frame(viewings_window, bg=self.primary_color, height=60)
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, 
                text="My Scheduled Viewings",
                font=('Arial', 16, 'bold'),
                bg=self.primary_color,
                fg='white').pack(pady=15)
        
        # Main content frame
        content_frame = tk.Frame(viewings_window, bg='#f0f2f5')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Viewings treeview with scrollbars
        tree_frame = tk.Frame(content_frame, bg='#f0f2f5')
        tree_frame.pack(fill='both', expand=True)
        
        y_scroll = ttk.Scrollbar(tree_frame)
        y_scroll.pack(side='right', fill='y')
        
        x_scroll = ttk.Scrollbar(tree_frame, orient='horizontal')
        x_scroll.pack(side='bottom', fill='x')
        
        viewings_tree = ttk.Treeview(tree_frame, 
                                   columns=("ID", "Property", "Date", "Status"),
                                   show='headings',
                                   height=10,
                                   yscrollcommand=y_scroll.set,
                                   xscrollcommand=x_scroll.set)
        
        # Configure columns
        viewings_tree.heading("ID", text="ID", anchor='center')
        viewings_tree.heading("Property", text="Property", anchor='center')
        viewings_tree.heading("Date", text="Date & Time", anchor='center')
        viewings_tree.heading("Status", text="Status", anchor='center')
        
        viewings_tree.column("ID", width=50, anchor='center')
        viewings_tree.column("Property", width=250, anchor='w')
        viewings_tree.column("Date", width=150, anchor='center')
        viewings_tree.column("Status", width=100, anchor='center')
        
        viewings_tree.pack(fill='both', expand=True)
        
        # Configure scrollbars
        y_scroll.config(command=viewings_tree.yview)
        x_scroll.config(command=viewings_tree.xview)
        
        # Load viewings
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT v.id, p.title, v.viewing_date, v.status
            FROM viewings v
            JOIN properties p ON v.property_id = p.id
            WHERE v.client_id = %s
            ORDER BY v.viewing_date
        """, (self.current_user,))
        
        for row in cursor:
            viewings_tree.insert("", "end", values=(
                row[0], 
                row[1], 
                row[2].strftime('%Y-%m-%d %H:%M'), 
                row[3]
            ))
        cursor.close()
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg='#f0f2f5')
        button_frame.pack(fill='x', pady=(10, 0))
        
        def cancel_viewing():
            selected = viewings_tree.focus()
            if not selected:
                messagebox.showwarning("Warning", "Please select a viewing")
                return
            
            viewing_id = viewings_tree.item(selected)['values'][0]
            
            if messagebox.askyesno("Confirm", "Are you sure you want to cancel this viewing?"):
                try:
                    cursor = self.connection.cursor()
                    cursor.execute("""
                        UPDATE viewings 
                        SET status = 'Cancelled' 
                        WHERE id = %s
                    """, (viewing_id,))
                    self.connection.commit()
                    cursor.close()
                    messagebox.showinfo("Success", "Viewing cancelled successfully")
                    viewings_window.destroy()
                    self.show_my_viewings()
                except Error as e:
                    messagebox.showerror("Error", f"Failed to cancel viewing: {e}")
        
        ttk.Button(button_frame, 
                 text="Cancel Viewing", 
                 command=cancel_viewing,
                 style='Accent.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, 
                 text="Close", 
                 command=viewings_window.destroy).pack(side='right')
                 
        ttk.Button(button_frame, 
                 text="Back to Home", 
                 command=lambda: [viewings_window.destroy(), self.show_home_page()]).pack(side='right', padx=5)
    
    def show_admin_dashboard(self):
        if self.user_type != 'admin':
            messagebox.showwarning("Warning", "Admin access required")
            return
        
        self.clear_window()
        
        # Create header
        self.create_header("Admin Dashboard")
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#f0f2f5')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Stats cards frame
        stats_frame = tk.Frame(content_frame, bg='#f0f2f5')
        stats_frame.pack(fill='x', pady=(0, 20))
        
        # Get stats
        cursor = self.connection.cursor()
        
        # Total properties card
        cursor.execute("SELECT COUNT(*) FROM properties")
        total_properties = cursor.fetchone()[0]
        self.create_stat_card(stats_frame, "Total Properties", total_properties, 0, self.primary_color)
        
        # Available properties card
        cursor.execute("SELECT COUNT(*) FROM properties WHERE status = 'Available'")
        available_properties = cursor.fetchone()[0]
        self.create_stat_card(stats_frame, "Available Properties", available_properties, 1, self.success_color)
        
        # Total users card
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        self.create_stat_card(stats_frame, "Total Users", total_users, 2, self.accent_color)
        
        cursor.close()
        
        # Admin actions frame
        action_frame = tk.Frame(content_frame, bg='#f0f2f5')
        action_frame.pack(fill='both', expand=True)
        
        # Action buttons
        actions = [
            ("Manage Users", self.manage_users, "#3498db"),
            ("View All Payments", self.view_all_payments, "#2ecc71"),
            ("View All Viewings", self.view_all_viewings, "#e74c3c"),
            ("Back to Home", self.show_home_page, "#95a5a6")
        ]
        
        for i, (text, command, color) in enumerate(actions):
            btn = tk.Button(action_frame,
                          text=text,
                          font=('Arial', 12),
                          bg=color,
                          fg='white',
                          activebackground=self.darken_color(color),
                          activeforeground='white',
                          relief='flat',
                          bd=0,
                          padx=20,
                          pady=15,
                          command=command)
            
            btn.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='nsew')
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.darken_color(b['bg'])))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
        
        # Configure grid weights
        action_frame.grid_columnconfigure(0, weight=1)
        action_frame.grid_columnconfigure(1, weight=1)
        for i in range(2):
            action_frame.grid_rowconfigure(i, weight=1)
    
    def create_stat_card(self, parent, title, value, position, color):
        """Create a card showing a statistic"""
        card = tk.Frame(parent, bg='white', padx=15, pady=15, bd=0)
        card.grid(row=0, column=position, padx=10, pady=10, sticky='nsew')
        
        # Title
        tk.Label(card, 
               text=title,
               font=('Arial', 10),
               fg='#7f8c8d',
               bg='white').pack(anchor='w')
        
        # Value
        value_label = tk.Label(card, 
                             text=str(value),
                             font=('Arial', 24, 'bold'),
                             fg=color,
                             bg='white')
        value_label.pack(anchor='w', pady=(5, 0))
        
        parent.grid_columnconfigure(position, weight=1)
    
    def manage_users(self):
        users_window = tk.Toplevel(self.root)
        users_window.title("User Management")
        users_window.geometry("800x400")
        
        tk.Label(users_window, text="All Users", font=('Arial', 14)).pack(pady=10)
        
        # Users treeview
        users_tree = ttk.Treeview(users_window, 
                                 columns=("ID", "Username", "Name", "Email", "Type"),
                                 show='headings', height=10)
        users_tree.heading("ID", text="ID")
        users_tree.heading("Username", text="Username")
        users_tree.heading("Name", text="Full Name")
        users_tree.heading("Email", text="Email")
        users_tree.heading("Type", text="User Type")
        
        users_tree.column("ID", width=50)
        users_tree.column("Username", width=100)
        users_tree.column("Name", width=150)
        users_tree.column("Email", width=200)
        users_tree.column("Type", width=100)
        
        users_tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Load users
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, username, full_name, email, user_type
            FROM users
            ORDER BY user_type, username
        """)
        
        for row in cursor:
            users_tree.insert("", "end", values=row)
        cursor.close()
        
        # Delete user button
        def delete_user():
            selected = users_tree.focus()
            if not selected:
                messagebox.showwarning("Warning", "Please select a user")
                return
            
            user_id = users_tree.item(selected)['values'][0]
            
            if messagebox.askyesno("Confirm", "Delete this user?"):
                try:
                    cursor = self.connection.cursor()
                    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                    self.connection.commit()
                    cursor.close()
                    messagebox.showinfo("Success", "User deleted")
                    users_window.destroy()
                    self.manage_users()
                except Error as e:
                    messagebox.showerror("Error", f"Failed to delete user: {e}")
        
        tk.Button(users_window, text="Delete User", command=delete_user).pack(pady=10)
    
    def view_all_payments(self):
        payments_window = tk.Toplevel(self.root)
        payments_window.title("All Payments")
        payments_window.geometry("900x400")
        
        tk.Label(payments_window, text="Payment History", font=('Arial', 14)).pack(pady=10)
        
        # Payments treeview
        payments_tree = ttk.Treeview(payments_window, 
                                   columns=("ID", "Property", "Client", "Amount", "Date", "Method"),
                                   show='headings', height=10)
        payments_tree.heading("ID", text="ID")
        payments_tree.heading("Property", text="Property")
        payments_tree.heading("Client", text="Client")
        payments_tree.heading("Amount", text="Amount")
        payments_tree.heading("Date", text="Date")
        payments_tree.heading("Method", text="Method")
        
        payments_tree.column("ID", width=50)
        payments_tree.column("Property", width=200)
        payments_tree.column("Client", width=150)
        payments_tree.column("Amount", width=100)
        payments_tree.column("Date", width=100)
        payments_tree.column("Method", width=100)
        
        payments_tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Load payments
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT p.id, pr.title, u.full_name, p.amount, p.payment_date, p.payment_method
            FROM payments p
            JOIN properties pr ON p.property_id = pr.id
            JOIN users u ON p.client_id = u.id
            ORDER BY p.payment_date DESC
        """)
        
        for row in cursor:
            payments_tree.insert("", "end", values=(
                row[0], row[1], row[2], f"${row[3]:,.2f}", 
                row[4].strftime('%Y-%m-%d'), row[5]
            ))
        cursor.close()
    
    def view_all_viewings(self):
        viewings_window = tk.Toplevel(self.root)
        viewings_window.title("All Viewings")
        viewings_window.geometry("900x400")
        
        tk.Label(viewings_window, text="All Viewings", font=('Arial', 14)).pack(pady=10)
        
        # Viewings treeview
        viewings_tree = ttk.Treeview(viewings_window, 
                                   columns=("ID", "Property", "Client", "Date", "Status"),
                                   show='headings', height=10)
        viewings_tree.heading("ID", text="ID")
        viewings_tree.heading("Property", text="Property")
        viewings_tree.heading("Client", text="Client")
        viewings_tree.heading("Date", text="Date & Time")
        viewings_tree.heading("Status", text="Status")
        
        viewings_tree.column("ID", width=50)
        viewings_tree.column("Property", width=250)
        viewings_tree.column("Client", width=150)
        viewings_tree.column("Date", width=150)
        viewings_tree.column("Status", width=100)
        
        viewings_tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Load viewings
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT v.id, p.title, u.full_name, v.viewing_date, v.status
            FROM viewings v
            JOIN properties p ON v.property_id = p.id
            JOIN users u ON v.client_id = u.id
            ORDER BY v.viewing_date DESC
        """)
        
        for row in cursor:
            viewings_tree.insert("", "end", values=(
                row[0], row[1], row[2], 
                row[3].strftime('%Y-%m-%d %H:%M'), 
                row[4]
            ))
        cursor.close()
        
        # Update status button
        def update_status():
            selected = viewings_tree.focus()
            if not selected:
                messagebox.showwarning("Warning", "Please select a viewing")
                return
            
            viewing_id = viewings_tree.item(selected)['values'][0]
            current_status = viewings_tree.item(selected)['values'][4]
            
            status_window = tk.Toplevel(viewings_window)
            status_window.title("Update Viewing Status")
            
            tk.Label(status_window, text="Select new status:").pack(pady=10)
            
            new_status = ttk.Combobox(status_window, 
                                    values=['Scheduled', 'Completed', 'Cancelled'],
                                    width=15)
            new_status.pack(pady=5)
            new_status.set(current_status)
            
            def save_status():
                try:
                    cursor = self.connection.cursor()
                    cursor.execute("""
                        UPDATE viewings 
                        SET status = %s 
                        WHERE id = %s
                    """, (new_status.get(), viewing_id))
                    self.connection.commit()
                    cursor.close()
                    messagebox.showinfo("Success", "Status updated")
                    status_window.destroy()
                    viewings_window.destroy()
                    self.view_all_viewings()
                except Error as e:
                    messagebox.showerror("Error", f"Failed to update status: {e}")
            
            tk.Button(status_window, text="Save", command=save_status).pack(pady=10)
        
        tk.Button(viewings_window, text="Update Status", command=update_status).pack(pady=10)
    
    def logout(self):
        self.current_user = None
        self.user_type = None
        self.show_login_page()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Configure accent button style
style = ttk.Style()
style.configure('Accent.TButton', 
               background='#e74c3c',
               foreground='white',
               font=('Arial', 10),
               padding=6)
style.map('Accent.TButton',
         background=[('active', '#c0392b')],
         foreground=[('active', 'white')])

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()