import tkinter as tk
from tkinter import ttk

def create_placeholder_svg():
    """Create a placeholder SVG image for donations without images"""
    return '''
    <svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
        <rect width="400" height="400" fill="#f0f0f0"/>
        <text x="200" y="180" font-family="Arial" font-size="24" fill="#666666" text-anchor="middle">No Image</text>
        <text x="200" y="220" font-family="Arial" font-size="16" fill="#999999" text-anchor="middle">Available</text>
        <path d="M160 140 h80 v80 h-80 z" fill="none" stroke="#999999" stroke-width="4"/>
        <path d="M170 180 l20 -20 l40 40" fill="none" stroke="#999999" stroke-width="4"/>
        <circle cx="200" cy="160" r="8" fill="#999999"/>
    </svg>
    '''

def show_placeholder_image(frame):
    """Display a placeholder image in the given frame"""
    # Create a label with placeholder text and styling
    placeholder_label = ttk.Label(
        frame,
        text="No Image\nAvailable",
        justify=tk.CENTER,
        font=('Segoe UI', 14)
    )
    
    # Create a frame for the icon
    icon_frame = ttk.Frame(frame, style='PlaceholderIcon.TFrame')
    
    # Position the elements
    placeholder_label.place(relx=0.5, rely=0.6, anchor='center')
    icon_frame.place(relx=0.5, rely=0.4, anchor='center', width=80, height=80)
    
    # Style the frame with a border
    frame.configure(style='Placeholder.TFrame')
    
    # Create styles if they don't exist
    style = ttk.Style()
    if 'Placeholder.TFrame' not in style.theme_names():
        style.configure('Placeholder.TFrame', background='#f0f0f0')
    if 'PlaceholderIcon.TFrame' not in style.theme_names():
        style.configure('PlaceholderIcon.TFrame', background='#999999')