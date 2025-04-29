import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import traceback

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.database.database_handler import DatabaseHandler
from src.utils.email_sender import send_email

class AcceptedRequestsPage:
    def __init__(self, parent, controller, user_data):
        """
        Initialize the Accepted Requests Page
        
        :param parent: Parent Tkinter window or frame
        :param controller: Main application controller
        :param user_data: Dictionary containing user information
        """
        self.parent = parent
        self.controller = controller
        
        # Extract user_id from user_data
        self.user_id = user_data['unique_id'] if isinstance(user_data, dict) else None
        
        # Create main frame
        self.frame = tk.Frame(parent)
        
        # Create page title
        title_label = tk.Label(
            self.frame, 
            text="Accepted Donation Requests", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Create Treeview for displaying accepted requests
        self.create_requests_treeview()
        
        # Refresh requests on initialization
        self.refresh_accepted_requests()
        
        # Create button frame
        button_frame = tk.Frame(self.frame)
        button_frame.pack(pady=10)
        
        # Add a button to mark request as delivered
        mark_delivered_button = tk.Button(
            button_frame, 
            text="Mark Delivered", 
            command=self.mark_request_delivered
        )
        mark_delivered_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_requests_treeview(self):
        """Create treeview for displaying accepted requests"""
        # Treeview container
        tree_container = tk.Frame(self.frame)
        tree_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_container)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        self.requests_tree = ttk.Treeview(
            tree_container, 
            columns=('request_id', 'donation_title', 'requester', 'request_date', 'actions'),
            show='headings',
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )
        
        # Column headings
        self.requests_tree.heading('request_id', text='Request ID')
        self.requests_tree.heading('donation_title', text='Donation Title')
        self.requests_tree.heading('requester', text='Requester')
        self.requests_tree.heading('request_date', text='Request Date')
        self.requests_tree.heading('actions', text='Actions')
        
        # Column widths
        self.requests_tree.column('request_id', width=100, anchor='center')
        self.requests_tree.column('donation_title', width=200)
        self.requests_tree.column('requester', width=150)
        self.requests_tree.column('request_date', width=150, anchor='center')
        self.requests_tree.column('actions', width=100, anchor='center')
        
        # Pack treeview
        self.requests_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbars
        tree_scroll_y.config(command=self.requests_tree.yview)
        tree_scroll_x.config(command=self.requests_tree.xview)
        
        # Bind double-click to show details
        self.requests_tree.bind('<Double-1>', self.show_request_details)
    
    def refresh_accepted_requests(self):
        """Refresh the list of accepted requests"""
        # Clear existing items
        for item in self.requests_tree.get_children():
            self.requests_tree.delete(item)
        
        try:
            # Fetch accepted requests
            self.db = DatabaseHandler()
            # Get requests that are approved and associated with the current user
            accepted_requests = self.db.search_requests(
                status='approved',
                donor_id=self.user_id
            )
            
            if not accepted_requests:
                # Show a message if no requests are found
                self.requests_tree.insert('', 'end', values=(
                    'No requests', '', '', '', ''
                ))
                return
            
            # Populate treeview
            for request in accepted_requests:
                # Format the date
                created_at = request.get('created_at', 'N/A')
                if isinstance(created_at, str):
                    created_at = created_at.split('.')[0]  # Remove microseconds
                
                # Add request to treeview
                self.requests_tree.insert('', 'end', values=(
                    request.get('unique_id', 'N/A'),
                    request.get('donation_title', 'N/A'),
                    request.get('requester_name', 'Unknown'),
                    created_at,
                    'Mark Delivered'
                ), tags=('request_row',))
            
            # Configure tag for row actions
            self.requests_tree.tag_bind('request_row', '<Button-1>', self.on_row_click)
        
        except Exception as e:
            print(f"Error refreshing accepted requests: {e}")
            messagebox.showerror("Error", f"Failed to load accepted requests: {str(e)}")
    
    def on_row_click(self, event):
        """Handle row click events, specifically for the 'Mark Delivered' action"""
        # Get the row that was clicked
        row_id = self.requests_tree.identify_row(event.y)
        
        # Get the column that was clicked
        column = self.requests_tree.identify_column(event.x)
        
        if row_id and column == '#5':  # Check if 'Actions' column is clicked
            # Get the request details
            values = self.requests_tree.item(row_id, 'values')
            request_id = values[0]
            
            # Confirm delivery
            confirm = messagebox.askyesno(
                "Confirm Delivery", 
                f"Mark request {request_id} as delivered?"
            )
            
            if confirm:
                # Mark request as delivered
                self.db = DatabaseHandler()
                result = self.db.mark_request_delivered(request_id)
                
                if result:
                    messagebox.showinfo("Success", "Request marked as delivered.")
                    self.refresh_accepted_requests()
                else:
                    messagebox.showerror("Error", "Failed to mark request as delivered.")
    
    def show_request_details(self, event):
        """Show detailed information about a selected request"""
        # Get the selected item
        selected_item = self.requests_tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a request to view details.")
            return
        
        # Get request details
        values = self.requests_tree.item(selected_item[0], 'values')
        request_id = values[0]
        
        # Fetch full request details
        try:
            # Ensure a new database connection
            db_handler = DatabaseHandler()
            
            # Attempt to retrieve request details
            request_details = db_handler.get_request_details_by_message(request_id)
            
            # Print all keys for debugging
            print("Request Details Keys:", request_details.keys())
            print("Full Request Details:", request_details)
            
            # Check if details were retrieved successfully
            if not request_details:
                messagebox.showerror(
                    "Error", 
                    f"Could not retrieve details for request {request_id}. "
                    "The request may have been deleted or is no longer available."
                )
                return
            
            # Create details window
            details_window = tk.Toplevel(self.frame)
            details_window.title(f"Request Details - {request_id}")
            details_window.geometry("700x600")
            
            # Create main container frame
            main_frame = tk.Frame(details_window)
            main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
            
            # Safe get function to handle missing keys
            def safe_get(dictionary, key, default='N/A'):
                return str(dictionary.get(key, default))
            
            # Create sections for different details
            sections = [
                # Donation Details Section
                {
                    'title': 'Donation Information',
                    'details': [
                        ("Title", safe_get(request_details, 'donation_title')),
                        ("Description", safe_get(request_details, 'donation_description'))
                    ]
                },
                # Donor Details Section
                {
                    'title': 'Donor Information',
                    'details': [
                        ("Name", safe_get(request_details, 'donor_name')),
                        ("Email", safe_get(request_details, 'donor_email'))
                    ]
                },
                # Request Details Section
                {
                    'title': 'Request Details',
                    'details': [
                        ("Request Message", safe_get(request_details, 'request_message')),
                        ("Status", safe_get(request_details, 'status'))
                    ]
                },
                # Requester Details Section
                {
                    'title': 'Requester Information',
                    'details': [
                        ("Username", safe_get(request_details, 'requester_username')),
                        ("Email", safe_get(request_details, 'requester_email'))
                    ]
                }
            ]
            
            # Create a canvas with scrollbar for better layout
            canvas = tk.Canvas(main_frame)
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Populate sections
            for section in sections:
                # Section title
                tk.Label(
                    scrollable_frame, 
                    text=section['title'], 
                    font=('Arial', 12, 'bold')
                ).pack(pady=(10, 5), anchor='w')
                
                # Details in each section
                for label, value in section['details']:
                    details_frame = tk.Frame(scrollable_frame)
                    details_frame.pack(fill='x', padx=10, pady=2)
                    
                    tk.Label(
                        details_frame, 
                        text=f"{label}:", 
                        font=('Arial', 10, 'bold'), 
                        width=20, 
                        anchor='w'
                    ).pack(side='left')
                    
                    tk.Label(
                        details_frame, 
                        text=str(value), 
                        font=('Arial', 10), 
                        wraplength=400, 
                        anchor='w'
                    ).pack(side='left', expand=True, fill='x')
            
            # Add a close button
            close_button = tk.Button(
                details_window, 
                text="Close", 
                command=details_window.destroy
            )
            close_button.pack(side=tk.BOTTOM, pady=10)
        
        except Exception as e:
            # Log the full error for debugging
            print(f"Error in show_request_details: {traceback.format_exc()}")
            
            # Show user-friendly error message
            messagebox.showerror(
                "Error", 
                f"An unexpected error occurred while retrieving request details: {str(e)}"
            )
    
    def mark_request_delivered(self):
        """
        Mark the selected request as delivered
        """
        # Get the selected item
        selected_item = self.requests_tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a request to mark as delivered.")
            return
        
        # Get request details
        values = self.requests_tree.item(selected_item[0], 'values')
        request_id = values[0]
        
        # Confirm delivery
        confirm = messagebox.askyesno(
            "Confirm Delivery", 
            f"Are you sure you want to mark request {request_id} as delivered?"
        )
        
        if not confirm:
            return
        
        try:
            # Initialize database handler
            db_handler = DatabaseHandler()
            
            # Mark request as delivered
            success = db_handler.mark_request_delivered(request_id)
            
            if success:
                # Get request details for email notifications
                request_details = db_handler.get_request_details_by_message(request_id)
                
                if request_details:
                    # Send email to requester
                    send_email(
                        to_email=request_details['requester_email'],
                        subject="Your Donation Request Has Been Delivered",
                        body=f"Dear {request_details['requester_username']},\n\nYour request for '{request_details['donation_title']}' has been marked as delivered. Thank you for using CrowdNest!"
                    )
                    
                    # Send email to donor
                    send_email(
                        to_email=request_details['donor_email'],
                        subject="Donation Request Marked as Delivered",
                        body=f"Dear {request_details['donor_name']},\n\nYou have successfully delivered '{request_details['donation_title']}' to {request_details['requester_username']}. Thank you for your generosity!"
                    )
                
                # Remove the item from the treeview
                self.requests_tree.delete(selected_item[0])
                
                # Show success message
                messagebox.showinfo(
                    "Success", 
                    f"Request {request_id} has been marked as delivered."
                )
                
                # Refresh the requests list
                self.refresh_accepted_requests()
            else:
                messagebox.showerror(
                    "Error", 
                    f"Failed to mark request {request_id} as delivered. Please try again."
                )
        
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"An unexpected error occurred: {str(e)}"
            )
            print(f"Error marking request delivered: {e}")
    
    def get_frame(self):
        """Return the main frame for this page"""
        return self.frame
