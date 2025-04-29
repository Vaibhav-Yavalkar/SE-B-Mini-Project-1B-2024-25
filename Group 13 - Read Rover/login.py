import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from dashboard import Dashboard
from database import create_connection
import bcrypt

class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Read Rover - Book Management System")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#f4f4f8")

        # Color scheme
        self.colors = {
            "primary": "#4361ee",
            "secondary": "#3f37c9",
            "light_primary": "#eef2ff",
            "success": "#2ecc71",
            "danger": "#e74c3c",
            "background": "#f4f4f8",
            "card": "#ffffff",
            "text": "#333333",
            "muted": "#777777",
            "highlight": "#f72585"
        }

        # Custom styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background=self.colors["card"])
        self.style.configure("TLabel", font=("Helvetica", 11), background=self.colors["card"])
        self.style.configure("TEntry", font=("Helvetica", 11))
        self.style.configure("TButton", font=("Helvetica", 12))
        self.style.configure("Title.TLabel", font=("Helvetica", 24, "bold"), foreground=self.colors["text"], background=self.colors["card"])
        self.style.configure("Subtitle.TLabel", font=("Helvetica", 16), foreground=self.colors["text"], background=self.colors["card"])
        self.style.configure("Link.TLabel", font=("Helvetica", 10, "underline"), foreground=self.colors["primary"], background=self.colors["card"])
        
        # Create main frame that fills the window
        self.main_frame = tk.Frame(self.root, bg=self.colors["background"])
        self.main_frame.pack(fill="both", expand=True)
        
        # Header with app name and logo
        self.create_header()
        
        # Content area with login form and welcome message
        self.create_content()
        
        # Footer
        self.create_footer()
        
        self.root.bind("<Return>", lambda event: self.login())

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
        
        # Right side of header - exit button
        exit_btn = tk.Button(header_frame, text="Exit", 
                            command=self.root.destroy,
                            bg=self.colors["danger"], fg="white",
                            font=("Helvetica", 12, "bold"),
                            width=8, height=1, 
                            relief="flat", bd=0)
        exit_btn.pack(side="right", padx=20, pady=15)

    def create_content(self):
        """Create content area with welcome message and login form"""
        content_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left side - Welcome message and features
        welcome_frame = tk.Frame(content_frame, bg=self.colors["background"])
        welcome_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Welcome message
        welcome_label = tk.Label(welcome_frame, text="Welcome to Read Rover", 
                                font=("Helvetica", 22, "bold"),
                                fg=self.colors["text"], bg=self.colors["background"])
        welcome_label.pack(anchor="nw", pady=(0, 10))
        
        tagline_label = tk.Label(welcome_frame, text="Your personal book management companion",
                                font=("Helvetica", 14, "italic"),
                                fg=self.colors["muted"], bg=self.colors["background"])
        tagline_label.pack(anchor="nw", pady=(0, 30))
        
        # Feature highlights
        features_frame = tk.Frame(welcome_frame, bg=self.colors["background"])
        features_frame.pack(fill="x", pady=10)
        
        features = [
            ("📚 Manage Your Library", "Keep track of all your books in one place"),
            ("🔖 Create Reading Lists", "Organize books by categories and priorities"),
            ("📊 Track Reading Progress", "Set goals and monitor your reading habits"),
            ("🌟 Rate and Review", "Share your thoughts on books you've read")
        ]
        
        for title, desc in features:
            feature_frame = tk.Frame(features_frame, bg=self.colors["light_primary"], bd=1, relief="flat")
            feature_frame.pack(fill="x", pady=10, ipady=10)
            
            title_label = tk.Label(feature_frame, text=title, 
                                  font=("Helvetica", 14, "bold"),
                                  fg=self.colors["primary"], bg=self.colors["light_primary"])
            title_label.pack(anchor="w", padx=15, pady=(10, 5))
            
            desc_label = tk.Label(feature_frame, text=desc, 
                                 font=("Helvetica", 12),
                                 fg=self.colors["text"], bg=self.colors["light_primary"])
            desc_label.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Right side - Login form
        self.login_container = tk.Frame(content_frame, bg=self.colors["card"], padx=30, pady=30, 
                                 bd=1, relief="solid", highlightbackground="#dddddd", highlightthickness=1)
        self.login_container.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.build_login_ui()

    def create_footer(self):
        """Create footer with additional information"""
        footer_frame = tk.Frame(self.main_frame, bg=self.colors["secondary"], height=40)
        footer_frame.pack(fill="x")
        
        copyright_label = tk.Label(footer_frame, text="© 2025 Read Rover - Your Personal Book Management System",
                                  font=("Helvetica", 10),
                                  fg="white", bg=self.colors["secondary"])
        copyright_label.pack(pady=10)

    def build_login_ui(self):
        """Build the login form UI."""
        # Title
        title_label = ttk.Label(self.login_container, text="Sign In", style="Title.TLabel")
        title_label.pack(pady=(0, 10))

        # Description
        description = ttk.Label(self.login_container, text="Access your bookshelf and personalized recommendations",
                                foreground=self.colors["muted"], background=self.colors["card"], justify="center")
        description.pack(pady=(0, 20))

        # Username input
        username_frame = ttk.Frame(self.login_container)
        username_frame.pack(fill="x", pady=10)

        ttk.Label(username_frame, text="Username", foreground=self.colors["text"]).pack(anchor="w", pady=(0, 5))

        username_input_frame = ttk.Frame(username_frame)
        username_input_frame.pack(fill="x")

        user_icon = ttk.Label(username_input_frame, text="👤", background=self.colors["light_primary"], width=3)
        user_icon.pack(side="left")

        self.entry_username = ttk.Entry(username_input_frame)
        self.entry_username.pack(side="left", fill="x", expand=True, ipady=5)
        self.entry_username.focus()

        # Password input
        password_frame = ttk.Frame(self.login_container)
        password_frame.pack(fill="x", pady=10)

        ttk.Label(password_frame, text="Password", foreground=self.colors["text"]).pack(anchor="w", pady=(0, 5))

        password_input_frame = ttk.Frame(password_frame)
        password_input_frame.pack(fill="x")

        password_icon = ttk.Label(password_input_frame, text="🔒", background=self.colors["light_primary"], width=3)
        password_icon.pack(side="left")

        self.entry_password = ttk.Entry(password_input_frame, show="•")
        self.entry_password.pack(side="left", fill="x", expand=True, ipady=5)

        # Show password
        self.show_password_var = tk.BooleanVar()
        show_password_frame = ttk.Frame(self.login_container)
        show_password_frame.pack(fill="x", pady=(5, 15))

        show_password_cb = ttk.Checkbutton(show_password_frame, text="Show password",
                                           variable=self.show_password_var,
                                           command=self.toggle_password)
        show_password_cb.pack(side="left")

        # Buttons
        login_button = tk.Button(self.login_container, text="SIGN IN", command=self.login,
                                 bg=self.colors["primary"], fg="white", font=("Helvetica", 14, "bold"),
                                 activebackground="#3651d9", activeforeground="white",
                                 relief="flat", bd=0, padx=20, pady=10)
        login_button.pack(fill="x", pady=10)
        
        register_button = tk.Button(self.login_container, text="REGISTER", command=self.redirect_to_signup,
                                   bg=self.colors["highlight"], fg="white", font=("Helvetica", 14, "bold"),
                                   activebackground="#e5127d", activeforeground="white",
                                   relief="flat", bd=0, padx=20, pady=10)
        register_button.pack(fill="x", pady=10)
        
        clear_button = tk.Button(self.login_container, text="CLEAR FIELDS", command=self.clear_fields,
                               bg=self.colors["muted"], fg="white", font=("Helvetica", 12),
                               activebackground="#666666", activeforeground="white",
                               relief="flat", bd=0, padx=20, pady=5)
        clear_button.pack(fill="x", pady=5)

        # Forgot password
        forgot_link_frame = ttk.Frame(self.login_container)
        forgot_link_frame.pack(fill="x", pady=10)

        self.forgot_password_link = ttk.Label(forgot_link_frame, text="Forgot Password?",
                                              style="Link.TLabel", cursor="hand2")
        self.forgot_password_link.pack(side="right")
        self.forgot_password_link.bind("<Button-1>", self.show_forgot_password)

    def toggle_password(self):
        self.entry_password.config(show="" if self.show_password_var.get() else "•")

    def clear_fields(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_username.focus()

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        user_id = self.validate_login(username, password)

        if user_id:
            messagebox.showinfo("Login Successful", f"Welcome {username}!")
            self.root.destroy()
            dashboard_root = tk.Tk()
            Dashboard(dashboard_root, user_id)
            dashboard_root.mainloop()
        else:
            self.entry_password.delete(0, tk.END)
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

    def validate_login(self, username, password):
        try:
            connection = create_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT user_id, password FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
                return user["user_id"]
            return None
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
            return None

    def redirect_to_signup(self, event=None):
        self.root.destroy()
        signup_root = tk.Tk()
        signup_root.title("Register - Read Rover")
        signup_root.geometry("800x600")
        signup_root.resizable(True, True)
        from register import RegisterWindow
        RegisterWindow(signup_root)
        signup_root.mainloop()

    def show_forgot_password(self, event):
        # Clear login form
        for widget in self.login_container.winfo_children():
            widget.destroy()
        self.forgot_password_frame()

    def forgot_password_frame(self):
        title_label = ttk.Label(self.login_container, text="Reset Your Password", style="Title.TLabel")
        title_label.pack(pady=(0, 20))

        description = ttk.Label(self.login_container, text="Enter your username or email address and we'll\nsend you instructions to reset your password.",
                                foreground=self.colors["muted"], background=self.colors["card"], justify="center")
        description.pack(pady=(0, 20))

        input_frame = ttk.Frame(self.login_container)
        input_frame.pack(fill="x", pady=10)

        ttk.Label(input_frame, text="Username or Email", foreground=self.colors["text"]).pack(anchor="w", pady=(0, 5))

        email_input_frame = ttk.Frame(input_frame)
        email_input_frame.pack(fill="x")
        
        email_icon = ttk.Label(email_input_frame, text="✉️", background=self.colors["light_primary"], width=3)
        email_icon.pack(side="left")

        self.entry_forgot_username = ttk.Entry(email_input_frame)
        self.entry_forgot_username.pack(side="left", fill="x", expand=True, ipady=5)
        self.entry_forgot_username.focus()

        reset_button = tk.Button(self.login_container, text="SEND RESET LINK", command=self.recover_password,
                                 bg=self.colors["primary"], fg="white", font=("Helvetica", 14, "bold"),
                                 activebackground="#3651d9", activeforeground="white",
                                 relief="flat", bd=0, padx=20, pady=10)
        reset_button.pack(fill="x", pady=20)

        back_link = ttk.Label(self.login_container, text="← Back to Login", style="Link.TLabel", cursor="hand2")
        back_link.pack(pady=10)
        back_link.bind("<Button-1>", self.show_login_page)

    def recover_password(self):
        username = self.entry_forgot_username.get().strip()
        if not username:
            messagebox.showwarning("Input Error", "Please enter your username or email.")
            return
        messagebox.showinfo("Password Recovery", "If the username or email exists in our system, you will receive reset instructions shortly.")
        self.show_login_page()

    def show_login_page(self, event=None):
        # Clear forgot password form
        for widget in self.login_container.winfo_children():
            widget.destroy()
        self.build_login_ui()

if __name__ == "__main__":
    root = tk.Tk()
    HomePage(root)
    root.mainloop()