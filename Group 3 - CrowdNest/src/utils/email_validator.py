import re
import smtplib
import random
import os
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class EmailValidator:
    @staticmethod
    def is_valid_email(email):
        """
        Validate email format using a comprehensive regex pattern
        
        :param email: Email address to validate
        :return: Boolean indicating email validity
        """
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None
    
    # Alias for is_valid_email to maintain compatibility
    validate_email = is_valid_email
    
    @staticmethod
    def generate_verification_code(length=6):
        """
        Generate a random verification code
        
        :param length: Length of verification code
        :return: Verification code as string
        """
        return ''.join(random.choices('0123456789', k=length))
    
    @staticmethod
    def send_verification_email(recipient_email, verification_code):
        """
        Send email verification code
        
        :param recipient_email: Email address to send verification code
        :param verification_code: Verification code to send
        :return: Boolean indicating email sending success
        """
        try:
            # Email configuration from environment variables
            smtp_server = os.getenv('SMTP_SERVER')
            smtp_port = int(os.getenv('SMTP_PORT'))
            sender_email = os.getenv('SMTP_EMAIL')
            smtp_password = os.getenv('SMTP_PASSWORD')
            
            # Validate input parameters
            if not smtp_server or not smtp_port or not sender_email or not smtp_password:
                error_msg = "Missing SMTP configuration. Check your .env file."
                print(error_msg)
                return False, error_msg
            
            # Create HTML message using template
            from src.utils.html_email_templates import HTMLEmailTemplates
            
            # Create a verification message with proper styling
            verification_message = f"Your verification code is: {verification_code}"
            html_content = HTMLEmailTemplates.verification_email_template("User", verification_message)
            
            # Create MIME message with HTML content
            message = HTMLEmailTemplates.create_mime_message(
                subject='CrowdNest Email Verification',
                html_content=html_content,
                from_email=sender_email,
                to_email=recipient_email
            )
            
            # Create SMTP session with detailed error handling
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.set_debuglevel(1)  # Enable debug output
                server.ehlo()  # Can help diagnose connection issues
                server.starttls()  # Enable security
                
                try:
                    server.login(sender_email, smtp_password)
                except smtplib.SMTPAuthenticationError as auth_err:
                    error_msg = (
                        "Gmail authentication failed. You need to use an App Password instead of your regular password.\n\n"
                        "To create an App Password:\n"
                        "1. Go to your Google Account > Security\n"
                        "2. Under 'Signing in to Google', select 'App passwords'\n"
                        "3. Generate a new app password for 'Mail'\n"
                        "4. Update your .env file with this password in the SMTP_PASSWORD field"
                    )
                    print(f"SMTP Authentication Error: {auth_err}")
                    print(error_msg)
                    return False, error_msg
                
                try:
                    server.send_message(message)
                except Exception as send_err:
                    error_msg = f"Email sending error: {send_err}"
                    print(error_msg)
                    traceback.print_exc()
                    return False, error_msg
            
            return True, ""
        except Exception as e:
            error_msg = f"Comprehensive email sending error: {e}"
            print(error_msg)
            traceback.print_exc()
            return False, error_msg
    
    @staticmethod
    def send_email(recipient_email, subject, body):
        """
        Send a general email
        
        :param recipient_email: Email of the recipient
        :param subject: Email subject
        :param body: Email body
        :return: Tuple of (success: bool, error_message: str)
        """
        try:
            # Email configuration from environment variables
            smtp_server = os.getenv('SMTP_SERVER')
            smtp_port = int(os.getenv('SMTP_PORT'))
            sender_email = os.getenv('SMTP_EMAIL')
            smtp_password = os.getenv('SMTP_PASSWORD')
            
            # Validate input parameters
            if not smtp_server or not smtp_port or not sender_email or not smtp_password:
                error_msg = "Missing SMTP configuration. Check your .env file."
                print(error_msg)
                return False, error_msg
            
            # Create message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            
            # Create SMTP session with detailed error handling
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.set_debuglevel(1)  # Enable debug output
                server.ehlo()  # Can help diagnose connection issues
                server.starttls()  # Enable security
                
                try:
                    server.login(sender_email, smtp_password)
                except smtplib.SMTPAuthenticationError as auth_err:
                    error_msg = "SMTP Authentication Error. Check your credentials."
                    print(f"{error_msg}: {auth_err}")
                    return False, error_msg
                
                try:
                    server.send_message(message)
                except Exception as send_err:
                    error_msg = f"Email sending error: {send_err}"
                    print(error_msg)
                    traceback.print_exc()
                    return False, error_msg
            
            return True, ""
        except Exception as e:
            error_msg = f"Comprehensive email sending error: {e}"
            print(error_msg)
            traceback.print_exc()
            return False, error_msg

    @staticmethod
    def send_communication_email(platform_email, platform_password, recipient_email, subject, body):
        """
        Send an email using platform's email credentials
        
        :param platform_email: Sender's email address
        :param platform_password: Sender's email password/app password
        :param recipient_email: Recipient's email address
        :param subject: Email subject
        :param body: Email body
        :return: Boolean indicating email sending success
        """
        try:
            # Validate email inputs
            if not platform_email or not platform_password or not recipient_email:
                print("Invalid email configuration: Missing required parameters")
                return False
            
            # Validate email format
            if not re.match(r"[^@]+@[^@]+\.[^@]+", recipient_email):
                print(f"Invalid recipient email: {recipient_email}")
                return False
            
            # Create message
            message = MIMEMultipart()
            message['From'] = platform_email
            message['To'] = recipient_email
            message['Subject'] = subject
            
            # Construct full body
            full_body = f"""{body}

            Sent via CrowdNest Platform
            """
            
            message.attach(MIMEText(full_body, 'plain'))
            
            # Create SMTP session with detailed error handling
            smtp_server = os.getenv('SMTP_SERVER')
            smtp_port = int(os.getenv('SMTP_PORT'))
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.set_debuglevel(1)  # Enable debug output
                server.ehlo()  # Can help diagnose connection issues
                server.starttls()  # Enable security
                
                try:
                    server.login(platform_email, platform_password)
                except smtplib.SMTPAuthenticationError as auth_err:
                    print(f"SMTP Authentication Error: {auth_err}")
                    print("Possible causes:")
                    print("1. Incorrect email or password")
                    print("2. Need to use App Password for Gmail")
                    print("3. Less secure app access might be disabled")
                    return False
                
                try:
                    # Explicitly validate recipient email
                    server.verify(recipient_email)
                    
                    # Send message
                    server.send_message(message)
                except smtplib.SMTPRecipientsRefused as recipient_err:
                    print(f"Recipient email refused: {recipient_err}")
                    print(f"Invalid recipient: {recipient_email}")
                    return False
                except Exception as send_err:
                    print(f"Email sending error: {send_err}")
                    traceback.print_exc()
                    return False
            
            return True
        except Exception as e:
            print(f"Comprehensive email sending error: {e}")
            traceback.print_exc()
            return False

    @staticmethod
    def send_request_notification(requester_name, requester_email, donor_email, donation_title):
        """
        Send notification email for donation request
        
        :param requester_name: Name of the person requesting the donation
        :param requester_email: Email of the requester
        :param donor_email: Email of the donor
        :param donation_title: Title of the requested donation
        :return: Boolean indicating email sending success
        """
        subject = f"New Donation Request: {donation_title}"
        body = f"""
        Hello,

        {requester_name} has requested your donation: {donation_title}

        You can accept or decline this request through the CrowdNest platform.
        Please log in to your account to manage this request.

        Best regards,
        CrowdNest Team
        """
        
        # Email configuration from environment variables
        platform_email = os.getenv('SMTP_EMAIL')
        platform_password = os.getenv('SMTP_PASSWORD')
        
        return EmailValidator.send_communication_email(
            platform_email,
            platform_password,
            donor_email,
            subject,
            body
        )
