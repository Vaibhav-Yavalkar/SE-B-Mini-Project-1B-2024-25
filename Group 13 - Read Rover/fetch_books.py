import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# Function to create a MySQL connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='keera@13',
            database='bookstore'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to fetch available books from the database
def fetch_books():
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM books"  # Fetch book details (title, author, price, type, etc.)
            cursor.execute(query)
            books = cursor.fetchall()
            cursor.close()
            connection.close()
            return books
    except Error as e:
        print(f"Error: {e}")
        return []

# Main Window with Treeview (Table for displaying books)
class BookstoreWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookstore")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f4f8")

        # Title label
        title_label = tk.Label(root, text="Available Books", font=("Helvetica", 18, "bold"), bg="#f0f4f8")
        title_label.pack(pady=10)

        # Create a frame for Treeview (table)
        frame = tk.Frame(root, bg="#f0f4f8")
        frame.pack(fill=tk.BOTH, expand=True)

        # Set up the Treeview (table) to display books
        self.treeview = ttk.Treeview(frame, columns=("ID", "Title", "Author", "Price", "Type"), show="headings")
        
        # Define the columns in the table
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Title", text="Title")
        self.treeview.heading("Author", text="Author")
        self.treeview.heading("Price", text="Price")
        self.treeview.heading("Type", text="Type")
        
        # Configure column widths
        self.treeview.column("ID", width=50, anchor="center")
        self.treeview.column("Title", width=150, anchor="w")
        self.treeview.column("Author", width=150, anchor="w")
        self.treeview.column("Price", width=80, anchor="e")
        self.treeview.column("Type", width=100, anchor="w")
        
        # Add the Treeview to the frame and make it scrollable
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Scrollbars for the Treeview
        y_scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.treeview.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview.config(yscrollcommand=y_scrollbar.set)

        # Populate the Treeview with books
        self.populate_books()

    def populate_books(self):
        books = fetch_books()
        for book in books:
            self.treeview.insert("", tk.END, values=(book["id"], book["title"], book["author"], book["price"], book["type"]))

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BookstoreWindow(root)
    root.mainloop()
