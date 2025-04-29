import os
import tkinter as tk
from tkinter import ttk, messagebox, font
import mysql.connector
from mysql.connector import Error
import stripe
import webbrowser
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from PIL import Image, ImageTk
import json

# Load environment variables
load_dotenv()

# Stripe API Setup
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")

class BuyBookWindow:
    def __init__(self, parent, user_id):
        self.user_id = user_id
        self.cart = []
        self.wishlist = []
        self.parent = parent
        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="All")
        self.sort_var = tk.StringVar(value="Title (A-Z)")

    # Use the parent window directly instead of creating a new one
        self.buy_window = parent  # Change this line
        self.buy_window.title("BookStore - Browse Books")
        self.buy_window.geometry("900x600")
        self.buy_window.configure(bg="#f5f5f5")
        self.buy_window.minsize(900, 600)
    
    # Rest of the code remains the same...
        
        # Set theme and styles
        self.setup_styles()
        
        # Create layout
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        # Load books
        self.update_books_list()

    def setup_styles(self):
        """Configure custom styles for the application"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure colors
        style.configure("TFrame", background="#f5f5f5")
        style.configure("Header.TFrame", background="#3f51b5")
        style.configure("Footer.TFrame", background="#e0e0e0")
        
        # Configure buttons
        style.configure("TButton", padding=6, relief="flat", background="#3f51b5", foreground="white")
        style.map("TButton", background=[("active", "#303f9f")])
        
        # Primary button style
        style.configure("Primary.TButton", font=("Arial", 10, "bold"), padding=8)
        
        # Secondary button style
        style.configure("Secondary.TButton", background="#e0e0e0", foreground="#333333")
        style.map("Secondary.TButton", background=[("active", "#d0d0d0")])
        
        # Configure Treeview
        style.configure("Treeview", 
                        background="#ffffff", 
                        foreground="#333333",
                        rowheight=30,
                        fieldbackground="#ffffff")
        style.map("Treeview", background=[("selected", "#b3e5fc")])
        style.configure("Treeview.Heading", 
                        background="#e1f5fe", 
                        foreground="#0277bd",
                        font=("Arial", 10, "bold"))

    def create_header(self):
        """Create the header section with title and navigation"""
        self.header_frame = ttk.Frame(self.buy_window, style="Header.TFrame")
        self.header_frame.pack(fill="x", pady=(0, 10))
        
        # Title
        title_label = tk.Label(self.header_frame, 
                               text="Available Books", 
                               font=("Arial", 16, "bold"), 
                               background="#3f51b5", 
                               foreground="white")
        title_label.pack(side="left", padx=20, pady=10)
        
        # Back button
        back_btn = ttk.Button(self.header_frame, 
                              text="← Back to Dashboard", 
                              command=self.go_back_to_dashboard,
                              style="Secondary.TButton")
        back_btn.pack(side="right", padx=20, pady=10)

    def create_main_content(self):
        """Create the main content area with book listings and filters"""
        # Main container
        main_frame = ttk.Frame(self.buy_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left panel for filters and search
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        
        # Search box
        search_frame = ttk.Frame(left_panel)
        search_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(search_frame, text="Search Books:", font=("Arial", 10, "bold")).pack(anchor="w")
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25)
        search_entry.pack(fill="x", pady=5)
        search_entry.bind("<Return>", lambda e: self.apply_filters())
        
        ttk.Button(search_frame, text="Search", command=self.apply_filters).pack(fill="x")
        
        # Filters
        filter_frame = ttk.Frame(left_panel)
        filter_frame.pack(fill="x", pady=10)
        
        tk.Label(filter_frame, text="Filter by Condition:", font=("Arial", 10, "bold")).pack(anchor="w")
        conditions = ["All", "New", "Like New", "Good", "Fair"]
        condition_menu = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=conditions, state="readonly")
        condition_menu.pack(fill="x", pady=5)
        condition_menu.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # Sort options
        sort_frame = ttk.Frame(left_panel)
        sort_frame.pack(fill="x", pady=10)
        
        tk.Label(sort_frame, text="Sort by:", font=("Arial", 10, "bold")).pack(anchor="w")
        sort_options = ["Title (A-Z)", "Title (Z-A)", "Price (Low-High)", "Price (High-Low)"]
        sort_menu = ttk.Combobox(sort_frame, textvariable=self.sort_var, values=sort_options, state="readonly")
        sort_menu.pack(fill="x", pady=5)
        sort_menu.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # Cart summary
        cart_frame = ttk.Frame(left_panel)
        cart_frame.pack(fill="x", pady=20)
        
        tk.Label(cart_frame, text="Your Cart", font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.cart_count_label = tk.Label(cart_frame, text="Items: 0", font=("Arial", 10))
        self.cart_count_label.pack(anchor="w", pady=2)
        
        self.cart_total_label = tk.Label(cart_frame, text="Total: $0.00", font=("Arial", 10))
        self.cart_total_label.pack(anchor="w", pady=2)
        
        ttk.Button(cart_frame, text="View Cart", command=self.view_cart, style="Primary.TButton").pack(fill="x", pady=5)
        
        # Wishlist summary
        wishlist_frame = ttk.Frame(left_panel)
        wishlist_frame.pack(fill="x", pady=10)
        
        tk.Label(wishlist_frame, text="Your Wishlist", font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.wishlist_count_label = tk.Label(wishlist_frame, text="Items: 0", font=("Arial", 10))
        self.wishlist_count_label.pack(anchor="w", pady=2)
        
        ttk.Button(wishlist_frame, text="View Wishlist", command=self.view_wishlist, style="Primary.TButton").pack(fill="x", pady=5)
        
        # Right panel for book listings
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Create book listing treeview
        columns = ("book_id", "title", "author", "price", "condition")
        self.treeview = ttk.Treeview(right_panel, columns=columns, show="headings", height=15)
        
        # Set column headings and widths
        self.treeview.heading("book_id", text="#ID", anchor="center")
        self.treeview.column("book_id", width=60, anchor="center")
        
        self.treeview.heading("title", text="Title", anchor="w")
        self.treeview.column("title", width=200, anchor="w") 
        
        self.treeview.heading("author", text="Author", anchor="w")
        self.treeview.column("author", width=150, anchor="w")
        
        self.treeview.heading("price", text="Price ($)", anchor="center")
        self.treeview.column("price", width=80, anchor="center")
        
        self.treeview.heading("condition", text="Condition", anchor="center")
        self.treeview.column("condition", width=100, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(right_panel, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.treeview.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Book action buttons
        book_action_frame = ttk.Frame(right_panel)
        book_action_frame.pack(fill="x", pady=10)
        
        ttk.Button(book_action_frame, text="Add to Cart", command=self.add_to_cart).pack(side="left", padx=5)
        ttk.Button(book_action_frame, text="Add to Wishlist", command=self.add_to_wishlist).pack(side="left", padx=5)
        ttk.Button(book_action_frame, text="View Details", command=self.view_book_details).pack(side="left", padx=5)
        
        # Enable row selection
        self.treeview.bind("<Double-1>", lambda e: self.view_book_details())

    def create_footer(self):
        """Create the footer section with status information"""
        footer_frame = ttk.Frame(self.buy_window, style="Footer.TFrame")
        footer_frame.pack(fill="x")
        
        self.status_label = tk.Label(footer_frame, 
                                     text="Ready", 
                                     font=("Arial", 9), 
                                     background="#e0e0e0")
        self.status_label.pack(side="left", padx=10, pady=5)
        
        refresh_btn = ttk.Button(footer_frame, 
                                text="↻ Refresh", 
                                command=self.update_books_list, 
                                style="Secondary.TButton")
        refresh_btn.pack(side="right", padx=10, pady=5)

    def go_back_to_dashboard(self):
        """Close this window and return to the main dashboard"""
        self.buy_window.destroy()  # Close BuyBookWindow, but do NOT destroy parent.

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="keera@13",
                database="bookstore"
            )
            return connection
        except Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
            return None

    def fetch_available_books(self):
        connection = self.create_connection()
        if not connection:
            return []
        try:
            cursor = connection.cursor()
            query = "SELECT book_id, title, author, price, `condition` FROM books WHERE status = 'Available'"
            cursor.execute(query)
            books = cursor.fetchall()
        except Error as e:
            messagebox.showerror("Error", f"Failed to fetch books: {e}")
            books = []
        finally:
            if connection:
                connection.close()
        return books

    def update_books_list(self):
        self.treeview.delete(*self.treeview.get_children())
        books = self.fetch_available_books()
        
        if not books:
            self.status_label.config(text="No available books found")
            return
            
        for book in books:
            self.treeview.insert("", "end", values=book)
            
        self.status_label.config(text=f"Found {len(books)} available books")

    def apply_filters(self):
        """Apply search, filter, and sort to the book list"""
        search_term = self.search_var.get().lower()
        condition_filter = self.filter_var.get()
        sort_option = self.sort_var.get()
        
        # Clear current list
        self.treeview.delete(*self.treeview.get_children())
        
        # Get all books
        books = self.fetch_available_books()
        filtered_books = []
        
        # Apply filters
        for book in books:
            # Apply search filter
            if search_term and not (search_term in str(book[1]).lower() or search_term in str(book[2]).lower()):
                continue
                
            # Apply condition filter
            if condition_filter != "All" and book[4] != condition_filter:
                continue
                
            filtered_books.append(book)
        
        # Apply sorting
        if sort_option == "Title (A-Z)":
            filtered_books.sort(key=lambda x: x[1])
        elif sort_option == "Title (Z-A)":
            filtered_books.sort(key=lambda x: x[1], reverse=True)
        elif sort_option == "Price (Low-High)":
            filtered_books.sort(key=lambda x: float(x[3]))
        elif sort_option == "Price (High-Low)":
            filtered_books.sort(key=lambda x: float(x[3]), reverse=True)
        
        # Update the list
        for book in filtered_books:
            self.treeview.insert("", "end", values=book)
            
        self.status_label.config(text=f"Found {len(filtered_books)} matching books")

    def add_to_cart(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a book to add to the cart.")
            return
            
        book_details = self.treeview.item(selected_item[0])["values"]
        
        # Check if book already in cart
        for item in self.cart:
            if item[0] == book_details[0]:  # Compare book_id
                messagebox.showinfo("Already in Cart", f"'{book_details[1]}' is already in your cart.")
                return
        
        self.cart.append(book_details)
        self.update_cart_summary()
        
        # Show confirmation with animation
        self.show_add_confirmation(book_details[1])
    
    def show_add_confirmation(self, title):
        """Show a temporary confirmation message when a book is added to cart"""
        confirm_window = tk.Toplevel(self.buy_window)
        confirm_window.overrideredirect(True)  # No window decorations
        confirm_window.configure(bg="#4caf50")
        
        # Position in the center of the parent window
        x = self.buy_window.winfo_x() + (self.buy_window.winfo_width() // 2) - 150
        y = self.buy_window.winfo_y() + (self.buy_window.winfo_height() // 2) - 50
        confirm_window.geometry(f"300x60+{x}+{y}")
        
        # Add message
        message = f"'{title}' added to cart"
        label = tk.Label(confirm_window, 
                        text=message, 
                        font=("Arial", 12), 
                        bg="#4caf50", 
                        fg="white",
                        wraplength=280)
        label.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Auto-close after 1.5 seconds
        confirm_window.after(1500, confirm_window.destroy)

    def update_cart_summary(self):
        """Update the cart summary in the sidebar"""
        total_price = sum(float(book[3]) for book in self.cart)
        self.cart_count_label.config(text=f"Items: {len(self.cart)}")
        self.cart_total_label.config(text=f"Total: ${total_price:.2f}")

    def view_cart(self):
        if not self.cart:
            messagebox.showinfo("Empty Cart", "Your shopping cart is empty.")
            return
            
        if hasattr(self, "cart_window") and self.cart_window.winfo_exists():
            self.cart_window.lift()
            return

        # Create cart window
        self.cart_window = tk.Toplevel(self.buy_window)
        self.cart_window.title("Shopping Cart")
        self.cart_window.geometry("500x400")
        self.cart_window.configure(bg="#f5f5f5")
        self.cart_window.transient(self.buy_window)
        self.cart_window.grab_set()
        
        # Header
        header_frame = ttk.Frame(self.cart_window, style="Header.TFrame")
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, 
                text="Your Shopping Cart", 
                font=("Arial", 14, "bold"), 
                bg="#3f51b5", 
                fg="white").pack(pady=10)
        
        # Cart items
        cart_frame = ttk.Frame(self.cart_window)
        cart_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Create treeview for cart items
        columns = ("title", "author", "price", "condition", "action")
        cart_tree = ttk.Treeview(cart_frame, columns=columns, show="headings", height=10)
        
        cart_tree.heading("title", text="Title")
        cart_tree.column("title", width=180, anchor="w")
        
        cart_tree.heading("author", text="Author")
        cart_tree.column("author", width=120, anchor="w")
        
        cart_tree.heading("price", text="Price")
        cart_tree.column("price", width=60, anchor="center")
        
        cart_tree.heading("condition", text="Condition")
        cart_tree.column("condition", width=80, anchor="center")
        
        cart_tree.heading("action", text="")
        cart_tree.column("action", width=40, anchor="center")
        
        cart_tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(cart_frame, orient="vertical", command=cart_tree.yview)
        cart_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Populate cart items
        for i, book in enumerate(self.cart):
            cart_tree.insert("", "end", iid=str(i), values=(book[1], book[2], f"${float(book[3]):.2f}", book[4], "❌"))
            
        # Handle remove action
        cart_tree.bind("<ButtonRelease-1>", lambda event: self.handle_cart_click(event, cart_tree))
        
        # Summary and checkout
        bottom_frame = ttk.Frame(self.cart_window)
        bottom_frame.pack(fill="x", padx=15, pady=10)
        
        # Calculate total
        total_price = sum(float(book[3]) for book in self.cart)
        
        # Summary label
        summary_frame = ttk.Frame(bottom_frame)
        summary_frame.pack(side="left", fill="y")
        
        tk.Label(summary_frame, 
                text=f"Total Items: {len(self.cart)}", 
                font=("Arial", 10)).pack(anchor="w")
                
        tk.Label(summary_frame, 
                text=f"Total: ${total_price:.2f}", 
                font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

        # Buttons
        button_frame = ttk.Frame(bottom_frame)
        button_frame.pack(side="right")
        
        ttk.Button(button_frame, 
                  text="Continue Shopping", 
                  command=self.cart_window.destroy,
                  style="Secondary.TButton").pack(side="left", padx=5)
                  
        ttk.Button(button_frame, 
                  text="Proceed to Checkout", 
                  command=lambda: self.checkout(self.cart_window),
                  style="Primary.TButton").pack(side="left", padx=5)

    def handle_cart_click(self, event, cart_tree):
        """Handle clicks on the cart treeview, particularly for the remove action"""
        region = cart_tree.identify_region(event.x, event.y)
        if region == "cell":
            column = cart_tree.identify_column(event.x)
            if column == "#5":  # Action column
                selected_id = cart_tree.focus()
                if selected_id:
                    self.remove_from_cart_by_index(int(selected_id), cart_tree)

    def remove_from_cart_by_index(self, index, cart_tree=None):
        """Remove an item from the cart by its index"""
        if 0 <= index < len(self.cart):
            removed_book = self.cart.pop(index)
            self.update_cart_summary()
            
            # Update cart tree if provided
            if cart_tree:
                cart_tree.delete(str(index))
                
                # Reindex remaining items
                for i in range(index, len(self.cart)):
                    cart_tree.item(str(i+1), values=cart_tree.item(str(i+1))["values"], tags=cart_tree.item(str(i+1))["tags"])
                    cart_tree.item(str(i+1), iid=str(i))

    def view_book_details(self):
        """Show detailed information about the selected book"""
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a book to view details.")
            return
            
        book = self.treeview.item(selected_item[0])["values"]
        
        # Create detail window
        detail_window = tk.Toplevel(self.buy_window)
        detail_window.title(f"Book Details: {book[1]}")
        detail_window.geometry("400x450")
        detail_window.configure(bg="#f5f5f5")
        detail_window.transient(self.buy_window)
        
        # Header with book title
        header_frame = ttk.Frame(detail_window, style="Header.TFrame")
        header_frame.pack(fill="x")
        
        title_label = tk.Label(header_frame, 
                              text=book[1], 
                              font=("Arial", 14, "bold"), 
                              bg="#3f51b5", 
                              fg="white")
        title_label.pack(pady=10)

        # Book details
        content_frame = ttk.Frame(detail_window)
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Info fields
        fields = [
            ("Book ID:", book[0]),
            ("Author:", book[2]),
            ("Price:", f"${float(book[3]):.2f}"),
            ("Condition:", book[4]),
        ]
        
        # Add additional details we might have in the database
        # In a real app, you would fetch these from the database
        additional_fields = [
            ("ISBN:", "978-1234567890"),
            ("Genre:", "Fiction"),
            ("Pages:", "326"),
            ("Publisher:", "Sample Publisher"),
            ("Publication Year:", "2023"),
        ]
        
        # Combine all fields
        all_fields = fields + additional_fields
        
        # Display fields
        for i, (label_text, value) in enumerate(all_fields):
            field_frame = ttk.Frame(content_frame)
            field_frame.pack(fill="x", pady=5)
            
            tk.Label(field_frame, 
                    text=label_text, 
                    font=("Arial", 10, "bold"), 
                    width=15, 
                    anchor="w").pack(side="left")
                    
            tk.Label(field_frame, 
                    text=str(value), 
                    font=("Arial", 10)).pack(side="left", padx=5)
        
        # Action buttons
        button_frame = ttk.Frame(detail_window)
        button_frame.pack(fill="x", padx=20, pady=15)
        
        ttk.Button(button_frame, 
                  text="Close", 
                  command=detail_window.destroy, 
                  style="Secondary.TButton").pack(side="left")
                  
        ttk.Button(button_frame, 
                  text="Add to Cart", 
                  command=lambda: [self.add_to_cart(), detail_window.destroy()], 
                  style="Primary.TButton").pack(side="right", padx=5)
        
        ttk.Button(button_frame, 
                  text="Add to Wishlist", 
                  command=lambda: [self.add_to_wishlist(), detail_window.destroy()], 
                  style="Primary.TButton").pack(side="right", padx=5)

    def add_to_wishlist(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a book to add to the wishlist.")
            return
            
        book_details = self.treeview.item(selected_item[0])["values"]
        
        # Check if book already in wishlist
        for item in self.wishlist:
            if item[0] == book_details[0]:  # Compare book_id
                messagebox.showinfo("Already in Wishlist", f"'{book_details[1]}' is already in your wishlist.")
                return
        
        self.wishlist.append(book_details)
        self.update_wishlist_summary()
        
        # Show confirmation with animation
        self.show_add_confirmation(book_details[1])

    def update_wishlist_summary(self):
        """Update the wishlist summary in the sidebar"""
        self.wishlist_count_label.config(text=f"Items: {len(self.wishlist)}")

    def view_wishlist(self):
        if not self.wishlist:
            messagebox.showinfo("Empty Wishlist", "Your wishlist is empty.")
            return
            
        if hasattr(self, "wishlist_window") and self.wishlist_window.winfo_exists():
            self.wishlist_window.lift()
            return

        # Create wishlist window
        self.wishlist_window = tk.Toplevel(self.buy_window)
        self.wishlist_window.title("Wishlist")
        self.wishlist_window.geometry("500x400")
        self.wishlist_window.configure(bg="#f5f5f5")
        self.wishlist_window.transient(self.buy_window)
        self.wishlist_window.grab_set()
        
        # Header
        header_frame = ttk.Frame(self.wishlist_window, style="Header.TFrame")
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, 
                text="Your Wishlist", 
                font=("Arial", 14, "bold"), 
                bg="#3f51b5", 
                fg="white").pack(pady=10)
        
        # Wishlist items
        wishlist_frame = ttk.Frame(self.wishlist_window)
        wishlist_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Create treeview for wishlist items
        columns = ("title", "author", "price", "condition", "action")
        wishlist_tree = ttk.Treeview(wishlist_frame, columns=columns, show="headings", height=10)
        
        wishlist_tree.heading("title", text="Title")
        wishlist_tree.column("title", width=180, anchor="w")
        
        wishlist_tree.heading("author", text="Author")
        wishlist_tree.column("author", width=120, anchor="w")
        
        wishlist_tree.heading("price", text="Price")
        wishlist_tree.column("price", width=60, anchor="center")
        
        wishlist_tree.heading("condition", text="Condition")
        wishlist_tree.column("condition", width=80, anchor="center")
        
        wishlist_tree.heading("action", text="")
        wishlist_tree.column("action", width=40, anchor="center")
        
        wishlist_tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(wishlist_frame, orient="vertical", command=wishlist_tree.yview)
        wishlist_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Populate wishlist items
        for i, book in enumerate(self.wishlist):
            wishlist_tree.insert("", "end", iid=str(i), values=(book[1], book[2], f"${float(book[3]):.2f}", book[4], "❌"))
            
        # Handle remove action
        wishlist_tree.bind("<ButtonRelease-1>", lambda event: self.handle_wishlist_click(event, wishlist_tree))
        
        # Bottom buttons
        button_frame = ttk.Frame(self.wishlist_window)
        button_frame.pack(fill="x", padx=15, pady=10)
        
        ttk.Button(button_frame, 
                  text="Close", 
                  command=self.wishlist_window.destroy, 
                  style="Secondary.TButton").pack(side="left", padx=5)
                  
        ttk.Button(button_frame, 
                  text="Add to Cart", 
                  command=self.add_to_cart_from_wishlist, 
                  style="Primary.TButton").pack(side="right", padx=5)

    def handle_wishlist_click(self, event, wishlist_tree):
        """Handle clicks on the wishlist treeview, particularly for the remove action"""
        region = wishlist_tree.identify_region(event.x, event.y)
        if region == "cell":
            column = wishlist_tree.identify_column(event.x)
            if column == "#5":  # Action column
                selected_id = wishlist_tree.focus()
                if selected_id:
                    self.remove_from_wishlist_by_index(int(selected_id), wishlist_tree)

    def remove_from_wishlist_by_index(self, index, wishlist_tree=None):
        """Remove an item from the wishlist by its index"""
        if 0 <= index < len(self.wishlist):
            removed_book = self.wishlist.pop(index)
            self.update_wishlist_summary()
            
            # Update wishlist tree if provided
            if wishlist_tree:
                wishlist_tree.delete(str(index))
                
                # Reindex remaining items
                for i in range(index, len(self.wishlist)):
                    wishlist_tree.item(str(i+1), values=wishlist_tree.item(str(i+1))["values"], tags=wishlist_tree.item(str(i+1))["tags"])
                    wishlist_tree.item(str(i+1), iid=str(i))

    def add_to_cart_from_wishlist(self):
        if not self.wishlist:
            messagebox.showinfo("Empty Wishlist", "Your wishlist is empty.")
            return
            
        for book in self.wishlist:
            self.add_to_cart()
        
        self.wishlist.clear()
        self.update_wishlist_summary()
        self.wishlist_window.destroy()

    def checkout(self, cart_window=None):
        """Start the checkout process"""
        if not self.cart:
            messagebox.showwarning("Checkout Error", "Your cart is empty.")
            return
            
        total_price = sum(float(book[3]) for book in self.cart)
        
        # Close cart window if it exists
        if cart_window and cart_window.winfo_exists():
            cart_window.destroy()
            
        self.payment_window(total_price)

    def payment_window(self, total_price):
        """Display payment options window"""
        payment_window = tk.Toplevel(self.buy_window)
        payment_window.title("Checkout - Payment Method")
        payment_window.geometry("450x400")
        payment_window.configure(bg="#f5f5f5")
        payment_window.transient(self.buy_window)
        payment_window.grab_set()

        # Header
        header_frame = ttk.Frame(payment_window, style="Header.TFrame")
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, 
                text="Select Payment Method", 
                font=("Arial", 14, "bold"), 
                bg="#3f51b5", 
                fg="white").pack(pady=10)

        # Order summary
        summary_frame = ttk.Frame(payment_window)
        summary_frame.pack(fill="x", padx=20, pady=15)
        
        tk.Label(summary_frame, 
                text="Order Summary", 
                font=("Arial", 12, "bold")).pack(anchor="w")
                
        tk.Label(summary_frame, 
                text=f"Total Items: {len(self.cart)}", 
                font=("Arial", 10)).pack(anchor="w", pady=2)
                
        tk.Label(summary_frame, 
                text=f"Total Amount: ${total_price:.2f}", 
                font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

        # Payment options
        options_frame = ttk.Frame(payment_window)
        options_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create payment method options
        payment_methods = [
            {
                "name": "Cash on Delivery",
                "description": "Pay when your books are delivered",
                "icon": "📦",
                "handler": lambda: self.complete_cod(payment_window)
            },
            {
                "name": "Credit/Debit Card",
                "description": "Pay securely with your card via Stripe",
                "icon": "💳",
                "handler": lambda: self.pay_with_stripe(payment_window, total_price)
            },
            {
                "name": "PayPal",
                "description": "Pay using your PayPal account",
                "icon": "🔒",
                "handler": lambda: self.pay_with_paypal(payment_window, total_price)
            }
        ]
        
        # Display payment options
        for method in payment_methods:
            self.create_payment_option(options_frame, method)
            
        # Bottom buttons
        button_frame = ttk.Frame(payment_window)
        button_frame.pack(fill="x", padx=20, pady=15)
        
        ttk.Button(button_frame, 
                  text="Cancel", 
                  command=payment_window.destroy, 
                  style="Secondary.TButton").pack(side="left")

    def create_payment_option(self, parent, method):
        """Create a payment option button"""
        option_frame = ttk.Frame(parent, padding=10)
        option_frame.pack(fill="x", pady=5)
        option_frame.configure(style="TFrame")
        
        # Add a hover effect
        option_frame.bind("<Enter>", lambda e: option_frame.configure(style="Secondary.TFrame"))
        option_frame.bind("<Leave>", lambda e: option_frame.configure(style="TFrame"))
        option_frame.bind("<Button-1>", lambda e: method["handler"]())
        
        # Icon
        icon_label = tk.Label(option_frame, 
                             text=method["icon"], 
                             font=("Arial", 20),
                             bg=option_frame["background"])
        icon_label.pack(side="left", padx=10)
        
        # Text info
        text_frame = ttk.Frame(option_frame)
        text_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        tk.Label(text_frame, 
                text=method["name"], 
                font=("Arial", 12, "bold"),
                anchor="w").pack(fill="x")
                
        tk.Label(text_frame, 
                text=method["description"], 
                font=("Arial", 9),
                anchor="w").pack(fill="x")
        
        # Select indicator
        tk.Label(option_frame, 
                text="▶", 
                font=("Arial", 12),
                bg=option_frame["background"]).pack(side="right", padx=10)

    def complete_cod(self, payment_window):
        """Complete checkout with Cash on Delivery payment"""
        order_id = self.save_order("Cash on Delivery")
        self.generate_invoice(payment_method="Cash on Delivery", order_id=order_id)
        
        # Show success message
        payment_window.destroy()
        self.show_order_success()
        
        # Clear cart
        self.cart.clear()
        self.update_cart_summary()

    def pay_with_paypal(self, payment_window, total_price):
        """Handle PayPal payment"""
        # In a real application, implement PayPal SDK integration
        # For this example, we'll simulate a successful payment
        
        # Show processing indicator
        self.status_label.config(text="Processing PayPal payment...")
        
        # Simulate processing delay
        payment_window.after(1500, lambda: self.complete_payment(payment_window, "PayPal"))

    def pay_with_stripe(self, payment_window, total_price):
        """Handle Stripe payment"""
        # In a real application, implement Stripe SDK integration
        # For this example, we'll simulate a successful payment
        
        # Show processing indicator
        self.status_label.config(text="Processing Stripe payment...")
        
        # Simulate processing delay
        payment_window.after(1500, lambda: self.complete_payment(payment_window, "Stripe"))

    def complete_payment(self, payment_window, payment_method):
        """Complete the payment process"""
        order_id = self.save_order(payment_method)
        self.generate_invoice(payment_method=payment_method, order_id=order_id)
        
        # Show success message
        payment_window.destroy()
        self.show_order_success()
        
        # Clear cart
        self.cart.clear()
        self.update_cart_summary()

    def save_order(self, payment_method):
        """Save the order to the database"""
        # In a real application, implement database interaction
        # For this example, we'll simulate a successful order save
        
        return "ORD-12345"

    def generate_invoice(self, payment_method, order_id):
        """Generate an invoice for the order"""
        # In a real application, implement invoice generation
        # For this example, we'll simulate a successful invoice generation
        
        pass

    def show_order_success(self):
        """Show a success message after a successful order"""
        success_window = tk.Toplevel(self.buy_window)
        success_window.title("Order Success")
        success_window.geometry("300x150")
        success_window.configure(bg="#f5f5f5")
        success_window.transient(self.buy_window)
        
        tk.Label(success_window, 
                text="Order Successful!", 
                font=("Arial", 14, "bold")).pack(pady=20)
                
        tk.Label(success_window, 
                text="Your order has been placed successfully.", 
                font=("Arial", 10)).pack(pady=10)
                
        ttk.Button(success_window, 
                  text="OK", 
                  command=success_window.destroy, 
                  style="Primary.TButton").pack(pady=10)
