import tkinter as tk
from tkinter import ttk
from src.constants import COLORS, CITIES_BY_STATE

class ModernUI:
    @staticmethod
    def create_scrollable_frame(parent):
        # Create a canvas with vertical and horizontal scrollbars
        canvas = tk.Canvas(parent, bg=COLORS['card'], highlightthickness=0)
        scrollbar_y = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(parent, orient="horizontal", command=canvas.xview)

        # Create a frame inside the canvas
        scrollable_frame = ttk.Frame(canvas, style='Card.TFrame')
        
        # Update the scroll region when the frame changes size
        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", update_scroll_region)

        # Attach the frame to the canvas
        frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Configure scrolling
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Pack scrollbars and canvas
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)

        # Enable scrolling with the mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)  # For Windows
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # For Linux (scroll up)
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # For Linux (scroll down)

        return scrollable_frame, canvas

    @staticmethod
    def create_header(parent):
        header = ttk.Frame(parent, style='Header.TFrame')
        header.pack(fill='x', side='top')
        
        # App title
        title = ttk.Label(header, text="CrowdNest", style='HeaderTitle.TLabel')
        title.pack(side='left', padx=20, pady=10)
        
        return header

    @staticmethod
    def create_card(parent, padding=(20, 20)):
        card = ttk.Frame(parent, style='Card.TFrame')
        card.pack(fill='both', expand=True, padx=padding[0], pady=padding[1])
        return card

    @staticmethod
    def create_button(parent, text, command, style='Primary.TButton', width=None):
        if style == 'Primary.TButton':
            btn = tk.Button(parent, text=text, command=command,
                          bg=COLORS['primary'],
                          fg='white',
                          font=('Segoe UI', 10, 'bold'),
                          relief='flat',
                          activebackground=COLORS['primary_dark'],
                          activeforeground='white',
                          cursor='hand2')
        else:  # Secondary button
            btn = tk.Button(parent, text=text, command=command,
                          bg=COLORS['secondary'],
                          fg='white',
                          font=('Segoe UI', 10),
                          relief='flat',
                          activebackground=COLORS['error'],
                          activeforeground='white',
                          cursor='hand2')
        
        if width:
            btn.configure(width=width)
            
        # Add hover effect
        btn.bind('<Enter>', lambda e: btn.configure(bg=COLORS['primary_dark'] if style == 'Primary.TButton' else COLORS['error']))
        btn.bind('<Leave>', lambda e: btn.configure(bg=COLORS['primary'] if style == 'Primary.TButton' else COLORS['secondary']))
        
        return btn

    @staticmethod
    def create_entry(parent, placeholder="", show=None, width=30):
        entry = ttk.Entry(parent, style='Modern.TEntry', width=width)
        if show:
            entry.configure(show=show)
        entry.insert(0, placeholder)
        entry.bind('<FocusIn>', lambda e: entry.delete(0, 'end') if entry.get() == placeholder else None)
        entry.bind('<FocusOut>', lambda e: entry.insert(0, placeholder) if entry.get() == '' else None)
        return entry

    @staticmethod
    def create_dropdown(parent, values, placeholder="Select", width=37):
        combo = ttk.Combobox(parent, values=values, width=width, state='readonly')
        combo.set(placeholder)
        return combo

    @staticmethod
    def create_location_selector(parent, state_var, city_var):
        # Create frame for location selection
        location_frame = ttk.Frame(parent, style='Card.TFrame')
        
        # State dropdown
        state_label = ttk.Label(location_frame, text="📍 State", style='Subtitle.TLabel')
        state_label.pack(anchor='w')
        
        state_dropdown = ttk.Combobox(location_frame, textvariable=state_var, values=list(CITIES_BY_STATE.keys()), state='readonly', width=37)
        state_dropdown.pack(pady=(5, 10))
        state_dropdown.set("Select State")
        
        # City dropdown
        city_label = ttk.Label(location_frame, text="🏙️ City", style='Subtitle.TLabel')
        city_label.pack(anchor='w')
        
        city_dropdown = ttk.Combobox(location_frame, textvariable=city_var, state='readonly', width=37)
        city_dropdown.pack(pady=(5, 0))
        city_dropdown.set("Select City")
        
        # Update city dropdown when state changes
        def update_cities(*args):
            selected_state = state_var.get()
            if selected_state in CITIES_BY_STATE:
                cities = CITIES_BY_STATE[selected_state]
                city_dropdown['values'] = cities
                city_dropdown.set("Select City")
            else:
                city_dropdown['values'] = []
                city_dropdown.set("Select City")
        
        state_var.trace('w', update_cities)
        return location_frame