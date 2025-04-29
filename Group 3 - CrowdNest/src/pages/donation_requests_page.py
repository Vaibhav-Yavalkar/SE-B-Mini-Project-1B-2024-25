import tkinter as tk
from tkinter import ttk, messagebox
from src.database.database_handler import DatabaseHandler
from src.constants import COLORS
import logging

class DonationRequestsPage:
    def __init__(self, parent, user_info, show_frame_callback):
        """Initialize the donation requests page"""
        # Create main frame
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Store parameters
        self.user_info = user_info
        self.show_frame = show_frame_callback
        self.db = DatabaseHandler()
        
        # Debug logging
        print(f"Initializing Donation Requests Page for User: {user_info}")
        print(f"User Role: {user_info.get('role', 'Unknown')}")
        print(f"User Unique ID: {user_info.get('unique_id', 'Unknown')}")
        
        # Create page components
        self._create_header()
        self._create_requests_table()
        self._create_action_buttons()
        
        # Load donation requests
        self.refresh_donation_requests()

    def _create_header(self):
        """Create page header"""
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill='x', pady=10)
        
        # Title
        ttk.Label(
            header_frame, 
            text="My Donation Requests", 
            font=('Segoe UI', 16, 'bold')
        ).pack(side='left', padx=20)
        
        # User greeting
        ttk.Label(
            header_frame, 
            text=f"Welcome, {self.user_info.get('name', 'Donor')}!", 
            font=('Segoe UI', 12)
        ).pack(side='right', padx=20)

    def _create_requests_table(self):
        """Create treeview for donation requests"""
        # Treeview frame
        table_frame = ttk.Frame(self.frame)
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Columns
        columns = ('unique_id', 'title', 'category', 'requester', 'donor', 'status', 'date')
        self.requests_tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show='headings'
        )
        
        # Define columns
        for col in columns:
            self.requests_tree.heading(col, text=col.title())
            self.requests_tree.column(col, width=100, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame, 
            orient='vertical', 
            command=self.requests_tree.yview
        )
        self.requests_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.requests_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def _create_action_buttons(self):
        """Create action buttons"""
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', pady=10, padx=20)
        
        # Buttons
        ttk.Button(
            button_frame, 
            text="Refresh",
            command=self.manual_refresh
        ).pack(side='left', padx=5)
        
        ttk.Button(
            button_frame, 
            text="View Request Details", 
            command=self.view_request_details
        ).pack(side='left', padx=5)
        
        # Buttons for donors
        if self.user_info.get('role') == 'donor':
            # Status update dropdown
            self.status_var = tk.StringVar()
            status_label = ttk.Label(button_frame, text="Update Status:")
            status_label.pack(side='left', padx=(10, 0))
            
            status_combo = ttk.Combobox(
                button_frame, 
                textvariable=self.status_var, 
                values=['pending', 'approved', 'rejected', 'in_progress', 'completed'], 
                width=15,
                state='readonly'
            )
            status_combo.pack(side='left', padx=5)
            status_combo.set('pending')
            
            # Update Status Button
            ttk.Button(
                button_frame, 
                text="Update Status", 
                command=self.update_request_status
            ).pack(side='left', padx=5)
        
        ttk.Button(
            button_frame, 
            text="Back to Dashboard", 
            command=lambda: self.show_frame('dashboard')
        ).pack(side='right', padx=5)

    def manual_refresh(self):
        """Handle manual refresh button click"""
        self._is_manual_refresh = True
        self.refresh_donation_requests()

    def refresh_donation_requests(self):
        """Refresh requests in treeview with comprehensive error handling"""
        # Clear existing items
        for i in self.requests_tree.get_children():
            self.requests_tree.delete(i)
        
        # Debug logging
        print("Attempting to fetch donation requests...")
        print(f"Current User ID: {self.user_info.get('unique_id', 'Unknown')}")
        
        # Fetch donation requests
        try:
            # Verify database connection
            if not self.db:
                print("ERROR: Database connection is not established.")
                messagebox.showerror("Database Error", "Database connection is not available.")
                return
            
            # Fetch requests based on user role
            if self.user_info.get('role') == 'donor':
                # For donors, fetch requests for their donations
                requests = self.db.get_user_donation_requests(self.user_info['unique_id'])
                print(f"Fetched {len(requests)} requests for donor")
            elif self.user_info.get('role') == 'requester':
                # For requesters, fetch their own requests
                requests = self.db.get_user_donation_requests(self.user_info['unique_id'])
                print(f"Fetched {len(requests)} requests for requester")
            else:
                # For admin or other roles, fetch all requests
                requests = self.db.get_all_donation_requests()
                print(f"Fetched {len(requests)} requests for admin/other role")
            
            # Debug: Print request details
            for req in requests:
                print(f"Request Details: {req}")
            
            # Populate treeview
            for request in requests:
                # Safely extract request details
                self.requests_tree.insert('', 'end', values=(
                    request.get('unique_id', 'N/A'),
                    request.get('donation_title', 'N/A'),
                    request.get('donation_category', 'N/A'),
                    request.get('requester_name', 'N/A'),
                    request.get('donor_name', 'N/A'),
                    request.get('status', 'Pending'),
                    str(request.get('created_at', 'N/A'))
                ))
            
            # Only show popup for manual refresh when no requests found
            if not requests and hasattr(self, '_is_manual_refresh') and self._is_manual_refresh:
                messagebox.showinfo("No Requests", "No donation requests found.")
                self._is_manual_refresh = False  # Reset the flag
            elif not requests:
                print(f"DEBUG: No donation requests found for user ID: {self.user_info.get('unique_id', 'Unknown')}")
            return
        
        except Exception as e:
            # Comprehensive error logging
            print(f"ERROR in refresh_donation_requests: {e}")
            import traceback
            traceback.print_exc()
            
            messagebox.showerror(
                "Error", 
                f"Could not fetch donation requests: {e}\n"
                "Please check your connection and try again."
            )

    def update_request_status(self):
        """Update the status of a selected donation request"""
        # Get selected item from treeview
        selected_item = self.requests_tree.selection()
        
        # Check if an item is selected
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a request to update.")
            return
        
        # Get the selected request details
        selected_values = self.requests_tree.item(selected_item[0])['values']
        
        # Get the selected status
        new_status = self.status_var.get()
        
        try:
            # Find the request in the database
            requests = self.db.get_user_donation_requests(self.user_info['unique_id'])
            
            # Find the matching request
            matching_request = next(
                (req for req in requests 
                 if req.get('unique_id') == selected_values[0]), 
                None
            )
            
            if not matching_request:
                messagebox.showerror("Error", "Could not find request to update.")
                return
            
            # Get the request ID
            request_id = matching_request.get('unique_id')
            
            if not request_id:
                messagebox.showerror("Error", "Invalid request ID.")
                return
            
            # Update request status in the database
            success, message = self.db.update_donation_request_status(
                request_id, 
                new_status, 
                self.user_info['unique_id']
            )
            
            if success:
                # Update the treeview
                self.requests_tree.item(
                    selected_item[0], 
                    values=(
                        selected_values[0],  # Unique ID
                        selected_values[1],  # Title
                        selected_values[2],  # Category
                        selected_values[3],  # Requester
                        selected_values[4],  # Donor
                        new_status,          # Updated Status
                        selected_values[6]   # Date
                    )
                )
                messagebox.showinfo("Success", message)
                
                # Refresh the requests to ensure latest data
                self.refresh_donation_requests()
            else:
                messagebox.showerror("Update Failed", message)
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not update request status: {e}")

    def view_request_details(self):
        """View detailed information about the selected request"""
        # Get selected item from treeview
        selected_item = self.requests_tree.selection()
        
        # Check if an item is selected
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a request to view details.")
            return
        
        # Get the selected request details
        selected_values = self.requests_tree.item(selected_item[0])['values']
        
        try:
            # Find the request in the database
            requests = self.db.get_user_donation_requests(self.user_info['unique_id'])
            
            # Find the matching request
            matching_request = next(
                (req for req in requests 
                 if req.get('unique_id') == selected_values[0]), 
                None
            )
            
            if not matching_request:
                messagebox.showerror("Error", "Could not find request details.")
                return
            
            # Create details window
            details_window = tk.Toplevel(self.frame)
            details_window.title("Request Details")
            details_window.geometry("500x400")
            
            # Details frame
            details_frame = ttk.Frame(details_window, padding="20 20 20 20")
            details_frame.pack(fill='both', expand=True)
            
            # Display request details
            details = [
                ("Donation Title", matching_request.get('donation_title', 'N/A')),
                ("Requester", matching_request.get('requester_name', 'N/A')),
                ("Donor", matching_request.get('donor_name', 'N/A')),
                ("Status", matching_request.get('status', 'N/A')),
                ("Request Date", str(matching_request.get('created_at', 'N/A'))),
                ("Category", matching_request.get('donation_category', 'N/A')),
                ("Request Message", matching_request.get('request_message', 'No message'))
            ]
            
            # Create labels for each detail
            for label_text, value in details:
                row_frame = ttk.Frame(details_frame)
                row_frame.pack(fill='x', pady=5)
                
                ttk.Label(
                    row_frame, 
                    text=f"{label_text}:", 
                    font=('Segoe UI', 10, 'bold'), 
                    width=20
                ).pack(side='left', anchor='w')
                
                ttk.Label(
                    row_frame, 
                    text=value, 
                    font=('Segoe UI', 10), 
                    wraplength=300
                ).pack(side='left', anchor='w')
            
            # Close button
            ttk.Button(
                details_frame, 
                text="Close", 
                command=details_window.destroy
            ).pack(side='bottom', pady=10)
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch request details: {e}")

    def approve_request(self):
        """Approve the selected donation request"""
        # Get selected item from treeview
        selected_item = self.requests_tree.selection()
        
        # Check if an item is selected
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a request to approve.")
            return
        
        # Get the selected request details
        selected_values = self.requests_tree.item(selected_item[0])['values']
        
        try:
            # Directly use the unique_id from the selected values
            request_id = selected_values[0]
            
            if not request_id:
                messagebox.showerror("Error", "Invalid request ID.")
                return
            
            # Update request status to approved
            success, message = self.db.update_donation_request_status(
                request_id, 
                'approved', 
                self.user_info['unique_id']
            )
            
            if success:
                # Update the treeview
                self.requests_tree.item(
                    selected_item[0], 
                    values=(
                        selected_values[0],  # Unique ID
                        selected_values[1],  # Title
                        selected_values[2],  # Category
                        selected_values[3],  # Requester
                        selected_values[4],  # Donor
                        'Approved',          # Updated Status
                        selected_values[6]   # Date
                    )
                )
                messagebox.showinfo("Success", "Request approved successfully.")
                
                # Refresh the view
                self.refresh_donation_requests()
            else:
                messagebox.showerror("Error", message)
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not approve request: {str(e)}")
            print(f"Error in approve_request: {e}")

    def reject_request(self):
        """Reject the selected donation request"""
        # Get selected item from treeview
        selected_item = self.requests_tree.selection()
        
        # Check if an item is selected
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a request to reject.")
            return
        
        # Get the selected request details
        selected_values = self.requests_tree.item(selected_item[0])['values']
        
        try:
            # Find the request in the database
            requests = self.db.get_user_donation_requests(self.user_info['unique_id'])
            
            # Find the matching request
            matching_request = next(
                (req for req in requests 
                 if req.get('unique_id') == selected_values[0]), 
                None
            )
            
            if not matching_request:
                messagebox.showerror("Error", "Could not find request to reject.")
                return
            
            # Get the request ID
            request_id = matching_request.get('unique_id')
            
            if not request_id:
                messagebox.showerror("Error", "Invalid request ID.")
                return
            
            # Update request status to rejected
            success, message = self.db.update_donation_request_status(
                request_id, 
                'rejected', 
                self.user_info['unique_id']
            )
            
            if success:
                # Update the treeview
                self.requests_tree.item(
                    selected_item[0], 
                    values=(
                        selected_values[0],  # Unique ID
                        selected_values[1],  # Title
                        selected_values[2],  # Category
                        selected_values[3],  # Requester
                        selected_values[4],  # Donor
                        'Rejected',          # Updated Status
                        selected_values[6]   # Date
                    )
                )
                messagebox.showinfo("Success", message)
                
                # Refresh the requests to ensure latest data
                self.refresh_donation_requests()
            else:
                messagebox.showerror("Rejection Failed", message)
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not reject request: {e}")
