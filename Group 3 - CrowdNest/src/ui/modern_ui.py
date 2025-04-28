import tkinter as tk
from tkinter import ttk
from src.constants import COLORS, STATES

class ModernUI:
    @staticmethod
    def setup_styles():
        """Setup modern UI styles"""
        style = ttk.Style()
        
        # Card style
        style.configure('Card.TFrame',
                       background=COLORS['card'],
                       relief='flat')
                       
        style.configure('Card.TLabel',
                       background=COLORS['card'],
                       foreground=COLORS['text'])
                       
        # Title styles
        style.configure('Title.TLabel',
                       background=COLORS['card'],
                       foreground=COLORS['text'],
                       font=('Segoe UI', 24, 'bold'))
                       
        style.configure('Subtitle.TLabel',
                       background=COLORS['card'],
                       foreground=COLORS['text_light'],
                       font=('Segoe UI', 12))
                       
        # Badge styles
        style.configure('StatusBadge.TLabel',
                       background=COLORS['success'],
                       foreground='white',
                       padding=(10, 5),
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat')
                       
        style.configure('CategoryBadge.TLabel',
                       background=COLORS['accent'],
                       foreground='white',
                       padding=(10, 5),
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat')
                       
        style.configure('ConditionBadge.TLabel',
                       background=COLORS['warning'],
                       foreground=COLORS['text'],
                       padding=(10, 5),
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat')
                       
        # Button styles
        style.configure('TButton',
                       background=COLORS['primary'],
                       foreground=COLORS['text'],
                       padding=(10, 5),
                       font=('Segoe UI', 10))
                       
        style.configure('Secondary.TButton',
                       background=COLORS['text_light'],
                       foreground=COLORS['text'])
                       
        # Entry styles
        style.configure('TEntry',
                       fieldbackground='white',
                       foreground=COLORS['text'],
                       insertcolor=COLORS['text'])
                       
        # Combobox styles
        style.configure('TCombobox',
                       fieldbackground='white',
                       background='white',
                       foreground=COLORS['text'],
                       selectbackground=COLORS['primary'],
                       selectforeground='white')
                       
        style.map('TCombobox',
                 fieldbackground=[('readonly', 'white')],
                 selectbackground=[('readonly', COLORS['primary'])],
                 foreground=[('readonly', COLORS['text'])])
        
        # Treeview style
        style.configure('Treeview',
                       background=COLORS['card'],
                       foreground=COLORS['text'],
                       fieldbackground=COLORS['card'])
                       
        style.configure('Treeview.Heading',
                       background=COLORS['primary'],
                       foreground='white',
                       relief='flat')
                       
        style.map('Treeview.Heading',
                 background=[('active', COLORS['accent'])])
    
    @staticmethod
    def create_card(parent, **kwargs):
        """Create a card-like frame"""
        frame = ttk.Frame(parent, style='Card.TFrame', **kwargs)
        return frame
    
    @staticmethod
    def create_button(parent, text, command=None, style='TButton', **kwargs):
        """Create a modern button"""
        btn = ttk.Button(parent,
                        text=text,
                        command=command,
                        style=style,
                        cursor='hand2',
                        **kwargs)
        return btn
    
    @staticmethod
    def create_entry(parent, placeholder, **kwargs):
        """Create a modern entry with placeholder"""
        entry = ttk.Entry(parent, style='TEntry', **kwargs)
        
        if placeholder:
            entry.insert(0, placeholder)
            entry.bind('<FocusIn>', lambda e: ModernUI._on_entry_focus_in(e, placeholder))
            entry.bind('<FocusOut>', lambda e: ModernUI._on_entry_focus_out(e, placeholder))
        
        return entry
    
    @staticmethod
    def _on_entry_focus_in(event, placeholder):
        """Handle entry focus in"""
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)
            event.widget.configure(foreground=COLORS['text'])
    
    @staticmethod
    def _on_entry_focus_out(event, placeholder):
        """Handle entry focus out"""
        if not event.widget.get():
            event.widget.insert(0, placeholder)
            event.widget.configure(foreground=COLORS['text_light'])

    @staticmethod
    def create_dropdown(parent, values, placeholder=None, textvariable=None, **kwargs):
        """Create a modern dropdown with optional placeholder"""
        if textvariable is None:
            textvariable = tk.StringVar()
        
        combo = ttk.Combobox(
            parent,
            values=values,
            textvariable=textvariable,
            state='readonly',
            font=('Poppins', 10),
            foreground='#1B1B1E',
            background='#FFFFFF',
            **kwargs
        )
        
        if placeholder:
            combo.set(placeholder)
        
        return combo

    @staticmethod
    def create_location_selector(parent, state_var, city_var, states_dict=None):
        """Create a location selector with state and city dropdowns
        
        :param parent: Parent widget
        :param state_var: Tkinter StringVar for state selection
        :param city_var: Tkinter StringVar for city selection
        :param states_dict: Optional dictionary of states and cities. 
                            If not provided, uses the default STATES from constants
        """
        frame = ttk.Frame(parent, style='Card.TFrame')
        
        # Use provided states_dict or default STATES
        locations = states_dict or STATES
        
        # Create state dropdown
        state_frame = ttk.Frame(frame, style='Card.TFrame')
        state_frame.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        state_dropdown = ModernUI.create_dropdown(
            state_frame,
            list(locations.keys()),
            "Select State",
            state_var
        )
        state_dropdown.pack(fill='x')
        
        # Create city dropdown
        city_frame = ttk.Frame(frame, style='Card.TFrame')
        city_frame.pack(side='left', fill='x', expand=True, padx=(5, 0))
        
        city_dropdown = ModernUI.create_dropdown(
            city_frame,
            [],
            "Select City",
            city_var
        )
        city_dropdown.pack(fill='x')
        
        def update_cities(*args):
            state = state_var.get()
            cities = locations.get(state, [])
            city_var.set('')  # Reset city selection
            city_dropdown['values'] = cities
            if cities:
                city_dropdown.set("Select City")
        
        state_var.trace('w', update_cities)
        return frame
