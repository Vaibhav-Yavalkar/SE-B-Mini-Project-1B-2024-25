import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.modern_ui import ModernUI

class LoginPage:
    def __init__(self, parent, login_callback, show_frame_callback):
        print(f"LoginPage: Initializing with parent {parent}")
        self.parent = parent
        self.login_callback = login_callback
        self.show_frame = show_frame_callback
        self.frame = None
        self.login_username = None
        self.login_password = None
        self.create_frame()
        print("LoginPage: Initialization complete")
        
    def create_frame(self):
        """Create the login page frame"""
        print("LoginPage: Creating frame")
        try:
            # Create frame
            self.frame = ModernUI.create_card(self.parent)
            
            # Create a canvas for centering
            canvas = tk.Canvas(self.frame, bg='#FFFFFF', highlightthickness=0)
            canvas.pack(fill='both', expand=True)
            
            # Create content frame
            content = ttk.Frame(canvas, style='Card.TFrame')
            canvas.create_window((0, 0), window=content, anchor='nw')
            
            # Configure canvas to center content
            def center_content(event):
                canvas.delete('all')
                canvas.create_window(
                    event.width // 2, 
                    event.height // 2, 
                    window=content, 
                    anchor='center'
                )
            
            canvas.bind('<Configure>', center_content)
            
            # Header
            header_frame = ttk.Frame(content, style='Card.TFrame')
            header_frame.pack(fill='x', pady=(0, 30), anchor="center")
            
            ttk.Label(header_frame, text="CrowdNest", font=('Poppins', 48, 'bold'), foreground='#0077B6').pack(anchor="center")
            ttk.Label(header_frame, text="Welcome Back", font=('Poppins', 24, 'bold'), foreground='#1B1B1E').pack(pady=(10, 5), anchor="center")
            ttk.Label(header_frame, text="Login to continue", font=('Poppins', 14), foreground='#6C757D').pack(anchor="center")
            
            # Form Frame
            form_frame = ttk.Frame(content, style='Card.TFrame')
            form_frame.pack(fill='x', pady=(20, 20), padx=40)
            
            # Username
            username_frame = ttk.Frame(form_frame, style='Card.TFrame')
            username_frame.pack(fill='x', pady=(0, 15))
            
            ttk.Label(username_frame, text="Username", style='Subtitle.TLabel').pack(anchor='w')
            self.login_username = ModernUI.create_entry(username_frame, "Enter your username", width=50)
            self.login_username.pack(fill='x', pady=(5, 0))
            
            # Password
            password_frame = ttk.Frame(form_frame, style='Card.TFrame')
            password_frame.pack(fill='x', pady=(0, 15))
            
            ttk.Label(password_frame, text="Password", style='Subtitle.TLabel').pack(anchor='w')
            self.login_password = ModernUI.create_entry(password_frame, "Enter your password", width=50, show="*")
            self.login_password.pack(fill='x', pady=(5, 0))
            
            # Login Button
            login_button = ModernUI.create_button(
                form_frame, 
                "Login", 
                self.login, 
                width=50
            )
            login_button.pack(pady=(20, 10))
            
            # Register Link
            register_frame = ttk.Frame(content, style='Card.TFrame')
            register_frame.pack(fill='x', pady=(10, 0))
            
            ttk.Label(register_frame, text="Don't have an account?", style='Subtitle.TLabel').pack(anchor='center')
            
            ModernUI.create_button(
                register_frame, 
                "Register", 
                lambda: self.show_frame('RegisterPage'), 
                style='Secondary.TButton', 
                width=50
            ).pack(pady=(5, 0))
            
            print("LoginPage: Frame creation complete")
        except Exception as e:
            print(f"LoginPage: Error creating frame - {e}")
            import traceback
            traceback.print_exc()
    
    def center_frame(self):
        """Center the frame within its parent"""
        if hasattr(self, 'frame'):
            # Configure frame to be centered
            self.frame.grid_rowconfigure(0, weight=1)
            self.frame.grid_columnconfigure(0, weight=1)
            
            # Ensure the frame is visible and centered
            self.frame.update_idletasks()
    
    def login(self):
        """Handle login attempt"""
        print(f"LoginPage: Login attempt for username {self.login_username.get()}")
        try:
            self.login_callback(self.login_username.get(), self.login_password.get())
        except Exception as e:
            print(f"LoginPage: Login error - {e}")
            messagebox.showerror("Login Error", str(e))