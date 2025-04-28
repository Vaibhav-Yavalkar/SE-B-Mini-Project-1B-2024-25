import tkinter as tk
from tkinter import ttk, messagebox, font
import bcrypt
import mysql.connector
import re
from PIL import Image, ImageTk
import os
from database import create_connection

# Function to hash the password using bcrypt
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Function to check if the username or email already exists
def check_user_exists(username, email):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            if result:
                return True
            return False
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return False

# Function to validate email format
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

# Function to validate password strength
def is_strong_password(password):
    # Password should be at least 8 characters with letters, numbers, and special characters
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number."
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character."
    
    return True, "Password is strong!"

# Function to register a new user
def register_user(username, password, email, security_question, security_answer):
    # Validate email format
    if not is_valid_email(email):
        messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
        return False
    
    # Validate password strength
    is_valid, password_message = is_strong_password(password)
    if not is_valid:
        messagebox.showwarning("Weak Password", password_message)
        return False
    
    # Check if user exists
    if check_user_exists(username, email):
        messagebox.showwarning("User Exists", "Username or email already exists.")
        return False

    hashed_password = hash_password(password)

    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = "INSERT INTO users (username, password, email, security_question, security_answer) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (username, hashed_password.decode('utf-8'), email, security_question, security_answer))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Registration", "User registered successfully!")
            return True
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", "Failed to register user. Please try again.")
        return False

# RegisterWindow class definition
class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Register - Read Rover")
        self.root.geometry('800x700')
        self.root.configure(bg="#f5f5f5")
        
        # Colors
        self.colors = {
            "primary": "#4361ee",
            "secondary": "#3f37c9",
            "accent": "#4CAF50",
            "danger": "#e74c3c",
            "background": "#f5f5f5",
            "card": "#ffffff",
            "text": "#333333",
            "muted": "#777777",
            "highlight": "#f72585"
        }
        
        # Font Styles
        self.title_font = font.Font(family='Helvetica', size=22, weight='bold')
        self.heading_font = font.Font(family='Helvetica', size=14, weight='bold')
        self.label_font = font.Font(family='Helvetica', size=12)
        self.button_font = font.Font(family='Helvetica', size=12, weight='bold')
        self.entry_font = font.Font(family='Helvetica', size=11)
        
        # Create main frame that fills the window
        self.main_frame = tk.Frame(self.root, bg=self.colors["background"])
        self.main_frame.pack(fill="both", expand=True)
        
        # Header with app name and logo
        self.create_header()
        
        # Content area with registration form
        self.create_content()
        
        # Footer
        self.create_footer()

    def create_header(self):
        """Create the header with app name and logo"""
        header_frame = tk.Frame(self.main_frame, bg=self.colors["primary"], height=80)
        header_frame.pack(fill="x")
        
        # App logo and name
        logo_frame = tk.Frame(header_frame, bg=self.colors["primary"])
        logo_frame.pack(side="left", padx=20)
        
        # Create logo canvas
        logo_canvas = tk.Canvas(logo_frame, width=50, height=50, bg=self.colors["primary"], highlightthickness=0)
        logo_canvas.create_rectangle(10, 5, 40, 45, fill="#ffffff", outline="")
        logo_canvas.create_rectangle(15, 12, 35, 15, fill=self.colors["primary"], outline="")
        logo_canvas.create_rectangle(15, 20, 35, 23, fill=self.colors["primary"], outline="")
        logo_canvas.create_rectangle(15, 28, 35, 31, fill=self.colors["primary"], outline="")
        logo_canvas.pack(side="left")
        
        # App name
        app_name = tk.Label(logo_frame, text="Read Rover", 
                           font=("Helvetica", 24, "bold"), 
                           fg="white", bg=self.colors["primary"])
        app_name.pack(side="left", padx=10)
        
        # Right side of header - back button
        back_btn = tk.Button(header_frame, text="Back to Login", 
                            command=self.back_to_login,
                            bg=self.colors["secondary"], fg="white",
                            font=("Helvetica", 12, "bold"),
                            width=12, height=1,
                            relief="flat", bd=0)
        back_btn.pack(side="right", padx=20, pady=15)

    def create_content(self):
        """Create content area with registration form"""
        content_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Registration form frame
        self.form_frame = tk.Frame(content_frame, bg=self.colors["card"], padx=30, pady=30, 
                                   bd=1, relief="solid", highlightbackground="#dddddd", highlightthickness=1)
        self.form_frame.pack(fill="both", expand=True)
        
        # Form title
        title_label = tk.Label(self.form_frame, text="Create Your Account", 
                              font=self.title_font, 
                              fg=self.colors["text"], bg=self.colors["card"])
        title_label.pack(pady=(0, 20))
        
        subtitle_label = tk.Label(self.form_frame, text="Join Read Rover to track your reading journey", 
                                 font=("Helvetica", 12), 
                                 fg=self.colors["muted"], bg=self.colors["card"])
        subtitle_label.pack(pady=(0, 30))
        
        # Form fields container
        fields_frame = tk.Frame(self.form_frame, bg=self.colors["card"])
        fields_frame.pack(fill="both", expand=True, padx=20)
        
        # Username field
        self.create_form_field(fields_frame, "Username", 0)
        self.entry_username = self.styled_entry(fields_frame, 0)
        
        # Email field
        self.create_form_field(fields_frame, "Email", 1)
        self.entry_email = self.styled_entry(fields_frame, 1)
        
        # Password with visibility toggle
        self.create_form_field(fields_frame, "Password", 2)
        self.password_frame = tk.Frame(fields_frame, bg=self.colors["card"])
        self.password_frame.grid(row=2, column=1, sticky="ew", pady=10)
        
        self.entry_password = tk.Entry(
            self.password_frame, 
            font=self.entry_font, 
            show="•", 
            bg=self.colors["light_primary"] if hasattr(self.colors, "light_primary") else "#f5f5f5", 
            relief="flat", 
            bd=1
        )
        self.entry_password.pack(side=tk.LEFT, fill="x", expand=True, ipady=8)
        
        self.password_visible = False
        self.toggle_btn = tk.Button(
            self.password_frame, 
            text="👁", 
            command=self.toggle_password_visibility, 
            relief="flat", 
            bg=self.colors["light_primary"] if hasattr(self.colors, "light_primary") else "#f5f5f5", 
            cursor="hand2"
        )
        self.toggle_btn.pack(side=tk.RIGHT)
        
        # Password strength indicator
        self.password_strength = tk.Label(fields_frame, text="", font=font.Font(size=9), 
                                        fg=self.colors["text"], bg=self.colors["card"])
        self.password_strength.grid(row=3, column=1, sticky="w", pady=(0, 10))
        self.entry_password.bind("<KeyRelease>", self.check_password_strength)
        
        # Security Question dropdown
        security_questions = [
            "What is your mother's maiden name?",
            "What was the name of your first pet?",
            "What is your favorite color?",
            "What is the name of your childhood best friend?"
        ]
        self.create_form_field(fields_frame, "Security Question", 4)
        
        self.security_question_var = tk.StringVar()
        self.security_question_var.set(security_questions[0])
        self.security_question_menu = ttk.Combobox(
            fields_frame, 
            textvariable=self.security_question_var, 
            values=security_questions, 
            font=self.entry_font, 
            state="readonly"
        )
        self.security_question_menu.grid(row=4, column=1, sticky="ew", pady=10, ipady=4)
        
        # Security Answer field
        self.create_form_field(fields_frame, "Security Answer", 5)
        self.entry_security_answer = self.styled_entry(fields_frame, 5)
        
        # Agreement checkbox
        self.agreement_var = tk.BooleanVar()
        agreement_frame = tk.Frame(fields_frame, bg=self.colors["card"])
        agreement_frame.grid(row=6, column=0, columnspan=2, sticky="w", pady=20)
        
        self.agreement_check = tk.Checkbutton(
            agreement_frame, 
            text="I agree to the Terms of Service and Privacy Policy",
            variable=self.agreement_var, 
            bg=self.colors["card"], 
            font=self.label_font
        )
        self.agreement_check.pack(anchor="w")
        
        # Buttons
        buttons_frame = tk.Frame(fields_frame, bg=self.colors["card"])
        buttons_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        # Register button
        self.btn_register = tk.Button(
            buttons_frame, 
            text="REGISTER", 
            command=self.on_register, 
            bg=self.colors["highlight"], 
            fg="white", 
            font=self.button_font, 
            width=20, 
            cursor="hand2", 
            padx=10, 
            pady=12,
            relief="flat", 
            bd=0
        )
        self.btn_register.pack(pady=10)
        
        # Back to login link
        back_link = tk.Label(
            buttons_frame, 
            text="Already have an account? Sign in", 
            fg=self.colors["primary"], 
            bg=self.colors["card"], 
            font=("Helvetica", 11, "underline"), 
            cursor="hand2"
        )
        back_link.pack(pady=5)
        back_link.bind("<Button-1>", lambda e: self.back_to_login())

    def create_footer(self):
        """Create footer with additional information"""
        footer_frame = tk.Frame(self.main_frame, bg=self.colors["secondary"], height=40)
        footer_frame.pack(fill="x")
        
        copyright_label = tk.Label(footer_frame, text="© 2025 Read Rover - Your Personal Book Management System",
                                  font=("Helvetica", 10),
                                  fg="white", bg=self.colors["secondary"])
        copyright_label.pack(pady=10)

    def create_form_field(self, parent, label_text, row):
        """Create a form field label with consistent styling"""
        tk.Label(
            parent, 
            text=f"{label_text}:", 
            font=self.label_font, 
            bg=self.colors["card"], 
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=10, padx=(0, 20))
    
    def styled_entry(self, parent, row):
        """Create a styled entry widget"""
        entry = tk.Entry(
            parent, 
            font=self.entry_font, 
            bg=self.colors["light_primary"] if hasattr(self.colors, "light_primary") else "#f5f5f5", 
            relief="flat", 
            bd=1
        )
        entry.grid(row=row, column=1, sticky="ew", pady=10, ipady=8)
        return entry
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.password_visible:
            self.entry_password.config(show="•")
            self.toggle_btn.config(text="👁")
        else:
            self.entry_password.config(show="")
            self.toggle_btn.config(text="🔒")
        self.password_visible = not self.password_visible
    
    def check_password_strength(self, event=None):
        """Check password strength and show feedback"""
        password = self.entry_password.get()
        if not password:
            self.password_strength.config(text="")
            return
        
        valid, message = is_strong_password(password)
        if valid:
            self.password_strength.config(text="Strong password", fg="green")
        else:
            self.password_strength.config(text=message, fg="red")
    
    def on_register(self):
        """Handle registration process"""
        # Collect input values
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        email = self.entry_email.get().strip()
        security_question = self.security_question_var.get()
        security_answer = self.entry_security_answer.get().strip()
        
        # Check agreement
        if not self.agreement_var.get():
            messagebox.showwarning("Agreement Required", "You must agree to the Terms of Service and Privacy Policy.")
            return
        
        # Validate inputs
        if not username or not password or not email or not security_answer:
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        
        # Register user with enhanced validation
        success = register_user(username, password, email, security_question, security_answer)
        if success:
            self.back_to_login()

    def back_to_login(self):
        """Navigate back to login page"""
        self.root.destroy()
        login_root = tk.Tk()
        # Import the HomePage class from the updated login.py file
        from login import HomePage  # Changed from LoginWindow to HomePage to match updated file
        HomePage(login_root)
        login_root.mainloop()

# Main function to run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = RegisterWindow(root)
    root.mainloop()