import tkinter as tk
from tkinter import ttk, messagebox, font
from PIL import Image, ImageTk, ImageDraw, ImageFont
import mysql.connector
import os
from datetime import datetime

class ProfileWindow:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        
        # Colors - Using a more consistent color scheme
        self.primary_color = "#1e88e5"
        self.accent_color = "#4CAF50"
        self.danger_color = "#f44336"
        self.text_color = "#212121"
        self.light_bg = "#f5f5f5"
        self.highlight_color = "#e3f2fd"
        
        # Use the provided root window instead of creating a new one
        self.profile_window = self.root
        self.profile_window.title("Read Rover - User Profile")
        self.profile_window.geometry("800x650")
        self.profile_window.configure(bg=self.light_bg)
        self.profile_window.resizable(True, True)
        
        # Center window
        self.center_window(self.profile_window, 800, 650)
        
        # Try to set icon if available
        try:
            self.profile_window.iconbitmap("book_icon.ico")
        except:
            pass
            
        # Create custom fonts
        self.title_font = font.Font(family='Helvetica', size=22, weight='bold')
        self.section_font = font.Font(family='Helvetica', size=16, weight='bold')
        self.label_font = font.Font(family='Helvetica', size=12)
        self.info_font = font.Font(family='Helvetica', size=12)
        self.button_font = font.Font(family='Helvetica', size=11, weight='bold')
        
        # Improved scrollable main container
        self.main_container = tk.Frame(self.profile_window, bg=self.light_bg)
        self.main_container.pack(fill="both", expand=True)
        
        # Add a canvas with scrollbar for responsive content
        self.canvas = tk.Canvas(self.main_container, bg=self.light_bg, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Main frame inside canvas
        self.main_frame = tk.Frame(self.canvas, bg=self.light_bg, padx=40, pady=30)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Configure canvas scrolling - Fixed mousewheel binding for cross-platform
        self.main_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Cross-platform scroll binding
        self.bind_mousewheel(self.profile_window)
        
        # Fetch user data
        self.user_info = self.fetch_user_info()
        
        # Create the UI components
        self.create_header()
        self.create_profile_info()
        self.create_password_change()
        self.create_action_section()
        self.create_footer()
    
    def center_window(self, window, width, height):
        """Center a window on the screen"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def bind_mousewheel(self, widget):
        """Cross-platform mousewheel binding"""
        widget.bind("<MouseWheel>", self.on_mousewheel)  # Windows
        widget.bind("<Button-4>", self.on_mousewheel)    # Linux scroll up
        widget.bind("<Button-5>", self.on_mousewheel)    # Linux scroll down
    
    def on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event=None):
        """Make the inner frame the same width as the canvas"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def on_mousewheel(self, event):
        """Cross-platform mousewheel handler"""
        if hasattr(event, 'delta'):  # Windows
            delta = -event.delta // 120
        elif event.num == 5:  # Linux scroll down
            delta = 1
        elif event.num == 4:  # Linux scroll up
            delta = -1
        else:
            return
        self.canvas.yview_scroll(delta, "units")
    
    def create_header(self):
        """Create the header section with user avatar and welcome message"""
        header_frame = tk.Frame(self.main_frame, bg=self.light_bg, pady=15)
        header_frame.pack(fill="x")
        
        # Avatar frame - Left side
        avatar_frame = tk.Frame(header_frame, bg=self.light_bg)
        avatar_frame.pack(side=tk.LEFT, padx=20)
        
        # Create circular avatar
        try:
            avatar_img = Image.open("user_avatar.png")
            avatar_img = avatar_img.resize((120, 120), Image.LANCZOS)
        except:
            # Create default avatar with initials
            avatar_img = self.create_initial_avatar(self.user_info.get("Username", "User"))
        
        self.avatar = ImageTk.PhotoImage(avatar_img)
        avatar_label = tk.Label(avatar_frame, image=self.avatar, bg=self.light_bg)
        avatar_label.pack(pady=10)
        
        # Welcome message - Right side
        welcome_frame = tk.Frame(header_frame, bg=self.light_bg)
        welcome_frame.pack(side=tk.LEFT, padx=20, fill="x", expand=True)
        
        welcome_text = f"Welcome, {self.user_info.get('Username', 'Reader')}!"
        welcome_label = tk.Label(welcome_frame, text=welcome_text, font=self.title_font, 
                               fg=self.primary_color, bg=self.light_bg, anchor="w")
        welcome_label.pack(fill="x", pady=5)
        
        joined_date = self.user_info.get('JoinDate', datetime.now().strftime("%B %d, %Y"))
        member_label = tk.Label(welcome_frame, text=f"Member since: {joined_date}", 
                              font=self.label_font, fg=self.text_color, bg=self.light_bg, anchor="w")
        member_label.pack(fill="x")
        
        # Status indicator
        status_frame = tk.Frame(welcome_frame, bg=self.light_bg, pady=10)
        status_frame.pack(fill="x", anchor="w")
        
        status_indicator = tk.Canvas(status_frame, width=12, height=12, bg=self.light_bg, 
                                   highlightthickness=0)
        status_indicator.create_oval(2, 2, 10, 10, fill="#4CAF50", outline="")
        status_indicator.pack(side=tk.LEFT)
        
        status_label = tk.Label(status_frame, text="Online", font=font.Font(size=10), 
                              fg="#4CAF50", bg=self.light_bg)
        status_label.pack(side=tk.LEFT, padx=5)
    
    def create_section_container(self, title):
        """Helper to create consistently styled section containers"""
        container = tk.Frame(self.main_frame, bg="white", bd=1, relief="solid", padx=25, pady=20)
        container.pack(fill="x", pady=15)
        
        # Section title
        title_frame = tk.Frame(container, bg="white")
        title_frame.pack(fill="x", anchor="w")
        
        section_label = tk.Label(title_frame, text=title, 
                               font=self.section_font, fg=self.primary_color, bg="white")
        section_label.pack(side=tk.LEFT, anchor="w", pady=(0, 10))
        
        # Separator
        separator = ttk.Separator(container, orient="horizontal")
        separator.pack(fill="x", pady=10)
        
        return container
    
    def create_profile_info(self):
        """Create the profile information section"""
        info_container = self.create_section_container("Personal Information")
        
        # Profile details in a grid
        details_frame = tk.Frame(info_container, bg="white", pady=15)
        details_frame.pack(fill="x")
        
        # User information fields
        fields = [
            ("Username", self.user_info.get("Username", "N/A")),
            ("Email", self.user_info.get("Email", "N/A")),
            ("Preferred Genre", self.user_info.get("PreferredGenre", "N/A"))
        ]
        
        # Create grid of labels with improved styling
        for i, (field, value) in enumerate(fields):
            field_label = tk.Label(details_frame, text=f"{field}:", font=self.label_font, 
                                 fg=self.text_color, bg="white", anchor="e")
            field_label.grid(row=i, column=0, sticky="e", padx=(0, 20), pady=12)
            
            value_frame = tk.Frame(details_frame, bg=self.highlight_color, padx=15, pady=8, bd=1, relief="solid")
            value_frame.grid(row=i, column=1, sticky="w", pady=12)
            
            value_label = tk.Label(value_frame, text=value, font=self.info_font, 
                                 fg=self.primary_color, bg=self.highlight_color, anchor="w")
            value_label.pack()
        
        # Configure grid weights
        details_frame.grid_columnconfigure(0, weight=1, minsize=150)
        details_frame.grid_columnconfigure(1, weight=2)
        
        # Edit profile button
        edit_button = tk.Button(info_container, text="✏️ Edit Profile", font=self.button_font,
                             bg=self.primary_color, fg="white", padx=15, pady=8,
                             activebackground="#1565C0", cursor="hand2",
                             command=self.edit_profile)
        edit_button.pack(anchor="e", pady=(15, 5))
    
    def create_password_change(self):
        """Create password change section"""
        password_container = self.create_section_container("Change Password")
        
        # Password change form
        form_frame = tk.Frame(password_container, bg="white", pady=15)
        form_frame.pack(fill="x")
        
        # Entry style dictionary
        entry_style = {"font": self.info_font, "bd": 1, "relief": "solid", "width": 25, 
                      "bg": self.highlight_color, "insertbackground": self.primary_color, "show": "•"}
        
        # Field labels and entries
        fields = [
            ("Current Password:", "current_pw_entry"),
            ("New Password:", "new_pw_entry"),
            ("Confirm New Password:", "confirm_pw_entry")
        ]
        
        for i, (label_text, entry_name) in enumerate(fields):
            label = tk.Label(form_frame, text=label_text, 
                           font=self.label_font, fg=self.text_color, bg="white", anchor="e")
            label.grid(row=i, column=0, sticky="e", padx=(0, 20), pady=12)
            
            entry = tk.Entry(form_frame, **entry_style)
            entry.grid(row=i, column=1, sticky="w", pady=12, ipady=5)
            setattr(self, entry_name, entry)  # Set as class attribute
        
        # Password requirements hint
        hint_text = "Password must be at least 8 characters long and include uppercase, lowercase, and numbers"
        hint_label = tk.Label(form_frame, text=hint_text, font=font.Font(size=9, slant="italic"),
                            fg="#757575", bg="white")
        hint_label.grid(row=3, column=1, sticky="w", pady=(0, 15))
        
        # Update button with icon
        update_button = tk.Button(form_frame, text="🔄 Update Password", font=self.button_font,
                                bg=self.primary_color, fg="white", padx=15, pady=8,
                                activebackground="#1565C0", cursor="hand2",
                                command=self.update_password)
        update_button.grid(row=4, column=1, sticky="w", pady=15)
        
        # Configure grid weights
        form_frame.grid_columnconfigure(0, weight=1, minsize=150)
        form_frame.grid_columnconfigure(1, weight=2)
    
    def create_action_section(self):
        """Create combined action section with help, settings and logout"""
        action_container = self.create_section_container("Account Actions")
        
        # Button frame for Help and Settings
        util_buttons_frame = tk.Frame(action_container, bg="white", pady=10)
        util_buttons_frame.pack(fill="x")
        
        # Helper to create styled buttons
        def create_button(parent, text, bg_color, command):
            return tk.Button(parent, text=text, font=self.button_font,
                          bg=bg_color, fg="white", padx=15, pady=8,
                          activebackground="#757575", cursor="hand2", command=command)
        
        # Help button
        help_button = create_button(
            util_buttons_frame, 
            "❓ Help & Support", 
            "#9E9E9E",
            lambda: messagebox.showinfo("Help", "Need assistance? Contact us at support@readrover.com")
        )
        help_button.pack(side=tk.LEFT, padx=5)
        
        # App settings button
        settings_button = create_button(
            util_buttons_frame, 
            "⚙️ App Settings", 
            "#9E9E9E",
            lambda: messagebox.showinfo("Settings", "App settings feature coming soon!")
        )
        settings_button.pack(side=tk.LEFT, padx=5)
        
        # Separator
        separator = ttk.Separator(action_container, orient="horizontal")
        separator.pack(fill="x", pady=15)
        
        # Logout section
        logout_frame = tk.Frame(action_container, bg="white", pady=10)
        logout_frame.pack(fill="x", pady=5)
        
        # Description
        logout_desc = tk.Label(logout_frame, 
                             text="Sign out from your account. You'll need to enter your credentials next time.",
                             font=self.label_font, fg=self.text_color, bg="white", anchor="w", justify="left")
        logout_desc.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        
        # Logout button with warning color and icon
        logout_button = create_button(
            logout_frame, 
            "🚪 Logout", 
            self.danger_color,
            self.logout
        )
        logout_button.configure(activebackground="#d32f2f", padx=20, pady=10)
        logout_button.pack(side=tk.RIGHT, padx=10)
    
    def create_footer(self):
        """Create footer with copyright information"""
        footer_frame = tk.Frame(self.main_frame, bg=self.light_bg, pady=10)
        footer_frame.pack(fill="x", side=tk.BOTTOM, pady=15)
        
        # App version
        version_label = tk.Label(footer_frame, text="Version 2.1.3", font=font.Font(size=9),
                               fg="#757575", bg=self.light_bg)
        version_label.pack(side=tk.LEFT)
        
        # Copyright
        footer_text = "© 2025 Read Rover. All rights reserved."
        footer_label = tk.Label(footer_frame, text=footer_text, font=font.Font(size=9),
                              fg="#757575", bg=self.light_bg)
        footer_label.pack(side=tk.RIGHT)
    
    def create_initial_avatar(self, username):
        """Create a circular avatar with user's initials - Fixed potential errors"""
        # Create a blank image with a blue background
        img = Image.new('RGB', (120, 120), self.primary_color)
        draw = ImageDraw.Draw(img)
        
        # Draw a circle
        draw.ellipse((0, 0, 120, 120), fill=self.primary_color)
        
        # Add text (initials)
        font_size = 48
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = None
            
        # Get initials - Improved with safer processing
        initials = "U"
        if username and isinstance(username, str):
            parts = username.strip().split()
            if parts:
                initials = parts[0][0].upper()
                if len(parts) > 1 and parts[1]:
                    initials += parts[1][0].upper()
        
        # Calculate text position for centering
        text_width, text_height = font_size, font_size
        
        try:
            if font:
                # Try newer Pillow versions first
                try:
                    left, top, right, bottom = draw.textbbox((0, 0), initials, font=font)
                    text_width = right - left
                    text_height = bottom - top
                except (AttributeError, TypeError):
                    # Fallback for older Pillow versions
                    text_width, text_height = draw.textsize(initials, font=font)
        except Exception:
            # If all fails, use reasonable defaults
            pass
            
        position = ((120 - text_width) // 2, (120 - text_height) // 2)
        
        # Draw the text
        draw.text(position, initials, fill="white", font=font)
        
        return img
    
    def fetch_user_info(self):
        """Fetch user information from the database with better error handling"""
        try:
            connection = self.create_connection()
            if connection:
                try:
                    cursor = connection.cursor(dictionary=True)
                    query = "SELECT * FROM users WHERE id = %s"
                    cursor.execute(query, (self.user_id,))
                    user_data = cursor.fetchone()
                    cursor.close()
                    connection.close()
                    
                    if user_data:
                        return {
                            "Username": user_data.get("username", "Unknown"),
                            "Email": user_data.get("email", "N/A"),
                            "PreferredGenre": user_data.get("preferred_genre", "Not specified"),
                            "JoinDate": user_data.get("created_at", datetime.now().strftime("%B %d, %Y"))
                        }
                except mysql.connector.Error as e:
                    print(f"Database query error: {e}")
        except Exception as e:
            print(f"Error fetching user data: {e}")
            
        # Fallback mock data
        return {
            "Username": "Simmi",
            "Email": "samx2708@gmail.com",
            "PreferredGenre": "Science Fiction & Fantasy",
            "JoinDate": "January 15, 2025"
        }
    
    def create_connection(self):
        """Create a database connection with improved error handling"""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='keera@13',
                database='bookstore',
                connection_timeout=5  # Added timeout to prevent hanging
            )
            if connection.is_connected():
                return connection
        except mysql.connector.Error as e:
            print(f"Database connection error: {e}")
            return None
    
    def edit_profile(self):
        """Open edit profile dialog"""
        messagebox.showinfo("Edit Profile", "Edit Profile feature coming soon!")
    
    def show_progress_window(self, title, message, callback):
        """Generic progress window for better UX"""
        progress_window = tk.Toplevel(self.profile_window)
        progress_window.title(title)
        progress_window.geometry("300x100")
        self.center_window(progress_window, 300, 100)
        progress_window.resizable(False, False)
        progress_window.configure(bg="white")
        progress_window.transient(self.profile_window)
        progress_window.grab_set()
        
        # Create a progress message
        message_label = tk.Label(progress_window, text=message, 
                               font=self.label_font, bg="white")
        message_label.pack(pady=(15, 10))
        
        # Create a progress bar
        progress = ttk.Progressbar(progress_window, orient="horizontal", length=250, mode="determinate")
        progress.pack(pady=5)
        
        # Start callback function
        callback(progress_window, progress)
        
        return progress_window
    
    def update_password(self):
        """Handle password update with improved validation"""
        current_password = self.current_pw_entry.get()
        new_password = self.new_pw_entry.get()
        confirm_password = self.confirm_pw_entry.get()
        
        # Basic validation
        if not current_password or not new_password or not confirm_password:
            messagebox.showerror("Error", "All fields are required!")
            return
            
        if new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match!")
            return
            
        if len(new_password) < 8:
            messagebox.showerror("Error", "Password should be at least 8 characters!")
            return
        
        # Password complexity check - at least one uppercase, lowercase and number
        if not (any(c.isupper() for c in new_password) and 
                any(c.islower() for c in new_password) and
                any(c.isdigit() for c in new_password)):
            messagebox.showerror("Error", "Password must include uppercase, lowercase, and numbers!")
            return
            
        # Simulate password update with progress window
        def update_progress(window, progress_bar):
            def step(val):
                progress_bar["value"] = val
                if val < 100:
                    window.after(50, step, val + 5)
                else:
                    window.destroy()
                    messagebox.showinfo("Success", "Password updated successfully!")
                    # Clear the password fields
                    self.current_pw_entry.delete(0, tk.END)
                    self.new_pw_entry.delete(0, tk.END)
                    self.confirm_pw_entry.delete(0, tk.END)
            
            window.after(100, step, 0)
        
        self.show_progress_window("Updating Password", "Updating your password...", update_progress)
    
    def logout(self):
        """Handle logout with improved user experience"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?", 
                             icon=messagebox.WARNING):
            
            # Show logout progress window
            def process_logout(window, progress_bar):
                progress_bar.config(mode="indeterminate")
                progress_bar.start(15)
                
                # Simulate a short delay before closing
                def finish():
                    window.destroy()
                    # Return to dashboard if we're coming from there
                    if hasattr(self.root, '_dashboard_return'):
                        self.root._dashboard_return()
                    else:
                        self.profile_window.destroy()
                        messagebox.showinfo("Logout", "You have been logged out successfully.")
                
                window.after(1500, finish)
            
            self.show_progress_window("Logging Out", "Logging you out...", process_logout)

# Test function
if __name__ == "__main__":
    root = tk.Tk()
    app = ProfileWindow(root, user_id=1)
    root.mainloop()