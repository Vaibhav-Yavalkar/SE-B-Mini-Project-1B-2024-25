import tkinter as tk
from tkinter import ttk, messagebox
from src.database.database_handler import DatabaseHandler
from src.constants import COLORS

class DonationHistoryPage:
    def __init__(self, parent, user_info, show_frame_callback):
        """Initialize the donation history page"""
        # Create main frame
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Store parameters
        self.user_info = user_info
        self.show_frame = show_frame_callback
        self.db = DatabaseHandler()
        
        # Create page components
        self._create_header()
        self._create_donation_history_table()
        self._create_action_buttons()
        
        # Load donation history
        self.refresh_donation_history()

    def _create_header(self):
        """Create page header"""
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill='x', pady=10)
        
        # Title
        ttk.Label(
            header_frame, 
            text="My Donation History", 
            font=('Segoe UI', 16, 'bold')
        ).pack(side='left', padx=20)
        
        # User greeting
        ttk.Label(
            header_frame, 
            text=f"Welcome, {self.user_info.get('name', 'Donor')}!", 
            font=('Segoe UI', 12)
        ).pack(side='right', padx=20)

    def _create_donation_history_table(self):
        """Create treeview for donation history"""
        # Treeview frame
        table_frame = ttk.Frame(self.frame)
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Columns
        columns = ('title', 'category', 'condition', 'location', 'status', 'date')
        self.donations_tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show='headings'
        )
        
        # Define columns
        for col in columns:
            self.donations_tree.heading(col, text=col.title())
            self.donations_tree.column(col, width=100, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame, 
            orient='vertical', 
            command=self.donations_tree.yview
        )
        self.donations_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.donations_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def _create_action_buttons(self):
        """Create action buttons"""
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', pady=10, padx=20)
        
        # Buttons
        ttk.Button(
            button_frame, 
            text="View Details", 
            command=self.view_donation_details
        ).pack(side='left', padx=5)
        
        ttk.Button(
            button_frame, 
            text="Back to Dashboard", 
            command=lambda: self.show_frame('dashboard')
        ).pack(side='right', padx=5)

    def refresh_donation_history(self):
        """Refresh donations in treeview"""
        # Clear existing items
        for i in self.donations_tree.get_children():
            self.donations_tree.delete(i)
        
        # Fetch donation history
        try:
            donations = self.db.get_user_donation_history(self.user_info['unique_id'])
            
            # Populate treeview
            for donation in donations:
                self.donations_tree.insert('', 'end', values=(
                    donation.get('title', 'N/A'),
                    donation.get('category', 'N/A'),
                    donation.get('condition', 'N/A'),
                    f"{donation.get('city', 'N/A')}, {donation.get('state', 'N/A')}",
                    donation.get('status', 'N/A'),
                    str(donation.get('created_at', 'N/A'))
                ))
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch donation history: {e}")

    def view_donation_details(self):
        """Show detailed view of selected donation"""
        # Get selected item from treeview
        selected_item = self.donations_tree.selection()
        
        # Check if an item is selected
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a donation to view details.")
            return
        
        # Get the selected donation details
        selected_values = self.donations_tree.item(selected_item[0])['values']
        
        # Find the full donation details from the database
        try:
            # First, search for the donation
            donations = self.db.search_donations(
                title=selected_values[0], 
                category=selected_values[1]
            )
            
            # If donation found, show details
            if donations:
                # Get the unique_id of the first matching donation
                donation_id = donations[0].get('unique_id')
                
                # Fetch full donation details
                donation = self.db.get_donation_details(donation_id)
                
                if donation:
                    # Create details window
                    details_window = tk.Toplevel(self.frame)
                    details_window.title(f"Donation Details: {donation.get('title', 'N/A')}")
                    details_window.geometry("500x600")
                    
                    # Create a frame for details
                    details_frame = ttk.Frame(details_window, padding="20 20 20 20")
                    details_frame.pack(fill='both', expand=True)
                    
                    # Donation Details
                    details = [
                        ("Title", donation.get('title', 'N/A')),
                        ("Description", donation.get('description', 'N/A')),
                        ("Category", donation.get('category', 'N/A')),
                        ("Condition", donation.get('condition', 'N/A')),
                        ("Location", f"{donation.get('city', 'N/A')}, {donation.get('state', 'N/A')}"),
                        ("Status", donation.get('status', 'N/A')),
                        ("Donor Name", donation.get('donor_name', 'N/A')),
                        ("Donor Email", donation.get('donor_email', 'N/A')),
                        ("Created At", str(donation.get('created_at', 'N/A')))
                    ]
                    
                    # Display details
                    for label_text, value in details:
                        detail_frame = ttk.Frame(details_frame)
                        detail_frame.pack(fill='x', pady=5)
                        
                        ttk.Label(detail_frame, text=f"{label_text}:", font=('Segoe UI', 10, 'bold'), width=15).pack(side='left')
                        ttk.Label(detail_frame, text=value, font=('Segoe UI', 10), wraplength=300).pack(side='left')
                    
                    # Close button
                    ttk.Button(
                        details_frame, 
                        text="Close", 
                        command=details_window.destroy
                    ).pack(pady=10)
                else:
                    messagebox.showinfo("No Details", "Could not find details for this donation.")
            else:
                messagebox.showinfo("No Details", "Could not find details for this donation.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching donation details: {e}")
            print(f"Donation details error: {e}")
