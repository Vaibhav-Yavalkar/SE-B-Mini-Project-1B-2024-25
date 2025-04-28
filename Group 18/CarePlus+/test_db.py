from db import Database
import mysql.connector
from mysql.connector import Error
import random
import string

def generate_random_username():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

def test_database_connection():
    try:
        # First, try to connect without database to create it if it doesn't exist
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Ary@n1974'
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS careplus_db")
        cursor.close()
        connection.close()
        print("Database 'careplus_db' created or already exists")

        # Now try to connect with the database
        db = Database()
        
        # Test user operations with random username to avoid conflicts
        test_username = generate_random_username()
        test_password = "test_password"
        
        # Test adding a user
        if db.add_user(test_username, test_password):
            print(f"Successfully added test user: {test_username}")
        else:
            print("Failed to add test user")
            return False

        # Test verifying the user
        if db.verify_user(test_username, test_password):
            print("Successfully verified test user")
        else:
            print("Failed to verify test user")
            return False

        # Test adding an appointment
        if db.add_appointment(
            test_username,
            "Test Patient",
            "Male",
            "1234567890",
            "test@example.com",
            "Test Diagnosis",
            "2024-03-20",
            "10:00:00"
        ):
            print("Successfully added test appointment")
        else:
            print("Failed to add test appointment")
            return False

        # Test getting appointments
        appointments = db.get_user_appointments(test_username)
        print(f"Found {len(appointments)} appointments for test user")
        if len(appointments) == 0:
            print("Error: No appointments found after adding one")
            return False

        print("\nAll database operations completed successfully!")
        return True

    except Error as e:
        print(f"\nError: {e}")
        print("\nPlease check the following:")
        print("1. Is MySQL server installed and running?")
        print("2. Are the credentials correct?")
        print("3. Is MySQL server accessible on localhost?")
        print("4. Is the MySQL Connector for Python installed?")
        return False

if __name__ == "__main__":
    test_database_connection() 