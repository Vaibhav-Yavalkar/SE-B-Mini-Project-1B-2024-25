import mysql.connector
import hashlib
import os
import uuid
from dotenv import load_dotenv
from datetime import datetime

class DatabaseHandler:
    def __init__(self, host=None, user=None, password=None, database=None):
        """
        Initialize database connection parameters and connection
        
        :param host: Database host (optional, uses env var or default)
        :param user: Database user (optional, uses env var or default)
        :param password: Database password (optional, uses env var or default)
        :param database: Database name (optional, uses env var or default)
        """
        # Load environment variables
        load_dotenv()
        
        # Store connection parameters with fallback to environment variables
        self.connection_params = {
            'host': host or os.getenv('DB_HOST', 'localhost'),
            'user': user or os.getenv('DB_USER', 'root'),
            'password': password or os.getenv('DB_PASSWORD', '12345678'),
            'database': database or os.getenv('DB_NAME', 'CrowdNest'),
            'buffered': True
        }
        
        # Initialize connection and cursor
        self.connection = None
        self.cursor = None
        
        # Establish initial connection
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        try:
            # Establish connection
            self.connection = mysql.connector.connect(
                host=self.connection_params['host'],
                user=self.connection_params['user'],
                password=self.connection_params['password'],
                database=self.connection_params['database'],
                buffered=True
            )
            
            # Create cursor with dictionary support
            self.cursor = self.connection.cursor(dictionary=True)
            
            print("Successfully connected to MySQL database")
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL Platform: {e}")
            raise
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        try:
            # Hash the provided password
            hashed_password = self.hash_password(password)
            
            # Query to check user credentials
            query = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
            self.cursor.execute(query, (username, hashed_password))
            
            user = self.cursor.fetchone()
            
            if user:
                # Remove sensitive information
                user.pop('password_hash', None)
                return user
            return None
        
        except mysql.connector.Error as e:
            print(f"Authentication error: {e}")
            return None
    
    def register_user(self, username, email, password, location=None):
        """Register a new user"""
        try:
            # Generate unique ID
            unique_id = str(uuid.uuid4())
            
            # Hash the password
            hashed_password = self.hash_password(password)
            
            # Prepare the query
            query = """
            INSERT INTO users 
            (unique_id, username, email, password_hash, location, created_at) 
            VALUES (%s, %s, %s, %s, %s, NOW())
            """
            
            # Execute the query
            self.cursor.execute(query, (
                unique_id,
                username,
                email,
                hashed_password,
                location
            ))
            
            # Commit the transaction
            self.connection.commit()
            
            return unique_id
        
        except mysql.connector.Error as e:
            print(f"Registration error: {e}")
            self.connection.rollback()
            return None
    
    def change_user_password(self, user_id, old_password, new_password):
        """Change user password"""
        try:
            # Hash passwords
            old_hashed_password = self.hash_password(old_password)
            new_hashed_password = self.hash_password(new_password)
            
            # Verify old password first
            verify_query = "SELECT * FROM users WHERE unique_id = %s AND password_hash = %s"
            self.cursor.execute(verify_query, (user_id, old_hashed_password))
            
            if not self.cursor.fetchone():
                return False
            
            # Update password
            update_query = "UPDATE users SET password_hash = %s WHERE unique_id = %s"
            self.cursor.execute(update_query, (new_hashed_password, user_id))
            self.connection.commit()
            
            return True
        
        except mysql.connector.Error as e:
            print(f"Password change error: {e}")
            self.connection.rollback()
            return False
    
    def get_user_details(self, user_id):
        """Get complete user details including profile information"""
        try:
            query = """
            SELECT u.*, 
                COUNT(DISTINCT d.unique_id) as total_donations,
                COUNT(DISTINCT r.unique_id) as total_requests
            FROM users u
            LEFT JOIN donations d ON u.unique_id = d.donor_id
            LEFT JOIN requests r ON u.unique_id = r.requester_id
            WHERE u.unique_id = %s
            GROUP BY u.unique_id
            """
            self.cursor.execute(query, (user_id,))
            user_details = self.cursor.fetchone()
            
            if user_details:
                # Remove sensitive information
                user_details.pop('password_hash', None)
                return user_details
            return None
            
        except mysql.connector.Error as e:
            print(f"Error fetching user details: {e}")
            return None
    
    def add_donation(self, donor_id, title, description, category, condition, state, city, image_path=None):
        """
        Legacy method to maintain backwards compatibility with existing calls
        
        :param donor_id: Unique ID of the donor
        :param title: Title of the donation
        :param description: Description of the donation
        :param category: Category of the donation
        :param condition: Condition of the donated item
        :param state: State where the donation is located
        :param city: City where the donation is located
        :param image_path: Optional path to donation image
        :return: Boolean indicating success
        """
        try:
            # If image_path is a file path, read the image data
            image_data = None
            image_type = None
            if image_path and os.path.isfile(image_path):
                with open(image_path, 'rb') as f:
                    image_data = f.read()
                image_type = os.path.splitext(image_path)[1][1:].lower()  # e.g., 'png', 'jpg'
            
            # Use create_donation method
            success, message, donation_data = self.create_donation(
                donor_id=donor_id,
                title=title,
                description=description,
                category=category,
                condition=condition,
                state=state,
                city=city,
                image_data=image_data,
                image_type=image_type
            )
            
            return success
        
        except Exception as e:
            print(f"Error in add_donation: {e}")
            return False
    
    def search_requests(self, search_query=None, status=None, donor_id=None, category=None):
        """
        Search donation requests with flexible parameters
        
        :param search_query: Optional text to search in request message
        :param status: Optional status filter (can be a single status or None)
        :param donor_id: Optional donor ID to filter requests for a specific donor
        :param category: Optional category filter
        :return: List of matching donation requests
        """
        try:
            # Base query with joins to get more details
            base_query = """
            SELECT 
                dr.*, 
                u.username as requester_name, 
                u.email as requester_email,
                d.title as donation_title,
                d.description as donation_description,
                d.category as donation_category,
                d.donor_id
            FROM donation_requests dr
            JOIN users u ON dr.requester_id = u.unique_id
            LEFT JOIN donations d ON dr.donation_id = d.unique_id
            WHERE 1=1
            """
            params = []

            # Add search conditions with input validation
            if search_query and isinstance(search_query, str):
                base_query += " AND dr.request_message LIKE %s"
                params.append(f"%{search_query}%")

            # Handle status filtering
            if status and isinstance(status, str):
                base_query += " AND dr.status = %s"
                params.append(status.lower())
            elif status is None:
                # If no status specified, include all except completed or withdrawn
                base_query += " AND dr.status NOT IN ('completed', 'withdrawn')"
            
            # Filter by donor ID if provided
            if donor_id and isinstance(donor_id, str):
                base_query += " AND d.donor_id = %s"
                params.append(donor_id)
            
            # Filter by category if provided
            if category and isinstance(category, str) and category != 'All':
                base_query += " AND d.category = %s"
                params.append(category)

            # Always order by most recent first
            base_query += " ORDER BY dr.created_at DESC"
            
            # Execute query
            self.cursor.execute(base_query, params)
            results = self.cursor.fetchall()

            # Additional processing to ensure consistent data
            processed_results = []
            for result in results:
                processed_result = dict(result)
                # Ensure consistent keys and formatting
                processed_result['status'] = processed_result.get('status', 'unknown').capitalize()
                processed_result['created_at'] = processed_result.get('created_at')
                processed_results.append(processed_result)

            return processed_results
            
        except mysql.connector.Error as e:
            print(f"Error searching requests: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error in search_requests: {e}")
            return []
    
    def get_request_details_by_message(self, request_message_or_id):
        """
        Retrieve comprehensive details about a donation request
        
        :param request_message_or_id: Request message or unique ID
        :return: Dictionary with detailed request information
        """
        # Extensive logging of input
        print("=" * 50)
        print("GET REQUEST DETAILS DEBUG")
        print(f"Input type: {type(request_message_or_id)}")
        print(f"Input value: {request_message_or_id}")
        print(f"Input str representation: '{str(request_message_or_id)}'")
        print("=" * 50)
        
        try:
            # Validate and clean input
            if not request_message_or_id:
                print("Error: Empty request message or ID provided")
                return None
            
            # Convert to string if not already
            request_message_or_id = str(request_message_or_id).strip()
            
            # Prepare multiple search queries to increase chances of finding the request
            search_queries = [
                # Full detailed query with exact match
                ("""
                SELECT 
                    dr.unique_id, 
                    dr.requester_id, 
                    dr.donation_id, 
                    dr.request_message, 
                    dr.status,
                    u.username as requester_username,
                    u.email as requester_email,
                    d.title as donation_title,
                    d.description as donation_description,
                    d.donor_id,
                    donor.username as donor_name,
                    donor.email as donor_email,
                    dr.created_at
                FROM donation_requests dr
                JOIN users u ON dr.requester_id = u.unique_id
                JOIN donations d ON dr.donation_id = d.unique_id
                JOIN users donor ON d.donor_id = donor.unique_id
                WHERE 
                    dr.unique_id = %s OR 
                    dr.request_message = %s
                """, (request_message_or_id, request_message_or_id)),
                
                # Simplified query with fewer joins
                ("""
                SELECT 
                    unique_id, 
                    requester_id, 
                    donation_id, 
                    request_message, 
                    status
                FROM donation_requests
                WHERE 
                    unique_id = %s OR 
                    request_message = %s
                """, (request_message_or_id, request_message_or_id)),
                
                # Partial match query
                ("""
                SELECT 
                    unique_id, 
                    requester_id, 
                    donation_id, 
                    request_message, 
                    status
                FROM donation_requests
                WHERE 
                    unique_id LIKE %s OR 
                    request_message LIKE %s
                """, (f"%{request_message_or_id}%", f"%{request_message_or_id}%"))
            ]
            
            # Try each query until a result is found
            for query, params in search_queries:
                print(f"Executing query: {query}")
                print(f"With parameters: {params}")
                
                self.cursor.execute(query, params)
                result = self.cursor.fetchone()
                
                if result:
                    # Convert result to dictionary and print for debugging
                    result_dict = dict(result)
                    
                    # Extensive logging
                    print("=" * 50)
                    print("REQUEST DETAILS FOUND:")
                    for key, value in result_dict.items():
                        print(f"{key}: {value}")
                    print("=" * 50)
                    
                    return result_dict
            
            # If no results found, print out all requests for debugging
            print("=" * 50)
            print("DEBUGGING: NO MATCHING REQUEST FOUND")
            print(f"Searched for: {request_message_or_id}")
            
            # List all requests
            list_all_query = """
            SELECT 
                unique_id, 
                request_message, 
                donation_id, 
                status,
                requester_id
            FROM donation_requests
            """
            self.cursor.execute(list_all_query)
            all_requests = self.cursor.fetchall()
            
            print("ALL DONATION REQUESTS:")
            for req in all_requests:
                print(req)
            print("=" * 50)
            
            return None
        
        except mysql.connector.Error as e:
            print(f"Database error retrieving request details: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error retrieving request details: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_request_details(self, request_id):
        """
        Retrieve details about a specific request using its unique ID
        
        :param request_id: Unique identifier of the request
        :return: Dictionary with request details or None
        """
        return self.get_request_details_by_message(request_id)

    def create_donation_request(self, user_id, title, description, category, condition, state, city, urgency, donation_id=None):
        """
        Create a new donation request and send email notifications
        
        :param user_id: ID of the requester
        :param title: Title of the request
        :param description: Description of the request
        :param category: Category of the requested item
        :param condition: Condition of the requested item
        :param state: State location
        :param city: City location
        :param urgency: Urgency level of the request
        :param donation_id: Optional ID of an existing donation
        :return: Tuple (success, message, request_id)
        """
        try:
            # Generate unique ID for the request
            request_id = str(uuid.uuid4())
            
            # Begin transaction
            self.connection.start_transaction()
            
            # Create the request
            query = """
            INSERT INTO donation_requests 
            (unique_id, requester_id, donation_id, request_message, status, created_at)
            VALUES (%s, %s, %s, %s, 'pending', NOW())
            """
            
            self.cursor.execute(query, (
                request_id,
                user_id,
                donation_id,
                description
            ))
            
            # Commit transaction
            self.connection.commit()
            
            return True, "Request created successfully", request_id
            
        except mysql.connector.Error as e:
            self.connection.rollback()
            error_message = f"Database error creating request: {e}"
            print(error_message)
            return False, error_message, None
            
        except Exception as e:
            self.connection.rollback()
            error_message = f"Unexpected error creating request: {e}"
            print(error_message)
            return False, error_message, None
    
    def get_user_donation_requests(self, user_id):
        """
        Retrieve all donation requests for a specific user

        :param user_id: ID of the user
        :return: List of donation requests or None
        """
        try:
            # Prepare the SQL query
            query = """
            SELECT 
                dr.unique_id,
                dr.request_message,
                d.title, 
                d.description, 
                d.category, 
                d.`condition`, 
                d.state, 
                d.city, 
                dr.status,
                dr.created_at
            FROM 
                donation_requests dr
            LEFT JOIN
                donations d ON dr.donation_id = d.unique_id
            WHERE 
                dr.requester_id = %s
            ORDER BY 
                dr.created_at DESC
            """
            
            # Execute the query
            self.cursor.execute(query, (user_id,))
            
            # Fetch all results
            results = self.cursor.fetchall()
            
            # Convert to list of dictionaries
            donation_requests = []
            for result in results:
                request = {
                    'unique_id': result['unique_id'],
                    'request_message': result['request_message'],
                    'title': result['title'],
                    'description': result['description'],
                    'category': result['category'],
                    'condition': result['condition'],
                    'state': result['state'],
                    'city': result['city'],
                    'status': result['status'],
                    'created_at': result['created_at']
                }
                donation_requests.append(request)
            
            return donation_requests
        
        except mysql.connector.Error as e:
            print(f"MySQL Error retrieving donation requests: {e}")
            return None
        
        except Exception as e:
            print(f"Unexpected error retrieving donation requests: {e}")
            return None
    
    def update_request_status(self, request_id, new_status, user_id=None):
        """
        Update the status of a donation request and send email notification
        
        :param request_id: Unique ID of the request to update
        :param new_status: New status for the request
        :param user_id: ID of the user making the status change (optional)
        :return: Boolean indicating success or failure
        """
        try:
            # Import email notification here to avoid circular imports
            from src.utils.email_notification import EmailNotification
            
            # Validate inputs
            if not request_id or not new_status:
                print("Error: Request ID and new status are required")
                return False
            
            # Validate status
            valid_statuses = ['pending', 'approved', 'rejected', 'completed']
            if new_status.lower() not in valid_statuses:
                print(f"Error: Invalid status. Must be one of {valid_statuses}")
                return False
            
            # Begin transaction - check if one is already in progress
            if not self.connection.in_transaction:
                self.connection.start_transaction()
            
            # Fetch current request details
            self.cursor.execute("""
                SELECT 
                    dr.unique_id, 
                    dr.request_message, 
                    dr.requester_id,
                    u.email as requester_email,
                    d.title as donation_title
                FROM donation_requests dr
                JOIN users u ON dr.requester_id = u.unique_id
                JOIN donations d ON dr.donation_id = d.unique_id
                WHERE dr.unique_id = %s
            """, (request_id,))
            request_details = self.cursor.fetchone()
            
            if not request_details:
                print(f"Error: No request found with ID {request_id}")
                self.connection.rollback()
                return False
            
            # Update request status
            update_query = """
            UPDATE donation_requests 
            SET 
                status = %s, 
                updated_at = CURRENT_TIMESTAMP
            WHERE unique_id = %s
            """
            
            # Use the provided user_id or use NULL
            update_params = (
                new_status.lower(), 
                request_id
            )
            
            self.cursor.execute(update_query, update_params)
            
            # Commit transaction
            self.connection.commit()
            
            # Send email notification
            try:
                from src.utils.email_sender import send_email
                from src.utils.html_email_templates import HTMLEmailTemplates
                
                # Create email subject
                email_subject = f"Your donation request status has been updated: {new_status.capitalize()}"
                
                # Use HTML template for status update
                email_body = HTMLEmailTemplates.generate_request_status_email(
                    status=new_status.lower(),
                    request_details={
                        'donation_title': request_details['donation_title'],
                        'requester_username': request_details['requester_id'],
                        'request_message': request_details['request_message']
                    }
                )
                
                # Send email with HTML template
                send_email(
                    to_email=request_details['requester_email'],
                    subject=email_subject,
                    body=email_body
                )
                
                print(f"Email notification sent to {request_details['requester_email']} for status update to {new_status}")
            except Exception as email_error:
                print(f"Warning: Failed to send email notification: {email_error}")
                import traceback
                traceback.print_exc()
            
            print(f"Successfully updated request {request_id} to status {new_status}")
            return True
        
        except mysql.connector.Error as e:
            # Rollback transaction on error
            self.connection.rollback()
            print(f"MySQL Error updating request status: {e}")
            return False
        except Exception as e:
            # Rollback transaction on unexpected error
            self.connection.rollback()
            print(f"Unexpected error updating request status: {e}")
            return False

    def create_donation(self, donor_id, title, description, category, condition, state, city, status='available', image_data=None, image_type=None):
        """
        Create a new donation in the database

        :param donor_id: Unique ID of the donor
        :param title: Title of the donation
        :param description: Description of the donation
        :param category: Category of the donation
        :param condition: Condition of the donated item
        :param state: State where the donation is located
        :param city: City where the donation is located
        :param status: Status of the donation (default 'available')
        :param image_data: Optional image data (bytes)
        :param image_type: Optional image type (e.g., 'png', 'jpeg')
        :return: Tuple (success_bool, message_str, donation_dict)
        """
        try:
            # Verify donor exists and get their email
            verify_donor_query = "SELECT email, username FROM users WHERE unique_id = %s"
            self.cursor.execute(verify_donor_query, (donor_id,))
            donor = self.cursor.fetchone()
            
            if not donor:
                return False, f"Donor with ID {donor_id} does not exist", None
            
            # Extract donor email and username
            donor_email = donor.get('email')
            donor_username = donor.get('username')
            
            # Generate unique ID for the donation
            unique_id = str(uuid.uuid4())
            
            # Prepare the query with escaped keywords
            query = """
            INSERT INTO donations 
            (unique_id, donor_id, title, description, category, 
            `condition`, state, city, status, image_data, image_type) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Execute the query
            self.cursor.execute(query, (
                unique_id,
                donor_id,
                title,
                description,
                category,
                condition,
                state,
                city,
                status,
                image_data,  # Raw image bytes or None
                image_type   # Image type or None
            ))
            
            # Commit the transaction
            self.connection.commit()
            
            # Debugging: Print full donation details
            print("Donation Creation Debug:")
            print(f"Unique ID: {unique_id}")
            print(f"Donor ID: {donor_id}")
            print(f"Title: {title}")
            print(f"Description: {description}")
            print(f"Category: {category}")
            print(f"Condition: {condition}")
            print(f"State: {state}")
            print(f"City: {city}")
            print(f"Status: {status}")
            print(f"Donor Email: {donor_email}")
            print(f"Donor Username: {donor_username}")
            
            # Perform direct database check after insertion
            direct_check_query = """
            SELECT 
                unique_id, donor_id, title, description, category, 
                `condition`, state, city, status 
            FROM donations 
            WHERE unique_id = %s
            """
            
            # Execute direct check
            self.cursor.execute(direct_check_query, (unique_id,))
            direct_check_result = self.cursor.fetchone()
            
            print("\nDirect Database Check:")
            if direct_check_result:
                print("Donation found in database immediately after insertion:")
                for key, value in direct_check_result.items():
                    print(f"{key}: {value}")
            else:
                print(f"WARNING: No donation found with ID {unique_id} immediately after insertion!")
            
            # List all donations to help diagnose
            try:
                self.cursor.execute("SELECT unique_id, title, donor_id FROM donations")
                all_donations = self.cursor.fetchall()
                print("\nRefresh method called. Donations found:", len(all_donations))
                for donation in all_donations:
                    print(f"Donation ID: {donation['unique_id']}, Title: {donation['title']}, Donor ID: {donation['donor_id']}")
                
                # Specific check for the newly created donation
                specific_check = self.get_donation_by_id(unique_id)
                if not specific_check:
                    print(f"No donation found with ID {unique_id}")
            except Exception as list_error:
                print(f"Error listing donations: {list_error}")
            
            # Prepare donation dictionary
            donation_data = {
                'unique_id': unique_id,
                'donor_id': donor_id,
                'donor_email': donor_email,
                'donor_username': donor_username,
                'title': title,
                'description': description,
                'category': category,
                'condition': condition,
                'state': state,
                'city': city,
                'status': status,
                'image_type': image_type
            }
            
            # Trigger UI update for donations list if possible
            try:
                # Attempt to find and call a method to refresh donations list
                from src.pages.donation_list_page import DonationListPage
                for instance in DonationListPage.instances:
                    instance.refresh_donations([donation_data])
            except Exception as e:
                print(f"Could not automatically refresh donations list: {e}")
            
            return True, f"Donation '{title}' created successfully with ID {unique_id}", donation_data
        
        except mysql.connector.Error as e:
            print(f"Error creating donation: {e}")
            self.connection.rollback()
            return False, f"Database error: {str(e)}", None
    
    def update_donation_status(self, donation_id, new_status):
        """
        Update the status of a donation
        
        :param donation_id: Unique ID of the donation
        :param new_status: New status for the donation
        :return: Boolean indicating success of the update
        """
        try:
            # Validate status
            valid_statuses = ['available', 'unavailable', 'pending', 'completed', 'reserved', 'withdrawn']
            if new_status.lower() not in valid_statuses:
                print(f"Invalid donation status: {new_status}")
                return False

            # Update query
            update_query = """
            UPDATE donations 
            SET status = %s, updated_at = NOW() 
            WHERE unique_id = %s
            """
            
            # Execute update
            self.cursor.execute(update_query, (new_status.lower(), donation_id))
            self.connection.commit()

            # Check if any rows were affected
            if self.cursor.rowcount > 0:
                print(f"Donation status updated to {new_status}")
                return True
            else:
                print(f"No donation found with ID: {donation_id}")
                return False

        except mysql.connector.Error as e:
            print(f"Database error updating donation status: {e}")
            self.connection.rollback()
            return False
        except Exception as e:
            print(f"Unexpected error updating donation status: {e}")
            return False

    def get_donation_status(self, donation_id):
        """
        Retrieve the current status of a donation

        :param donation_id: Unique ID of the donation
        :return: Tuple (status_str or None, message_str)
        """
        # Validate input
        if not donation_id:
            return None, "Invalid donation ID provided"
        
        try:
            # Ensure database connection is active
            if not self.connection.is_connected():
                self.reconnect()
            
            # Reset cursor to ensure it's in a good state
            self.reset_cursor()
            
            # Prepare the query with additional error checking
            query = """
            SELECT status, unique_id FROM donations 
            WHERE unique_id = %s
            """
            
            # Execute the query with error handling
            try:
                self.cursor.execute(query, (donation_id,))
            except mysql.connector.Error as exec_err:
                print(f"Query execution error: {exec_err}")
                return None, f"Database query error: {str(exec_err)}"
            
            # Fetch the result
            result = self.cursor.fetchone()
            
            if result:
                # Verify the donation ID matches
                if result['unique_id'] == donation_id:
                    return result['status'], "Donation status retrieved successfully"
                else:
                    print(f"Mismatched donation ID: expected {donation_id}, got {result['unique_id']}")
                    return None, "Donation ID mismatch"
            else:
                print(f"No donation found with ID {donation_id}")
                return None, f"No donation found with ID {donation_id}"
        
        except mysql.connector.Error as e:
            print(f"MySQL Connector Error retrieving donation status: {e}")
            # Log the specific error details
            if hasattr(e, 'errno'):
                print(f"MySQL Error Number: {e.errno}")
                print(f"MySQL Error State: {e.sqlstate}")
            return None, f"Database error: {str(e)}"
        
        except Exception as e:
            print(f"Unexpected error retrieving donation status: {e}")
            # Log the full traceback for debugging
            import traceback
            traceback.print_exc()
            return None, f"Unexpected error: {str(e)}"
        
        finally:
            # Ensure cursor is reset after operation
            try:
                self.reset_cursor()
            except Exception as reset_err:
                print(f"Error resetting cursor: {reset_err}")

    def reset_cursor(self):
        """Reset the database cursor"""
        try:
            # Close existing cursor if it exists
            if self.cursor:
                self.cursor.close()
            
            # Recreate cursor with dictionary support
            self.cursor = self.connection.cursor(dictionary=True)
        except mysql.connector.Error as e:
            print(f"Error resetting cursor: {e}")
            # Attempt to reconnect if cursor reset fails
            try:
                self.connect()
            except Exception as reconnect_error:
                print(f"Failed to reconnect: {reconnect_error}")
                raise
    
    def close(self):
        """Close database connection and cursor"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            print("Database connection closed successfully")
        except mysql.connector.Error as e:
            print(f"Error closing database connection: {e}")

    def create_donation_request(self, user_id, title, description, category, condition, state, city, urgency=None):
        """
        Create a new donation request with comprehensive validation and error handling.

        :param user_id: ID of the user creating the request
        :param title: Title of the donation request
        :param description: Detailed description of the needed donation
        :param category: Category of the donation
        :param condition: Condition of the requested item
        :param state: State where the donation is needed
        :param city: City where the donation is needed
        :param urgency: Optional urgency level of the request
        :return: Tuple (success, message, request_id)
        """
        # Validate input parameters
        def validate_input():
            # Check for empty or None values
            if not all([user_id, title, description, category, condition, state, city]):
                return False, "All fields are required"
            
            # Validate title length
            if len(title) < 5 or len(title) > 100:
                return False, "Title must be between 5 and 100 characters"
            
            # Validate description length
            if len(description) < 10 or len(description) > 500:
                return False, "Description must be between 10 and 500 characters"
            
            # Validate category
            valid_categories = ['Clothing', 'Food', 'Books', 'Electronics', 'Furniture', 'Other']
            if category not in valid_categories:
                return False, f"Invalid category. Must be one of {', '.join(valid_categories)}"
            
            # Validate condition
            valid_conditions = ['New', 'Like New', 'Good', 'Acceptable']
            if condition not in valid_conditions:
                return False, f"Invalid condition. Must be one of {', '.join(valid_conditions)}"
            
            # Validate urgency
            valid_urgencies = ['Low', 'Medium', 'High']
            if urgency and urgency.capitalize() not in valid_urgencies:
                return False, f"Invalid urgency. Must be one of {', '.join(valid_urgencies)}"
            
            return True, "Validation successful"

        # Validate inputs first
        validation_result, validation_message = validate_input()
        if not validation_result:
            return False, validation_message, None

        try:
            # Verify user exists and get current total_requests
            self.cursor.execute("SELECT * FROM users WHERE unique_id = %s", (user_id,))
            user = self.cursor.fetchone()
            if not user:
                return False, "User does not exist", None
            
            # Prepare the SQL query with additional validation
            query = """
            INSERT INTO donation_requests (
                requester_id, 
                title, 
                description, 
                category, 
                `condition`, 
                state, 
                city, 
                urgency, 
                status, 
                created_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()
            )
            """
            
            # Set default status and handle optional urgency
            status = 'OPEN'
            urgency = urgency.capitalize() if urgency else 'Medium'
            
            # Check if a transaction is already in progress before starting a new one
            if not self.connection.in_transaction:
                self.connection.start_transaction()
            
            # Execute the donation request query
            self.cursor.execute(query, (
                user_id, 
                title, 
                description, 
                category, 
                condition, 
                state, 
                city, 
                urgency, 
                status
            ))
            
            # Get the ID of the newly created request
            request_id = self.cursor.lastrowid
            
            # Update total_requests for the user
            update_total_requests_query = """
            UPDATE users 
            SET total_requests = COALESCE(total_requests, 0) + 1,
                updated_at = NOW()
            WHERE unique_id = %s
            """
            self.cursor.execute(update_total_requests_query, (user_id,))
            
         # Verify the update
            self.cursor.execute("SELECT total_requests, email FROM users WHERE unique_id = %s", (user_id,))
            user_data = self.cursor.fetchone()
            
            # Send email notification to requester
            if user_data and user_data['email']:
                # Prepare email content
                email_subject = f"Donation Request Created - {title}"
                email_body = f"""Dear User,

Your donation request has been successfully created.

Request Details:
Title: {title}
Category: {category}
Condition: {condition}
Location: {city}, {state}
Urgency: {urgency}
Status: {status}

We will notify you when donors respond to your request.

Best regards,
CrowdNest Team"""
                
                # Send email to requester
                from src.utils.email_sender import send_email
                email_result = send_email(
                    to_email=user_data['email'],
                    subject=email_subject,
                    body=email_body
                )
                
                # Send notification to admin
                admin_subject = "New Donation Request Created"
                admin_body = f"""A new donation request has been created.

Request Details:
Requester ID: {user_id}
Title: {title}
Category: {category}
Condition: {condition}
Location: {city}, {state}
Urgency: {urgency}
Status: {status}

Please review the request."""
                
                admin_email = os.getenv('SMTP_EMAIL')
                if admin_email:
                    send_email(
                        to_email=admin_email,
                        subject=admin_subject,
                        body=admin_body
                    )
            updated_total_requests = self.cursor.fetchone()['total_requests']
            
            # Debug print
            print(f"User {user_id} total_requests updated to: {updated_total_requests}")
            
            # Commit the transaction
            self.connection.commit()
            
            # Log successful request creation
            print(f"Donation request created successfully. Request ID: {request_id}")
            
            return True, "Donation request created successfully", request_id
        
        except mysql.connector.Error as e:
            # Rollback in case of database error
            self.connection.rollback()
            
            # Log detailed error
            error_message = f"MySQL Error creating donation request: {e}"
            print(error_message)
            
            # Check for specific MySQL error codes
            if e.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                return False, "A similar donation request already exists", None
            elif e.errno == mysql.connector.errorcode.ER_NO_REFERENCED_ROW_2:
                return False, "Invalid user ID", None
            
            return False, f"Database error: {e}", None
        
        except Exception as e:
            # Rollback in case of unexpected error
            self.connection.rollback()
            
            # Log unexpected error
            error_message = f"Unexpected error creating donation request: {e}"
            print(error_message)
            
            return False, f"Unexpected error: {e}", None

    def send_donor_contact_email(self, donation_id=None, requester_message=None, requester_id=None, **kwargs):
        """
        Send an email to the donor about a potential donation request
        
        Supports two calling conventions:
        1. send_donor_contact_email(donation_id, requester_message, requester_id)
        2. send_donor_contact_email(sender_id, recipient_email, subject, message)
        
        :param donation_id: Unique ID of the donation or sender_id
        :param requester_message: Requester message or recipient_email
        :param requester_id: Requester ID or subject
        :param kwargs: Additional keyword arguments
        :return: Dictionary with email sending result
        """
        import logging
        import traceback
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='donor_email.log',
            filemode='a'
        )
        
        try:
            # Ensure database connection is active
            if not self.connection.is_connected():
                logging.warning("Database connection lost. Attempting to reconnect.")
                self.reconnect()
            
            # Determine calling convention
            if all(key in kwargs for key in ['sender_id', 'recipient_email', 'subject', 'message']):
                # Legacy calling convention
                sender_id = kwargs['sender_id']
                recipient_email = kwargs['recipient_email']
                subject = kwargs['subject']
                message = kwargs['message']
                
                # Fetch sender details
                sender_query = """
                SELECT 
                    unique_id, 
                    username, 
                    email 
                FROM users 
                WHERE unique_id = %s
                """
                
                logging.info(f"Fetching sender information for ID: {sender_id}")
                
                self.cursor.execute(sender_query, (sender_id,))
                sender_info = self.cursor.fetchone()
                
                if not sender_info:
                    logging.error(f"Sender information not found for ID: {sender_id}")
                    return {
                        'success': False,
                        'message': 'Sender information not found',
                        'error_code': 'SENDER_NOT_FOUND'
                    }
                
                # Prepare email details
                sender_name = sender_info['username']
                
                # Prepare email record
                insert_email_query = """
                INSERT INTO email_communications 
                (sender_id, recipient_email, subject, message, sent_at, status) 
                VALUES (%s, %s, %s, %s, NOW(), 'pending')
                """
                
                try:
                    # Send email
                    from src.utils.email_sender import send_email
                    
                    logging.info(f"Attempting to send email to {recipient_email}")
                    logging.info(f"Sender: {sender_name}, Subject: {subject}")
                    
                    email_result = send_email(
                        to_email=recipient_email, 
                        subject=subject, 
                        body=message,
                        from_name=sender_name
                    )
                    
                    # Log email sending result
                    if email_result:
                        logging.info(f"Email sent successfully to {recipient_email}")
                        status = 'sent'
                    else:
                        logging.error(f"Failed to send email to {recipient_email}")
                        status = 'failed'
                    
                    # Record email communication
                    self.cursor.execute(insert_email_query, (
                        sender_id, 
                        recipient_email, 
                        subject, 
                        message
                    ))
                    
                    # Commit transaction
                    self.connection.commit()
                    
                    return {
                        'success': email_result,
                        'message': 'Donor contact email processed',
                        'recipient': recipient_email,
                        'status': status
                    }
                
                except Exception as email_err:
                    logging.error(f"Error sending donor contact email: {email_err}")
                    logging.error(traceback.format_exc())
                    
                    self.connection.rollback()
                    
                    return {
                        'success': False,
                        'message': f'Failed to send donor contact email: {str(email_err)}',
                        'error_code': 'EMAIL_SEND_FAILED',
                        'error_details': str(email_err)
                    }
            
            elif all([donation_id, requester_message, requester_id]):
                # New calling convention
                # Fetch comprehensive donor and requester information
                donor_query = """
                SELECT 
                    d.unique_id as donation_unique_id,
                    d.title as donation_title,
                    d.description as donation_description,
                    d.category as donation_category,
                    d.`condition` as donation_condition,
                    d.state as donation_state,
                    d.city as donation_city,
                    
                    u_donor.unique_id as donor_id,
                    u_donor.email as donor_email,
                    u_donor.username as donor_username,
                    u_donor.location as donor_location,
                    
                    u_requester.unique_id as requester_user_id,
                    u_requester.username as requester_username,
                    u_requester.email as requester_email,
                    u_requester.location as requester_location,
                    u_requester.contact_number as requester_contact
                FROM donations d
                JOIN users u_donor ON d.donor_id = u_donor.unique_id
                JOIN users u_requester ON u_requester.unique_id = %s
                WHERE d.unique_id = %s
                """
                
                logging.info(f"Fetching donation details for donation_id: {donation_id}, requester_id: {requester_id}")
                
                self.cursor.execute(donor_query, (requester_id, donation_id))
                contact_info = self.cursor.fetchone()
                
                # Validate contact information
                if not contact_info:
                    logging.error(f"No contact information found for donation_id: {donation_id}, requester_id: {requester_id}")
                    return {
                        'success': False,
                        'message': 'Donor or requester information not found',
                        'error_code': 'CONTACT_INFO_NOT_FOUND'
                    }
                
                # Prepare email details
                sender_name = contact_info['requester_username']
                recipient_email = contact_info['donor_email']
                
                # Validate email addresses
                if not recipient_email:
                    logging.error(f"No email found for donor with ID: {contact_info['donor_id']}")
                    return {
                        'success': False,
                        'message': 'Donor email not available',
                        'error_code': 'MISSING_DONOR_EMAIL'
                    }
                
                # Prepare email subject and body
                email_subject = f"Donation Request: {contact_info['donation_title']}"
                from src.utils.html_email_templates import HTMLEmailTemplates
                email_body = HTMLEmailTemplates.generate_request_status_email(
                    status='pending', 
                    request_details=contact_info,
                    requester_message=requester_message
                )
                
                # Prepare email record
                insert_email_query = """
                INSERT INTO email_communications 
                (sender_id, recipient_email, subject, message, sent_at, status) 
                VALUES (%s, %s, %s, %s, NOW(), 'pending')
                """
                
                try:
                    # Send email
                    from src.utils.email_sender import send_email
                    
                    logging.info(f"Attempting to send email to {recipient_email}")
                    logging.info(f"Sender: {sender_name}, Subject: {email_subject}")
                    
                    email_result = send_email(
                        to_email=recipient_email, 
                        subject=email_subject, 
                        body=email_body,
                        from_name=sender_name
                    )
                    
                    # Log email sending result
                    if email_result:
                        logging.info(f"Email sent successfully to {recipient_email}")
                        status = 'sent'
                    else:
                        logging.error(f"Failed to send email to {recipient_email}")
                        status = 'failed'
                    
                    # Record email communication
                    self.cursor.execute(insert_email_query, (
                        contact_info['requester_user_id'], 
                        recipient_email, 
                        email_subject, 
                        email_body
                    ))
                    
                    # Commit transaction
                    self.connection.commit()
                    
                    return {
                        'success': email_result,
                        'message': 'Donor contact email processed',
                        'recipient': recipient_email,
                        'status': status
                    }
                
                except Exception as email_err:
                    logging.error(f"Error sending donor contact email: {email_err}")
                    logging.error(traceback.format_exc())
                    
                    self.connection.rollback()
                    
                    return {
                        'success': False,
                        'message': f'Failed to send donor contact email: {str(email_err)}',
                        'error_code': 'EMAIL_SEND_FAILED',
                        'error_details': str(email_err)
                    }
            
            else:
                logging.error("Invalid arguments provided for send_donor_contact_email")
                return {
                    'success': False,
                    'message': 'Invalid arguments provided',
                    'error_code': 'INVALID_ARGUMENTS'
                }
        
        except mysql.connector.Error as e:
            logging.error(f"MySQL Connector Error in donor communication: {e}")
            logging.error(traceback.format_exc())
            return {
                'success': False,
                'message': 'Database error during donor communication',
                'error_code': 'DB_ERROR',
                'error_details': str(e)
            }
        
        except Exception as e:
            logging.error(f"Unexpected error in donor communication: {e}")
            logging.error(traceback.format_exc())
            return {
                'success': False,
                'message': 'Unexpected error during donor communication',
                'error_code': 'UNEXPECTED_ERROR',
                'error_details': str(e)
            }
        
        finally:
            # Ensure cursor is reset
            try:
                self.reset_cursor()
            except Exception as reset_err:
                logging.error(f"Error resetting cursor: {reset_err}")

    def get_donation_donor_details(self, donation_id):
        """
        Retrieve donor details for a specific donation

        :param donation_id: Unique ID of the donation
        :return: Dictionary with donor details or None
        """
        try:
            query = """
            SELECT 
                u.unique_id,
                u.username,
                u.email,
                d.title as donation_title
            FROM donations d
            JOIN users u ON d.donor_id = u.unique_id
            WHERE d.unique_id = %s
            """
            self.cursor.execute(query, (donation_id,))
            donor_details = self.cursor.fetchone()
            
            return donor_details
        
        except mysql.connector.Error as e:
            print(f"Error fetching donation donor details: {e}")
            return None
    
    def get_all_donation_requests(self):
        """
        Retrieve all donation requests for admin or system-wide view

        :return: List of dictionaries containing donation request details
        """
        try:
            query = """
            SELECT 
                dr.unique_id,
                dr.requester_id,
                dr.donation_id,
                dr.request_message,
                dr.status,
                dr.created_at,
                d.title as donation_title,
                d.category as donation_category,
                d.description as donation_description,
                u_requester.username as requester_username,
                u_requester.email as requester_email,
                u_donor.username as donor_username,
                u_donor.email as donor_email
            FROM donation_requests dr
            JOIN donations d ON dr.donation_id = d.unique_id
            JOIN users u_requester ON dr.requester_id = u_requester.unique_id
            JOIN users u_donor ON d.donor_id = u_donor.unique_id
            ORDER BY dr.created_at DESC
            """
            
            self.cursor.execute(query)
            requests = self.cursor.fetchall()
            
            # Convert to list of dictionaries
            request_list = []
            for req in requests:
                request_list.append({
                    'unique_id': req['unique_id'],
                    'requester_id': req['requester_id'],
                    'donation_id': req['donation_id'],
                    'request_message': req['request_message'],
                    'status': req['status'],
                    'created_at': req['created_at'],
                    'donation_title': req['donation_title'],
                    'donation_category': req['donation_category'],
                    'donation_description': req['donation_description'],
                    'requester_username': req['requester_username'],
                    'requester_email': req['requester_email'],
                    'donor_username': req['donor_username'],
                    'donor_email': req['donor_email']
                })
            
            return request_list
        
        except mysql.connector.Error as e:
            print(f"Error fetching all donation requests: {e}")
            return []
    
    def create_user(self, username, password, email, location=None):
        """
        Create a new user in the database

        :param username: Unique username for the user
        :param password: User's password (will be hashed)
        :param email: User's email address
        :param location: Optional location information
        :return: Tuple (success_bool, message_str)
        """
        try:
            # Check if username or email already exists
            check_query = "SELECT * FROM users WHERE username = %s OR email = %s"
            self.cursor.execute(check_query, (username, email))
            existing_user = self.cursor.fetchone()
            
            if existing_user:
                return False, "Username or email already exists"
            
            # Hash the password
            hashed_password = self.hash_password(password)
            
            # Generate unique ID
            unique_id = str(uuid.uuid4())
            
            # Prepare the query
            query = """
            INSERT INTO users 
            (unique_id, username, email, password_hash, location, created_at) 
            VALUES (%s, %s, %s, %s, %s, NOW())
            """
            
            # Execute the query
            self.cursor.execute(query, (
                unique_id,
                username,
                email,
                hashed_password,
                location
            ))
            
            # Commit the transaction
            self.connection.commit()
            
            return True, "User created successfully"
        
        except mysql.connector.Error as e:
            print(f"Error creating user: {e}")
            self.connection.rollback()
            return False, f"Database error: {str(e)}"
        
    def verify_user(self, username, password):
        """
        Verify user credentials and return user details

        :param username: Username to verify
        :param password: Password to verify
        :return: Tuple (user_dict or None, message_str)
        """
        try:
            # Hash the provided password
            hashed_password = self.hash_password(password)
            
            # Prepare the query
            query = """
            SELECT * FROM users 
            WHERE username = %s AND password_hash = %s
            """
            
            # Execute the query
            self.cursor.execute(query, (username, hashed_password))
            user = self.cursor.fetchone()
            
            if user:
                return user, "User verified successfully"
            else:
                return None, "Invalid username or password"
        
        except mysql.connector.Error as e:
            print(f"Error verifying user: {e}")
            return None, f"Database error: {str(e)}"
    
    def update_donation_status(self, donation_id, new_status):
        """
        Update the status of a donation
        
        :param donation_id: Unique ID of the donation
        :param new_status: New status for the donation (e.g., 'unavailable', 'completed')
        :return: Boolean indicating success of the update
        """
        try:
            # Validate status
            valid_statuses = ['available', 'unavailable', 'pending', 'completed', 'reserved', 'withdrawn']
            if new_status.lower() not in valid_statuses:
                print(f"Invalid donation status: {new_status}")
                return False

            # Update query
            update_query = """
            UPDATE donations 
            SET status = %s, updated_at = NOW() 
            WHERE unique_id = %s
            """
            
            # Execute update
            self.cursor.execute(update_query, (new_status.lower(), donation_id))
            self.connection.commit()

            # Check if any rows were affected
            if self.cursor.rowcount > 0:
                print(f"Donation status updated to {new_status}")
                return True
            else:
                print(f"No donation found with ID: {donation_id}")
                return False

        except mysql.connector.Error as e:
            print(f"Database error updating donation status: {e}")
            self.connection.rollback()
            return False
        except Exception as e:
            print(f"Unexpected error updating donation status: {e}")
            return False

    def get_donation_details(self, donation_id):
        """
        Retrieve comprehensive details for a specific donation
        
        :param donation_id: Unique ID of the donation
        :return: Dictionary containing donation details or None
        """
        try:
            # Ensure database connection is active
            if not self.connection.is_connected():
                self.reconnect()
            
            # Comprehensive query to fetch donation and donor details
            query = """
            SELECT 
                d.unique_id, 
                d.title, 
                d.description, 
                d.category, 
                d.`condition`, 
                d.state,
                d.city,
                d.image_data,
                d.image_type,
                d.status,
                d.created_at, 
                
                u.unique_id AS donor_id,
                u.username AS donor_username,
                u.email AS donor_email,
                u.location AS donor_location
            FROM 
                donations d
            LEFT JOIN 
                users u ON d.donor_id = u.unique_id
            WHERE 
                d.unique_id = %s
            """
            
            # Execute the query
            self.cursor.execute(query, (donation_id,))
            donation = self.cursor.fetchone()
            
            # Check if donation exists
            if not donation:
                print(f"No donation found with ID {donation_id}")
                return None
            
            # Prepare donation details dictionary
            donation_details = {
                'unique_id': donation['unique_id'],
                'title': donation['title'],
                'description': donation['description'],
                'category': donation['category'],
                'condition': donation['condition'],
                'state': donation['state'],
                'city': donation['city'],
                'image_data': donation['image_data'],
                'image_type': donation['image_type'],
                'status': donation['status'],
                'created_at': donation['created_at'],
                
                # Donor Information
                'donor_id': donation['donor_id'],
                'donor_username': donation['donor_username'],
                'donor_email': donation['donor_email'],
                'donor_location': donation['donor_location'],
                
                # Additional Images (placeholder for future implementation)
                'additional_images': []
            }
            
            # Validate donor contact information
            if not donation_details['donor_email']:
                print(f"Warning: No contact information found for donation {donation_id}")
            
            return donation_details
        
        except mysql.connector.Error as e:
            print(f"MySQL Connector Error retrieving donation details: {e}")
            return None
        
        except Exception as e:
            print(f"Unexpected error retrieving donation details: {e}")
            import traceback
            traceback.print_exc()
            return None
        
        finally:
            # Ensure cursor is reset
            try:
                self.reset_cursor()
            except Exception as reset_err:
                print(f"Error resetting cursor: {reset_err}")

    def process_donation_request(self, request_unique_id, action, user_id):
        """
        Process a donation request (accept or reject)
        
        :param request_unique_id: Unique ID of the donation request
        :param action: 'accept' or 'reject'
        :param user_id: Unique ID of the user processing the request
        :return: Tuple (success_bool, message_str)
        """
        # Validate input
        if action not in ['accept', 'reject']:
            return False, "Invalid action. Must be 'accept' or 'reject'."
        
        try:
            # Ensure database connection is active
            if not self.connection.is_connected():
                self.reconnect()
            
            # Check if a transaction is already in progress before starting a new one
            if not self.connection.in_transaction:
                self.connection.start_transaction()
            
            # First, verify the request and check if the user has permission
            verify_request_query = """
            SELECT 
                dr.unique_id, 
                dr.status, 
                dr.requester_id,
                dr.donation_id,
                u_requester.username as requester_username,
                u_requester.email as requester_email,
                d.title as donation_title,
                d.donor_id,
                d.status as donation_status,
                u_donor.username as donor_username,
                u_donor.email as donor_email
            FROM donation_requests dr
            JOIN users u_requester ON dr.requester_id = u_requester.unique_id
            JOIN donations d ON dr.donation_id = d.unique_id
            JOIN users u_donor ON d.donor_id = u_donor.unique_id
            WHERE dr.unique_id = %s
            FOR UPDATE  # Lock the row to prevent concurrent modifications
            """
            
            self.cursor.execute(verify_request_query, (request_unique_id,))
            request_info = self.cursor.fetchone()
            
            # Validate request exists
            if not request_info:
                print(f"No donation request found with unique ID {request_unique_id}")
                self.connection.rollback()
                return False, f"No donation request found with unique ID {request_unique_id}"
            
            # Check if request is already processed
            if request_info['status'] != 'pending':
                self.connection.rollback()
                return False, f"Request is already {request_info['status']}"
            
            # Verify user is the donor of the donation
            if request_info['donor_id'] != user_id:
                self.connection.rollback()
                return False, "You are not authorized to process this request"
            
            # Verify donation is still available
            try:
                # Get donation status directly from the donations table
                donation_status_query = "SELECT status FROM donations WHERE unique_id = %s"
                self.cursor.execute(donation_status_query, (request_info['donation_id'],))
                donation_status_result = self.cursor.fetchone()
                
                if not donation_status_result:
                    self.connection.rollback()
                    return False, "Unable to verify donation status"
                    
                donation_status = donation_status_result['status']
                print(f"Donation status: {donation_status}")
                
                if donation_status.lower() != 'available':
                    self.connection.rollback()
                    return False, f"Donation is no longer {donation_status}"
            except Exception as status_error:
                print(f"Error checking donation status: {status_error}")
                print("Request Info Keys:", list(request_info.keys()))
                self.connection.rollback()
                return False, "Unable to verify donation status"
            
            # Prepare update queries
            if action == 'accept':
                # Update request status to approved
                update_request_query = """
                UPDATE donation_requests 
                SET 
                    status = 'approved', 
                    updated_at = CURRENT_TIMESTAMP
                WHERE unique_id = %s
                """
                
                # Update donation status to reserved
                update_donation_query = """
                UPDATE donations d
                JOIN donation_requests dr ON d.unique_id = dr.donation_id
                SET 
                    d.status = 'reserved',
                    d.updated_at = CURRENT_TIMESTAMP
                WHERE dr.unique_id = %s
                """
                
                try:
                    # Validate input length to prevent truncation
                    max_status_length = 20  # Adjust based on your database column definition
                    truncated_status = 'approved'[:max_status_length]
                    
                    # Update request status
                    self.cursor.execute(update_request_query, (request_unique_id,))
                    request_update_count = self.cursor.rowcount
                    
                    # Update donation status
                    self.cursor.execute(update_donation_query, (request_unique_id,))
                    donation_update_count = self.cursor.rowcount
                    
                    # Validate updates
                    if request_update_count == 0 or donation_update_count == 0:
                        print(f"No rows updated. Request updates: {request_update_count}, Donation updates: {donation_update_count}")
                        print(f"Request details: {request_info}")
                        self.connection.rollback()
                        return False, "Failed to update request or donation status"
                    
                    # Send email notification
                    try:
                        from src.utils.email_sender import send_email
                        from src.utils.html_email_templates import HTMLEmailTemplates
                        
                        # Create email subject
                        email_subject = f"Your request for {request_info['donation_title']} has been accepted"
                        
                        # Use HTML template for accepted request
                        email_body = HTMLEmailTemplates.generate_request_status_email(
                            status='approved',
                            request_details=request_info
                        )
                        
                        # Send email with HTML template
                        send_email(
                            to_email=request_info['requester_email'],
                            subject=email_subject,
                            body=email_body
                        )
                        
                        print(f"Email notification sent to {request_info['requester_email']} for approval")
                    except Exception as email_error:
                        print(f"Warning: Failed to send email notification: {email_error}")
                        import traceback
                        traceback.print_exc()
                    
                    # Commit transaction
                    self.connection.commit()
                    
                    print(f"Donation request {request_unique_id} approved")
                    return True, "Donation request approved successfully"
                
                except Exception as update_err:
                    # Rollback transaction in case of any error
                    self.connection.rollback()
                    print(f"Error updating request/donation: {update_err}")
                    print(f"Request details: {request_info}")
                    import traceback
                    traceback.print_exc()
                    return False, f"Failed to process request: {str(update_err)}"
            
            elif action == 'reject':
                # Update request status to rejected
                update_request_query = """
                UPDATE donation_requests 
                SET 
                    status = 'rejected', 
                    updated_at = CURRENT_TIMESTAMP
                WHERE unique_id = %s
                """
                
                try:
                    # Validate input length to prevent truncation
                    max_status_length = 20  # Adjust based on your database column definition
                    truncated_status = 'rejected'[:max_status_length]
                    
                    # Update request status
                    self.cursor.execute(update_request_query, (request_unique_id,))
                    request_update_count = self.cursor.rowcount
                    
                    # Validate updates
                    if request_update_count == 0:
                        print(f"No rows updated. Request updates: {request_update_count}")
                        print(f"Request details: {request_info}")
                        self.connection.rollback()
                        return False, "Failed to update request status"
                    
                    # Send email notification
                    try:
                        from src.utils.email_sender import send_email
                        from src.utils.html_email_templates import HTMLEmailTemplates
                        
                        # Create email subject
                        email_subject = f"Your request for {request_info['donation_title']} has been declined"
                        
                        # Use HTML template for rejected request
                        email_body = HTMLEmailTemplates.generate_request_status_email(
                            status='rejected',
                            request_details=request_info
                        )
                        
                        # Send email with HTML template
                        send_email(
                            to_email=request_info['requester_email'],
                            subject=email_subject,
                            body=email_body
                        )
                        
                        print(f"Email notification sent to {request_info['requester_email']} for rejection")
                    except Exception as email_error:
                        print(f"Warning: Failed to send email notification: {email_error}")
                        import traceback
                        traceback.print_exc()
                    
                    # Commit transaction
                    self.connection.commit()
                    
                    print(f"Donation request {request_unique_id} rejected")
                    return True, "Donation request rejected successfully"
                
                except Exception as update_err:
                    # Rollback transaction in case of any error
                    self.connection.rollback()
                    print(f"Error updating request: {update_err}")
                    print(f"Request details: {request_info}")
                    import traceback
                    traceback.print_exc()
                    return False, f"Failed to process request: {str(update_err)}"
        
        except mysql.connector.Error as e:
            # Rollback transaction
            self.connection.rollback()
            print(f"MySQL Connector Error processing donation request: {e}")
            return False, f"Database error: {str(e)}"
        
        except Exception as e:
            # Rollback transaction
            self.connection.rollback()
            print(f"Unexpected error processing donation request: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Unexpected error: {str(e)}"
        
        finally:
            # Ensure cursor is reset
            try:
                self.reset_cursor()
            except Exception as reset_err:
                print(f"Error resetting cursor: {reset_err}")

    def mark_request_delivered(self, request_unique_id, user_id=None):
        """
        Mark a donation request as delivered
        
        :param request_unique_id: Unique ID of the request to mark as delivered
        :param user_id: Optional user ID to verify permissions
        :return: Dictionary with operation status and details
        """
        try:
            # Validate input
            if not request_unique_id:
                return {
                    'success': False, 
                    'message': 'Invalid request ID',
                    'error_code': 'INVALID_REQUEST_ID'
                }
            
            # Check if a transaction is already in progress before starting a new one
            if not self.connection.in_transaction:
                self.connection.start_transaction()
            
            # First, verify the request exists and check permissions if user_id is provided
            verify_query = """
            SELECT 
                dr.unique_id, 
                dr.status, 
                dr.requester_id,
                dr.donation_id,
                u_requester.username as requester_username,
                u_requester.email as requester_email,
                d.title as donation_title,
                d.donor_id,
                u_donor.username as donor_username,
                u_donor.email as donor_email
            FROM donation_requests dr
            JOIN users u_requester ON dr.requester_id = u_requester.unique_id
            JOIN donations d ON dr.donation_id = d.unique_id
            JOIN users u_donor ON d.donor_id = u_donor.unique_id
            WHERE dr.unique_id = %s
            """
            
            self.cursor.execute(verify_query, (request_unique_id,))
            request_details = self.cursor.fetchone()
            
            # Check if request exists
            if not request_details:
                return {
                    'success': False, 
                    'message': 'Request not found',
                    'error_code': 'REQUEST_NOT_FOUND'
                }
            
            # Check if request is already delivered
            if request_details['status'] == 'delivered':
                return {
                    'success': False, 
                    'message': 'Request already marked as delivered',
                    'error_code': 'ALREADY_DELIVERED'
                }
            
            # Verify user permissions if user_id is provided
            if user_id:
                # Check if user is either the requester or the donor
                if user_id not in [request_details['requester_id'], request_details['donor_id']]:
                    return {
                        'success': False, 
                        'message': 'Unauthorized to mark this request as delivered',
                        'error_code': 'UNAUTHORIZED'
                    }
            
            # Update request status to delivered
            update_request_query = """
            UPDATE donation_requests 
            SET 
                status = 'delivered', 
                updated_at = CURRENT_TIMESTAMP
            WHERE unique_id = %s
            """
            
            # Update associated donation status to completed
            update_donation_query = """
            UPDATE donations d
            JOIN donation_requests dr ON d.unique_id = dr.donation_id
            SET 
                d.status = 'completed',
                d.updated_at = CURRENT_TIMESTAMP
            WHERE dr.unique_id = %s
            """
            
            self.cursor.execute(update_request_query, (request_unique_id,))
            
            self.cursor.execute(update_donation_query, (request_unique_id,))
            
            # Commit the transaction
            self.connection.commit()
            
            # Prepare return result with details
            result = {
                'success': True, 
                'message': 'Request successfully marked as delivered',
                'request_id': request_unique_id,
                'donation_title': request_details['donation_title'],
                'requester_username': request_details['requester_username'],
                'requester_email': request_details['requester_email'],
                'donor_username': request_details['donor_username'],
                'donor_email': request_details['donor_email']
            }
            
            # Send email notification about delivery to both requester and donor
            try:
                from src.utils.email_sender import send_email
                from src.utils.html_email_templates import HTMLEmailTemplates
                
                # Create delivery confirmation email for requester
                requester_subject = f"Donation Delivered: {request_details['donation_title']}"
                requester_body = HTMLEmailTemplates.generate_request_status_email(
                    status='delivered', 
                    request_details=request_details
                )
                
                # Create delivery confirmation email for donor
                donor_subject = f"Donation Delivered: {request_details['donation_title']}"
                donor_body = HTMLEmailTemplates.generate_request_status_email(
                    status='delivered', 
                    request_details=request_details
                )
                
                # Send emails to both requester and donor
                send_email(
                    to_email=request_details['requester_email'],
                    subject=requester_subject,
                    body=requester_body
                )
                
                send_email(
                    to_email=request_details['donor_email'],
                    subject=donor_subject,
                    body=donor_body
                )
                
                print(f"Delivery confirmation emails sent to requester and donor for request {request_unique_id}")
                
            except Exception as email_error:
                print(f"Warning: Failed to send delivery notification email: {email_error}")
                import traceback
                print(traceback.format_exc())
            
            return result
        
        except mysql.connector.Error as e:
            # Rollback in case of database error
            self.connection.rollback()
            return {
                'success': False, 
                'message': f'Database error: {str(e)}',
                'error_code': 'DB_ERROR',
                'mysql_error_code': e.errno
            }
        except Exception as e:
            # Rollback for any unexpected error
            self.connection.rollback()
            return {
                'success': False, 
                'message': f'Unexpected error: {str(e)}',
                'error_code': 'UNEXPECTED_ERROR'
            }

    def diagnose_request_retrieval(self, request_id):
        """
        Comprehensive diagnostic method to investigate request retrieval issues
        
        :param request_id: Unique ID of the request to diagnose
        :return: Dictionary with diagnostic information
        """
        try:
            # Initialize diagnostic dictionary
            diagnostic_info = {
                'request_id': request_id,
                'request_record': None,
                'requester_details': None,
                'donation_details': None,
                'donor_details': None,
                'error_messages': []
            }
            
            # Check request record
            try:
                self.cursor.execute("""
                    SELECT 
                        unique_id, 
                        request_message, 
                        requester_id, 
                        donation_id, 
                        status 
                    FROM donation_requests 
                    WHERE unique_id = %s
                """, (request_id,))
                diagnostic_info['request_record'] = self.cursor.fetchone()
            except Exception as e:
                diagnostic_info['error_messages'].append(f"Error fetching request record: {str(e)}")
            
            # If request record exists, check related records
            if diagnostic_info['request_record']:
                requester_id = diagnostic_info['request_record'].get('requester_id')
                donation_id = diagnostic_info['request_record'].get('donation_id')
                
                # Check requester details
                if requester_id:
                    try:
                        self.cursor.execute("""
                            SELECT 
                                unique_id, 
                                username, 
                                email
                            FROM users 
                            WHERE unique_id = %s
                        """, (requester_id,))
                        diagnostic_info['requester_details'] = self.cursor.fetchone()
                    except Exception as e:
                        diagnostic_info['error_messages'].append(f"Error fetching requester details: {str(e)}")
                
                # Check donation details
                if donation_id:
                    try:
                        self.cursor.execute("""
                            SELECT 
                                unique_id, 
                                title, 
                                description, 
                                donor_id
                            FROM donations 
                            WHERE unique_id = %s
                        """, (donation_id,))
                        diagnostic_info['donation_details'] = self.cursor.fetchone()
                        
                        # Check donor details if donation exists
                        if diagnostic_info['donation_details']:
                            donor_id = diagnostic_info['donation_details'].get('donor_id')
                            if donor_id:
                                try:
                                    self.cursor.execute("""
                                        SELECT 
                                            unique_id, 
                                            username, 
                                            email
                                        FROM users 
                                        WHERE unique_id = %s
                                    """, (donor_id,))
                                    diagnostic_info['donor_details'] = self.cursor.fetchone()
                                except Exception as e:
                                    diagnostic_info['error_messages'].append(f"Error fetching donor details: {str(e)}")
                    except Exception as e:
                        diagnostic_info['error_messages'].append(f"Error fetching donation details: {str(e)}")
            
            return diagnostic_info
        
        except Exception as e:
            print(f"Unexpected error in diagnose_request_retrieval: {e}")
            return {
                'request_id': request_id,
                'error_messages': [f"Unexpected error: {str(e)}"]
            }

    def get_user_donation_history(self, user_id):
        """
        Retrieve donation history for a specific user
        
        :param user_id: Unique ID of the user
        :return: List of donations made by the user
        """
        try:
            query = """
            SELECT 
                d.unique_id,
                d.title,
                d.description,
                d.category,
                d.`condition`,
                d.state,
                d.city,
                d.status,
                d.created_at,
                d.image_path,
                u.username as donor_name,
                u.email as donor_email
            FROM 
                donations d
            JOIN 
                users u ON d.donor_id = u.unique_id
            WHERE 
                d.donor_id = %s
            ORDER BY 
                d.created_at DESC
            """
            self.cursor.execute(query, (user_id,))
            
            # Fetch all results
            donations = self.cursor.fetchall()
            
            # Convert to list of dictionaries for easier handling
            donation_history = []
            for donation in donations:
                donation_history.append({
                    'unique_id': donation['unique_id'],
                    'title': donation['title'],
                    'description': donation['description'],
                    'category': donation['category'],
                    'condition': donation['condition'],
                    'state': donation['state'],
                    'city': donation['city'],
                    'status': donation['status'],
                    'created_at': donation['created_at'],
                    'image_path': donation['image_path'],
                    'donor_name': donation['donor_name'],
                    'donor_email': donation['donor_email']
                })
            
            return donation_history
        
        except mysql.connector.Error as e:
            print(f"Error fetching donation history: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error retrieving donation history: {e}")
            return []

    def mark_request_delivered(self, request_id):
        """
        Mark a donation request as delivered and send confirmation emails
        
        :param request_id: Unique ID of the request to mark as delivered
        :return: Boolean indicating success
        """
        try:
            # Get request details including donation and user information
            request_details = self.get_request_details(request_id)
            
            if not request_details:
                print(f"Could not find request with ID: {request_id}")
                return False
            
            # Update request status to completed
            update_query = "UPDATE donation_requests SET status = 'completed', updated_at = NOW() WHERE unique_id = %s"
            self.cursor.execute(update_query, (request_id,))
            
            # Update donation status to completed
            if request_details['donation_id']:
                donation_update = "UPDATE donations SET status = 'completed' WHERE unique_id = %s"
                self.cursor.execute(donation_update, (request_details['donation_id'],))
            
            self.connection.commit()
            
            # Send confirmation emails
            try:
                # Email to requester
                requester_subject = "Donation Delivery Confirmed"
                requester_body = f"""Dear {request_details['requester_username']},

Your requested donation has been marked as delivered:

Donation: {request_details['donation_title']}
Donor: {request_details['donor_name']}
Status: Delivered

Thank you for using CrowdNest!"""
                
                send_email(
                    to_email=request_details['requester_email'],
                    subject=requester_subject,
                    body=requester_body
                )
                
                # Email to donor
                donor_subject = "Donation Delivery Confirmation"
                donor_body = f"""Dear {request_details['donor_name']},

Your donation has been successfully delivered:

Donation: {request_details['donation_title']}
Receiver: {request_details['requester_username']}
Status: Delivered

Thank you for your generosity!"""
                
                send_email(
                    to_email=request_details['donor_email'],
                    subject=donor_subject,
                    body=donor_body
                )
                
            except Exception as e:
                print(f"Error sending confirmation emails: {e}")
                # Continue execution even if email sending fails
            
            return True
            
        except mysql.connector.Error as e:
            print(f"Database error marking request as delivered: {e}")
            self.connection.rollback()
            return False
        except Exception as e:
            print(f"Unexpected error marking request as delivered: {e}")
            self.connection.rollback()
            return False
    
    def search_donations(self, search_term=None, category=None, state=None, city=None, page=1, page_size=10):
        """
        Search for donations with comprehensive filtering and pagination

        :param search_term: Optional text to search in title or description
        :param category: Optional donation category filter
        :param state: Optional state location filter
        :param city: Optional city location filter
        :param page: Page number for pagination (default 1)
        :param page_size: Number of results per page (default 10)
        :return: Dictionary with donations and pagination info
        """
        try:
            # Validate page and page_size
            page = max(1, page)
            page_size = max(1, min(page_size, 50))  # Limit max page size
            offset = (page - 1) * page_size

            # Prepare base filtering conditions
            conditions = ["d.status = 'available'"]
            params = []
            
            # Search term filter (if provided)
            if search_term:
                conditions.append("(d.title LIKE %s OR d.description LIKE %s)")
                search_param = f"%{search_term}%"
                params.extend([search_param, search_param])
            
            # Category filter
            if category and category.lower() != 'all categories':
                conditions.append("d.category = %s")
                params.append(category)
            
            # State filter
            if state and state.lower() != 'all locations':
                conditions.append("d.state = %s")
                params.append(state)
            
            # City filter
            if city:
                conditions.append("d.city = %s")
                params.append(city)
            
            # Combine conditions
            where_clause = " AND ".join(conditions)

            # Donations query with DISTINCT to prevent duplicates
            donations_query = f"""
            SELECT DISTINCT
                d.unique_id,
                d.title,
                d.description,
                d.category,
                d.`condition`,
                d.state,
                d.city,
                d.status,
                d.created_at,
                d.image_path,
                u.username as donor_name,
                u.email as donor_email
            FROM donations d
            JOIN users u ON d.donor_id = u.unique_id
            WHERE {where_clause}
            ORDER BY d.created_at DESC
            LIMIT %s OFFSET %s
            """
            
            # Add pagination parameters
            pagination_params = params + [page_size, offset]
            
            # Execute donations query
            self.cursor.execute(donations_query, pagination_params)
            donations = self.cursor.fetchall()

            # Count query
            count_query = f"""
            SELECT COUNT(DISTINCT d.unique_id) as total_count
            FROM donations d
            JOIN users u ON d.donor_id = u.unique_id
            WHERE {where_clause}
            """
            
            # Execute count query
            self.cursor.execute(count_query, params)
            count_result = self.cursor.fetchone()
            
            # Get total count
            total_count = count_result['total_count'] if count_result else 0

            # Prepare return dictionary
            return {
                'donations': [
                    {
                        'unique_id': donation['unique_id'],
                        'title': donation['title'],
                        'description': donation['description'],
                        'category': donation['category'],
                        'condition': donation['condition'],
                        'state': donation['state'],
                        'city': donation['city'],
                        'status': donation['status'],
                        'created_at': donation['created_at'],
                        'image_path': donation['image_path'],
                        'donor_name': donation['donor_name'],
                        'donor_email': donation['donor_email']
                    } for donation in donations
                ],
                'pagination': {
                    'total_count': total_count,
                    'page': page,
                    'page_size': page_size,
                    'total_pages': (total_count + page_size - 1) // page_size
                }
            }
        
        except mysql.connector.Error as e:
            print(f"MySQL Connector Error searching donations: {e}")
            # Additional error details
            if hasattr(e, 'errno'):
                print(f"MySQL Error Number: {e.errno}")
                print(f"MySQL Error State: {e.sqlstate}")
            return {
                'donations': [],
                'pagination': {
                    'total_count': 0,
                    'page': page,
                    'page_size': page_size,
                    'total_pages': 0
                }
            }
        
        except Exception as e:
            print(f"Unexpected error searching donations: {e}")
            import traceback
            traceback.print_exc()
            return {
                'donations': [],
                'pagination': {
                    'total_count': 0,
                    'page': page,
                    'page_size': page_size,
                    'total_pages': 0
                }
            }
        
        finally:
            # Ensure cursor is reset
            try:
                self.reset_cursor()
            except Exception as reset_err:
                print(f"Error resetting cursor: {reset_err}")

    def update_donation_status(self, donation_id, new_status):
        """
        Update the status of a specific donation
        
        :param donation_id: Unique ID of the donation
        :param new_status: New status to set (e.g., 'available', 'pending', 'completed')
        :return: Tuple (success_bool, message_str)
        """
        # Validate input
        valid_statuses = ['available', 'unavailable', 'pending', 'completed', 'reserved', 'withdrawn']
        if new_status not in valid_statuses:
            return False, f"Invalid status. Must be one of {valid_statuses}"
        
        try:
            # Ensure database connection is active
            if not self.connection.is_connected():
                self.reconnect()
            
            # Prepare the update query
            query = """
            UPDATE donations 
            SET status = %s, updated_at = NOW() 
            WHERE unique_id = %s
            """
            
            # Execute the update
            try:
                # Validate input length to prevent truncation
                max_status_length = 20  # Adjust based on your database column definition
                truncated_status = new_status[:max_status_length]
                
                self.cursor.execute(query, (truncated_status, donation_id))
                self.connection.commit()
            except mysql.connector.Error as exec_err:
                print(f"Query execution error: {exec_err}")
                self.connection.rollback()
                return False, f"Database query error: {str(exec_err)}"
            
            # Check if any rows were affected
            if self.cursor.rowcount > 0:
                print(f"Donation {donation_id} status updated to {new_status}")
                return True, f"Donation status updated to {new_status}"
            else:
                print(f"No donation found with ID {donation_id}")
                return False, f"No donation found with ID {donation_id}"
        
        except mysql.connector.Error as e:
            print(f"MySQL Connector Error updating donation status: {e}")
            return False, f"Database error: {str(e)}"
        
        except Exception as e:
            print(f"Unexpected error updating donation status: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Unexpected error: {str(e)}"
        
        finally:
            # Ensure cursor is reset
            try:
                self.reset_cursor()
            except Exception as reset_err:
                print(f"Error resetting cursor: {reset_err}")

    def create_request(self, requester_id, donation_id, request_message):
        """
        Create a new donation request
        
        :param requester_id: Unique ID of the user requesting the donation
        :param donation_id: Unique ID of the donation being requested
        :param request_message: Message from requester explaining their interest
        :return: Unique request ID if successful, None otherwise
        """
        # Validate input
        if not all([requester_id, donation_id, request_message]):
            print("Invalid input: Missing required parameters")
            return None
        
        try:
            # Ensure database connection is active
            if not self.connection.is_connected():
                self.reconnect()
            
            # First, verify the donation exists and is available
            check_donation_query = """
            SELECT unique_id, status, donor_id 
            FROM donations 
            WHERE unique_id = %s AND status = 'available'
            """
            
            self.cursor.execute(check_donation_query, (donation_id,))
            donation = self.cursor.fetchone()
            
            if not donation:
                print(f"Donation {donation_id} not found or not available")
                return None
            
            # Prevent requesting own donation
            if donation['donor_id'] == requester_id:
                print("Cannot request your own donation")
                return None
            
            # Generate unique ID for the request
            unique_id = str(uuid.uuid4())
            
            # Prepare the request insertion query
            insert_request_query = """
            INSERT INTO donation_requests (
                unique_id, 
                requester_id, 
                donation_id, 
                request_message, 
                status, 
                created_at
            ) VALUES (
                %s, %s, %s, %s, 'pending', NOW()
            )
            """
            
            # Execute the query
            try:
                # Validate input length to prevent truncation
                max_request_message_length = 500  # Adjust based on your database column definition
                truncated_request_message = request_message[:max_request_message_length]
                
                self.cursor.execute(insert_request_query, (
                    unique_id,
                    requester_id, 
                    donation_id, 
                    truncated_request_message
                ))
                
                # Commit the transaction
                self.connection.commit()
                
                print(f"Donation request created successfully. Request ID: {unique_id}")
                return unique_id
            
            except mysql.connector.Error as insert_err:
                print(f"Error inserting donation request: {insert_err}")
                self.connection.rollback()
                return None
        
        except mysql.connector.Error as e:
            print(f"MySQL Connector Error creating donation request: {e}")
            return None
        
        except Exception as e:
            print(f"Unexpected error creating donation request: {e}")
            import traceback
            traceback.print_exc()
            return None
        
        finally:
            # Ensure cursor is reset
            try:
                self.reset_cursor()
            except Exception as reset_err:
                print(f"Error resetting cursor: {reset_err}")

    def clear_test_donations(self):
        """
        Clear all test donations from the database
        
        This method is intended for development and testing purposes.
        It removes donations that are marked as test or have specific test identifiers.
        
        :return: Tuple (success_bool, message_str)
        """
        try:
            # Ensure database connection is active
            if not self.connection.is_connected():
                self.reconnect()
            
            # Begin transaction - check if one is already in progress
            if not self.connection.in_transaction:
                self.connection.start_transaction()
            
            # First, delete associated donation requests
            delete_requests_query = """
            DELETE dr FROM donation_requests dr
            JOIN donations d ON dr.donation_id = d.unique_id
            WHERE 
                d.title LIKE '%[TEST]%' OR 
                d.description LIKE '%[TEST]%' OR 
                d.donor_name LIKE '%Test User%'
            """
            
            # Delete associated images and files
            delete_images_query = """
            DELETE FROM donation_images
            WHERE donation_id IN (
                SELECT unique_id FROM donations 
                WHERE 
                    title LIKE '%[TEST]%' OR 
                    description LIKE '%[TEST]%' OR 
                    donor_name LIKE '%Test User%'
            )
            """
            
            # Delete donations
            delete_donations_query = """
            DELETE FROM donations 
            WHERE 
                title LIKE '%[TEST]%' OR 
                description LIKE '%[TEST]%' OR 
                donor_name LIKE '%Test User%'
            """
            
            # Execute deletion queries
            try:
                # Delete associated images first
                self.cursor.execute(delete_images_query)
                image_deleted_count = self.cursor.rowcount
                
                # Delete associated requests
                self.cursor.execute(delete_requests_query)
                request_deleted_count = self.cursor.rowcount
                
                # Delete donations
                self.cursor.execute(delete_donations_query)
                donation_deleted_count = self.cursor.rowcount
                
                # Commit the transaction
                self.connection.commit()
                
                print(f"Cleared test donations:")
                print(f"- Deleted {image_deleted_count} donation images")
                print(f"- Deleted {request_deleted_count} donation requests")
                print(f"- Deleted {donation_deleted_count} donations")
                
                return True, f"Cleared {donation_deleted_count} test donations"
            
            except mysql.connector.Error as delete_err:
                print(f"Error deleting test donations: {delete_err}")
                self.connection.rollback()
                return False, "Failed to clear test donations"
        
        except mysql.connector.Error as e:
            print(f"MySQL Connector Error clearing test donations: {e}")
            return False, f"Database error: {str(e)}"
        
        except Exception as e:
            print(f"Unexpected error clearing test donations: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Unexpected error: {str(e)}"
        
        finally:
            # Ensure cursor is reset
            try:
                self.reset_cursor()
            except Exception as reset_err:
                print(f"Error resetting cursor: {reset_err}")

    def login(self, username, password):
        """
        Authenticate user login
        
        :param username: User's username
        :param password: User's password
        :return: Dictionary with login result
        """
        try:
            # Ensure database connection is active
            if not self.connection.is_connected():
                self.reconnect()
            
            # Query to verify user credentials
            query = """
            SELECT 
                unique_id, 
                username, 
                password_hash, 
                email, 
                location,
                status
            FROM users 
            WHERE username = %s
            """
            
            # Execute query
            self.cursor.execute(query, (username,))
            user = self.cursor.fetchone()
            
            # Check if user exists
            if not user:
                return {
                    'success': False,
                    'message': 'User not found',
                    'error_code': 'USER_NOT_FOUND'
                }
            
            # Verify password (assuming password_hash is stored securely)
            if not self.verify_password(password, user['password_hash']):
                return {
                    'success': False,
                    'message': 'Invalid password',
                    'error_code': 'INVALID_PASSWORD'
                }
            
            # Check user status
            if user['status'] != 'active':
                return {
                    'success': False,
                    'message': f'Account is {user["status"]}',
                    'error_code': 'ACCOUNT_INACTIVE'
                }
            
            # Prepare user info
            user_info = {
                'unique_id': user['unique_id'],
                'username': user['username'],
                'email': user['email'],
                'location': user['location']
            }
            
            # Update last login (optional)
            update_last_login_query = """
            UPDATE users 
            SET last_login = NOW() 
            WHERE unique_id = %s
            """
            self.cursor.execute(update_last_login_query, (user['unique_id'],))
            self.connection.commit()
            
            return {
                'success': True,
                'message': 'Login successful',
                'user': user_info
            }
        
        except mysql.connector.Error as e:
            print(f"Database error during login: {e}")
            return {
                'success': False,
                'message': 'Database error',
                'error_code': 'DB_ERROR'
            }
        
        except Exception as e:
            print(f"Unexpected error during login: {e}")
            return {
                'success': False,
                'message': 'Unexpected error',
                'error_code': 'UNEXPECTED_ERROR'
            }
        
        finally:
            # Ensure cursor is reset
            try:
                self.reset_cursor()
            except Exception as reset_err:
                print(f"Error resetting cursor: {reset_err}")

    def get_donor_requests(self, donor_id, page=1, per_page=10):
        """
        Retrieve donation requests received by a specific donor
        
        :param donor_id: Unique ID of the donor
        :param page: Page number for pagination
        :param per_page: Number of requests per page
        :return: Dictionary with donation requests and pagination info
        """
        try:
            # Ensure database connection is active
            if not self.connection.is_connected():
                self.reconnect()
            
            # Calculate offset for pagination
            offset = (page - 1) * per_page

            # Query to get total count of requests
            count_query = """
            SELECT COUNT(*) as total_requests
            FROM donation_requests dr
            JOIN donations d ON dr.donation_id = d.unique_id
            WHERE d.donor_id = %s
            """
            
            # Query to get paginated donation requests
            requests_query = """
            SELECT 
                dr.unique_id as request_id,
                dr.donation_id,
                d.title as donation_title,
                d.category as donation_category,
                u_requester.username as requester_username,
                u_requester.email as requester_email,
                dr.request_message,
                dr.request_status,
                dr.created_at
            FROM donation_requests dr
            JOIN donations d ON dr.donation_id = d.unique_id
            JOIN users u_requester ON dr.requester_id = u_requester.unique_id
            WHERE d.donor_id = %s
            ORDER BY dr.created_at DESC
            LIMIT %s OFFSET %s
            """
            
            # Execute count query
            self.cursor.execute(count_query, (donor_id,))
            total_count = self.cursor.fetchone()['total_requests']
            
            # Execute requests query
            self.cursor.execute(requests_query, (donor_id, per_page, offset))
            requests = self.cursor.fetchall()
            
            # Calculate pagination details
            total_pages = (total_count + per_page - 1) // per_page
            
            return {
                'success': True,
                'requests': requests,
                'pagination': {
                    'total_requests': total_count,
                    'current_page': page,
                    'total_pages': total_pages,
                    'per_page': per_page
                }
            }
        
        except mysql.connector.Error as e:
            print(f"MySQL Connector Error retrieving donor requests: {e}")
            return {
                'success': False,
                'message': 'Error retrieving donation requests',
                'error_code': 'DB_ERROR'
            }
        
        except Exception as e:
            print(f"Unexpected error retrieving donor requests: {e}")
            return {
                'success': False,
                'message': 'Unexpected error retrieving donation requests',
                'error_code': 'UNEXPECTED_ERROR'
            }
        
        finally:
            # Ensure cursor is reset
            try:
                self.reset_cursor()
            except Exception as reset_err:
                print(f"Error resetting cursor: {reset_err}")

    def list_donation_requests(self, user_id, search_term=None, status=None, received_only=True):
        """
        List donation requests for a specific user with optional search and filtering

        :param user_id: Unique ID of the user (donor or requester)
        :param search_term: Optional search term to filter requests
        :param status: Optional status to filter requests
        :param received_only: If True, show only requests received by the user (default: True)
        :return: List of donation requests
        """
        try:
            # Ensure database connection is active
            if not self.connection.is_connected():
                self.reconnect()
            
            # Comprehensive query to fetch donation requests with details
            query = """
            SELECT 
                dr.unique_id AS request_id,
                dr.donation_id,
                dr.requester_id,
                dr.status AS request_status,
                dr.created_at AS request_created_at,
                
                d.unique_id AS donation_unique_id,
                d.title AS donation_title,
                d.category AS donation_category,
                d.description AS donation_description,
                u_requester.username AS requester_username,
                u_requester.email AS requester_email,
                
                u_donor.unique_id AS donor_id,
                u_donor.username AS donor_username,
                u_donor.email AS donor_email
            FROM 
                donation_requests dr
            JOIN 
                donations d ON dr.donation_id = d.unique_id
            JOIN 
                users u_requester ON dr.requester_id = u_requester.unique_id
            JOIN 
                users u_donor ON d.donor_id = u_donor.unique_id
            WHERE 
                1=1
            """
            
            # Prepare query parameters
            params = []
            
            # Filter by user's role (received or made requests)
            if received_only:
                # Show only requests for donations owned by the user
                query += " AND d.donor_id = %s"
                params.append(user_id)
            else:
                # Show requests made by the user
                query += " AND dr.requester_id = %s"
                params.append(user_id)
            
            # Add search term filter if provided
            if search_term:
                query += " AND (d.title LIKE %s OR d.description LIKE %s OR u_requester.username LIKE %s)"
                search_param = f"%{search_term}%"
                params.extend([search_param, search_param, search_param])
            
            # Add status filter if provided
            if status:
                query += " AND dr.status = %s"
                params.append(status)
            
            # Add ordering
            query += " ORDER BY dr.created_at DESC"
            
            # Execute the query
            self.cursor.execute(query, tuple(params))
            requests = self.cursor.fetchall()
            
            # Log query details for debugging
            print(f"Listing donation requests - User ID: {user_id}, Received Only: {received_only}, Search Term: {search_term}, Status: {status}")
            print(f"Total requests found: {len(requests)}")
            
            # Process and return results
            return requests
        
        except mysql.connector.Error as e:
            print(f"MySQL Connector Error listing donation requests: {e}")
            return []
        
        except Exception as e:
            print(f"Unexpected error listing donation requests: {e}")
            import traceback
            traceback.print_exc()
            return []
        
        finally:
            # Ensure cursor is reset
            try:
                self.reset_cursor()
            except Exception as reset_err:
                print(f"Error resetting cursor: {reset_err}")

    def get_donation_by_id(self, donation_id):
        """
        Retrieve a donation by its unique ID
        
        :param donation_id: Unique ID of the donation
        :return: Dictionary with donation details or None
        """
        try:
            # Extensive logging before query
            print("=" * 50)
            print("GET DONATION BY ID DEBUG")
            print(f"Input donation_id type: {type(donation_id)}")
            print(f"Input donation_id value: '{donation_id}'")
            print(f"Input donation_id str representation: '{str(donation_id)}'")
            
            # Validate input
            if not donation_id:
                print("Error: Empty donation ID provided")
                return None
            
            # Ensure donation_id is a string
            donation_id = str(donation_id).strip()
            
            # Prepare the query to get full donation details
            query = """
            SELECT 
                d.unique_id, 
                d.donor_id, 
                d.title, 
                d.description, 
                d.category, 
                d.condition, 
                d.state, 
                d.city, 
                d.status,
                u.username as donor_username,
                u.email as donor_email
            FROM donations d
            JOIN users u ON d.donor_id = u.unique_id
            WHERE d.unique_id = %s
            """
            
            # Print the exact query being executed
            print(f"Executing query with ID: '{donation_id}'")
            
            # Execute the query
            self.cursor.execute(query, (donation_id,))
            
            # Fetch the donation
            donation = self.cursor.fetchone()
            
            # Log raw database result
            print("Raw database result:")
            print(donation)
            
            if donation:
                # Convert to dictionary and add debugging
                donation_dict = dict(donation)
                
                # Debugging print
                print("Donation Found Debug:")
                for key, value in donation_dict.items():
                    print(f"{key}: {value}")
                
                return donation_dict
            
            # If no donation found, print comprehensive debug message
            print(f"No donation found with ID '{donation_id}'")
            
            # Additional diagnostic query to check all donation IDs
            print("\nChecking all donation IDs:")
            self.cursor.execute("SELECT unique_id FROM donations")
            all_ids = self.cursor.fetchall()
            print("Existing donation IDs:")
            for id_row in all_ids:
                print(f"  {id_row['unique_id']}")
            
            print("=" * 50)
            return None
        
        except mysql.connector.Error as e:
            print(f"MySQL Error retrieving donation: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error retrieving donation: {e}")
            return None
