import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os

# Define colors once at the top
PRIMARY_COLOR = "#1E3D59"  # Dark blue
SECONDARY_COLOR = "#F5F0E1"  # Off-white/cream
ACCENT_COLOR = "#FF6E40"  # Orange
BUTTON_COLOR = "#2E86AB"  # Lighter blue
HOVER_COLOR = "#4FB0AE"  # Teal
TEXT_COLOR = "#FFFFFF"  # White
DARK_ACCENT = "#0D2137"  # Darker blue for contrast

def run_script(script_name):
    """Helper function to run another Python script"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, script_name)
    subprocess.Popen(["python", script_path])

def logout():
    """Handle logout"""
    root.destroy()
    messagebox.showinfo("Logout", "Successfully Logged Out!")
    run_script("Login&signup.py")

def location_selected(location):
    """Handle location selection"""
    root.destroy()
    script_name = "available_space.py" if location == "SHOPPING MALL" else "available_space1.py"
    run_script(script_name)

def go_back():
    """Handle back action"""
    root.destroy()
    run_script("Login&signup.py")

def set_hover_state(button, enter=True):
    """Set hover state for buttons"""
    button['background'] = HOVER_COLOR if enter else DARK_ACCENT

def update_card_color(card, loc_label, desc_label, enter=True):
    """Update card and its children colors"""
    color = HOVER_COLOR if enter else BUTTON_COLOR
    card.config(bg=color)
    loc_label.config(bg=color)
    desc_label.config(bg=color)

def on_resize(event):
    """Handle window resize"""
    # Update canvas size to match window
    canvas.config(width=event.width, height=event.height)
    # Redraw the gradient
    canvas.delete("gradient")
    draw_gradient(event.width, event.height)
    # Center the content frame
    canvas.coords(window_id, event.width/2, event.height/2)

def draw_gradient(width, height):
    """Draw gradient background"""
    for i in range(height):
        # Calculate color for this line based on position
        ratio = i / height
        r1, g1, b1 = int(PRIMARY_COLOR[1:3], 16), int(PRIMARY_COLOR[3:5], 16), int(PRIMARY_COLOR[5:7], 16)
        r2, g2, b2 = int(DARK_ACCENT[1:3], 16), int(DARK_ACCENT[3:5], 16), int(DARK_ACCENT[5:7], 16)
        
        r = int(r1 + ratio * (r2 - r1))
        g = int(g1 + ratio * (g2 - g1))
        b = int(b1 + ratio * (b2 - b1))
        
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, width, i, fill=color, tags="gradient")

# Create main window
root = tk.Tk()
root.title("ParkWatch Dashboard")
root.geometry("1000x700")
root.minsize(800, 600)


# Configure ttk style
style = ttk.Style()
style.theme_use('clam')
style.configure("TProgressbar", thickness=10, troughcolor=SECONDARY_COLOR, 
                background=ACCENT_COLOR, borderwidth=0)

# Create background canvas
canvas = tk.Canvas(root, highlightthickness=0, bg=PRIMARY_COLOR)
canvas.pack(fill="both", expand=True)
draw_gradient(1000, 700)
root.bind("<Configure>", on_resize)

# Main content frame
content_frame = tk.Frame(canvas, bg=PRIMARY_COLOR)
window_id = canvas.create_window(500, 350, window=content_frame, anchor="center")

# App header with logo
header_frame = tk.Frame(content_frame, bg=PRIMARY_COLOR)
header_frame.pack(pady=20, fill="x")

# Logo (simulated with text)
logo_label = tk.Label(header_frame, text="P", font=("Verdana", 24, "bold"), 
                     bg=ACCENT_COLOR, fg=SECONDARY_COLOR, width=2, height=1)
logo_label.grid(row=0, column=0, padx=10)

# Title next to logo
title_label = tk.Label(header_frame, text="PARKWATCH", 
                      font=("Montserrat", 24, "bold"), 
                      bg=PRIMARY_COLOR, fg=SECONDARY_COLOR)
title_label.grid(row=0, column=1)

# Welcome message
welcome_frame = tk.Frame(content_frame, bg=PRIMARY_COLOR)
welcome_frame.pack(pady=20)

welcome_label = tk.Label(welcome_frame, 
                        text="Welcome to Parkwatch", 
                        font=("Helvetica", 18, "bold"), 
                        bg=PRIMARY_COLOR, fg=SECONDARY_COLOR)
welcome_label.pack()

welcome_subtitle = tk.Label(welcome_frame, 
                           text="Find available parking spaces", 
                           font=("Helvetica", 12), 
                           bg=PRIMARY_COLOR, fg=SECONDARY_COLOR)
welcome_subtitle.pack(pady=5)

# Separator
separator = ttk.Separator(content_frame, orient='horizontal')
separator.pack(fill='x', padx=50, pady=10)

# Location Selection
location_title = tk.Label(content_frame, text="SELECT PARKING LOCATION", 
                         font=("Arial", 14, "bold"), 
                         bg=PRIMARY_COLOR, fg=ACCENT_COLOR)
location_title.pack(pady=10)

location_selection_frame = tk.Frame(content_frame, bg=PRIMARY_COLOR)
location_selection_frame.pack(pady=20)

# Create location cards
locations = [("SHOPPING MALL", "Find parking at the mall's garage"), 
             ("COLLEGE", "Locate spots around campus")]

for i, (location, description) in enumerate(locations):
    # Card frame
    card = tk.Frame(location_selection_frame, bg=BUTTON_COLOR, 
                   relief=tk.RAISED, bd=0, padx=15, pady=15)
    card.grid(row=0, column=i, padx=20, pady=10)
    
    # Location label
    loc_label = tk.Label(card, text=location, font=("Arial", 14, "bold"), 
                        bg=BUTTON_COLOR, fg=TEXT_COLOR)
    loc_label.pack(pady=5)
    
    # Description
    desc_label = tk.Label(card, text=description, font=("Arial", 10), 
                         bg=BUTTON_COLOR, fg=TEXT_COLOR, wraplength=150)
    desc_label.pack(pady=5)
    
    # Select button
    select_btn = tk.Button(card, text="SELECT", font=("Arial", 11, "bold"), 
                  bg=ACCENT_COLOR, fg=TEXT_COLOR, relief=tk.FLAT,
                  activebackground=HOVER_COLOR, activeforeground=TEXT_COLOR,
                  padx=20, pady=8, command=lambda loc=location: location_selected(loc))
    select_btn.pack(pady=10)
    
    # Button hover effects
    select_btn.bind("<Enter>", lambda e, btn=select_btn: btn.config(bg=HOVER_COLOR))
    select_btn.bind("<Leave>", lambda e, btn=select_btn: btn.config(bg=ACCENT_COLOR))
    
    # Make card clickable
    card.bind("<Button-1>", lambda e, loc=location: location_selected(loc))
    
    # Card hover effects - using lambda to capture the current loop variables
    card.bind("<Enter>", lambda e, c=card, l=loc_label, d=desc_label: 
              update_card_color(c, l, d, True))
    card.bind("<Leave>", lambda e, c=card, l=loc_label, d=desc_label: 
              update_card_color(c, l, d, False))

# Navigation buttons
back_frame = tk.Frame(content_frame, bg=PRIMARY_COLOR)
back_frame.pack(pady=20)

back_button = tk.Button(back_frame, text="← BACK TO LOGIN", font=("Arial", 12), 
                       bg=DARK_ACCENT, fg=TEXT_COLOR, 
                       relief=tk.FLAT, padx=15, pady=8,
                       command=go_back)
back_button.pack(side=tk.LEFT, padx=10)

logout_button = tk.Button(back_frame, text="LOGOUT", font=("Arial", 12), 
                         bg=DARK_ACCENT, fg=TEXT_COLOR, 
                         relief=tk.FLAT, padx=15, pady=8,
                         command=logout)
logout_button.pack(side=tk.LEFT, padx=10)

# Button hover effects
back_button.bind("<Enter>", lambda e: back_button.config(bg=ACCENT_COLOR))
back_button.bind("<Leave>", lambda e: back_button.config(bg=DARK_ACCENT))
logout_button.bind("<Enter>", lambda e: logout_button.config(bg=ACCENT_COLOR))
logout_button.bind("<Leave>", lambda e: logout_button.config(bg=DARK_ACCENT))

# Footer
footer_frame = tk.Frame(content_frame, bg=DARK_ACCENT, padx=20, pady=10)
footer_frame.pack(side="bottom", fill="x", pady=20)

footer_label = tk.Label(footer_frame, text="© 2025 ParkWatch. All rights reserved.", 
                       font=("Arial", 10), 
                       bg=DARK_ACCENT, fg=SECONDARY_COLOR)
footer_label.pack(side="left")

version_label = tk.Label(footer_frame, text="v2.0", 
                        font=("Arial", 10), 
                        bg=DARK_ACCENT, fg=SECONDARY_COLOR)
version_label.pack(side="right")

# Start the main event loop
root.mainloop()