from tkinter import ttk, messagebox, simpledialog, StringVar as tkStringVar
import tkinter as tk
from src.ui.modern_ui import ModernUI
from src.utils.email_validator import EmailValidator
from src.constants import COLORS, CATEGORIES, CONDITIONS, STATES
from src.database.database_handler import DatabaseHandler
import os
import io
from PIL import Image, ImageTk

class DonationListPage:
    # Track all instances of DonationListPage
    instances = []

    def __init__(self, parent, user_info, show_frame_callback):
        """Initialize the donation list page"""
        # Add this instance to the list of instances
        self.__class__.instances.append(self)
        
        self.parent = parent
        self.user_info = user_info
        self.show_frame = show_frame_callback
        self.db = DatabaseHandler()
        
        # Create main frame
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create and pack components
        self._create_header()
        self._create_search_area()
        self._create_donations_table()
        self._create_action_buttons()
        
        # Load initial donations
        self.refresh_donations()

    def _create_header(self):
        """Create page header"""
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill='x', pady=10)
        
        # Title
        ttk.Label(
            header_frame, 
            text="Available Donations", 
            font=('Segoe UI', 16, 'bold')
        ).pack(side='left', padx=20)
        
        # User greeting
        ttk.Label(
            header_frame, 
            text=f"Welcome, {self.user_info.get('name', 'Donor')}!", 
            font=('Segoe UI', 12)
        ).pack(side='right', padx=20)

    def _create_search_area(self):
        """Create search and filter components"""
        search_frame = ttk.Frame(self.frame)
        search_frame.pack(fill='x', pady=10, padx=20)
        
        # Search entry
        self.search_var = tk.StringVar()
        ttk.Label(search_frame, text="Search:").pack(side='left')
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=10)
        
        # Category dropdown
        self.category_var = tk.StringVar()
        ttk.Label(search_frame, text="Category:").pack(side='left')
        category_combo = ttk.Combobox(
            search_frame, 
            textvariable=self.category_var, 
            values=['All Categories'] + list(CATEGORIES), 
            width=20
        )
        category_combo.pack(side='left', padx=10)
        category_combo.set('All Categories')
        
        # Location dropdown
        self.location_var = tk.StringVar()
        ttk.Label(search_frame, text="Location:").pack(side='left')
        location_combo = ttk.Combobox(
            search_frame, 
            textvariable=self.location_var, 
            values=['All Locations'] + list(STATES.keys()), 
            width=20
        )
        location_combo.pack(side='left', padx=10)
        location_combo.set('All Locations')
        
        # Search button
        ttk.Button(
            search_frame, 
            text="Search", 
            command=self.search_donations
        ).pack(side='left', padx=10)

        # Clear filters button
        ttk.Button(
            search_frame, 
            text="Clear Filters", 
            command=self.clear_filters
        ).pack(side='left', padx=10)

    def _create_donations_table(self):
        """Create treeview for donations"""
        # Donations table frame
        donations_frame = ttk.Frame(self.frame)
        donations_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Create treeview
        self.donations_tree = ttk.Treeview(
            donations_frame, 
            columns=(
                'ID', 
                'Title', 
                'Category', 
                'Description',
                'Donor'
            ), 
            show='headings'
        )
        
        # Configure column headings
        for col in self.donations_tree['columns']:
            self.donations_tree.heading(col, text=col)
            self.donations_tree.column(col, width=100, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            donations_frame, 
            orient='vertical', 
            command=self.donations_tree.yview
        )
        self.donations_tree.configure(yscroll=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.donations_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double-click event to view details
        self.donations_tree.bind('<Double-1>', self.view_donation_details)
        
        # Refresh button
        refresh_btn = ttk.Button(
            donations_frame, 
            text="Refresh", 
            command=self.refresh_donations
        )
        refresh_btn.pack(side='bottom', padx=5, pady=5)

    def _create_action_buttons(self):
        """Create action buttons for the donations table"""
        action_frame = ttk.Frame(self.frame)
        action_frame.pack(fill='x', pady=10, padx=20)
        
        # View Details button
        ModernUI.create_button(
            action_frame,
            "View Details", 
            self.view_donation_details_btn,
            style='Primary.TButton'
        ).pack(side='left', padx=5)
        
        # Contact Donor button
        ModernUI.create_button(
            action_frame,
            "Contact Donor", 
            self.contact_donor,
            style='Secondary.TButton'
        ).pack(side='left', padx=5)
        
        # Delete Donation button (only for donors)
        if self.user_info.get('role') == 'donor':
            ModernUI.create_button(
                action_frame,
                "Delete Donation", 
                self.delete_donation,
                style='Danger.TButton'
            ).pack(side='left', padx=5)
        
        # Back to Dashboard button
        ModernUI.create_button(
            action_frame,
            "Back to Dashboard", 
            lambda: self.show_frame('dashboard'),
            style='Neutral.TButton'
        ).pack(side='right', padx=5)

    def refresh_donations(self, donations=None):
        """
        Refresh donations in treeview
        
        :param donations: Optional list of donations to load. 
                          If None, fetches donations from database.
                          Can be a single donation dictionary or a list.
        """
        try:
            # Set manual refresh flag
            self._is_manual_refresh = True
            
            # Clear existing items if fetching from database
            if donations is None:
                for i in self.donations_tree.get_children():
                    self.donations_tree.delete(i)
            
            # Normalize donations to a list
            if donations is None:
                donations_result = self.db.search_donations()
                donations = donations_result.get('donations', [])
            elif isinstance(donations, dict):
                # If a single donation dictionary is passed
                donations = [donations]
            
            # Print debug information
            print(f"Refresh method called. Donations found: {len(donations)}")
            
            # Check if donations list is empty
            if not donations:
                messagebox.showinfo("No Donations", "No available donations found.")
                return
            
            # Update treeview with donation information
            for donation in donations:
                # Ensure the donation is available
                if donation.get('status', '').lower() == 'available':
                    self.donations_tree.insert('', 'end', values=(
                        donation.get('unique_id', 'N/A'),
                        donation.get('title', 'N/A'),
                        donation.get('category', 'N/A'),
                        donation.get('description', 'N/A'),
                        donation.get('donor_name', 'N/A')
                    ))
        
        except Exception as e:
            print(f"Error refreshing donations: {e}")
            messagebox.showerror("Error", f"Failed to refresh donations list: {e}")

    def copy_to_clipboard(self, text):
        """Copy text to clipboard and show feedback"""
        self.parent.clipboard_clear()
        self.parent.clipboard_append(text)
        self.parent.update()
        
        # Show feedback tooltip
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+%d+%d" % (self.parent.winfo_pointerx(), self.parent.winfo_pointery()))
        
        label = ttk.Label(tooltip, text="Email copied!", padding=5, background='#4CAF50', foreground='white')
        label.pack()
        
        # Auto-close tooltip after 1.5 seconds
        self.parent.after(1500, tooltip.destroy)

    def update_cities(self, event=None):
        """Update city dropdown based on selected state"""
        selected_state = self.state_var.get()
        if selected_state and selected_state != 'All Locations':
            cities = STATES.get(selected_state, [])
            self.city_combo['values'] = ['All Cities'] + cities
            self.city_combo.set('All Cities')
        else:
            self.city_combo['values'] = []
            self.city_combo.set('')

    def clear_filters(self):
        """Clear all search filters and reset donations view"""
        # Reset search variables
        self.search_var.set('')
        self.category_var.set('All Categories')
        self.location_var.set('All Locations')

        # Refresh donations to show all
        self.refresh_donations()

    def search_donations(self):
        """Search and filter donations based on user input"""
        # Clear existing items in the treeview
        for item in self.donations_tree.get_children():
            self.donations_tree.delete(item)

        # Get search parameters
        search_term = self.search_var.get().strip()
        category = self.category_var.get()
        location = self.location_var.get()

        # Perform search
        search_result = self.db.search_donations(
            search_term=search_term if search_term else None,
            category=category if category != 'All Categories' else None,
            state=location if location != 'All Locations' else None
        )

        # Refresh donations with search results
        donations = search_result.get('donations', [])
        
        # If no donations found, show info message
        if not donations:
            messagebox.showinfo("No Results", "No donations found matching your search criteria.")
        
        # Add search results to treeview
        for donation in donations:
            self.donations_tree.insert('', 'end', values=(
                donation.get('unique_id', 'N/A'),
                donation.get('title', 'N/A'),
                donation.get('category', 'N/A'),
                donation.get('description', 'N/A'),
                donation.get('donor_name', 'N/A')
            ))

    def view_donation_details_btn(self):
        """
        View donation details when the details button is clicked
        """
        # Get selected item
        selected_item = self.donations_tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a donation to view details.")
            return
        
        # Get the first selected item
        item = selected_item[0]
        
        # Get donation details from the selected row
        donation_details = self.donations_tree.item(item, 'values')
        
        if not donation_details or len(donation_details) < 5:
            messagebox.showerror("Invalid Selection", "Unable to retrieve donation details.")
            return
        
        # Extract details based on treeview columns
        unique_id = donation_details[0]
        title = donation_details[1]
        category = donation_details[2]
        description = donation_details[3]
        donor_name = donation_details[4]
        
        # Open donation details view
        try:
            # Fetch specific donation details
            donation_result = self.db.get_donation_details(unique_id)
            
            if not donation_result:
                messagebox.showerror("Error", f"Could not find details for donation: {title}")
                return
            
            # Create a details window
            details_window = tk.Toplevel(self.frame)
            details_window.title(f"Donation Details - {title}")
            details_window.geometry("800x600")
            
            # Main container
            main_frame = ttk.Frame(details_window, padding="20 20 20 20")
            main_frame.pack(fill='both', expand=True)
            
            # Create two columns
            left_frame = ttk.Frame(main_frame)
            left_frame.pack(side='left', fill='both', expand=True, padx=10)
            
            right_frame = ttk.Frame(main_frame)
            right_frame.pack(side='right', fill='both', expand=True, padx=10)
            
            # Donation Image
            image_path = donation_result.get('image_path')
            image_data = donation_result.get('image_data')
            image_type = donation_result.get('image_type')
            
            # Try to display image
            if image_data:
                try:
                    # Convert image data to PIL Image
                    image = Image.open(io.BytesIO(image_data))
                    resized_image = image.resize((400, 400), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(resized_image)
                    
                    # Display image
                    image_label = ttk.Label(left_frame, image=photo)
                    image_label.image = photo  # Keep a reference
                    image_label.pack(pady=20)
                except Exception as img_err:
                    print(f"Error loading image data: {img_err}")
                    messagebox.showwarning("Image Error", "Could not load donation image.")
            elif image_path and os.path.exists(image_path):
                try:
                    original_image = Image.open(image_path)
                    resized_image = original_image.resize((400, 400), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(resized_image)
                    
                    # Display image
                    image_label = ttk.Label(left_frame, image=photo)
                    image_label.image = photo  # Keep a reference
                    image_label.pack(pady=20)
                except Exception as img_err:
                    print(f"Error loading image: {img_err}")
                    messagebox.showwarning("Image Error", "Could not load donation image.")
            
            # Donation Details
            details = [
                ("Title", title),
                ("Category", category),
                ("Condition", donation_result.get('condition', 'N/A')),
                ("Location", f"{donation_result.get('city', 'N/A')}, {donation_result.get('state', 'N/A')}"),
                ("Donor Name", donor_name),
                ("Donation ID", unique_id),
                ("Description", description),
                ("Created At", str(donation_result.get('created_at', 'N/A'))),
                ("Donor Email", donation_result.get('donor_email', 'N/A'))
            ]
            
            # Display details in right frame
            for label_text, value in details:
                detail_frame = ttk.Frame(right_frame)
                detail_frame.pack(fill='x', pady=5)
                
                label = ttk.Label(detail_frame, text=f"{label_text}:", font=('Segoe UI', 10, 'bold'), width=15)
                label.pack(side='left', anchor='w')
                
                value_label = ttk.Label(
                    detail_frame, 
                    text=value, 
                    font=('Segoe UI', 10), 
                    wraplength=300,
                    justify='left'
                )
                value_label.pack(side='left', anchor='w')
            
            # Associated Requests Section
            requests = donation_result.get('associated_requests', [])
            if requests:
                # Add a separator
                ttk.Separator(right_frame, orient='horizontal').pack(fill='x', pady=10)
                
                # Requests header
                requests_header = ttk.Label(right_frame, text="Associated Requests", font=('Segoe UI', 12, 'bold'))
                requests_header.pack(pady=5)
                
                # Display requests
                for request in requests:
                    request_frame = ttk.Frame(right_frame)
                    request_frame.pack(fill='x', pady=3)
                    
                    request_label = ttk.Label(
                        request_frame, 
                        text=f"Request ID: {request.get('request_id', 'N/A')} | "
                             f"Requester: {request.get('requester_name', 'N/A')} | "
                             f"Status: {request.get('request_status', 'N/A')}", 
                        font=('Segoe UI', 10)
                    )
                    request_label.pack(side='left')
            
            # Action buttons frame
            action_frame = ttk.Frame(details_window)
            action_frame.pack(fill='x', pady=10, padx=20)
            
            # Store donation ID for button actions
            donation_id = unique_id
            
            # Contact Donor Button
            contact_btn = ttk.Button(
                action_frame, 
                text="Contact Donor", 
                command=lambda: self._contact_donor_from_details(donation_id)
            )
            contact_btn.pack(side='left', padx=5)
            
            # Request Donation Button
            request_btn = ttk.Button(
                action_frame, 
                text="Request Donation", 
                command=lambda: self._request_donation_from_details(donation_id)
            )
            request_btn.pack(side='left', padx=5)
            
            # Close Button
            close_btn = ttk.Button(
                action_frame, 
                text="Close", 
                command=details_window.destroy
            )
            close_btn.pack(side='right', padx=5)
        
        except Exception as e:
            print(f"Error creating donation details window: {e}")
            messagebox.showerror("Error", f"Could not display donation details: {e}")

    def view_donation_details(self, event=None):
        """
        View donation details on double-click or button press
        Handles both treeview events and button clicks
        """
        # Determine the selected item
        if event:
            # Double-click event
            selected_item = self.donations_tree.identify_row(event.y)
            if not selected_item:
                return
        else:
            # Button click
            selected_item = self.donations_tree.selection()
            if not selected_item:
                messagebox.showwarning("Selection Error", "Please select a donation to view details.")
                return
            selected_item = selected_item[0]
        
        # Get donation details from the selected row
        donation_details = self.donations_tree.item(selected_item, 'values')
        
        if not donation_details or len(donation_details) < 5:
            messagebox.showerror("Invalid Selection", "Unable to retrieve donation details.")
            return
        
        # Extract details based on treeview columns
        unique_id = donation_details[0]
        title = donation_details[1]
        category = donation_details[2]
        description = donation_details[3]
        donor_name = donation_details[4]
        
        # Open donation details view
        try:
            # Fetch specific donation details
            donation_result = self.db.get_donation_details(unique_id)
            
            if not donation_result:
                messagebox.showerror("Error", f"Could not find details for donation: {title}")
                return
            
            # Create a details window
            details_window = tk.Toplevel(self.frame)
            details_window.title(f"Donation Details - {title}")
            details_window.geometry("800x600")
            
            # Main container
            main_frame = ttk.Frame(details_window, padding="20 20 20 20")
            main_frame.pack(fill='both', expand=True)
            
            # Create two columns
            left_frame = ttk.Frame(main_frame)
            left_frame.pack(side='left', fill='both', expand=True, padx=10)
            
            right_frame = ttk.Frame(main_frame)
            right_frame.pack(side='right', fill='both', expand=True, padx=10)
            
            # Donation Image
            image_path = donation_result.get('image_path')
            image_data = donation_result.get('image_data')
            image_type = donation_result.get('image_type')
            
            # Try to display image
            if image_data:
                try:
                    # Convert image data to PIL Image
                    image = Image.open(io.BytesIO(image_data))
                    resized_image = image.resize((400, 400), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(resized_image)
                    
                    # Display image
                    image_label = ttk.Label(left_frame, image=photo)
                    image_label.image = photo  # Keep a reference
                    image_label.pack(pady=20)
                except Exception as img_err:
                    print(f"Error loading image data: {img_err}")
                    messagebox.showwarning("Image Error", "Could not load donation image.")
            elif image_path and os.path.exists(image_path):
                try:
                    original_image = Image.open(image_path)
                    resized_image = original_image.resize((400, 400), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(resized_image)
                    
                    # Display image
                    image_label = ttk.Label(left_frame, image=photo)
                    image_label.image = photo  # Keep a reference
                    image_label.pack(pady=20)
                except Exception as img_err:
                    print(f"Error loading image: {img_err}")
                    messagebox.showwarning("Image Error", "Could not load donation image.")
            
            # Donation Details
            details = [
                ("Title", title),
                ("Category", category),
                ("Condition", donation_result.get('condition', 'N/A')),
                ("Location", f"{donation_result.get('city', 'N/A')}, {donation_result.get('state', 'N/A')}"),
                ("Donor Name", donor_name),
                ("Donation ID", unique_id),
                ("Description", description),
                ("Created At", str(donation_result.get('created_at', 'N/A'))),
                ("Donor Email", donation_result.get('donor_email', 'N/A'))
            ]
            
            # Display details in right frame
            for label_text, value in details:
                detail_frame = ttk.Frame(right_frame)
                detail_frame.pack(fill='x', pady=5)
                
                label = ttk.Label(detail_frame, text=f"{label_text}:", font=('Segoe UI', 10, 'bold'), width=15)
                label.pack(side='left', anchor='w')
                
                value_label = ttk.Label(
                    detail_frame, 
                    text=value, 
                    font=('Segoe UI', 10), 
                    wraplength=300,
                    justify='left'
                )
                value_label.pack(side='left', anchor='w')
            
            # Associated Requests Section
            requests = donation_result.get('associated_requests', [])
            if requests:
                # Add a separator
                ttk.Separator(right_frame, orient='horizontal').pack(fill='x', pady=10)
                
                # Requests header
                requests_header = ttk.Label(right_frame, text="Associated Requests", font=('Segoe UI', 12, 'bold'))
                requests_header.pack(pady=5)
                
                # Display requests
                for request in requests:
                    request_frame = ttk.Frame(right_frame)
                    request_frame.pack(fill='x', pady=3)
                    
                    request_label = ttk.Label(
                        request_frame, 
                        text=f"Request ID: {request.get('request_id', 'N/A')} | "
                             f"Requester: {request.get('requester_name', 'N/A')} | "
                             f"Status: {request.get('request_status', 'N/A')}", 
                        font=('Segoe UI', 10)
                    )
                    request_label.pack(side='left')
            
            # Action buttons frame
            action_frame = ttk.Frame(details_window)
            action_frame.pack(fill='x', pady=10, padx=20)
            
            # Store donation ID for button actions
            donation_id = unique_id
            
            # Contact Donor Button
            contact_btn = ttk.Button(
                action_frame, 
                text="Contact Donor", 
                command=lambda: self._contact_donor_from_details(donation_id)
            )
            contact_btn.pack(side='left', padx=5)
            
            # Request Donation Button
            request_btn = ttk.Button(
                action_frame, 
                text="Request Donation", 
                command=lambda: self._request_donation_from_details(donation_id)
            )
            request_btn.pack(side='left', padx=5)
            
            # Close Button
            close_btn = ttk.Button(
                action_frame, 
                text="Close", 
                command=details_window.destroy
            )
            close_btn.pack(side='right', padx=5)
        
        except Exception as e:
            print(f"Error creating donation details window: {e}")
            messagebox.showerror("Error", f"Could not display donation details: {e}")

    def _contact_donor_from_details(self, donation_id):
        """
        Contact donor from donation details view
        
        :param donation_id: Unique ID of the donation
        """
        # Validate input
        if not donation_id:
            messagebox.showerror("Contact Error", "Invalid donation ID.")
            return
        
        try:
            # Fetch donation details with comprehensive error handling
            try:
                donation = self.db.get_donation_details(donation_id)
                if not donation:
                    messagebox.showerror("Contact Error", f"Could not retrieve details for donation ID {donation_id}")
                    return
            except Exception as detail_err:
                print(f"Error fetching donation details: {detail_err}")
                messagebox.showerror("Contact Error", "Failed to retrieve donation details.")
                return
            
            # Comprehensive donor information validation
            donor_email = donation.get('donor_email', '').strip()
            donor_name = donation.get('donor_username', 'Unknown Donor').strip()
            
            # Detailed donor information availability check
            missing_info = []
            if not donor_email:
                missing_info.append("Email")
            if not donor_name or donor_name == 'Unknown Donor':
                missing_info.append("Name")
            
            # If all contact information is missing, provide detailed error
            if len(missing_info) == 2:
                messagebox.showerror(
                    "Contact Error", 
                    "Donor contact information is not available.\n\n"
                    "Please contact the platform administrator to update donor details."
                )
                return
            
            # Partial information handling
            if missing_info:
                missing_str = ", ".join(missing_info)
                info_warning = f"Warning: The following donor contact information is missing: {missing_str}"
                
                # Ask user if they want to proceed
                proceed = messagebox.askyesno(
                    "Incomplete Contact Information", 
                    f"{info_warning}\n\nDo you want to proceed with sending a message?"
                )
                
                if not proceed:
                    return
            
            # Open email composition dialog
            subject = f"Inquiry about Donation: {donation.get('title', 'Untitled Donation')}"
            default_message = f"""Hello {donor_name or 'Donor'},

I am interested in the donation: {donation.get('title', 'Untitled Donation')}.
Category: {donation.get('category', 'N/A')}
Condition: {donation.get('condition', 'N/A')}

Could you provide more information about this donation?

Best regards,
{self.user_info.get('name', 'Potential Recipient')}"""
            
            # Use simpledialog to allow user to edit message
            message = simpledialog.askstring(
                "Contact Donor", 
                "Edit your message:", 
                initialvalue=default_message,
                parent=self.frame
            )
            
            if not message or not message.strip():
                messagebox.showwarning("Message Empty", "Message cannot be empty. Contact cancelled.")
                return
            
            # Send email with comprehensive error handling
            try:
                email_sent = self.db.send_donor_contact_email(
                    sender_id=self.user_info['unique_id'],
                    recipient_email=donor_email,
                    subject=subject,
                    message=message
                )
                
                if email_sent:
                    messagebox.showinfo("Email Sent", "Your message has been sent to the donor.")
                else:
                    messagebox.showerror("Email Error", "Failed to send email. Please try again later or contact support.")
            
            except Exception as email_err:
                print(f"Unexpected email sending error: {email_err}")
                messagebox.showerror("Email Error", f"An unexpected error occurred: {str(email_err)}")
        
        except Exception as e:
            print(f"Unexpected error in donor contact process: {e}")
            messagebox.showerror("Contact Error", f"An unexpected error occurred: {str(e)}")

    def _request_donation_from_details(self, donation_id):
        """
        Request donation from donation details view
        
        :param donation_id: Unique ID of the donation
        """
        # Validate input
        if not donation_id:
            messagebox.showerror("Request Error", "Invalid donation ID.")
            return
        
        try:
            # Fetch donation details with comprehensive error handling
            try:
                donation_details = self.db.get_donation_details(donation_id)
                if not donation_details:
                    messagebox.showerror("Request Error", f"Could not retrieve details for donation ID {donation_id}")
                    return
            except Exception as detail_err:
                print(f"Error fetching donation details: {detail_err}")
                messagebox.showerror("Request Error", "Failed to retrieve donation details.")
                return
            
            # Check donation status with comprehensive error handling
            try:
                status, status_message = self.db.get_donation_status(donation_id)
                if status is None:
                    print(f"Status retrieval failed: {status_message}")
                    messagebox.showwarning("Status Check", "Could not verify donation status.")
                elif status == 'withdrawn':
                    messagebox.showinfo("Donation Unavailable", "This donation has been withdrawn.")
                    return
            except Exception as status_err:
                print(f"Unexpected error checking donation status: {status_err}")
                messagebox.showwarning("Status Check", "Unable to verify donation status.")
            
            # Verify user is not the donor
            if donation_details.get('donor_id') == self.user_info['unique_id']:
                messagebox.showerror("Request Error", "You cannot request your own donation.")
                return
            
            # Prompt for request message
            request_message = simpledialog.askstring(
                "Request Donation", 
                f"Enter your request message for '{donation_details.get('title', 'Donation')}':",
                parent=self.parent
            )
            
            if not request_message or not request_message.strip():
                messagebox.showwarning("Request Cancelled", "Request message cannot be empty.")
                return
            
            # Create donation request
            try:
                request_id = self.db.create_request(
                    requester_id=self.user_info['unique_id'], 
                    donation_id=donation_id, 
                    request_message=request_message
                )
                
                if request_id:
                    messagebox.showinfo(
                        "Success", 
                        f"Request for '{donation_details.get('title', 'Donation')}' sent successfully!\nRequest ID: {request_id}"
                    )
                else:
                    messagebox.showerror(
                        "Request Error", 
                        f"Failed to create request. Please try again."
                    )
            
            except Exception as request_err:
                print(f"Unexpected error creating donation request: {request_err}")
                messagebox.showerror(
                    "Request Error", 
                    f"An error occurred while requesting the donation: {str(request_err)}"
                )
        
        except Exception as e:
            print(f"Unexpected error in donation request process: {e}")
            messagebox.showerror("Request Error", f"An unexpected error occurred: {str(e)}")

    def view_donation_details(self, event=None):
        """
        View donation details on double-click or button press
        Handles both treeview events and button clicks
        """
        # Determine the selected item
        if event:
            # Double-click event
            selected_item = self.donations_tree.identify_row(event.y)
            if not selected_item:
                return
        else:
            # Button click
            selected_item = self.donations_tree.selection()
            if not selected_item:
                messagebox.showwarning("Selection Error", "Please select a donation to view details.")
                return
            selected_item = selected_item[0]
        
        # Get donation details from the selected row
        donation_details = self.donations_tree.item(selected_item, 'values')
        
        if not donation_details or len(donation_details) < 5:
            messagebox.showerror("Invalid Selection", "Unable to retrieve donation details.")
            return
        
        # Extract details based on treeview columns
        unique_id = donation_details[0]
        title = donation_details[1]
        category = donation_details[2]
        description = donation_details[3]
        donor_name = donation_details[4]
        
        # Open donation details view
        try:
            # Fetch specific donation details
            donation_result = self.db.get_donation_details(unique_id)
            
            if not donation_result:
                messagebox.showerror("Error", f"Could not find details for donation: {title}")
                return
            
            # Create a details window
            details_window = tk.Toplevel(self.frame)
            details_window.title(f"Donation Details - {title}")
            details_window.geometry("800x600")
            
            # Main container
            main_frame = ttk.Frame(details_window, padding="20 20 20 20")
            main_frame.pack(fill='both', expand=True)
            
            # Create two columns
            left_frame = ttk.Frame(main_frame)
            left_frame.pack(side='left', fill='both', expand=True, padx=10)
            
            right_frame = ttk.Frame(main_frame)
            right_frame.pack(side='right', fill='both', expand=True, padx=10)
            
            # Donation Image
            image_path = donation_result.get('image_path')
            image_data = donation_result.get('image_data')
            image_type = donation_result.get('image_type')
            
            # Try to display image
            if image_data:
                try:
                    # Convert image data to PIL Image
                    image = Image.open(io.BytesIO(image_data))
                    resized_image = image.resize((400, 400), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(resized_image)
                    
                    # Display image
                    image_label = ttk.Label(left_frame, image=photo)
                    image_label.image = photo  # Keep a reference
                    image_label.pack(pady=20)
                except Exception as img_err:
                    print(f"Error loading image data: {img_err}")
                    messagebox.showwarning("Image Error", "Could not load donation image.")
            elif image_path and os.path.exists(image_path):
                try:
                    original_image = Image.open(image_path)
                    resized_image = original_image.resize((400, 400), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(resized_image)
                    
                    # Display image
                    image_label = ttk.Label(left_frame, image=photo)
                    image_label.image = photo  # Keep a reference
                    image_label.pack(pady=20)
                except Exception as img_err:
                    print(f"Error loading image: {img_err}")
                    messagebox.showwarning("Image Error", "Could not load donation image.")
            
            # Donation Details
            details = [
                ("Title", title),
                ("Category", category),
                ("Condition", donation_result.get('condition', 'N/A')),
                ("Location", f"{donation_result.get('city', 'N/A')}, {donation_result.get('state', 'N/A')}"),
                ("Donor Name", donor_name),
                ("Donation ID", unique_id),
                ("Description", description),
                ("Created At", str(donation_result.get('created_at', 'N/A'))),
                ("Donor Email", donation_result.get('donor_email', 'N/A'))
            ]
            
            # Display details in right frame
            for label_text, value in details:
                detail_frame = ttk.Frame(right_frame)
                detail_frame.pack(fill='x', pady=5)
                
                label = ttk.Label(detail_frame, text=f"{label_text}:", font=('Segoe UI', 10, 'bold'), width=15)
                label.pack(side='left', anchor='w')
                
                value_label = ttk.Label(
                    detail_frame, 
                    text=value, 
                    font=('Segoe UI', 10), 
                    wraplength=300,
                    justify='left'
                )
                value_label.pack(side='left', anchor='w')
            
            # Associated Requests Section
            requests = donation_result.get('associated_requests', [])
            if requests:
                # Add a separator
                ttk.Separator(right_frame, orient='horizontal').pack(fill='x', pady=10)
                
                # Requests header
                requests_header = ttk.Label(right_frame, text="Associated Requests", font=('Segoe UI', 12, 'bold'))
                requests_header.pack(pady=5)
                
                # Display requests
                for request in requests:
                    request_frame = ttk.Frame(right_frame)
                    request_frame.pack(fill='x', pady=3)
                    
                    request_label = ttk.Label(
                        request_frame, 
                        text=f"Request ID: {request.get('request_id', 'N/A')} | "
                             f"Requester: {request.get('requester_name', 'N/A')} | "
                             f"Status: {request.get('request_status', 'N/A')}", 
                        font=('Segoe UI', 10)
                    )
                    request_label.pack(side='left')
            
            # Action buttons frame
            action_frame = ttk.Frame(details_window)
            action_frame.pack(fill='x', pady=10, padx=20)
            
            # Store donation ID for button actions
            donation_id = unique_id
            
            # Contact Donor Button
            contact_btn = ttk.Button(
                action_frame, 
                text="Contact Donor", 
                command=lambda: self._contact_donor_from_details(donation_id)
            )
            contact_btn.pack(side='left', padx=5)
            
            # Request Donation Button
            request_btn = ttk.Button(
                action_frame, 
                text="Request Donation", 
                command=lambda: self._request_donation_from_details(donation_id)
            )
            request_btn.pack(side='left', padx=5)
            
            # Close Button
            close_btn = ttk.Button(
                action_frame, 
                text="Close", 
                command=details_window.destroy
            )
            close_btn.pack(side='right', padx=5)
        
        except Exception as e:
            print(f"Error creating donation details window: {e}")
            messagebox.showerror("Error", f"Could not display donation details: {e}")

    def contact_donor(self):
        """
        Contact the donor of a selected donation
        """
        # Get selected item
        selected_item = self.donations_tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a donation to contact the donor.")
            return
        
        # Get the first selected item
        item = selected_item[0]
        
        # Get donation details from the selected row
        donation_details = self.donations_tree.item(item, 'values')
        
        if not donation_details or len(donation_details) < 1:
            messagebox.showerror("Invalid Selection", "Unable to retrieve donation details.")
            return
        
        # Assuming the first column is the unique ID
        donation_id = donation_details[0]
        
        # Verify donation exists
        try:
            # Fetch donation details including donor information
            donation = self.db.get_donation_details(donation_id)
            
            if not donation:
                messagebox.showerror("Invalid Donation", "Unable to find donation details.")
                return
            
            # Check donation status
            status, status_message = self.db.get_donation_status(donation_id)
            if status == 'withdrawn':
                messagebox.showinfo("Donation Unavailable", "This donation has been withdrawn.")
                return
            
            # Get donor contact information
            donor_email = donation.get('donor_email')
            donor_name = donation.get('donor_username')
            
            if not donor_email:
                messagebox.showerror("Contact Error", "Donor contact information not available.")
                return
            
            # Open email composition dialog
            subject = f"Inquiry about Donation: {donation.get('title', 'Untitled Donation')}"
            default_message = f"Hello {donor_name},\n\nI am interested in the donation: {donation.get('title', 'Untitled Donation')}.\n\nCould you provide more information?"
            
            # Use simpledialog to allow user to edit message
            message = simpledialog.askstring(
                "Contact Donor", 
                "Edit your message:", 
                initialvalue=default_message,
                parent=self.frame
            )
            
            if message:
                # Send email or trigger email sending mechanism
                try:
                    email_sent = self.db.send_donor_contact_email(
                        sender_id=self.user_info['unique_id'],
                        recipient_email=donor_email,
                        subject=subject,
                        message=message
                    )
                    
                    if email_sent:
                        messagebox.showinfo("Email Sent", "Your message has been sent to the donor.")
                    else:
                        messagebox.showerror("Email Error", "Failed to send email. Please try again later or contact support.")
                
                except Exception as email_err:
                    messagebox.showerror("Email Error", f"An unexpected error occurred: {str(email_err)}")
        
        except Exception as e:
            messagebox.showerror("Contact Error", f"An error occurred: {str(e)}")

    def request_donation(self, donation_id=None):
        """Request the selected donation"""
        # If no donation_id provided, try to get from selected item
        if donation_id is None:
            selected_item = self.donations_tree.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a donation to request.")
                return
            
            # Extract donation details
            donation_details = self.donations_tree.item(selected_item[0])['values']
            donation_id = donation_details[0]
            donation_title = donation_details[1]
        else:
            # Fetch donation details using the provided ID
            try:
                donation = self.db.get_donation_details(donation_id)
                if not donation:
                    messagebox.showerror("Error", f"Donation with ID {donation_id} not found.")
                    return
                donation_title = donation.get('title', 'Unknown Donation')
            except Exception as e:
                messagebox.showerror("Error", f"Could not verify donation: {str(e)}")
                return
        
        # Prompt for request message
        request_message = simpledialog.askstring(
            "Request Donation", 
            f"Enter your request message for '{donation_title}':",
            parent=self.parent
        )
        
        if not request_message:
            messagebox.showwarning("Cancelled", "Donation request cancelled.")
            return
        
        try:
            # Verify user is not the donor
            donation_details = self.db.get_donation_details(donation_id)
            if donation_details.get('donor_id') == self.user_info['unique_id']:
                messagebox.showerror("Error", "You cannot request your own donation.")
                return
            
            # Create donation request
            request_id = self.db.create_request(
                requester_id=self.user_info['unique_id'], 
                donation_id=donation_id, 
                request_message=request_message
            )
            
            if request_id:
                messagebox.showinfo(
                    "Success", 
                    f"Request for '{donation_title}' sent successfully!\nRequest ID: {request_id}"
                )
            else:
                messagebox.showerror(
                    "Error", 
                    f"Failed to create request for '{donation_title}'. Please try again."
                )
        
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"An error occurred while requesting the donation: {str(e)}"
            )

    def send_email_dialog(self):
        """Open dialog to send email to donation owner"""
        selected_item = self.donations_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a donation to contact.")
            return

        # Get donor's email
        donor_email = self.donations_tree.item(selected_item[0])['values'][4]

        # Open email composition dialog
        email_window = tk.Toplevel(self.parent)
        email_window.title("Send Email")
        email_window.geometry("400x300")

        # Subject
        ttk.Label(email_window, text="Subject:").pack(anchor='w', padx=20, pady=(10,0))
        subject_var = tk.StringVar()
        subject_entry = ttk.Entry(email_window, textvariable=subject_var, width=50)
        subject_entry.pack(padx=20, pady=(0,10))

        # Message body
        ttk.Label(email_window, text="Message:").pack(anchor='w', padx=20, pady=(10,0))
        message_text = tk.Text(email_window, height=10, width=50)
        message_text.pack(padx=20, pady=(0,10))

        def send_email():
            """Send the composed email"""
            subject = subject_var.get()
            message = message_text.get("1.0", tk.END).strip()

            if not subject or not message:
                messagebox.showwarning("Incomplete", "Please enter both subject and message.")
                return

            try:
                # Use the current user's name from user_info
                sender_name = self.user_info.get('name', self.user_info.get('username', 'CrowdNest User'))
                
                EmailValidator.send_communication_email(
                    sender_name=sender_name,
                    sender_email=self.user_info['email'],
                    recipient_email=donor_email,
                    subject=subject,
                    body=message
                )
                messagebox.showinfo("Success", "Email sent successfully!")
                email_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send email: {str(e)}")

        # Send button
        ttk.Button(email_window, text="Send Email", command=send_email).pack(pady=10)

    def delete_donation(self):
        """Delete the selected donation"""
        selected_item = self.donations_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a donation to delete.")
            return

        # Get donation ID
        donation_id = self.donations_tree.item(selected_item[0])['values'][0]

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this donation?")
        if confirm:
            try:
                self.db.delete_donation(donation_id)
                messagebox.showinfo("Success", "Donation deleted successfully.")
                self.refresh_donations()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete donation: {str(e)}")

    def sort_column(self, col, reverse):
        """Sort treeview column when header is clicked"""
        l = [(self.donations_tree.set(k, col), k) for k in self.donations_tree.get_children('')]
        l.sort(reverse=reverse)
        
        for index, (val, k) in enumerate(l):
            self.donations_tree.move(k, '', index)
        
        # Toggle sort direction
        self.donations_tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def load_donations(self, donations=None):
        """
        Load donations into the treeview
        
        :param donations: Optional list of donations to load. 
                          If None, fetches donations from database.
        """
        # Clear existing treeview
        for item in self.donations_tree.get_children():
            self.donations_tree.delete(item)
        
        # Fetch donations if not provided
        if donations is None:
            try:
                # Fetch only available donations
                donations = self.db.search_donations(
                    status='available',  # Add status filter
                    exclude_user_id=self.user_info.get('unique_id')  # Exclude user's own donations
                )
            except Exception as e:
                print(f"Error fetching donations: {e}")
                messagebox.showerror("Fetch Error", "Could not load donations.")
                return
        
        # Validate donations
        if not donations:
            print("No available donations found.")
            return
        
        # Sort donations by most recent first
        try:
            donations.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        except Exception as sort_err:
            print(f"Error sorting donations: {sort_err}")
        
        # Populate treeview
        for donation in donations:
            try:
                # Extract relevant details
                title = donation.get('title', 'Untitled')
                category = donation.get('category', 'N/A')
                description = donation.get('description', 'N/A')
                
                # Only add if status is available
                if donation.get('status', '').lower() == 'available':
                    self.donations_tree.insert('', 'end', values=(
                        title, category, description, donation.get('donor_name', 'N/A')
                    ))
            
            except Exception as insert_err:
                print(f"Error inserting donation: {insert_err}")