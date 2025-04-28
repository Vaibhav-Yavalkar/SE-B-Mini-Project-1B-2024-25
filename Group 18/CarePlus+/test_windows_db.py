from db import Database
import mysql.connector
from mysql.connector import Error
import random
import string
import os
import sys
import subprocess

def check_mysql_service():
    print("\nChecking MySQL service status...")
    try:
        # Check if MySQL service is running
        result = subprocess.run(['sc', 'query', 'MySQL80'], capture_output=True, text=True)
        if 'RUNNING' in result.stdout:
            print("✓ MySQL service is running")
            return True
        else:
            print("✗ MySQL service is not running")
            print("Please start MySQL service using:")
            print("1. Open Services (services.msc)")
            print("2. Find 'MySQL80' service")
            print("3. Right-click and select 'Start'")
            return False
    except Exception as e:
        print(f"✗ Error checking MySQL service: {e}")
        return False

def test_mysql_installation():
    print("\nChecking MySQL installation...")
    try:
        import mysql.connector
        print("✓ MySQL Connector is installed")
        
        # Check MySQL Connector version
        version = mysql.connector.__version__
        print(f"✓ MySQL Connector version: {version}")
        
        # Check if pip is installed
        try:
            subprocess.run(['pip', '--version'], capture_output=True, check=True)
            print("✓ pip is installed")
        except:
            print("✗ pip is not installed")
            print("Please install pip first")
            return False
            
        return True
    except ImportError:
        print("✗ MySQL Connector is not installed")
        print("\nPlease install MySQL Connector using one of these methods:")
        print("1. Using pip:")
        print("   pip install mysql-connector-python")
        print("2. Or download from:")
        print("   https://dev.mysql.com/downloads/connector/python/")
        return False

def test_mysql_server():
    print("\nChecking MySQL server connection...")
    try:
        # First try without password
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root'
            )
            print("✓ Connected to MySQL server without password")
            conn.close()
            return True
        except:
            # If that fails, try with password
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Ary@n1974'
            )
            if conn.is_connected():
                print("✓ Connected to MySQL server with password")
                conn.close()
                return True
    except Error as e:
        print("✗ Could not connect to MySQL server")
        print(f"Error: {e}")
        print("\nTroubleshooting steps:")
        print("1. Is MySQL server installed?")
        print("   - Download from: https://dev.mysql.com/downloads/installer/")
        print("2. Is MySQL service running?")
        print("   - Open Services (services.msc)")
        print("   - Find 'MySQL' service")
        print("   - Make sure it's running")
        print("3. Are the credentials correct?")
        print("   - Default username: root")
        print("   - Check your password")
        print("4. Is MySQL running on the default port (3306)?")
        return False

def generate_random_username():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

def test_database_operations():
    print("\nTesting database operations...")
    try:
        print("Initializing database connection...")
        db = Database()
        print("✓ Database connection successful")
        
        # Test user operations
        test_username = generate_random_username()
        test_password = "test_password"
        
        print(f"\nTesting user operations with username: {test_username}")
        if db.add_user(test_username, test_password):
            print("✓ Added test user")
        else:
            print("✗ Failed to add test user")
            return False

        if db.verify_user(test_username, test_password):
            print("✓ Verified test user")
        else:
            print("✗ Failed to verify test user")
            return False

        # Test appointment
        print("\nTesting appointment operations...")
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
            print("✓ Added test appointment")
        else:
            print("✗ Failed to add test appointment")
            return False

        appointments = db.get_user_appointments(test_username)
        if len(appointments) > 0:
            print(f"✓ Retrieved {len(appointments)} appointments")
            print("\nAppointment details:")
            for appt in appointments:
                print(f"- Date: {appt['appointment_date']}, Time: {appt['appointment_time']}")
        else:
            print("✗ No appointments found")
            return False

        print("\n✓ All database operations completed successfully!")
        return True

    except Error as e:
        print(f"\n✗ Database error: {e}")
        print("\nError details:")
        print(f"Error code: {e.errno}")
        print(f"SQL State: {e.sqlstate}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

def main():
    print("CarePlus+ Database Test Utility")
    print("==============================")

    # Check MySQL service
    if not check_mysql_service():
        return

    # Check MySQL installation
    if not test_mysql_installation():
        return

    # Check MySQL server
    if not test_mysql_server():
        return

    # Test database operations
    test_database_operations()

if __name__ == "__main__":
    main() 