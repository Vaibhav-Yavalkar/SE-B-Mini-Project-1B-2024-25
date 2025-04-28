import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.modern_ui import ModernUI

class ProfilePage:
    def __init__(self, parent, user_info, show_frame_callback):
        """Initialize the profile page"""
        self.parent = parent
        # Ensure user_info is a dictionary with default values
        self.user_info = user_info if isinstance(user_info, dict) else {}
        self.show_frame = show_frame_callback
        self.frame = None
        self.profile_entries = {}
        self.profile_labels = {}
        
        # Fetch additional user details if needed
        self.fetch_user_details()
        self.create_frame()
        
    def create_frame(self):
        """Create the profile page frame"""
        self.frame = ModernUI.create_card(self.parent)
        self.frame.pack(fill='both', expand=True, padx=20, pady=20)
        
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
        
        # Profile Header
        header_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(20, 30))
        
        # Profile Avatar
        avatar_frame = ttk.Frame(header_frame, style='Card.TFrame')
        avatar_frame.pack(pady=20)
        
        self.avatar_label = ttk.Label(
            avatar_frame,
            text="👤",
            font=('Segoe UI', 48),
            background='#0077B6',
            foreground='white'
        )
        self.avatar_label.pack()
        
        # Username
        username = self.user_info.get('username', 'Guest')
        ttk.Label(
            avatar_frame,
            text=username,
            font=('Segoe UI', 16),
            foreground='#333333'
        ).pack(pady=(10, 0))
        
        # Back to Dashboard button
        ModernUI.create_button(
            scrollable_frame,
            "Back to Dashboard",
            lambda: self.show_frame('dashboard'),
            style='Secondary.TButton'
        ).pack(side='bottom', pady=20)
        
        # Placeholder for more profile details
        details_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        details_frame.pack(fill='x', padx=20, pady=10)
        
        # Email
        email = self.user_info.get('email', 'Not provided')
        ttk.Label(
            details_frame,
            text=f"Email: {email}",
            style='Card.TLabel'
        ).pack(anchor='w', pady=5)
        
        # Location
        location = self.user_info.get('location', 'Not specified')
        ttk.Label(
            details_frame,
            text=f"Location: {location}",
            style='Card.TLabel'
        ).pack(anchor='w', pady=5)
        
        # Additional details
        details = [
            ("Full Name", "full_name", "Not provided"),
            ("Total Donations", "total_donations", 0),
            ("Total Requests", "total_requests", 0),
            ("Member Since", "created_at", "Not available")
        ]
        
        for label, key, default in details:
            value = self.user_info.get(key, default)
            # Create a frame for each detail
            detail_frame = ttk.Frame(details_frame, style='Card.TFrame')
            detail_frame.pack(fill='x', pady=5)
            
            # Label
            ttk.Label(
                detail_frame,
                text=label,
                style='Card.TLabel',
                font=('Segoe UI', 10, 'bold')
            ).pack(side='left', padx=(0, 10))
            
            # Value
            ttk.Label(
                detail_frame,
                text=str(value),
                style='Card.TLabel',
                font=('Segoe UI', 10)
            ).pack(side='left')
    def fetch_user_details(self):
        """Fetch additional user details from the database"""
        try:
            from src.database.database_handler import DatabaseHandler
            db = DatabaseHandler()
            
            # Get user ID from current user info
            user_id = self.user_info.get('unique_id')
            if not user_id:
                raise ValueError("User ID not found in session")
            
            # Fetch user details
            query = """
            SELECT u.*, 
                   COUNT(DISTINCT d.unique_id) as total_donations,
                   COUNT(DISTINCT dr.unique_id) as total_requests,
                   DATE_FORMAT(u.created_at, '%Y-%m-%d') as member_since
            FROM users u
            LEFT JOIN donations d ON u.unique_id = d.donor_id
            LEFT JOIN donation_requests dr ON u.unique_id = dr.requester_id
            WHERE u.unique_id = %s
            GROUP BY u.unique_id
            """
            
            db.cursor.execute(query, (user_id,))
            user_details = db.cursor.fetchone()
            
            if not user_details:
                raise ValueError("User details not found in database")
                
            # Update user_info with fetched details
            self.user_info.update({
                'username': user_details['username'],
                'email': user_details['email'],
                'location': user_details['location'],
                'full_name': user_details['full_name'],
                'total_donations': user_details['total_donations'],
                'total_requests': user_details['total_requests'],
                'created_at': user_details['member_since']
            })
            
            # Close database connection
            db.close()
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch user details: {str(e)}")
            # Ensure user_info is at least an empty dictionary if fetch fails
            self.user_info = {}