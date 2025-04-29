import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

# ✅ Correct database name
DATABASE_NAME = "bookstore"

def create_connection():
    """Create and return a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="keera@13",  # ✅ Ensure this is correct
            database=DATABASE_NAME
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"❌ Database Connection Error: {e}")
        messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")
    return None  # Return None if connection fails

def donate_book(title, author, condition, user_id):
    """Inserts donated book details into the database without an image."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='yourpassword',  # Replace with your actual password
            database='bookstore'
        )
        cursor = connection.cursor()
        query = """INSERT INTO books (title, author, `condition`, user_id, status) 
                   VALUES (%s, %s, %s, %s, 'Pending')"""
        cursor.execute(query, (title, author, condition, user_id))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except mysql.connector.Error as e:
        print("Database error:", e)
        return False

def list_book_for_sale():
    """Fetch all available books for sale."""
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT book_id, title, author, price, `condition` FROM books WHERE status = 'Available'"
            cursor.execute(query)
            books = cursor.fetchall()
            cursor.close()
            connection.close()
            return books
    except Error as e:
        print(f"Error: {e}")
        return []
    
def upload_image(book_id, image_path):
    """Upload image to database and store the image path."""
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            # Assuming you have a column `image` for storing the image path in the books table
            query = "UPDATE books SET image = %s WHERE book_id = %s"
            cursor.execute(query, (image_path, book_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True
    except Error as e:
        print(f"Error: {e}")
        return False
    
def fetch_wishlist(user_id):
    """Fetch all books in a user's wishlist."""
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT b.id, b.title, b.author, b.price, b.condition FROM wishlist w JOIN books b ON w.book_id = b.id WHERE w.user_id = %s"
            cursor.execute(query, (user_id,))
            wishlist = cursor.fetchall()  # Get all rows from the query
            cursor.close()
            connection.close()
            return wishlist
    except Error as e:
        print(f"Error: {e}")
        return []


# 📌 ✅ Fetch books from the database
def fetch_books():
    """Retrieve all books from the database."""
    connection = create_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT id, title, author, price, book_type, `condition`, status FROM books ORDER BY id DESC"
        cursor.execute(query)
        books = cursor.fetchall()
        return books if books else []
    except Error as e:
        print(f"❌ Fetch Books Error: {e}")
        messagebox.showerror("Error", f"Failed to fetch books: {e}")
        return []
    finally:
        if connection:
            cursor.close()
            connection.close()

# 📌 ✅ Save a new book to the database (No image)
def save_book(title, author, price, book_type, condition, user_id, status='Available'):
    """Insert a new book into the database (No image)."""
    connection = create_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO books (title, author, price, `condition`, book_type, status, user_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (title, author, price, condition, book_type, status, user_id))
        connection.commit()
        messagebox.showinfo("Success", "Book listed successfully!")
    except Error as e:
        connection.rollback()  # Rollback if an error occurs
        messagebox.showerror("Error", f"Failed to list book: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# 📌 ✅ Update book status (e.g., Available → Sold)
def update_book_status(book_id, status):
    """Update the status of a book."""
    connection = create_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE books SET status = %s WHERE id = %s", (status, book_id))
        connection.commit()
        return cursor.rowcount > 0
    except Error as e:
        connection.rollback()
        messagebox.showerror("Error", f"Failed to update book status: {e}")
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()

def mark_book_as_sold(book_id):
    return update_book_status(book_id, 'Sold')

def mark_book_as_available(book_id):
    return update_book_status(book_id, 'Available')

# 📌 ✅ Fetch book details before purchase
def get_book_by_id(book_id):
    """Retrieve book details by ID."""
    connection = create_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        return book
    except Error as e:
        print(f"❌ Error fetching book: {e}")
        return None
    finally:
        if connection:
            cursor.close()
            connection.close()

# 📌 ✅ Insert a purchase transaction
def insert_transaction(user_id, book_id, amount):
    """Insert a transaction into the database."""
    connection = create_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        query = "INSERT INTO transactions (user_id, book_id, amount) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, book_id, float(amount)))  # Ensure amount is float
        connection.commit()
        print("✅ Transaction inserted successfully.")
    except Error as e:
        connection.rollback()
        print(f"❌ Transaction Error: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# 📌 ✅ Buy a book (Checks availability, updates status, logs transaction)
def buy_book(user_id, book_id):
    """Handles the process of buying a book."""
    book = get_book_by_id(book_id)
    
    if not book:
        messagebox.showerror("Error", "Book not found!")
        return False
    
    if book['status'] != 'Available':
        messagebox.showerror("Error", "Book is no longer available!")
        return False
    
    amount = book['price']
    
    # ✅ 1. Mark book as sold
    if not mark_book_as_sold(book_id):
        messagebox.showerror("Error", "Failed to update book status!")
        return False
    
    # ✅ 2. Insert transaction record
    insert_transaction(user_id, book_id, amount)
    
    messagebox.showinfo("Success", "Purchase successful! Book marked as sold.")
    return True

# ✅ Test database connection
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        print("✅ Database connection successful!")
        conn.close()
    else:
        print("❌ Failed to connect to the database.")
