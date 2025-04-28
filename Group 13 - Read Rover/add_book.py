import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class AddBookWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Add Book")
        self.root.geometry("400x300")

        ttk.Label(root, text="Title:").pack(pady=5)
        self.title_entry = ttk.Entry(root)
        self.title_entry.pack(pady=5)

        ttk.Label(root, text="Author:").pack(pady=5)
        self.author_entry = ttk.Entry(root)
        self.author_entry.pack(pady=5)

        ttk.Label(root, text="Price:").pack(pady=5)
        self.price_entry = ttk.Entry(root)
        self.price_entry.pack(pady=5)

        ttk.Label(root, text="Condition:").pack(pady=5)
        self.condition_entry = ttk.Entry(root)
        self.condition_entry.pack(pady=5)

        ttk.Button(root, text="Add Book", command=self.add_book).pack(pady=10)

    def create_connection(self):
        """Create a MySQL connection."""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='keera@13',  # Update with your MySQL password
                database='bookstore'
            )
            return connection
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
            return None

    def add_book(self):
        """Insert book details into the database."""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        price = self.price_entry.get().strip()
        condition = self.condition_entry.get().strip()

        if not title or not author or not price or not condition:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        try:
            price = float(price)
        except ValueError:
            messagebox.showwarning("Input Error", "Price must be a number!")
            return

        connection = self.create_connection()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO books (title, author, price, `condition`, status) VALUES (%s, %s, %s, %s, 'Available')",
                (title, author, price, condition)
            )
            connection.commit()
            messagebox.showinfo("Success", "Book added successfully!")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to add book: {e}")
        finally:
            connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AddBookWindow(root)
    root.mainloop()
