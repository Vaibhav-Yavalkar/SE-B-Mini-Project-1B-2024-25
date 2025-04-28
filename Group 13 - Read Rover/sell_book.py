import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import sys
import importlib

# Function to create MySQL connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='keera@13',
            database='bookstore'
        )
        return connection if connection.is_connected() else None
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to save the book into the database
def save_book(title, author, price, book_type, condition, user_id, status='Available'):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = "INSERT INTO books (title, author, price, book_type, `condition`, status, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (title, author, price, book_type, condition, status, user_id))

            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "Book listed for sale successfully!")
            return True
        else:
            messagebox.showerror("Error", "Failed to connect to the database.")
            return False
    except Error as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", "Failed to list book for sale.")
        return False

# Updated SellBookWindow to match dashboard style
class SellBookWindow:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Sell Book - Read Rover")
        self.root.geometry("450x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f7ff")

        # Main container
        self.main_frame = tk.Frame(self.root, bg="#f0f7ff")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Page title
        title_label = tk.Label(
            self.main_frame,
            text="Sell Your Book",
            font=("Helvetica", 22, "bold"),
            fg="#42a5f5",
            bg="#f0f7ff"
        )
        title_label.pack(pady=(10, 20))

        # Form container
        form_frame = tk.Frame(self.main_frame, bg="#f0f7ff")
        form_frame.pack(fill="both", expand=True)

        # Create entry fields
        self.entry_title = self.create_input_field(form_frame, "Title:", 0)
        self.entry_author = self.create_input_field(form_frame, "Author:", 1)
        self.entry_price = self.create_input_field(form_frame, "Price ($):", 2)
        
        # Book type dropdown
        self.book_type = self.create_dropdown(
            form_frame, 
            "Book Type:", 
            ["Fiction", "Non-Fiction", "Sci-Fi", "Romance", "Fantasy", "Biography"], 
            3
        )
        
        # Book condition dropdown
        self.book_condition = self.create_dropdown(
            form_frame, 
            "Condition:", 
            ["New", "Like New", "Used", "Very Used"], 
            4
        )

        # Buttons frame
        button_frame = tk.Frame(form_frame, bg="#f0f7ff")
        button_frame.pack(fill="x", pady=20)

        # Submit button
        submit_btn = tk.Button(
            button_frame,
            text="List Book for Sale",
            command=self.save_book,
            font=("Helvetica", 12, "bold"),
            bg="#42a5f5",
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        submit_btn.pack(side="left", padx=(0, 10))
        
        # Add hover effect to submit button
        self.add_hover_effect(submit_btn, "#42a5f5")

        # Back to Dashboard button
        back_btn = tk.Button(
            button_frame,
            text="Back to Dashboard",
            command=self.go_to_dashboard,
            font=("Helvetica", 12),
            bg="#e0e0e0",
            fg="#555555",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        back_btn.pack(side="left")
        
        # Add hover effect to back button
        self.add_hover_effect(back_btn, "#e0e0e0")

    def create_input_field(self, parent, label_text, row):
        """Create an input field with label."""
        # Container for each field
        field_frame = tk.Frame(parent, bg="#f0f7ff")
        field_frame.pack(fill="x", pady=10)
        
        # Label
        label = tk.Label(
            field_frame,
            text=label_text,
            font=("Helvetica", 12),
            anchor="w",
            bg="#f0f7ff",
            fg="#555555"
        )
        label.pack(fill="x")
        
        # Entry
        entry = tk.Entry(
            field_frame,
            font=("Helvetica", 11),
            bd=1,
            relief="solid"
        )
        entry.pack(fill="x", pady=(5, 0))
        
        return entry

    def create_dropdown(self, parent, label_text, values, row):
        """Create a dropdown with label."""
        # Container for the dropdown
        field_frame = tk.Frame(parent, bg="#f0f7ff")
        field_frame.pack(fill="x", pady=10)
        
        # Label
        label = tk.Label(
            field_frame,
            text=label_text,
            font=("Helvetica", 12),
            anchor="w",
            bg="#f0f7ff",
            fg="#555555"
        )
        label.pack(fill="x")
        
        # Dropdown
        dropdown = ttk.Combobox(
            field_frame,
            font=("Helvetica", 11),
            values=values,
            state="readonly"
        )
        dropdown.current(0)  # Set default value
        dropdown.pack(fill="x", pady=(5, 0))
        
        return dropdown

    def add_hover_effect(self, button, base_color):
        """Adds hover effect to buttons."""
        if base_color == "#42a5f5":  # Blue button
            hover_color = "#1e88e5"  # Darker blue
        else:  # Grey button
            hover_color = "#bdbdbd"  # Darker grey

        def on_enter(event):
            button.config(bg=hover_color)

        def on_leave(event):
            button.config(bg=base_color)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def clear_form(self):
        """Clear all form fields."""
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.book_type.current(0)
        self.book_condition.current(0)
        
        # Set focus back to title field
        self.entry_title.focus()

    def go_to_dashboard(self):
        """Return to the dashboard."""
        try:
            # Try to import the dashboard module
            if 'dashboard' in sys.modules:
                # If already imported, reload it
                dashboard_module = importlib.reload(sys.modules['dashboard'])
            else:
                # Import for the first time
                dashboard_module = importlib.import_module('dashboard')
            
            # Clear current window contents
            for widget in self.root.winfo_children():
                widget.destroy()
                
            # Initialize dashboard with the same root and user_id
            dashboard_module.DashboardWindow(self.root, self.user_id)
        except (ImportError, AttributeError) as e:
            print(f"Error returning to dashboard: {e}")
            # Fallback if dashboard module can't be loaded
            messagebox.showinfo("Navigation", "Returning to dashboard...")
            self.root.destroy()

    def save_book(self):
        """Handle book submission."""
        try:
            title = self.entry_title.get()
            author = self.entry_author.get()
            price = float(self.entry_price.get()) if self.entry_price.get() else 0
            book_type = self.book_type.get()
            condition = self.book_condition.get()

            if title and author and price > 0 and book_type and condition:
                success = save_book(title, author, price, book_type, condition, self.user_id)
                if success:
                    # Clear form instead of closing window
                    self.clear_form()
                    # Ask if user wants to list another book
                    list_another = messagebox.askyesno("Continue?", "Would you like to list another book?")
                    if not list_another:
                        # Return to dashboard instead of closing
                        self.go_to_dashboard()
            else:
                messagebox.showwarning("Input Error", "Please fill in all fields with valid values.")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid price.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SellBookWindow(root, 1)  # 1 is a sample user_id
    root.mainloop()