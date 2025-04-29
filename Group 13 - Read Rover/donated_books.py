import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from mysql.connector import Error
import tkinter.font as tkfont
from datetime import datetime

# Function to create MySQL connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='keera@13',
            database='donate_book'
        )
        return connection if connection.is_connected() else None
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to fetch all donated books from the database
def get_donated_books():
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT db.id, db.title, db.author, db.book_type, db.condition, db.status, 
                   CONCAT(u.first_name, ' ', u.last_name) as donor_name
            FROM donated_books db
            LEFT JOIN users u ON db.donor_id = u.id
            WHERE db.status = 'Available'
            ORDER BY db.id DESC
            """
            cursor.execute(query)
            books = cursor.fetchall()
            
            cursor.close()
            connection.close()
            return books
        else:
            messagebox.showerror("Error", "Failed to connect to the database.")
            return []
    except Error as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", "Failed to fetch donated books.")
        return []

# Function to checkout books
def checkout_books(book_ids, user_id):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            
            successful_checkouts = []
            failed_checkouts = []
            
            for book_id in book_ids:
                # First check if the book is still available
                check_query = "SELECT status, title FROM donated_books WHERE id = %s"
                cursor.execute(check_query, (book_id,))
                result = cursor.fetchone()
                
                if not result or result[0] != 'Available':
                    failed_checkouts.append((book_id, "No longer available"))
                    continue
                
                # Update the book status to 'Checked Out'
                update_query = "UPDATE donated_books SET status = 'Checked Out', recipient_id = %s WHERE id = %s"
                cursor.execute(update_query, (user_id, book_id))
                successful_checkouts.append((book_id, result[1]))  # Store book_id and title
            
            connection.commit()
            cursor.close()
            connection.close()
            return successful_checkouts, failed_checkouts
        else:
            messagebox.showerror("Error", "Failed to connect to the database.")
            return [], []
    except Error as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", "Failed to checkout books.")
        return [], []

class CustomTooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        # Create toplevel window
        self.tooltip_window = tk.Toplevel(self.widget)
        # Remove decoration
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip_window, text=self.text, justify='left',
                         background="#ffffd0", relief="solid", borderwidth=1,
                         font=("Segoe UI", 9, "normal"), padx=5, pady=2)
        label.pack()
        
    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class ViewDonatedBooksWindow:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Read Rover - Donated Books")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        self.root.resizable(True, True)
        
        # Set theme colors
        self.primary_color = "#2196F3"  # Blue
        self.secondary_color = "#FFC107"  # Amber
        self.accent_color = "#FF5722"  # Deep Orange
        self.bg_color = "#F5F7FA"  # Light gray/blue
        self.text_color = "#37474F"  # Dark blue-gray
        self.light_text = "#78909C"  # Lighter blue-gray
        self.success_color = "#4CAF50"  # Green
        self.danger_color = "#F44336"  # Red
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure treeview style
        self.style.configure("Treeview", 
                             background=self.bg_color,
                             foreground=self.text_color,
                             rowheight=30,
                             fieldbackground=self.bg_color,
                             font=('Segoe UI', 10))
        self.style.configure("Treeview.Heading", 
                             font=('Segoe UI', 10, 'bold'),
                             background=self.primary_color,
                             foreground="white")
        self.style.map('Treeview', background=[('selected', self.primary_color)], 
                       foreground=[('selected', 'white')])
        
        # Configure ttk widgets style
        self.style.configure("TButton", padding=6, relief="flat", 
                             background=self.primary_color, foreground="white")
        self.style.configure("TCombobox", padding=5, background=self.bg_color)
        self.style.map('TCombobox', fieldbackground=[('readonly', "white")])
        self.style.map('TCombobox', selectbackground=[('readonly', self.primary_color)])
        self.style.map('TCombobox', selectforeground=[('readonly', "white")])
        
        # Set root background
        self.root.configure(bg=self.bg_color)
        
        # Create custom fonts
        self.title_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.subtitle_font = tkfont.Font(family="Segoe UI", size=12)
        self.button_font = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.text_font = tkfont.Font(family="Segoe UI", size=10)
        
        # Shopping cart
        self.cart = []

        # Create header frame
        self.create_header()
        
        # Create main container with two sections
        self.create_main_container()
        
        # Load books
        self.load_books()
        
    def create_header(self):
        """Create application header with logo and title"""
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=70)
        header_frame.pack(fill="x", side="top")
        
        # App logo and name
        logo_frame = tk.Frame(header_frame, bg=self.primary_color)
        logo_frame.pack(side="left", padx=20)
        
        # Create app name with custom font
        app_name = tk.Label(logo_frame, text="Read Rover", 
                          font=('Segoe UI', 20, 'bold'), 
                          fg="white", bg=self.primary_color)
        app_name.pack(side="left")
        
        # Current date display
        current_date = datetime.now().strftime("%B %d, %Y")
        date_label = tk.Label(header_frame, text=current_date,
                            font=('Segoe UI', 10),
                            fg="white", bg=self.primary_color)
        date_label.pack(side="right", padx=20)
        
        # Navigation breadcrumb
        breadcrumb = tk.Label(header_frame, text="Home > Donated Books",
                            font=('Segoe UI', 10),
                            fg="white", bg=self.primary_color)
        breadcrumb.pack(side="right", padx=10)

    def create_main_container(self):
        """Create main container with books list and cart"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Page title with icon
        title_frame = tk.Frame(main_frame, bg=self.bg_color)
        title_frame.pack(fill="x", pady=(0, 15))
        
        title_label = tk.Label(
            title_frame,
            text="Donated Books Catalog",
            font=self.title_font,
            fg=self.primary_color,
            bg=self.bg_color
        )
        title_label.pack(side="left")
        
        # Subtitle with book count
        self.books_count_var = tk.StringVar()
        subtitle_label = tk.Label(
            title_frame,
            textvariable=self.books_count_var,
            font=self.subtitle_font,
            fg=self.light_text,
            bg=self.bg_color
        )
        subtitle_label.pack(side="left", padx=(10, 0))
        
        # Create container for books and cart
        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.pack(fill="both", expand=True)
        
        # Books section (left)
        books_frame = tk.Frame(content_frame, bg=self.bg_color)
        books_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Create search and filter panel
        self.create_search_filter_panel(books_frame)
        
        # Create books treeview
        self.create_book_treeview(books_frame)
        
        # Add to cart button
        action_frame = tk.Frame(books_frame, bg=self.bg_color)
        action_frame.pack(fill="x", pady=10)
        
        add_cart_button = tk.Button(
            action_frame,
            text="Add to Cart",
            command=self.add_to_cart,
            font=self.button_font,
            bg=self.primary_color,
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        add_cart_button.pack(side="left")
        self.add_hover_effect(add_cart_button, self.primary_color)
        
        book_details_button = tk.Button(
            action_frame,
            text="View Details",
            command=self.view_book_details,
            font=self.button_font,
            bg="#9E9E9E",  # Gray
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        book_details_button.pack(side="left", padx=10)
        self.add_hover_effect(book_details_button, "#9E9E9E", "#757575")
        
        # Cart section (right)
        cart_frame = tk.Frame(content_frame, bg="white", width=320, bd=1, relief="solid")
        cart_frame.pack(side="right", fill="both")
        cart_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Create shopping cart UI
        self.create_cart_ui(cart_frame)
        
    def create_search_filter_panel(self, parent_frame):
        """Create search and filter panel"""
        panel_frame = tk.Frame(parent_frame, bg="white", bd=1, relief="solid")
        panel_frame.pack(fill="x", pady=(0, 15))
        
        # Inner padding
        inner_frame = tk.Frame(panel_frame, bg="white", padx=15, pady=15)
        inner_frame.pack(fill="x")
        
        # Panel title
        panel_title = tk.Label(
            inner_frame,
            text="Search & Filter",
            font=('Segoe UI', 12, 'bold'),
            fg=self.text_color,
            bg="white"
        )
        panel_title.pack(anchor="w", pady=(0, 10))
        
        # Search bar with icon
        search_frame = tk.Frame(inner_frame, bg="white")
        search_frame.pack(fill="x", pady=(0, 15))
        
        # Search icon (simulated with emoji)
        search_icon = tk.Label(
            search_frame,
            text="🔍",
            font=('Segoe UI', 12),
            bg="white",
            fg=self.light_text
        )
        search_icon.pack(side="left")
        
        # Search entry
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame, 
            textvariable=self.search_var,
            font=self.text_font,
            bd=0,
            highlightthickness=1,
            highlightbackground="#E0E0E0",
            highlightcolor=self.primary_color
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Search button
        search_button = tk.Button(
            search_frame,
            text="Search",
            command=self.search_books,
            font=self.text_font,
            bg=self.primary_color,
            fg="white",
            relief="flat",
            padx=15,
            cursor="hand2"
        )
        search_button.pack(side="right")
        self.add_hover_effect(search_button, self.primary_color)
        
        # Filter section with two rows
        filter_section = tk.Frame(inner_frame, bg="white")
        filter_section.pack(fill="x", pady=(0, 10))
        
        # First row: Book Type and Condition filters
        filter_row1 = tk.Frame(filter_section, bg="white")
        filter_row1.pack(fill="x", pady=(0, 10))
        
        # Book Type filter
        type_label = tk.Label(
            filter_row1,
            text="Book Type:",
            font=self.text_font,
            bg="white",
            fg=self.text_color
        )
        type_label.pack(side="left", padx=(0, 5))
        
        self.type_var = tk.StringVar()
        type_dropdown = ttk.Combobox(
            filter_row1,
            textvariable=self.type_var,
            values=["All Types", "Fiction", "Non-Fiction", "Sci-Fi", "Romance", "Fantasy", "Biography", "Children", "Educational"],
            width=15,
            state="readonly",
            font=self.text_font
        )
        type_dropdown.current(0)
        type_dropdown.pack(side="left", padx=(0, 20))
        
        # Condition filter
        condition_label = tk.Label(
            filter_row1,
            text="Condition:",
            font=self.text_font,
            bg="white",
            fg=self.text_color
        )
        condition_label.pack(side="left", padx=(0, 5))
        
        self.condition_var = tk.StringVar()
        condition_dropdown = ttk.Combobox(
            filter_row1,
            textvariable=self.condition_var,
            values=["All Conditions", "New", "Like New", "Used", "Very Used"],
            width=15,
            state="readonly",
            font=self.text_font
        )
        condition_dropdown.current(0)
        condition_dropdown.pack(side="left")
        
        # Second row: Filter Buttons
        filter_row2 = tk.Frame(filter_section, bg="white")
        filter_row2.pack(fill="x")
        
        # Apply filters button
        filter_button = tk.Button(
            filter_row2,
            text="Apply Filters",
            command=self.apply_filters,
            font=self.text_font,
            bg=self.primary_color,
            fg="white",
            relief="flat",
            padx=15,
            cursor="hand2"
        )
        filter_button.pack(side="left")
        self.add_hover_effect(filter_button, self.primary_color)
        
        # Reset filters button
        reset_button = tk.Button(
            filter_row2,
            text="Reset",
            command=self.reset_filters,
            font=self.text_font,
            bg="#E0E0E0",
            fg=self.text_color,
            relief="flat",
            padx=15,
            cursor="hand2"
        )
        reset_button.pack(side="left", padx=10)
        self.add_hover_effect(reset_button, "#E0E0E0", "#BDBDBD")

    def create_book_treeview(self, parent_frame):
        """Create a styled treeview to display the donated books."""
        # Create container frame with border
        treeview_container = tk.Frame(parent_frame, bg="white", bd=1, relief="solid")
        treeview_container.pack(fill="both", expand=True)
        
        # Inner padding
        treeview_frame = tk.Frame(treeview_container, bg="white", padx=5, pady=5)
        treeview_frame.pack(fill="both", expand=True)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(treeview_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Configure the treeview
        columns = ("id", "title", "author", "type", "condition", "donor")
        self.book_tree = ttk.Treeview(
            treeview_frame, 
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            style="Treeview"
        )
        
        # Configure column headings
        self.book_tree.heading("id", text="ID")
        self.book_tree.heading("title", text="Title")
        self.book_tree.heading("author", text="Author")
        self.book_tree.heading("type", text="Type")
        self.book_tree.heading("condition", text="Condition")
        self.book_tree.heading("donor", text="Donor")
        
        # Configure column widths
        self.book_tree.column("id", width=50, anchor="center")
        self.book_tree.column("title", width=220)
        self.book_tree.column("author", width=150)
        self.book_tree.column("type", width=100, anchor="center")
        self.book_tree.column("condition", width=100, anchor="center")
        self.book_tree.column("donor", width=150)
        
        # Pack the treeview
        self.book_tree.pack(side="left", fill="both", expand=True)
        
        # Configure the scrollbar
        scrollbar.config(command=self.book_tree.yview)
        
        # Bind double-click event
        self.book_tree.bind("<Double-1>", self.on_book_selected)
        
        # Add tooltip for the treeview
        CustomTooltip(self.book_tree, "Double-click on a book to add it to your cart")

    def create_cart_ui(self, parent_frame):
        """Create a visually appealing shopping cart UI"""
        # Cart header
        cart_header = tk.Frame(parent_frame, bg=self.secondary_color, height=40)
        cart_header.pack(fill="x")
        
        # Cart icon and title
        cart_title = tk.Label(
            cart_header,
            text="🛒 Your Shopping Cart",
            font=('Segoe UI', 12, 'bold'),
            fg=self.text_color,
            bg=self.secondary_color,
            padx=10,
            pady=5
        )
        cart_title.pack(side="left")
        
        # Cart items counter
        self.cart_items_var = tk.StringVar()
        self.cart_items_var.set("0 items")
        cart_count = tk.Label(
            cart_header,
            textvariable=self.cart_items_var,
            font=('Segoe UI', 10),
            fg=self.text_color,
            bg=self.secondary_color,
            padx=10
        )
        cart_count.pack(side="right")
        
        # Cart content area
        cart_content = tk.Frame(parent_frame, bg="white")
        cart_content.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create cart treeview
        self.create_cart_treeview(cart_content)
        
        # Cart buttons
        cart_buttons = tk.Frame(cart_content, bg="white")
        cart_buttons.pack(fill="x", pady=(10, 0))
        
        # Remove selected button
        remove_button = tk.Button(
            cart_buttons,
            text="🗑️ Remove Selected",
            command=self.remove_from_cart,
            font=self.text_font,
            bg=self.danger_color,
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        remove_button.pack(side="left")
        self.add_hover_effect(remove_button, self.danger_color, "#D32F2F")
        
        # Clear cart button
        clear_button = tk.Button(
            cart_buttons,
            text="Clear All",
            command=self.clear_cart,
            font=self.text_font,
            bg="#9E9E9E",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        clear_button.pack(side="left", padx=5)
        self.add_hover_effect(clear_button, "#9E9E9E", "#757575")
        
        # Cart summary area
        cart_summary = tk.Frame(parent_frame, bg="#F5F5F5", height=100)
        cart_summary.pack(fill="x", side="bottom")
        
        # Summary content with padding
        summary_content = tk.Frame(cart_summary, bg="#F5F5F5", padx=15, pady=10)
        summary_content.pack(fill="x")
        
        # Total display
        total_frame = tk.Frame(summary_content, bg="#F5F5F5")
        total_frame.pack(fill="x", pady=5)
        
        total_label = tk.Label(
            total_frame,
            text="Total:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.text_color,
            bg="#F5F5F5"
        )
        total_label.pack(side="left")
        
        self.total_var = tk.StringVar()
        self.total_var.set("$0.00")
        total_value = tk.Label(
            total_frame,
            textvariable=self.total_var,
            font=('Segoe UI', 16, 'bold'),
            fg=self.primary_color,
            bg="#F5F5F5"
        )
        total_value.pack(side="right")
        
        # Checkout button
        checkout_button = tk.Button(
            summary_content,
            text="Proceed to Checkout",
            command=self.checkout,
            font=self.button_font,
            bg=self.success_color,
            fg="white",
            relief="flat",
            padx=15,
            pady=10,
            cursor="hand2"
        )
        checkout_button.pack(fill="x", pady=(10, 0))
        self.add_hover_effect(checkout_button, self.success_color, "#388E3C")
        
        # Empty cart message (shown when cart is empty)
        self.empty_cart_frame = tk.Frame(cart_content, bg="white")
        self.empty_cart_message = tk.Label(
            self.empty_cart_frame,
            text="Your cart is empty.\nAdd books from the catalog to get started.",
            font=self.text_font,
            fg=self.light_text,
            bg="white",
            justify="center"
        )
        self.empty_cart_message.pack(pady=50)
        
        # Show empty cart message initially
        self.empty_cart_frame.pack(fill="both", expand=True)

    def create_cart_treeview(self, parent_frame):
        """Create a treeview to display the cart items."""
        # Create frame for treeview
        cart_treeview_frame = tk.Frame(parent_frame, bg="white")
        cart_treeview_frame.pack(fill="both", expand=True)
        
        # Create scrollbar
        cart_scrollbar = ttk.Scrollbar(cart_treeview_frame)
        cart_scrollbar.pack(side="right", fill="y")
        
        # Configure the treeview
        columns = ("id", "title", "author")
        self.cart_tree = ttk.Treeview(
            cart_treeview_frame, 
            columns=columns,
            show="headings",
            yscrollcommand=cart_scrollbar.set,
            style="Treeview",
            height=8
        )
        
        # Configure column headings
        self.cart_tree.heading("id", text="ID")
        self.cart_tree.heading("title", text="Title")
        self.cart_tree.heading("author", text="Author")
        
        # Configure column widths
        self.cart_tree.column("id", width=40, anchor="center")
        self.cart_tree.column("title", width=170)
        self.cart_tree.column("author", width=90)
        
        # Pack the treeview
        self.cart_tree.pack(side="left", fill="both", expand=True)
        
        # Configure the scrollbar
        cart_scrollbar.config(command=self.cart_tree.yview)

    def load_books(self):
        """Load all donated books into the treeview."""
        # Clear existing items
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        # Get books from database
        books = get_donated_books()
        
        # Update books count
        self.books_count_var.set(f"Found {len(books)} books")
        
        # Add books to treeview
        for book in books:
            self.book_tree.insert(
                "", 
                "end", 
                values=(
                    book['id'],
                    book['title'],
                    book['author'],
                    book['book_type'],
                    book['condition'],
                    book['donor_name'] if book['donor_name'] else "Anonymous"
                )
            )
        
        # Alternating row colors
        self.add_alternating_row_colors()

    def add_alternating_row_colors(self):
        """Add alternating row colors to treeview"""
        for i, item in enumerate(self.book_tree.get_children()):
            if i % 2 == 0:
                self.book_tree.item(item, tags=('even',))
            else:
                self.book_tree.item(item, tags=('odd',))
        
        # Configure tag colors
        self.book_tree.tag_configure('even', background='white')
        self.book_tree.tag_configure('odd', background='#F5F5F5')

    def search_books(self):
        """Search books based on search term."""
        search_term = self.search_var.get().strip().lower()
        
        # Clear existing items
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        # Get all books
        books = get_donated_books()
        
        # Filter books based on search term
        if search_term:
            filtered_books = [
                book for book in books
                if search_term in book['title'].lower() or 
                   search_term in book['author'].lower()
            ]
        else:
            filtered_books = books
        
        # Apply additional filters if active
        filtered_books = self.filter_books(filtered_books)
        
        # Update books count
        self.books_count_var.set(f"Found {len(filtered_books)} books")
        
        # Add filtered books to treeview
        for book in filtered_books:
            self.book_tree.insert(
                "", 
                "end", 
                values=(
                    book['id'],
                    book['title'],
                    book['author'],
                    book['book_type'],
                    book['condition'],
                    book['donor_name'] if book['donor_name'] else "Anonymous"
                )
            )
        
        # Alternating row colors
        self.add_alternating_row_colors()

    def apply_filters(self):
        """Apply selected filters to the book list."""
        # Clear existing items
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        # Get all books
        books = get_donated_books()
        
        # Apply filters
        filtered_books = self.filter_books(books)
        
        # Update books count
        self.books_count_var.set(f"Found {len(filtered_books)} books")
        
        # Add filtered books to treeview
        for book in filtered_books:
            self.book_tree.insert(
                "", 
                "end", 
                values=(
                    book['id'],
                    book['title'],
                    book['author'],
                    book['book_type'],
                    book['condition'],
                    book['donor_name'] if book['donor_name'] else "Anonymous"
                )
            )
        
        # Alternating row colors
        self.add_alternating_row_colors()

    def filter_books(self, books):
        """Filter books based on selected filters."""
        filtered_books = books
        
        # Apply book type filter
        book_type = self.type_var.get()
        if book_type != "All Types":
            filtered_books = [book for book in filtered_books if book['book_type'] == book_type]
        
        # Apply condition filter
        condition = self.condition_var.get()
        if condition != "All Conditions":
            filtered_books = [book for book in filtered_books if book['condition'] == condition]
        
        return filtered_books

    def reset_filters(self):
        """Reset all filters and reload books."""
        self.search_var.set("")
        self.type_var.set("All Types")
        self.condition_var.set("All Conditions")
        self.load_books()

    def on_book_selected(self, event):
        """Handle double-click on a book."""
        # Get selected item
        selection = self.book_tree.selection()
        if selection:
            self.add_to_cart()

    def add_to_cart(self):
        """Add selected book to cart."""
        # Get selected item
        selection = self.book_tree.selection()
        if not selection:
            messagebox.showinfo("Selection Required", "Please select a book to add to cart.")
            return
        
        item = self.book_tree.item(selection[0])
        book_values = item['values']
        book_id = book_values[0]
        
        # Check if book is already in cart
        for cart_item in self.cart:
            if cart_item[0] == book_id:
                messagebox.showinfo("Already in Cart", "This book is already in your cart.")
                return
        
        # Add to cart
        self.cart.append(book_values[:3])  # Store id, title, author
        
        # Update cart treeview
        self.cart_tree.insert("", "end", values=book_values[:3])
        
        # Update cart display
        self.update_cart_display()
        
        # Show success notification
        self.show_notification(f"'{book_values[1]}' added to cart")

    def update_cart_display(self):
        """Update cart display with current items"""
        # Update cart counter
        items_count = len(self.cart)
        self.cart_items_var.set(f"{items_count} item{'s' if items_count != 1 else ''}")
        
        # Show/hide empty cart message
        if items_count > 0:
            self.empty_cart_frame.pack_forget()
            self.cart_tree.pack(side="left", fill="both", expand=True)
        else:
            self.cart_tree.pack_forget()
            self.empty_cart_frame.pack(fill="both", expand=True)

    def remove_from_cart(self):
        """Remove selected item from cart."""
        # Get selected item from cart
        selection = self.cart_tree.selection()
        if not selection:
            messagebox.showinfo("Selection Required", "Please select a book to remove from cart.")
            return
        
        # Remove from cart treeview
        for item_id in selection:
            item = self.cart_tree.item(item_id)
            book_id = item['values'][0]
            
            # Remove from cart list
            self.cart = [book for book in self.cart if book[0] != book_id]
            
            # Remove from treeview
            self.cart_tree.delete(item_id)
        
        # Update cart display
        self.update_cart_display()
        
        # Show notification
        self.show_notification("Item removed from cart")

    def clear_cart(self):
        """Clear all items from cart."""
        if not self.cart:
            return
            
        if messagebox.askyesno("Clear Cart", "Are you sure you want to clear your cart?"):
            # Clear cart list
            self.cart = []
            
            # Clear cart treeview
            for item in self.cart_tree.get_children():
                self.cart_tree.delete(item)
            
            # Update cart display
            self.update_cart_display()
            
            # Show notification
            self.show_notification("Cart cleared")

    def checkout(self):
        """Process checkout of all items in cart."""
        if not self.cart:
            messagebox.showinfo("Empty Cart", "Your cart is empty. Please add books before checkout.")
            return
        
        # Confirm checkout
        checkout_message = f"You are about to check out {len(self.cart)} book{'s' if len(self.cart) != 1 else ''}.\n\nThese books are free of charge. Continue?"
        if not messagebox.askyesno("Confirm Checkout", checkout_message):
            return
        
        # Get book IDs from cart
        book_ids = [item[0] for item in self.cart]
        
        # Process checkout
        successful, failed = checkout_books(book_ids, self.user_id)
        
        # Prepare result message
        if successful:
            self.show_checkout_success_dialog(successful, failed)
            
            # Clear successful items from cart
            successful_ids = [item[0] for item in successful]
            self.cart = [item for item in self.cart if item[0] not in successful_ids]
            
            # Update cart treeview
            for item in self.cart_tree.get_children():
                item_id = self.cart_tree.item(item)['values'][0]
                if item_id in successful_ids:
                    self.cart_tree.delete(item)
            
            # Update cart display
            self.update_cart_display()
            
            # Refresh book list
            self.load_books()
        else:
            messagebox.showerror("Checkout Failed", "Failed to checkout any books. Please try again.")

    def show_checkout_success_dialog(self, successful, failed):
        """Show a detailed checkout success dialog with animated effects"""
        checkout_dialog = tk.Toplevel(self.root)
        checkout_dialog.title("Checkout Complete")
        checkout_dialog.geometry("400x450")
        checkout_dialog.resizable(False, False)
        checkout_dialog.configure(bg="white")
        checkout_dialog.transient(self.root)
        checkout_dialog.grab_set()
        
        # Add some padding
        container = tk.Frame(checkout_dialog, bg="white", padx=20, pady=20)
        container.pack(fill="both", expand=True)
        
        # Success icon
        success_label = tk.Label(
            container,
            text="✅",
            font=("Segoe UI", 48),
            fg=self.success_color,
            bg="white"
        )
        success_label.pack(pady=(10, 0))
        
        # Success header
        header_label = tk.Label(
            container,
            text="Checkout Complete!",
            font=("Segoe UI", 18, "bold"),
            fg=self.success_color,
            bg="white"
        )
        header_label.pack(pady=(0, 10))
        
        # Summary
        summary_text = f"You have successfully checked out {len(successful)} book{'s' if len(successful) != 1 else ''}."
        summary_label = tk.Label(
            container,
            text=summary_text,
            font=("Segoe UI", 12),
            fg=self.text_color,
            bg="white"
        )
        summary_label.pack(pady=(0, 10))
        
        # Create a frame for the successful books
        books_frame = tk.Frame(container, bg="white", bd=1, relief="solid", padx=10, pady=10)
        books_frame.pack(fill="x", pady=10)
        
        # Title for the books list
        books_title = tk.Label(
            books_frame,
            text="Books checked out:",
            font=("Segoe UI", 12, "bold"),
            fg=self.text_color,
            bg="white"
        )
        books_title.pack(anchor="w")
        
        # Books list
        books_list_frame = tk.Frame(books_frame, bg="white")
        books_list_frame.pack(fill="x", pady=5)
        
        for book_id, book_title in successful:
            book_item = tk.Label(
                books_list_frame,
                text=f"• {book_title}",
                font=("Segoe UI", 10),
                fg=self.text_color,
                bg="white",
                anchor="w",
                justify="left"
            )
            book_item.pack(anchor="w", pady=2)
        
        # Failed books section (if any)
        if failed:
            failed_frame = tk.Frame(container, bg="#FFF3E0", bd=1, relief="solid", padx=10, pady=10)
            failed_frame.pack(fill="x", pady=10)
            
            failed_title = tk.Label(
                failed_frame,
                text="Books not available:",
                font=("Segoe UI", 12, "bold"),
                fg="#E65100",
                bg="#FFF3E0"
            )
            failed_title.pack(anchor="w")
            
            failed_list_frame = tk.Frame(failed_frame, bg="#FFF3E0")
            failed_list_frame.pack(fill="x", pady=5)
            
            for book_id, reason in failed:
                # Find book title in cart
                title = next((item[1] for item in self.cart if item[0] == book_id), "Unknown")
                failed_item = tk.Label(
                    failed_list_frame,
                    text=f"• {title}",
                    font=("Segoe UI", 10),
                    fg="#E65100",
                    bg="#FFF3E0",
                    anchor="w"
                )
                failed_item.pack(anchor="w", pady=2)
        
        # Close button
        close_button = tk.Button(
            container,
            text="Continue Shopping",
            command=checkout_dialog.destroy,
            font=("Segoe UI", 12, "bold"),
            bg=self.primary_color,
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        close_button.pack(pady=15)
        self.add_hover_effect(close_button, self.primary_color)

    def view_book_details(self):
        """Show detailed information about the selected book"""
        # Get selected item
        selection = self.book_tree.selection()
        if not selection:
            messagebox.showinfo("Selection Required", "Please select a book to view details.")
            return
        
        item = self.book_tree.item(selection[0])
        book_values = item['values']
        
        # Create book details dialog
        details_dialog = tk.Toplevel(self.root)
        details_dialog.title(f"Book Details: {book_values[1]}")
        details_dialog.geometry("500x400")
        details_dialog.resizable(False, False)
        details_dialog.configure(bg="white")
        details_dialog.transient(self.root)
        details_dialog.grab_set()
        
        # Add some padding
        container = tk.Frame(details_dialog, bg="white", padx=20, pady=20)
        container.pack(fill="both", expand=True)
        
        # Book title
        title_label = tk.Label(
            container,
            text=book_values[1],
            font=("Segoe UI", 16, "bold"),
            fg=self.primary_color,
            bg="white",
            wraplength=460,
            justify="left"
        )
        title_label.pack(anchor="w")
        
        # Book ID
        id_label = tk.Label(
            container,
            text=f"Book ID: {book_values[0]}",
            font=("Segoe UI", 10),
            fg=self.light_text,
            bg="white"
        )
        id_label.pack(anchor="w", pady=(0, 10))
        
        # Book information in two columns
        info_frame = tk.Frame(container, bg="white")
        info_frame.pack(fill="x", pady=10)
        
        # Left column
        left_col = tk.Frame(info_frame, bg="white")
        left_col.pack(side="left", fill="both", expand=True)
        
        # Right column
        right_col = tk.Frame(info_frame, bg="white")
        right_col.pack(side="right", fill="both", expand=True)
        
        # Author info
        author_label = tk.Label(
            left_col,
            text="Author:",
            font=("Segoe UI", 10, "bold"),
            fg=self.text_color,
            bg="white"
        )
        author_label.pack(anchor="w", pady=(0, 2))
        
        author_value = tk.Label(
            left_col,
            text=book_values[2],
            font=("Segoe UI", 10),
            fg=self.text_color,
            bg="white"
        )
        author_value.pack(anchor="w", pady=(0, 10))
        
        # Type info
        type_label = tk.Label(
            left_col,
            text="Book Type:",
            font=("Segoe UI", 10, "bold"),
            fg=self.text_color,
            bg="white"
        )
        type_label.pack(anchor="w", pady=(0, 2))
        
        type_value = tk.Label(
            left_col,
            text=book_values[3],
            font=("Segoe UI", 10),
            fg=self.text_color,
            bg="white"
        )
        type_value.pack(anchor="w", pady=(0, 10))
        
        # Condition info
        condition_label = tk.Label(
            right_col,
            text="Condition:",
            font=("Segoe UI", 10, "bold"),
            fg=self.text_color,
            bg="white"
        )
        condition_label.pack(anchor="w", pady=(0, 2))
        
        condition_value = tk.Label(
            right_col,
            text=book_values[4],
            font=("Segoe UI", 10),
            fg=self.text_color,
            bg="white"
        )
        condition_value.pack(anchor="w", pady=(0, 10))
        
        # Donor info
        donor_label = tk.Label(
            right_col,
            text="Donated By:",
            font=("Segoe UI", 10, "bold"),
            fg=self.text_color,
            bg="white"
        )
        donor_label.pack(anchor="w", pady=(0, 2))
        
        donor_value = tk.Label(
            right_col,
            text=book_values[5],
            font=("Segoe UI", 10),
            fg=self.text_color,
            bg="white"
        )
        donor_value.pack(anchor="w", pady=(0, 10))
        
        # Description placeholder
        description_label = tk.Label(
            container,
            text="Description:",
            font=("Segoe UI", 10, "bold"),
            fg=self.text_color,
            bg="white"
        )
        description_label.pack(anchor="w", pady=(10, 5))
        
        description_text = tk.Text(
            container,
            height=5,
            width=40,
            font=("Segoe UI", 10),
            wrap="word",
            bd=1,
            relief="solid",
            bg="#F5F5F5"
        )
        description_text.insert("1.0", "This donated book is available for checkout. The book is free of charge and part of our community book sharing program.")
        description_text.config(state="disabled")
        description_text.pack(fill="x", pady=(0, 15))
        
        # Action buttons
        buttons_frame = tk.Frame(container, bg="white")
        buttons_frame.pack(fill="x")
        
        # Close button
        close_button = tk.Button(
            buttons_frame,
            text="Close",
            command=details_dialog.destroy,
            font=("Segoe UI", 10),
            bg="#E0E0E0",
            fg=self.text_color,
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        close_button.pack(side="left")
        self.add_hover_effect(close_button, "#E0E0E0", "#BDBDBD")
        
        # Add to cart button
        add_cart_button = tk.Button(
            buttons_frame,
            text="Add to Cart",
            command=lambda: [self.add_to_cart(), details_dialog.destroy()],
            font=("Segoe UI", 10, "bold"),
            bg=self.primary_color,
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        add_cart_button.pack(side="right")
        self.add_hover_effect(add_cart_button, self.primary_color)

    def show_notification(self, message, duration=2000):
        """Show a temporary notification message"""
        # Create notification window
        notification = tk.Toplevel(self.root)
        notification.overrideredirect(True)
        notification.configure(bg=self.primary_color)
        notification.attributes("-alpha", 0.9)
        
        # Calculate position
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 150
        y = self.root.winfo_y() + 100
        notification.geometry(f"300x50+{x}+{y}")
        
        # Add message
        message_label = tk.Label(
            notification,
            text=message,
            font=("Segoe UI", 11),
            fg="white",
            bg=self.primary_color,
            padx=10,
            pady=10
        )
        message_label.pack(fill="both", expand=True)
        
        # Auto-close after duration
        notification.after(duration, notification.destroy)

    def add_hover_effect(self, button, base_color, hover_color=None):
        """Adds hover effect to buttons."""
        if hover_color is None:
            # Create a darker shade of the base color
            r, g, b = self.root.winfo_rgb(base_color)
            r = max(0, int(r / 65535 * 0.8 * 65535))
            g = max(0, int(g / 65535 * 0.8 * 65535))
            b = max(0, int(b / 65535 * 0.8 * 65535))
            hover_color = f"#{r:04x}{g:04x}{b:04x}"

        def on_enter(event):
            button.config(bg=hover_color)

        def on_leave(event):
            button.config(bg=base_color)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

# Helper class for loading images
class ImageLoader:
    @staticmethod
    def load_image(file_path, width, height):
        try:
            from PIL import Image, ImageTk
            image = Image.open(file_path)
            image = image.resize((width, height), Image.LANCZOS)
            return ImageTk.PhotoImage(image)
        except:
            return None

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    # Set app icon (if available)
    try:
        root.iconbitmap("book_icon.ico")
    except:
        pass
    
    # Set window minimum size
    root.minsize(900, 600)
    
    # Apply a theme if available
    try:
        from ttkthemes import ThemedStyle
        style = ThemedStyle(root)
        style.set_theme("arc")  # Modern theme
    except:
        pass
    
    app = ViewDonatedBooksWindow(root, 1)  # 1 is a sample user_id
    root.mainloop()