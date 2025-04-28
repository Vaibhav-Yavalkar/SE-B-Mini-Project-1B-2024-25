import mysql.connector
from mysql.connector import Error
import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/database.log'),
        logging.StreamHandler()
    ]
)

class Database:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Ary@n1974',
            'database': 'careplus_db',
            'auth_plugin': 'mysql_native_password'
        }
        self.connection = None
        self.connect()
        self.recreate_feedback_table()

    def connect(self):
        try:
            # First try to connect without database to create it if it doesn't exist
            config_without_db = self.db_config.copy()
            config_without_db.pop('database', None)
            
            temp_connection = mysql.connector.connect(**config_without_db)
            cursor = temp_connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_config['database']}")
            temp_connection.close()
            
            # Now connect to the database
            self.connection = mysql.connector.connect(**self.db_config)
            logging.info("Successfully connected to MySQL database")
            
            # Create tables if they don't exist
            self.create_tables()
            
        except Error as e:
            logging.error(f"Error connecting to MySQL: {e}")
            raise

    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create appointments table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    patient_name VARCHAR(100) NOT NULL,
                    gender VARCHAR(10) NOT NULL,
                    contact VARCHAR(15) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    diagnosis TEXT,
                    appointment_date DATE NOT NULL,
                    appointment_time TIME NOT NULL,
                    status VARCHAR(20) DEFAULT 'Pending',
                    notification_sent BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (username) REFERENCES users(username)
                )
            """)
            
            # Create notifications table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    message TEXT NOT NULL,
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (username) REFERENCES users(username)
                )
            """)
            
            # Create feedback table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    rating INT NOT NULL,
                    department VARCHAR(50) NOT NULL,
                    comments TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
                )
            """)
            
            # Create chat_messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    message TEXT NOT NULL,
                    is_bot BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (username) REFERENCES users(username)
                )
            """)
            
            self.connection.commit()
            logging.info("Successfully created all tables")
            
        except Error as e:
            logging.error(f"Error creating tables: {e}")
            raise

    def add_user(self, username, password):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            self.connection.commit()
            return True
        except Error as e:
            logging.error(f"Error adding user: {e}")
            return False

    def verify_user(self, username, password):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            return result and result[0] == password
        except Error as e:
            logging.error(f"Error verifying user: {e}")
            return False

    def add_appointment(self, username, patient_name, gender, contact, email, diagnosis, appointment_date, appointment_time, status="Pending"):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO appointments 
                (username, patient_name, gender, contact, email, diagnosis, appointment_date, appointment_time, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (username, patient_name, gender, contact, email, diagnosis, appointment_date, appointment_time, status))
            self.connection.commit()
            return True
        except Error as e:
            logging.error(f"Error adding appointment: {e}")
            return False

    def get_user_appointments(self, username):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM appointments 
                WHERE username = %s 
                ORDER BY appointment_date, appointment_time
            """, (username,))
            return cursor.fetchall()
        except Error as e:
            logging.error(f"Error getting user appointments: {e}")
            return []

    def get_all_appointments(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM appointments 
                ORDER BY appointment_date, appointment_time
            """)
            return cursor.fetchall()
        except Error as e:
            logging.error(f"Error getting all appointments: {e}")
            return []

    def get_all_users(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users ORDER BY username")
            return cursor.fetchall()
        except Error as e:
            logging.error(f"Error getting all users: {e}")
            return []

    def get_user_details(self, username):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            return cursor.fetchone()
        except Error as e:
            logging.error(f"Error getting user details: {e}")
            return None

    def update_appointment_status(self, username, date, time, new_status):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE appointments 
                SET status = %s 
                WHERE username = %s AND appointment_date = %s AND appointment_time = %s
            """, (new_status, username, date, time))
            self.connection.commit()
            return True
        except Error as e:
            logging.error(f"Error updating appointment status: {e}")
            return False

    def delete_user(self, username):
        try:
            cursor = self.connection.cursor()
            # First delete all appointments for the user
            cursor.execute("DELETE FROM appointments WHERE username = %s", (username,))
            # Then delete the user
            cursor.execute("DELETE FROM users WHERE username = %s", (username,))
            self.connection.commit()
            return True
        except Error as e:
            logging.error(f"Error deleting user: {e}")
            return False

    def get_appointments_in_range(self, start_date, end_date):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM appointments 
                WHERE appointment_date BETWEEN %s AND %s 
                ORDER BY appointment_date, appointment_time
            """, (start_date, end_date))
            return cursor.fetchall()
        except Error as e:
            logging.error(f"Error getting appointments in range: {e}")
            return []

    def add_notification(self, username, message):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO notifications (username, message)
                VALUES (%s, %s)
            """, (username, message))
            self.connection.commit()
            return True
        except Error as e:
            logging.error(f"Error adding notification: {e}")
            return False

    def get_unread_notifications(self, username):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM notifications 
                WHERE username = %s AND is_read = FALSE 
                ORDER BY created_at DESC
            """, (username,))
            return cursor.fetchall()
        except Error as e:
            logging.error(f"Error getting unread notifications: {e}")
            return []

    def mark_notifications_as_read(self, username):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE notifications 
                SET is_read = TRUE 
                WHERE username = %s AND is_read = FALSE
            """, (username,))
            self.connection.commit()
            return True
        except Error as e:
            logging.error(f"Error marking notifications as read: {e}")
            return False

    def add_feedback(self, username, rating, comments, department):
        try:
            # Validate inputs
            if not username or not rating or not department:
                logging.error("Missing required fields for feedback")
                return False
                
            # Validate rating is an integer between 1 and 5
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    logging.error(f"Invalid rating value: {rating}")
                    return False
            except ValueError:
                logging.error(f"Rating must be an integer, got: {rating}")
                return False
                
            # Validate department
            valid_departments = ["General", "Cardiology", "Orthopedics", "Pediatrics", "Dental", "Other"]
            if department not in valid_departments:
                logging.error(f"Invalid department: {department}")
                return False
                
            # Check if user exists
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            if not cursor.fetchone():
                logging.error(f"User not found: {username}")
                return False
                
            # Insert feedback
            cursor = self.connection.cursor()
            logging.info(f"Attempting to add feedback for user: {username}")
            logging.info(f"Feedback details - Rating: {rating}, Department: {department}")
            
            cursor.execute("""
                INSERT INTO feedback (username, rating, comments, department)
                VALUES (%s, %s, %s, %s)
            """, (username, rating, comments, department))
            
            self.connection.commit()
            logging.info("Feedback added successfully")
            return True
            
        except Error as e:
            logging.error(f"Error adding feedback: {e}")
            logging.error(f"Error code: {e.errno}")
            logging.error(f"SQL State: {e.sqlstate}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error adding feedback: {e}")
            return False

    def add_chat_message(self, username, message, is_bot=False):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO chat_messages (username, message, is_bot)
                VALUES (%s, %s, %s)
            """, (username, message, is_bot))
            self.connection.commit()
            return True
        except Error as e:
            logging.error(f"Error adding chat message: {e}")
            return False

    def get_chat_history(self, username, limit=50):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM chat_messages 
                WHERE username = %s 
                ORDER BY created_at DESC 
                LIMIT %s
            """, (username, limit))
            return cursor.fetchall()
        except Error as e:
            logging.error(f"Error getting chat history: {e}")
            return []

    def delete_appointment(self, username, date, time):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                DELETE FROM appointments 
                WHERE username = %s AND appointment_date = %s AND appointment_time = %s
            """, (username, date, time))
            self.connection.commit()
            return True
        except Exception as e:
            logging.error(f"Error deleting appointment: {e}")
            return False

    def check_appointment_notifications(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            today = datetime.now().date()
            
            # Get all appointments for today that haven't had notifications sent
            cursor.execute("""
                SELECT a.*, u.username 
                FROM appointments a
                JOIN users u ON a.username = u.username
                WHERE a.appointment_date = %s 
                AND a.notification_sent = FALSE
                AND a.status != 'Cancelled'
            """, (today,))
            
            appointments = cursor.fetchall()
            
            for appointment in appointments:
                # Create notification message
                message = f"Reminder: You have an appointment today at {appointment['appointment_time']} with Dr. Smith"
                
                # Add notification
                cursor.execute("""
                    INSERT INTO notifications (username, message)
                    VALUES (%s, %s)
                """, (appointment['username'], message))
                
                # Mark notification as sent
                cursor.execute("""
                    UPDATE appointments 
                    SET notification_sent = TRUE 
                    WHERE id = %s
                """, (appointment['id'],))
            
            self.connection.commit()
            return True
        except Error as e:
            logging.error(f"Error checking appointment notifications: {e}")
            return False

    def delete_test_appointments(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM appointments WHERE patient_name = 'Test Patient'")
            self.connection.commit()
            return True
        except Error as e:
            logging.error(f"Error deleting test appointments: {e}")
            return False

    def is_slot_available(self, date, time):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM appointments 
                WHERE appointment_date = %s 
                AND appointment_time = %s 
                AND status != 'Cancelled'
            """, (date, time))
            result = cursor.fetchone()
            return result['count'] == 0
        except Error as e:
            logging.error(f"Error checking slot availability: {e}")
            return False

    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logging.info("Database connection closed")

    def recreate_feedback_table(self):
        try:
            cursor = self.connection.cursor()
            # Drop existing feedback table if it exists
            cursor.execute("DROP TABLE IF EXISTS feedback")
            
            # Create feedback table with correct structure
            cursor.execute("""
                CREATE TABLE feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    rating INT NOT NULL,
                    department VARCHAR(50) NOT NULL,
                    comments TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
                )
            """)
            self.connection.commit()
            logging.info("Feedback table recreated successfully")
        except Error as e:
            logging.error(f"Error recreating feedback table: {e}")
            raise 