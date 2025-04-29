import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .html_email_templates import HTMLEmailTemplates

def send_email(to_email, subject, body, from_name='CrowdNest', from_email=None):
    """
    Send an email using SMTP
    
    :param to_email: Recipient email address
    :param subject: Email subject
    :param body: Email body
    :param from_name: Sender name (optional)
    :param from_email: Sender email (optional)
    :return: Boolean indicating email sending success
    """
    try:
        # Load SMTP configuration from environment variables
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        smtp_username = os.getenv('SMTP_EMAIL')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        # Validate SMTP configuration
        missing_configs = []
        if not smtp_server:
            missing_configs.append('SMTP_SERVER')
        if not smtp_username:
            missing_configs.append('SMTP_EMAIL')
        if not smtp_password:
            missing_configs.append('SMTP_PASSWORD')
            
        if missing_configs:
            print(f"Missing SMTP configuration: {', '.join(missing_configs)}")
            return False
        
        # Use default from_email if not provided
        from_email = from_email or smtp_username
        
        # Create HTML email content
        html_content = HTMLEmailTemplates.create_generic_email_template(
            title=subject,
            message=body,
            sender_name=from_name
        )
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Attach HTML content
        msg.attach(MIMEText(html_content, 'html'))
        
        # Send email with enhanced error handling
        try:
            with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
                server.starttls()
                try:
                    server.login(smtp_username, smtp_password)
                except smtplib.SMTPAuthenticationError:
                    print("SMTP authentication failed - check username and password")
                    return False
                
                try:
                    server.send_message(msg)
                    print(f"Email sent successfully to {to_email}")
                    return True
                except smtplib.SMTPRecipientsRefused:
                    print(f"Invalid recipient email address: {to_email}")
                    return False
        except smtplib.SMTPConnectError:
            print(f"Failed to connect to SMTP server: {smtp_server}:{smtp_port}")
            return False
    
    except smtplib.SMTPException as smtp_err:
        print(f"SMTP Error sending email: {smtp_err}")
        return False
    
    except Exception as e:
        print(f"Unexpected error sending email: {e}")
        import traceback
        traceback.print_exc()
        return False
