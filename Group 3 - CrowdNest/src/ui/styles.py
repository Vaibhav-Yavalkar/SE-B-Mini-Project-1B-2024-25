import tkinter as tk
from tkinter import ttk
from src.constants import COLORS

class CustomStyle:
    @staticmethod
    def configure_styles():
        style = ttk.Style()
        
        # Configure main theme
        style.configure('.',
            background=COLORS['background'],
            foreground=COLORS['text'],
            font=('Segoe UI', 10)
        )
        
        # Header styles
        style.configure('Header.TFrame',
            background=COLORS['primary']
        )
        
        style.configure('HeaderTitle.TLabel',
            background=COLORS['primary'],
            foreground='white',
            font=('Segoe UI', 18, 'bold')
        )
        
        # Modern label styles
        style.configure('Title.TLabel',
            font=('Segoe UI', 28, 'bold'),
            foreground=COLORS['primary'],
            background=COLORS['card']
        )
        
        style.configure('Subtitle.TLabel',
            font=('Segoe UI', 14),
            foreground=COLORS['text_light'],
            background=COLORS['card']
        )
        
        # Modern entry style
        style.configure('Modern.TEntry',
            padding=(15, 10),
            font=('Segoe UI', 11)
        )
        
        # Modern frame styles
        style.configure('Card.TFrame',
            background=COLORS['card']
        )
        
        # Modern Treeview
        style.configure('Treeview',
            background=COLORS['card'],
            fieldbackground=COLORS['card'],
            foreground=COLORS['text'],
            font=('Segoe UI', 10),
            rowheight=40
        )
        style.configure('Treeview.Heading',
            background=COLORS['primary'],
            foreground='white',
            font=('Segoe UI', 10, 'bold')
        )
        
        # Add combobox style
        style.configure('TCombobox',
            background=COLORS['card'],
            foreground=COLORS['text'],
            fieldbackground=COLORS['card'],
            selectbackground=COLORS['primary'],
            selectforeground='white',
            padding=(15, 10),
            font=('Segoe UI', 11)
        )
        
        style.map('TCombobox',
            fieldbackground=[('readonly', COLORS['card'])],
            selectbackground=[('readonly', COLORS['primary'])]
        )