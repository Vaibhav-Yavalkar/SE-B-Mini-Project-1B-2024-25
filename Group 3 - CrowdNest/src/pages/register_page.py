import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from src.ui.modern_ui import ModernUI
from src.constants import STATES
from src.utils.email_validator import EmailValidator
import random
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RegisterPage:
    def __init__(self, parent, register_callback, show_frame_callback):
        self.parent = parent
        self.register_callback = register_callback
        self.show_frame = show_frame_callback
        self.frame = None
        self.reg_entries = {}
        self.reg_state_var = tk.StringVar()
        self.reg_city_var = tk.StringVar()
        self.password_strength_label = None
        
        # Email verification variables
        self.verification_code = None
        self.verification_window = None
        self.verification_entry = None
        
        # Profile picture upload variable
        self.profile_picture_path = None
        
        self.create_frame()
        
    def generate_verification_code(self):
        """Generate a 6-digit verification code"""
        return str(random.randint(100000, 999999))
    
    def send_verification_email(self, email):
        """Send verification email"""
        try:
            # Generate verification code
            self.verification_code = self.generate_verification_code()
            
            # Email configuration from environment variables
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', 587))
            sender_email = os.getenv('SMTP_EMAIL')
            sender_password = os.getenv('SMTP_PASSWORD')
            
            if not smtp_server or not smtp_port or not sender_email or not sender_password:
                messagebox.showerror("Email Configuration Error", "Missing SMTP configuration. Check your .env file.")
                return False
            
            # Create HTML message using template
            from src.utils.html_email_templates import HTMLEmailTemplates
            
            # Create a verification message with proper styling
            verification_message = f"Your verification code is: {self.verification_code}"
            html_content = HTMLEmailTemplates.verification_email_template("User", verification_message)
            
            # Create MIME message with HTML content
            msg = HTMLEmailTemplates.create_mime_message(
                subject='CrowdNest Email Verification',
                html_content=html_content,
                from_email=sender_email,
                to_email=email
            )
            
            # Send email with detailed error handling
            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.ehlo()  # Can help diagnose connection issues
                    server.starttls()
                    
                    try:
                        server.login(sender_email, sender_password)
                    except smtplib.SMTPAuthenticationError:
                        messagebox.showerror("Authentication Error", 
                            "Email login failed. If using Gmail, make sure you're using an App Password.\n\n"
                            "To create an App Password:\n"
                            "1. Go to your Google Account > Security\n"
                            "2. Under 'Signing in to Google', select 'App passwords'\n"
                            "3. Generate a new app password for 'Mail'\n"
                            "4. Update your .env file with this password")
                        return False
                    
                    server.send_message(msg)
            except Exception as send_err:
                messagebox.showerror("Email Sending Error", f"Failed to send email: {send_err}")
                return False
            
            return True
        except Exception as e:
            messagebox.showerror("Email Error", f"Could not send verification email: {e}")
            return False
    
    def verify_email(self):
        """Open email verification window"""
        email = self.login_email.get().strip()
        
        # Validate email first
        if not EmailValidator.validate_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address")
            return
        
        # Send verification email
        try:
            self.send_verification_email(email)
            
            # Create verification window
            self.verification_window = tk.Toplevel(self.parent)
            self.verification_window.title("Email Verification")
            self.verification_window.geometry("300x200")
            
            # Verification instructions
            ttk.Label(
                self.verification_window, 
                text="A verification code has been sent to your email.\nPlease enter the code below:", 
                wraplength=250
            ).pack(pady=(20, 10))
            
            # Verification code entry
            self.verification_entry = ModernUI.create_entry(
                self.verification_window, 
                "Enter 6-digit code", 
                width=30
            )
            self.verification_entry.pack(pady=(10, 10))
            
            # Verify button
            ttk.Button(
                self.verification_window, 
                text="Verify", 
                command=self.check_verification_code,
                style='Accent.TButton'
            ).pack(pady=(10, 0))
        
        except Exception as e:
            messagebox.showerror("Verification Error", str(e))
    
    def check_verification_code(self):
        """Check if entered verification code matches"""
        if not self.verification_window:
            return
        
        entered_code = self.verification_entry.get().strip()
        
        if entered_code == self.verification_code:
            messagebox.showinfo("Verification Successful", "Your email has been verified!")
            self.verification_window.destroy()
        else:
            messagebox.showerror("Verification Failed", "Incorrect verification code")
    
    def create_frame(self):
        # Create main frame with proper configuration
        self.frame = ModernUI.create_card(self.parent)
        self.frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Set minimum size for the frame
        min_width = 500
        min_height = 600
        self.frame.configure(width=min_width, height=min_height)
        
        # Main container with proper padding
        main_container = ttk.Frame(self.frame, style='Card.TFrame')
        main_container.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(main_container, highlightthickness=0)
        canvas.configure(bg='#ffffff')
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        
        # Configure scrollable frame
        scrollable_frame = ttk.Frame(canvas, style='Card.TFrame')
        scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Create window in canvas
        self.canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Content wrapper with proper padding
        content_wrapper = ttk.Frame(scrollable_frame, style='Card.TFrame')
        content_wrapper.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Header Section
        header_frame = ttk.Frame(content_wrapper, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        # CrowdNest Logo and Title
        title_label = ttk.Label(
            header_frame,
            text="CrowdNest",
            style='Title.TLabel',
            font=('Poppins', 24, 'bold')
        )
        title_label.pack(pady=(0, 5))
        
        # Welcome Message
        welcome_label = ttk.Label(
            header_frame,
            text="Welcome to CrowdNest! Create your account to get started.",
            style='Subtitle.TLabel',
            font=('Poppins', 12)
        )
        welcome_label.pack(pady=(0, 20))
        
        # Registration Form
        form_frame = ttk.Frame(content_wrapper, style='Card.TFrame')
        form_frame.pack(fill='x', pady=(20, 20))
        
        # Registration Entries Configuration
        entries_config = [
            ("Username", "Enter your username", 'login_username'),
            ("Email", "Enter your email", 'login_email'),
            ("Password", "Enter your password", 'login_password', '*'),
            ("Confirm Password", "Confirm your password", 'login_confirm_password', '*')
        ]
        
        for label_text, placeholder, attr_name, *show_char in entries_config:
            frame = ttk.Frame(form_frame, style='Card.TFrame')
            frame.pack(fill='x', pady=(0, 15))
            
            ttk.Label(frame, text=label_text, style='Subtitle.TLabel', font=('Poppins', 10, 'bold')).pack(anchor='w')
            
            # Determine show character (for password fields)
            show_param = show_char[0] if show_char else ''
            
            entry = ModernUI.create_entry(frame, placeholder, width=50, show=show_param)
            entry.pack(fill='x', pady=(5, 0))
            
            # Store reference to entry
            setattr(self, attr_name, entry)
        
        # Location Section
        location_section = ttk.LabelFrame(form_frame, text="Location Details", style='Card.TFrame')
        location_section.pack(fill='x', pady=(20, 15), padx=0)
        
        # State Dropdown
        state_frame = ttk.Frame(location_section, style='Card.TFrame')
        state_frame.pack(fill='x', pady=(10, 5), padx=10)
        
        ttk.Label(state_frame, text="State", style='Subtitle.TLabel', font=('Poppins', 10, 'bold')).pack(anchor='w')
        state_dropdown = ttk.Combobox(
            state_frame, 
            textvariable=self.reg_state_var, 
            values=list(STATES.keys()), 
            width=47, 
            font=('Poppins', 10)
        )
        state_dropdown.pack(fill='x', pady=(5, 0))
        
        # City Dropdown
        city_frame = ttk.Frame(location_section, style='Card.TFrame')
        city_frame.pack(fill='x', pady=(0, 10), padx=10)
        
        ttk.Label(city_frame, text="City", style='Subtitle.TLabel', font=('Poppins', 10, 'bold')).pack(anchor='w')
        city_dropdown = ttk.Combobox(
            city_frame, 
            textvariable=self.reg_city_var, 
            values=STATES.get(self.reg_state_var.get(), []), 
            width=47, 
            font=('Poppins', 10)
        )
        city_dropdown.pack(fill='x', pady=(5, 0))
        
        # Update city dropdown when state changes
        def update_cities(*args):
            selected_state = self.reg_state_var.get()
            city_dropdown['values'] = STATES.get(selected_state, [])
        
        self.reg_state_var.trace('w', update_cities)
        
        # Button Container
        button_container = ttk.Frame(form_frame, style='Card.TFrame')
        button_container.pack(fill='x', pady=(20, 10))
        
        # Verify Email Button
        verify_email_button = ttk.Button(
            button_container, 
            text="Verify Email", 
            command=self.verify_email, 
            width=50,
            style='Accent.TButton'
        )
        verify_email_button.pack(side='top', pady=(0, 10), expand=True)
        
        # Register Button
        register_button = ttk.Button(
            button_container, 
            text="Register", 
            command=self.register, 
            width=50,
            style='Primary.TButton'
        )
        register_button.pack(side='top', pady=(0, 10), expand=True)
        
        # Login Section
        login_frame = ttk.Frame(content_wrapper, style='Card.TFrame')
        login_frame.pack(fill='x', pady=(10, 30))
        
        ttk.Label(login_frame, text="Already have an account?", style='Subtitle.TLabel', font=('Poppins', 10)).pack(anchor='center')
        
        login_button = ttk.Button(
            login_frame, 
            text="Login", 
            command=lambda: self.show_frame('LoginPage'), 
            width=50,
            style='Secondary.TButton'
        )
        login_button.pack(pady=(5, 0), expand=True)
        
        # Configure canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Update canvas window when frame size changes
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            width = event.width if event.width > 400 else 400  # Minimum width
            canvas.itemconfig(self.canvas_window, width=width)
        
        scrollable_frame.bind('<Configure>', on_frame_configure)
        canvas.bind('<Configure>', on_frame_configure)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Cleanup function
        def cleanup():
            canvas.unbind_all("<MouseWheel>")
        
        self.frame.bind("<Unmap>", lambda e: cleanup())
    
    def register(self):
        """Handle user registration"""
        # Retrieve form data
        username = self.login_username.get().strip()
        email = self.login_email.get().strip()
        password = self.login_password.get()
        confirm_password = self.login_confirm_password.get()
        state = self.reg_state_var.get()
        city = self.reg_city_var.get()

        # Validate inputs
        if not all([username, email, password, confirm_password, state, city]):
            messagebox.showerror("Error", "All fields are required")
            return

        # Validate email
        if not EmailValidator.validate_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address")
            return

        # Check if email is verified
        if not self.verification_code:
            messagebox.showerror("Email Not Verified", "Please verify your email first")
            return

        # Validate password
        password = password.strip()
        confirm_password = confirm_password.strip()
        if password != confirm_password:
            messagebox.showerror("Password Mismatch", "Passwords do not match")
            return

        if len(password.strip()) < 6:
            messagebox.showerror("Weak Password", "Password must be at least 6 characters long")
            return

        # Validate state and city
        if not state or state == "Select State":
            messagebox.showerror("Invalid State", "Please select a valid state")
            return

        if not city or city == "Select City":
            messagebox.showerror("Invalid City", "Please select a valid city")
            return

        # Combine state and city
        location = f"{city}, {state}"

        # Call registration callback
        self.register_callback(username, email, password.strip(), location)
    
    def center_frame(self):
        """Center the frame within its parent"""
        if hasattr(self, 'frame'):
            # Configure frame to be centered
            self.frame.grid_rowconfigure(0, weight=1)
            self.frame.grid_columnconfigure(0, weight=1)
            
            # Ensure the frame is visible and centered
            self.frame.update_idletasks()