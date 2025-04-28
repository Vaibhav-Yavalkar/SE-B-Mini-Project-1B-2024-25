import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.modern_ui import ModernUI
from src.constants import COLORS, CATEGORIES, STATES
from src.database.database_handler import DatabaseHandler
from src.utils.email_sender import send_email
from src.utils.html_email_templates import HTMLEmailTemplates

class RequestListPage:
    def __init__(self, parent, user_info, show_frame_callback):
        """Initialize the request list page"""
        self.parent = parent
        self.user_info = user_info
        self.show_frame = show_frame_callback
        self.db = DatabaseHandler()
        
        # Create frame
        self.frame = ModernUI.create_card(parent)
        self.frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(
            self.frame,
            text="Resource Requests",
            style='Title.TLabel'
        ).pack(pady=(0, 20))
        
        # Search and filter frame
        self._create_search_frame()
        
        # Requests treeview
        self._create_requests_treeview()
        
        # Load initial requests
        self.refresh_requests()
        
        # Add buttons for accept and deny
        self.action_frame = tk.Frame(self.frame)
        self.action_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        self.accept_button = tk.Button(self.action_frame, text="Accept Request", command=self.accept_request, state=tk.DISABLED)
        self.accept_button.pack(side=tk.LEFT, padx=5)
        
        self.deny_button = tk.Button(self.action_frame, text="Deny Request", command=self.deny_request, state=tk.DISABLED)
        self.deny_button.pack(side=tk.LEFT, padx=5)
        
        # Bind selection event to enable/disable buttons
        self.requests_tree.bind('<<TreeviewSelect>>', self.on_request_select)

    def _create_search_frame(self):
        """Create search and filter components"""
        search_frame = ttk.Frame(self.frame)
        search_frame.pack(fill='x', pady=(0, 10))
        
        # Search entry
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=5)
        search_entry.insert(0, "Search requests...")
        search_entry.bind('<FocusIn>', lambda e: search_entry.delete(0, tk.END) if search_entry.get() == "Search requests..." else None)
        search_entry.bind('<FocusOut>', lambda e: search_entry.insert(0, "Search requests...") if not search_entry.get() else None)
        
        # Category dropdown
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(
            search_frame, 
            textvariable=self.category_var, 
            values=['All'] + list(CATEGORIES), 
            width=15, 
            state='readonly'
        )
        category_combo.set('All')
        category_combo.pack(side='left', padx=5)
        
        # Status dropdown
        self.status_var = tk.StringVar()
        status_combo = ttk.Combobox(
            search_frame, 
            textvariable=self.status_var, 
            values=['All', 'Open', 'Fulfilled', 'Closed'], 
            width=10, 
            state='readonly'
        )
        status_combo.set('All')
        status_combo.pack(side='left', padx=5)
        
        # Search button
        search_btn = ModernUI.create_button(
            search_frame,
            "Search",
            self.search_requests,
            style='Primary.TButton'
        )
        search_btn.pack(side='left', padx=5)
    
    def _create_requests_treeview(self):
        """Create treeview for displaying requests"""
        # Columns
        columns = ('unique_id', 'title', 'category', 'requester', 'status', 'date')
        
        # Treeview with scrollbar
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')
        
        # Treeview
        self.requests_tree = ttk.Treeview(
            tree_frame, 
            columns=columns, 
            show='headings', 
            yscrollcommand=tree_scroll.set
        )
        
        # Define column headings
        self.requests_tree.heading('unique_id', text='Unique ID', command=lambda: self.sort_column('unique_id', False))
        self.requests_tree.heading('title', text='Request Title', command=lambda: self.sort_column('title', False))
        self.requests_tree.heading('category', text='Category', command=lambda: self.sort_column('category', False))
        self.requests_tree.heading('requester', text='Requester', command=lambda: self.sort_column('requester', False))
        self.requests_tree.heading('status', text='Status', command=lambda: self.sort_column('status', False))
        self.requests_tree.heading('date', text='Date', command=lambda: self.sort_column('date', False))
        
        # Define column widths
        self.requests_tree.column('unique_id', width=150, anchor='w')
        self.requests_tree.column('title', width=250, anchor='w')
        self.requests_tree.column('category', width=100, anchor='center')
        self.requests_tree.column('requester', width=150, anchor='w')
        self.requests_tree.column('status', width=100, anchor='center')
        self.requests_tree.column('date', width=100, anchor='center')
        
        # Configure scrollbar
        tree_scroll.config(command=self.requests_tree.yview)
        
        # Pack treeview
        self.requests_tree.pack(side='left', fill='both', expand=True)
        
        # Bind selection event
        self.requests_tree.bind('<<TreeviewSelect>>', self.on_request_select)
        
        # Bind double-click event
        self.requests_tree.bind('<Double-1>', self.on_request_double_click)

    def search_requests(self):
        """Search and filter requests based on user input"""
        search_term = self.search_var.get().lower()
        category = self.category_var.get()
        status = self.status_var.get()
        
        # Get current user ID from session
        user_id = self.user_info.get('unique_id')
        
        # Fetch requests from database with filters
        try:
            requests = self.db.search_requests(
                search_query=search_term if search_term != "search requests..." else None,
                category=category if category != 'All' else None,
                status=status.lower() if status != 'All' else None,
                donor_id=user_id
            )
            
            # Clear existing items
            for item in self.requests_tree.get_children():
                self.requests_tree.delete(item)
            
            # Populate treeview
            if requests:
                for request in requests:
                    self.requests_tree.insert('', 'end', values=(
                        request.get('unique_id', 'N/A'),  # Use unique_id as first value
                        request.get('request_message', 'N/A')[:50],  # Use request message as title
                        request.get('donation_title', 'N/A'),  # Show donation title
                        request.get('requester_name', 'Unknown'),
                        request.get('status', 'Unknown').capitalize(), 
                        request.get('created_at', 'N/A')
                    ))
        except Exception as e:
            messagebox.showerror("Search Error", str(e))
    
    def view_request_details(self, event):
        """View details of selected request"""
        selected_item = self.requests_tree.selection()
        if not selected_item:
            return
        
        # Get request details
        request_details = self.requests_tree.item(selected_item)['values']
        
        # Show details in a popup
        details_window = tk.Toplevel(self.frame)
        details_window.title("Request Details")
        details_window.geometry("400x300")
        
        # Details display
        details_frame = ttk.Frame(details_window)
        details_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        details = [
            ("Unique ID", request_details[0]),
            ("Title", request_details[1]),
            ("Category", request_details[2]),
            ("Requester", request_details[3]),
            ("Status", request_details[4]),
            ("Date", request_details[5])
        ]
        
        for label, value in details:
            ttk.Label(details_frame, text=f"{label}:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
            ttk.Label(details_frame, text=value).pack(anchor='w', pady=(0, 10))
    
    def sort_column(self, col, reverse):
        """Sort treeview column"""
        l = [(self.requests_tree.set(k, col), k) for k in self.requests_tree.get_children('')]
        l.sort(reverse=reverse)
        
        for index, (val, k) in enumerate(l):
            self.requests_tree.move(k, '', index)
        
        # Toggle sort direction
        self.requests_tree.heading(col, command=lambda: self.sort_column(col, not reverse))
    
    def refresh_requests(self):
        """Refresh requests list with default view"""
        # Reset search and filters
        self.search_var.set("Search requests...")
        self.category_var.set('All')
        self.status_var.set('All')
        
        # Clear existing items
        for item in self.requests_tree.get_children():
            self.requests_tree.delete(item)
        
        # Fetch all requests by default
        try:
            # Get current user ID from session
            user_id = self.user_info.get('unique_id')
            
            # Fetch requests filtered by the current user's donor_id
            requests = self.db.search_requests(donor_id=user_id)
            
            # Populate treeview
            if requests:
                for request in requests:
                    self.requests_tree.insert('', 'end', values=(
                        request.get('unique_id', 'N/A'),  # Use unique_id as first value
                        request.get('request_message', 'N/A')[:50],  # Use request message as title
                        request.get('donation_title', 'N/A'),  # Show donation title
                        request.get('requester_name', 'Unknown'),
                        request.get('status', 'Unknown').capitalize(), 
                        request.get('created_at', 'N/A')
                    ))
                
                # Update status var to reflect the number of requests
                status_text = f"Requests: {len(requests)}"
                self.status_var.set(status_text)
           
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load requests: {str(e)}")
            print(f"Request loading error: {e}")

    def on_request_select(self, event):
        """Enable/disable buttons based on request selection"""
        selected_items = self.requests_tree.selection()
        if selected_items:
            self.accept_button.config(state=tk.NORMAL)
            self.deny_button.config(state=tk.NORMAL)
            
            # Show request details
            selected_item = self.requests_tree.item(selected_items[0])
            self.show_request_details(selected_item['values'])
        else:
            self.accept_button.config(state=tk.DISABLED)
            self.deny_button.config(state=tk.DISABLED)

    def show_request_details(self, request_values):
        """Display detailed information about the selected request"""
        details_window = tk.Toplevel(self.frame)
        details_window.title("Request Details")
        details_window.geometry("700x600")
        
        try:
            # Get the request details
            request_unique_id = request_values[0]
            request_details = self.db.get_request_details_by_message(request_unique_id)
            
            if not request_details:
                messagebox.showerror("Error", "Could not fetch request details.")
                return
            
            # Print all keys for debugging
            print("Request Details Keys:", request_details.keys())
            print("Full Request Details:", request_details)
            
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
                        ("Unique ID", safe_get(request_details, 'unique_id')),
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
            scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
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
            messagebox.showerror("Error", f"Failed to load request details: {str(e)}")
            print(f"Request details error: {e}")

    def accept_request(self):
        """Accept the selected donation request"""
        selected_items = self.requests_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a request to accept.")
            return
        
        try:
            # Get the selected request's details
            selected_item = self.requests_tree.item(selected_items[0])
            request_unique_id = selected_item['values'][0]  # First value is now unique_id
            
            # Get the request details to confirm
            request_details = self.db.get_request_details_by_message(request_unique_id)
            
            if not request_details:
                messagebox.showerror("Error", "Could not find request details.")
                return
                
            # Debug information
            print(f"Request details keys: {request_details.keys()}")
            
            # Process the donation request with user_id from session
            user_id = self.user_info.get('unique_id')
            if not user_id:
                messagebox.showerror("Error", "User ID not found in session.")
                return
                
            success, message = self.db.process_donation_request(request_unique_id, 'accept', user_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_requests()  # Refresh the list
            else:
                messagebox.showerror("Error", message)
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def deny_request(self):
        """Deny the selected donation request"""
        selected_items = self.requests_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a request to deny.")
            return
        
        try:
            # Get the selected request's details
            selected_item = self.requests_tree.item(selected_items[0])
            request_unique_id = selected_item['values'][0]  # First value is now unique_id
            
            # Get the request details to confirm
            request_details = self.db.get_request_details_by_message(request_unique_id)
            
            if not request_details:
                messagebox.showerror("Error", "Could not find request details.")
                return
            
            # Process the donation request with user_id from session
            user_id = self.user_info.get('unique_id')
            if not user_id:
                messagebox.showerror("Error", "User ID not found in session.")
                return
            
            success, message = self.db.process_donation_request(request_unique_id, 'reject', user_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_requests()  # Refresh the list
            else:
                messagebox.showerror("Error", message)
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def on_request_double_click(self, event):
        """Handle double-click event on a request"""
        selected_item = self.requests_tree.selection()
        if not selected_item:
            return
        
        # Get request details
        request_details = self.requests_tree.item(selected_item)['values']
        
        # Show details in a popup
        details_window = tk.Toplevel(self.frame)
        details_window.title("Request Details")
        details_window.geometry("500x400")
        
        # Details display
        details_frame = ttk.Frame(details_window)
        details_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        details = [
            ("Unique ID", request_details[0]),
            ("Title", request_details[1]),
            ("Category", request_details[2]),
            ("Requester", request_details[3]),
            ("Status", request_details[4]),
            ("Date", request_details[5])
        ]
        
        # Display details
        for label, value in details:
            row_frame = ttk.Frame(details_frame)
            row_frame.pack(fill='x', pady=5)
            
            ttk.Label(row_frame, text=f"{label}:", style='Subtitle.TLabel', width=15).pack(side='left')
            ttk.Label(row_frame, text=str(value), style='Subtitle.TLabel').pack(side='left')
        
        # Fetch full request details
        try:
            full_request_details = self.db.get_request_details_by_message(request_details[1])
            
            # Additional details section
            ttk.Label(details_frame, text="Additional Details", style='Title.TLabel').pack(pady=(20, 10))
            
            additional_details = [
                ("Donation Title", full_request_details.get('donation_title', 'N/A')),
                ("Donation Description", full_request_details.get('donation_description', 'N/A')),
                ("Donor Name", full_request_details.get('donor_name', 'N/A')),
                ("Request Message", full_request_details.get('request_message', 'N/A'))
            ]
            
            for label, value in additional_details:
                row_frame = ttk.Frame(details_frame)
                row_frame.pack(fill='x', pady=5)
                
                ttk.Label(row_frame, text=f"{label}:", style='Subtitle.TLabel', width=20).pack(side='left')
                ttk.Label(row_frame, text=str(value), style='Subtitle.TLabel', wraplength=300).pack(side='left')
        
        except Exception as e:
            messagebox.showwarning("Details Retrieval", f"Could not fetch full details: {str(e)}")
        
        # Close button
        close_btn = ModernUI.create_button(
            details_frame,
            "Close",
            details_window.destroy,
            style='Secondary.TButton'
        )
        close_btn.pack(pady=(20, 0))
