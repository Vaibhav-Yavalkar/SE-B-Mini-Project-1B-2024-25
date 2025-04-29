import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create and return a database connection."""
    try:
        connection = mysql.connector.connect(
            host='localhost',          # Host where the MySQL server is running (usually localhost)
            user='root',      # Replace with your MySQL username
            password='keera@13',  # Replace with your MySQL password
            database='bookstore'       # Replace with your database name
        )

        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def close_connection(connection):
    """Close the database connection."""
    if connection.is_connected():
        connection.close()
        print("Connection closed")

# Test the connection
if __name__ == "__main__":
    connection = create_connection()
    if connection:
        # Perform any queries if needed
        close_connection(connection)
