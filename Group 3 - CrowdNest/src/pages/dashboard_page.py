import tkinter as tk
from tkinter import ttk
from src.ui.modern_ui import ModernUI
from datetime import datetime

class DashboardPage:
    def __init__(self, parent, current_user=None, show_frame_callback=None):
        self.parent = parent
        self.show_frame = show_frame_callback
        self.current_user = current_user
        self.frame = None
        self.welcome_label = None
        self.notifications_frame = None
        self.frames = {}
        self.create_frame()
        
    def update_user_info(self, user_data):
        """Update the dashboard with current user information"""
        if user_data and self.welcome_label:
            # Handle user_data as tuple from database query
            if isinstance(user_data, tuple):
                # Assuming tuple order: unique_id, username, email, password_hash, location, total_donations, total_requests, total_messages
                username = user_data[1] if len(user_data) > 1 else 'User'
                total_donations = user_data[5] if len(user_data) > 5 else 0
                total_requests = user_data[6] if len(user_data) > 6 else 0
                total_messages = user_data[7] if len(user_data) > 7 else 0
            else:
                # Handle as dictionary for backward compatibility
                username = user_data.get('username', 'User')
                total_donations = user_data.get('total_donations', 0)
                total_requests = user_data.get('total_requests', 0)
                total_messages = user_data.get('total_messages', 0)
            
            welcome_text = f"{username}\n\nDonations: {total_donations} | Requests: {total_requests} | Messages: {total_messages}"
            self.welcome_label.configure(text=welcome_text)
            
            # Update notifications if the callback is available
            if hasattr(self, 'get_notifications_callback') and self.get_notifications_callback and hasattr(self, 'current_user') and self.current_user:
                self.update_notifications()
                
    def create_frame(self):
        self.frame = ModernUI.create_card(self.parent)
        
        # Create a scrollable canvas for the content
        canvas = tk.Canvas(self.frame, bg='#FFFFFF', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Card.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=800)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        
        # Welcome section
        welcome_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        welcome_frame.pack(fill='x', pady=(20, 30))
        
        ttk.Label(welcome_frame, text="Welcome Back!", style='Title.TLabel').pack()
        self.welcome_label = ttk.Label(welcome_frame, text="", style='Subtitle.TLabel')
        self.welcome_label.pack()
        
        # Quick Actions
        actions_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        actions_frame.pack(fill='x', padx=40, pady=20)
        
        ttk.Label(actions_frame, text="Quick Actions", style='Title.TLabel').pack(anchor='w', pady=(0, 10))
        
        buttons_frame = ttk.Frame(actions_frame, style='Card.TFrame')
        buttons_frame.pack(fill='x')
        
        quick_actions = [
            ("Donations", "DonationListPage", '🎁'),
            ("My Profile", "ProfilePage", '👤'),
            ("Logout", "LoginPage", '🚪')
        ]
        
        for text, target, icon in quick_actions:
            if self.show_frame is not None:
                if text == "Logout":
                    btn = ModernUI.create_button(
                        buttons_frame,
                        f"{icon} {text}",
                        lambda: self._handle_logout(),
                        width=20
                    )
                else:
                    btn = ModernUI.create_button(
                        buttons_frame,
                        f"{icon} {text}",
                        lambda t=target: self.show_frame(t),
                        width=20
                    )
                btn.pack(side='left', padx=5)
            else:
                print(f"Warning: show_frame callback not set for {text}")
        
        # Notifications section
        notifications_container = ttk.Frame(scrollable_frame, style='Card.TFrame')
        notifications_container.pack(fill='x', padx=40, pady=20)
        
        ttk.Label(notifications_container, text="Recent Notifications", style='Title.TLabel').pack(anchor='w', pady=(0, 10))
        
        # Create a container for notification items
        self.notifications_frame = ttk.Frame(notifications_container, style='Card.TFrame')
        self.notifications_frame.pack(fill='x')
        
        # Initial "No notifications" message
        self.no_notifications_label = ttk.Label(
            self.notifications_frame, 
            text="No recent notifications", 
            style='Subtitle.TLabel'
        )
        self.no_notifications_label.pack(pady=10)
        
        self.frames['dashboard'] = self.frame
        
        # Maximize window
        self.frame.pack(fill=tk.BOTH, expand=True)  # Ensure frame fills the entire parent
    
    def _handle_logout(self):
        """Handle logout action"""
        # Clear current user data
        self.current_user = None
        # Reset welcome label
        if self.welcome_label:
            self.welcome_label.configure(text="")
        # Navigate to login page
        if self.show_frame:
            self.show_frame('LoginPage')
    
    def update_notifications(self):
        """Update the notifications section with recent notifications"""
        if not hasattr(self, 'get_notifications_callback') or not self.get_notifications_callback or not hasattr(self, 'current_user') or not self.current_user:
            return
            
        # Clear existing notifications
        for widget in self.notifications_frame.winfo_children():
            widget.destroy()
            
        # Get recent notifications
        notifications = self.get_notifications_callback(self.current_user['unique_id'])
        
        if not notifications:
            self.no_notifications_label = ttk.Label(
                self.notifications_frame, 
                text="No recent notifications", 
                style='Subtitle.TLabel'
            )
            self.no_notifications_label.pack(pady=10)
            return
            
        # Display notifications
        for notification in notifications[:5]:  # Show only the 5 most recent
            notification_item = ttk.Frame(self.notifications_frame, style='Card.TFrame')
            notification_item.pack(fill='x', pady=5)
            
            # Format timestamp
            created_at = notification.get('created_at', datetime.now())
            if isinstance(created_at, str):
                try:
                    created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    created_at = datetime.now()
                    
            formatted_time = created_at.strftime('%b %d, %Y %I:%M %p')
            
            # Display notification content
            content = notification.get('content', 'Notification')
            is_read = notification.get('is_read', False)
            
            # Style based on read status
            style = 'Subtitle.TLabel' if is_read else 'SubtitleBold.TLabel'
            
            # Icon based on notification type
            notification_type = notification.get('type', 'system')
            icon = {
                'donation_request': '🔔',
                'request_accepted': '✅',
                'request_rejected': '❌',
                'new_message': '💬',
                'system': 'ℹ️'
            }.get(notification_type, 'ℹ️')
            
            ttk.Label(notification_item, text=f"{icon} {content}", style=style).pack(anchor='w')
            ttk.Label(notification_item, text=formatted_time, style='Small.TLabel').pack(anchor='w')