import tkinter as tk
from tkinter import ttk, messagebox
from src.constants import COLORS

class NavigationPane:
    def __init__(self, parent, show_frame_callback):
        self.frame = ttk.Frame(parent, style='Navigation.TFrame')
        self.show_frame = show_frame_callback
        
        # Add methods to be dynamically replaced by main app
        self.create_donation_history = None
        self.logout_callback = None
        
        # Configure navigation frame style
        style = ttk.Style(parent)
        style.configure('Navigation.TFrame', 
                       background=COLORS['primary'],
                       relief='flat')
        
        # Logo section
        logo_frame = ttk.Frame(self.frame, style='Navigation.TFrame')
        logo_frame.pack(fill='x', pady=(20, 40))
        ttk.Label(logo_frame, 
                 text="🎁", 
                 font=('Segoe UI', 32),
                 background=COLORS['primary'],
                 foreground='white').pack()
        ttk.Label(logo_frame, 
                 text="CrowdNest", 
                 font=('Segoe UI', 16, 'bold'),
                 background=COLORS['primary'],
                 foreground='white').pack()
        
        # Navigation buttons
        nav_buttons = [
            {"text": "🏠 Dashboard", "command": lambda: self.show_frame('DashboardPage')},
            {"text": "🎁 Browse Donations", "command": lambda: self.show_frame('DonationListPage')},
            {"text": "➕ Create Donation", "command": lambda: self.show_frame('DonationFormPage')},
            {"text": "📜 Donation History", "command": lambda: self.show_frame('DonationHistoryPage')},
            {"text": "📋 Request List", "command": lambda: self.show_frame('RequestListPage')},
            {"text": "📝 Accepted Requests", "command": lambda: self.show_frame('AcceptedRequestsPage')},
            {"text": "👤 Profile", "command": lambda: self.show_frame('ProfilePage')}
        ]
        
        # Create navigation buttons
        for button_info in nav_buttons:
            button = ttk.Button(
                self.frame, 
                text=button_info['text'], 
                command=button_info['command'], 
                style='Navigation.TButton'
            )
            button.pack(fill='x', padx=10, pady=5)
        
        # Logout button
        logout_button = ttk.Button(
            self.frame, 
            text="🚪 Logout", 
            command=self.perform_logout, 
            style='Logout.TButton'
        )
        logout_button.pack(fill='x', padx=10, pady=(20, 10), side='bottom')
    
    def open_donation_history(self):
        """Open donation history popup"""
        # Directly call the method to create donation history page
        # This assumes the main app has set up the method correctly
        if hasattr(self.show_frame, '__self__'):
            # This is a method bound to an instance
            app_instance = self.show_frame.__self__
            if hasattr(app_instance, 'create_donation_history_page'):
                app_instance.create_donation_history_page()
            else:
                messagebox.showinfo("Info", "Donation history feature not available")
        else:
            messagebox.showinfo("Info", "Donation history feature not available")
    
    def perform_logout(self):
        """Perform logout"""
        self.logout_callback()
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
        
    def pack_forget(self):
        self.frame.pack_forget()
    
    def update_user_info(self, user_info):
        """Update navigation pane with user information"""
        # Store user info for reference
        self.user_info = user_info
        
        # Update any user-specific navigation elements if needed
        # This method ensures the navigation pane reflects the current user's state
        pass