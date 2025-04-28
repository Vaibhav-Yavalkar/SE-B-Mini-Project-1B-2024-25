import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import subprocess
import os
try:
    from PIL import Image, ImageTk  # For logo handling
except ImportError:
    pass  # PIL is optional for logo display
import re

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Tanay@26",
    "database": "parkwatch"
}

# Color scheme
COLORS = {
    "primary": "#1E3A8A",      # Dark blue
    "secondary": "#2563EB",    # Medium blue
    "accent": "#4F46E5",       # Purple
    "success": "#10B981",      # Green
    "warning": "#F59E0B",      # Orange
    "error": "#EF4444",        # Red
    "background": "#F3F4F6",   # Light gray
    "card": "#FFFFFF",         # White
    "text_primary": "#1F2937", # Dark gray
    "text_secondary": "#6B7280", # Medium gray
    "text_light": "#FFFFFF"    # White
}

# Function to connect to MySQL
def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        show_custom_error("Database Error", f"Error connecting to MySQL: {err}")
        return None

# Custom styled messagebox - Error
def show_custom_error(title, message):
    error_window = tk.Toplevel()
    error_window.title(title)
    error_window.geometry("400x200")
    error_window.configure(bg=COLORS["background"])
    error_window.grab_set()  # Make window modal
    
    # Center the window
    center_window(error_window, 400, 200)
    
    error_frame = tk.Frame(error_window, bg=COLORS["card"], padx=20, pady=20)
    error_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    tk.Label(error_frame, text="⚠️ Error", font=("Helvetica", 16, "bold"), fg=COLORS["error"], bg=COLORS["card"]).pack(pady=(0, 10))
    tk.Label(error_frame, text=message, font=("Helvetica", 12), fg=COLORS["text_primary"], bg=COLORS["card"], wraplength=350).pack(pady=10)
    
    def close_error():
        error_window.destroy()
    
    tk.Button(error_frame, text="OK", font=("Helvetica", 12), bg=COLORS["error"], fg=COLORS["text_light"], 
              command=close_error, width=10, cursor="hand2", relief="flat").pack(pady=10)

# Custom styled messagebox - Success
def show_custom_success(title, message):
    success_window = tk.Toplevel()
    success_window.title(title)
    success_window.geometry("400x200")
    success_window.configure(bg=COLORS["background"])
    success_window.grab_set()  # Make window modal
    
    # Center the window
    center_window(success_window, 400, 200)
    
    success_frame = tk.Frame(success_window, bg=COLORS["card"], padx=20, pady=20)
    success_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    tk.Label(success_frame, text="✅ Success", font=("Helvetica", 16, "bold"), fg=COLORS["success"], bg=COLORS["card"]).pack(pady=(0, 10))
    tk.Label(success_frame, text=message, font=("Helvetica", 12), fg=COLORS["text_primary"], bg=COLORS["card"], wraplength=350).pack(pady=10)
    
    def close_success():
        success_window.destroy()
    
    tk.Button(success_frame, text="OK", font=("Helvetica", 12), bg=COLORS["success"], fg=COLORS["text_light"], 
              command=close_success, width=10, cursor="hand2", relief="flat").pack(pady=10)

# Function to handle User Login
def user_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        show_custom_error("Input Error", "Please fill in both username and password fields")
        return

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            show_custom_success("Login Success", f"Welcome {username}!")
            login_window.destroy()
            # Open the dashboard after successful login
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dashboard_path = os.path.join(current_dir, "dashboard.py")
            subprocess.Popen(["python", dashboard_path])
        else:
            show_custom_error("Authentication Error", "Invalid username or password")

# Function to handle Admin Login
def admin_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        show_custom_error("Input Error", "Please fill in both username and password fields")
        return

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin_users WHERE username = %s AND password = %s", (username, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            show_custom_success("Admin Login Success", f"Welcome Admin {username}!")
            login_window.destroy()
            # Open the admin dashboard
            current_dir = os.path.dirname(os.path.abspath(__file__))
            admin_dashboard_path = os.path.join(current_dir, "admin_dashboard.py")
            
            # Check if admin_dashboard.py exists, otherwise inform the user
            if os.path.exists(admin_dashboard_path):
                subprocess.Popen(["python", admin_dashboard_path])
            else:
                show_custom_error("Missing File", "Admin dashboard file not found. Please create admin_dashboard.py")
        else:
            show_custom_error("Authentication Error", "Invalid admin credentials")

# Function to center a window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

# Create styled entry with label
def create_styled_entry(parent, label_text, show_char=None, icon=None, width=300):
    container_frame = tk.Frame(parent, bg=COLORS["card"])
    container_frame.pack(pady=5)
    
    frame = tk.Frame(container_frame, bg=COLORS["card"], width=width)
    frame.pack()
    
    tk.Label(frame, text=label_text, font=("Helvetica", 12), bg=COLORS["card"], fg=COLORS["text_primary"], anchor="w").pack(fill="x")
    
    entry_frame = tk.Frame(frame, bg=COLORS["background"], highlightbackground=COLORS["secondary"], highlightthickness=1, width=width)
    entry_frame.pack(pady=2)
    
    if icon:
        tk.Label(entry_frame, text=icon, font=("Helvetica", 12), bg=COLORS["background"], fg=COLORS["text_secondary"], width=2).pack(side="left")
    
    entry = tk.Entry(entry_frame, font=("Helvetica", 12), relief="flat", bg=COLORS["background"], fg=COLORS["text_primary"], 
                    insertbackground=COLORS["text_primary"], width=30)  # Fixed width for entry fields
    if show_char:
        entry.config(show=show_char)
    entry.pack(side="left", ipady=8, padx=5)
    
    return entry

# Create styled button
def create_styled_button(parent, text, command, bg_color, icon=None, width=15):
    button_frame = tk.Frame(parent, bg=COLORS["card"])
    button_frame.pack(pady=5)
    
    button = tk.Button(button_frame, text=text, font=("Helvetica", 12, "bold"), 
                      bg=bg_color, fg=COLORS["text_light"], 
                      command=command, width=width, 
                      relief="flat", cursor="hand2")
    
    # Hover effect
    def on_enter(e):
        button['background'] = shade_color(bg_color, 0.9)
    
    def on_leave(e):
        button['background'] = bg_color
    
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    
    if icon:
        button.config(text=f"{icon} {text}")
    
    button.pack(ipady=8)
    return button

# Function to darken or lighten a color for hover effects
def shade_color(hex_color, factor):
    # Convert hex to RGB
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Apply factor
    r = int(max(0, min(255, r * factor)))
    g = int(max(0, min(255, g * factor)))
    b = int(max(0, min(255, b * factor)))
    
    # Convert back to hex
    return f"#{r:02x}{g:02x}{b:02x}"

# Validation functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r'^\d{10}$'
    return re.match(pattern, phone) is not None

def validate_vehicle_number(vehicle_number):
    # Standard Indian vehicle number format: XX XX XX XXXX
    pattern = r'^[A-Z]{2}\s?[0-9]{1,2}\s?[A-Z]{1,2}\s?[0-9]{1,4}$'
    return re.match(pattern, vehicle_number.upper()) is not None

# Function to handle signup
def signup():
    for widget in login_window.winfo_children():
        widget.destroy()

    login_window.title("Signup")

    tk.Label(login_window, text="ParkWatch Signup", font=("Helvetica", 18, "bold"), fg="black", bg="#ffffff").pack(pady=10)
    tk.Label(login_window, text="Sign up to manage your parking easily!", font=("Arial", 12), fg="black", bg="#ffffff").pack(pady=5)

    # Username
    tk.Label(login_window, text="Username:                        ", font=("Arial", 14), bg="#ffffff", fg="black").pack(pady=5)
    username_entry_signup = tk.Entry(login_window, font=("Arial", 14))
    username_entry_signup.pack(pady=5)

    # Password
    tk.Label(login_window, text="Password:                        ", font=("Arial", 14), bg="#ffffff", fg="black").pack(pady=5)
    password_entry_signup = tk.Entry(login_window, font=("Arial", 14), show="*")
    password_entry_signup.pack(pady=5)

    # Confirm Password
    tk.Label(login_window, text="Confirm Password:          ", font=("Arial", 14), bg="#ffffff", fg="black").pack(pady=5)
    confirm_password_entry = tk.Entry(login_window, font=("Arial", 14), show="*")
    confirm_password_entry.pack(pady=5)

    # Name 
    tk.Label(login_window, text="Name:                              ", font=("Arial", 14), bg="#ffffff", fg="black").pack(pady=5)
    name_entry = tk.Entry(login_window, font=("Arial", 14))
    name_entry.pack(pady=5)

    # Phone
    tk.Label(login_window, text="Phone No:                        ", font=("Arial", 14), bg="#ffffff", fg="black").pack(pady=5)
    phone_entry = tk.Entry(login_window, font=("Arial", 14))
    phone_entry.pack(pady=5)

    # Email
    tk.Label(login_window, text="Email ID:                          ", font=("Arial", 14), bg="#ffffff", fg="black").pack(pady=5)
    email_entry = tk.Entry(login_window, font=("Arial", 14))
    email_entry.pack(pady=5)

    # Driving License
    tk.Label(login_window, text="Driving License No:          ", font=("Arial", 14), bg="#ffffff", fg="black").pack(pady=5)
    dl_entry = tk.Entry(login_window, font=("Arial", 14))
    dl_entry.pack(pady=5)

    # Vehicle Number
    tk.Label(login_window, text="Vehicle Number:              ", font=("Arial", 14), bg="#ffffff", fg="black").pack(pady=5)
    vehicle_entry = tk.Entry(login_window, font=("Arial", 14))
    vehicle_entry.pack(pady=5)

    # Submit Button
    submit_button = tk.Button(login_window, text="Submit", font=("Arial", 14, "bold"), bg="#2980B9", fg="white", relief="raised", width=15, height=2,
                              command=lambda: submit_signup(
                                  username_entry_signup.get(), password_entry_signup.get(), confirm_password_entry.get(),
                                  name_entry.get(), phone_entry.get(), email_entry.get(), dl_entry.get(), vehicle_entry.get()
                              ))
    submit_button.pack(pady=20)

    # Back to Login Button
    back_button = tk.Button(login_window, text="Back to Login", font=("Arial", 12), bg="#34495E", fg="white", 
                            command=reset_to_login)
    back_button.pack(pady=10)

# Reset to Login Screen
def reset_to_login():
    for widget in login_window.winfo_children():
        widget.destroy()
    
    login_window.title("Login")

    # Title Label
    tk.Label(login_window, text="Login", font=("Helvetica", 24, "bold"), fg="white", bg="#2C3E50").pack(pady=20)

    # Username
    tk.Label(login_window, text="Username:", font=("Arial", 14), bg="#2C3E50", fg="white").pack(pady=5)
    global username_entry
    username_entry = tk.Entry(login_window, font=("Arial", 14))
    username_entry.pack(pady=5)

    # Password
    tk.Label(login_window, text="Password:", font=("Arial", 14), bg="#2C3E50", fg="white").pack(pady=5)
    global password_entry
    password_entry = tk.Entry(login_window, font=("Arial", 14), show="*")
    password_entry.pack(pady=5)

    # Login Button
    tk.Button(login_window, text="Login", font=("Arial", 14, "bold"), bg="#2980B9", fg="white", relief="raised", width=15, height=2, command=user_login).pack(pady=10)

    # Signup Button
    tk.Button(login_window, text="Signup", font=("Arial", 14, "bold"), bg="#2980B9", fg="white", relief="raised", width=15, height=2, command=signup).pack(pady=5)

    # Additional text below Signup button
    tk.Label(login_window, text="New to ParkWatch? Sign up now!", font=("Arial", 12), fg="white", bg="#2C3E50").pack(pady=10)


# Function to handle signup submission
def submit_signup(username, password, confirm_password, name, phone, email, dl_number, vehicle_number):
    # Validate inputs
    errors = []
    
    if username == "" or password == "" or confirm_password == "" or name == "" or phone == "" or email == "" or dl_number == "" or vehicle_number == "":
        errors.append("Please fill in all fields.")
    
    if password != confirm_password:
        errors.append("Passwords do not match.")
    
    if not validate_email(email):
        errors.append("Please enter a valid email address.")
        
    if not validate_phone(phone):
        errors.append("Please enter a valid 10-digit phone number.")
    
    if not validate_vehicle_number(vehicle_number):
        errors.append("Please enter a valid vehicle registration number (e.g., MH 01 AB 1234).")
    
    if errors:
        show_custom_error("Validation Error", "\n".join(errors))
        return

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            show_custom_error("Registration Error", "Username already exists. Please choose a different username.")
            conn.close()
            return
        
        try:
            cursor.execute("""
                INSERT INTO users (username, name, password, phone, email, driving_license, vehicle_number) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (username, name, password, phone, email, dl_number, vehicle_number.upper()))
            conn.commit()
            show_custom_success("Registration Success", f"Account created for {username}! You can now log in.")
            reset_to_login()
        except mysql.connector.Error as err:
            show_custom_error("Database Error", f"Failed to register: {err}")
        finally:
            conn.close()

# Reset to Login Screen
def reset_to_login():
    for widget in login_window.winfo_children():
        widget.destroy()
    
    login_window.title("ParkWatch - Smart Parking Management")

    # Main frame
    main_frame = tk.Frame(login_window, bg=COLORS["background"], padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)
    
    # Card container - holds the white card
    card_frame = tk.Frame(main_frame, bg=COLORS["card"], padx=40, pady=30)
    card_frame.pack(fill="both", expand=True)
    
    # Header frame - now fully centered with logo and title
    header_frame = tk.Frame(card_frame, bg=COLORS["card"])
    header_frame.pack(fill="x", pady=10)
    
    # Center container for header elements
    header_center = tk.Frame(header_frame, bg=COLORS["card"])
    header_center.pack(anchor="center")
    
    # Try to load the logo - centered above the title
    try:
        logo_image = tk.PhotoImage(file="parking_logo.png")
        logo_image = logo_image.subsample(8, 8)  # Adjust logo size
        logo_label = tk.Label(header_center, image=logo_image, bg=COLORS["card"])
        logo_label.image = logo_image  # Keep a reference
        logo_label.pack(pady=(0, 10))
    except Exception as e:
        print(f"Error loading logo: {e}")
    
    # Title and subtitle, now centered
    title_frame = tk.Frame(header_center, bg=COLORS["card"])
    title_frame.pack()
    
    tk.Label(title_frame, text="ParkWatch", font=("Helvetica", 28, "bold"), 
             fg=COLORS["primary"], bg=COLORS["card"]).pack(anchor="center")
    
    tk.Label(title_frame, text="Smart Parking Management System", 
             font=("Helvetica", 14), fg=COLORS["text_secondary"], 
             bg=COLORS["card"]).pack(pady=(5, 0), anchor="center")
    
    # Divider
    divider = tk.Frame(card_frame, height=1, bg=COLORS["text_secondary"])
    divider.pack(fill="x", pady=20)
    
    # Login form frame - center aligned with fixed width
    form_container = tk.Frame(card_frame, bg=COLORS["card"])
    form_container.pack()
    
    login_form = tk.Frame(form_container, bg=COLORS["card"], width=400)
    login_form.pack()
    
    # Form title
    tk.Label(login_form, text="Sign In", font=("Helvetica", 18, "bold"), 
             fg=COLORS["text_primary"], bg=COLORS["card"]).pack(pady=(0, 20))
    
    # Username entry
    global username_entry
    username_entry = create_styled_entry(login_form, "Username", icon="👤")
    
    # Password entry
    global password_entry
    password_entry = create_styled_entry(login_form, "Password", show_char="*", icon="🔒")
    
    # Buttons frame
    buttons_frame = tk.Frame(login_form, bg=COLORS["card"])
    buttons_frame.pack(pady=20)
    
    # User Login button
    user_login_btn = create_styled_button(buttons_frame, "User  Login", user_login, COLORS["secondary"], icon="👤")
    
    # Admin Login button
    admin_login_btn = create_styled_button(buttons_frame, "Admin Login", admin_login, COLORS["accent"], icon="👑")
    
    # Divider
    divider2 = tk.Frame(card_frame, height=1, bg=COLORS["text_secondary"])
    divider2.pack(fill="x", pady=10)
    
    # Footer with signup option
    footer_frame = tk.Frame(card_frame, bg=COLORS["card"])
    footer_frame.pack(fill="x", pady=10)
    
    tk.Label(footer_frame, text="New to ParkWatch?", 
             font=("Helvetica", 12), fg=COLORS["text_secondary"], 
             bg=COLORS["card"]).pack(pady=(0, 10))
    
    # Signup button
    signup_btn = create_styled_button(footer_frame, "Create New Account", signup, COLORS["success"])

# Create Login Window
login_window = tk.Tk()
login_window.title("ParkWatch - Smart Parking Management")
login_window.configure(bg=COLORS["background"])

# Set window size and center it
window_width = 700
window_height = 800
center_window(login_window, window_width, window_height)

# Set window icon
try:
    login_window.iconphoto(True, tk.PhotoImage(file="parking_logo.png"))
except Exception as e:
    print(f"Error loading icon: {e}")

# Initialize with login screen
reset_to_login()

# Start the Tkinter event loop
login_window.mainloop()