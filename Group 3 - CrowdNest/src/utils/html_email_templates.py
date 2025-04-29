from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class HTMLEmailTemplates:
    # Brand colors
    PRIMARY_COLOR = "#4A90E2"  # Blue
    SECONDARY_COLOR = "#F5F7FA"  # Light Gray
    TEXT_COLOR = "#333333"  # Dark Gray
    ACCENT_COLOR = "#2ECC71"  # Green

    @staticmethod
    def _get_base_template(content):
        return f"""
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <title>CrowdNest</title>
        </head>
        <body style="margin: 0; padding: 0;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f4f4f4;">
                <tr>
                    <td align="center" style="padding: 20px 0;">
                        <table border="0" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <tr>
                                <td align="center" bgcolor="{HTMLEmailTemplates.PRIMARY_COLOR}" style="padding: 20px;">
                                    <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-family: Arial, sans-serif;">CrowdNest</h1>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 30px; font-family: Arial, sans-serif;">
                                    {content}
                                </td>
                            </tr>
                            <tr>
                                <td align="center" bgcolor="{HTMLEmailTemplates.SECONDARY_COLOR}" style="padding: 20px;">
                                    <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; margin: 0; font-size: 14px; font-family: Arial, sans-serif;">CrowdNest Community - Connecting People Through Giving</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

    @staticmethod
    def request_donation_template(requester_name, donator_name, donation_item, additional_message=None):
        content = f"""
        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">Dear {donator_name},</p>
        
        <div style="background-color: {HTMLEmailTemplates.SECONDARY_COLOR}; padding: 20px; border-radius: 6px; margin: 20px 0;">
            <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; margin: 0;">I hope this email finds you well. My name is {requester_name}, and I am reaching out regarding the {donation_item} you have listed on CrowdNest.</p>
        </div>
        """

        if additional_message:
            content += f"""
            <div style="background-color: #FFF8E1; padding: 15px; border-left: 4px solid #FFC107; margin: 20px 0;">
                <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; margin: 0;"><strong>Additional Context:</strong> {additional_message}</p>
            </div>
            """

        content += f"""
        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">I would greatly appreciate your consideration in donating this item. If you are willing to help, please respond to this email, and we can discuss the details of the donation.</p>

        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">Thank you for your kindness and support.</p>

        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">
            Best regards,<br>
            {requester_name}<br>
            <span style="color: {HTMLEmailTemplates.PRIMARY_COLOR};">CrowdNest Community</span>
        </p>
        """

        return HTMLEmailTemplates._get_base_template(content)

    @staticmethod
    def donation_confirmation_template(donator_name, requester_name, donation_item):
        content = f"""
        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">Dear {requester_name},</p>

        <div style="background-color: {HTMLEmailTemplates.ACCENT_COLOR}; color: white; padding: 20px; border-radius: 6px; margin: 20px 0;">
            <p style="margin: 0;">I am pleased to confirm that I would like to donate the {donation_item} to you through the CrowdNest platform.</p>
        </div>

        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">Let's discuss the logistics of the donation. Please reply to this email with your preferred method of collection or delivery.</p>

        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">
            Best regards,<br>
            {donator_name}<br>
            <span style="color: {HTMLEmailTemplates.PRIMARY_COLOR};">CrowdNest Community</span>
        </p>
        """

        return HTMLEmailTemplates._get_base_template(content)

    @staticmethod
    def donation_received_template(donator_name, requester_name, donation_item):
        content = f"""
        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">Dear {donator_name},</p>

        <div style="background-color: {HTMLEmailTemplates.SECONDARY_COLOR}; padding: 20px; border-radius: 6px; margin: 20px 0;">
            <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; margin: 0;">I wanted to express my heartfelt gratitude for donating the {donation_item}. Your generosity has made a significant difference in my life.</p>
        </div>

        <div style="text-align: center; margin: 30px 0;">
            <p style="color: {HTMLEmailTemplates.PRIMARY_COLOR}; font-size: 18px; font-weight: bold;">Thank you for being a part of the CrowdNest community and helping those in need.</p>
        </div>

        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">
            Warmest regards,<br>
            {requester_name}<br>
            <span style="color: {HTMLEmailTemplates.PRIMARY_COLOR};">CrowdNest Community</span>
        </p>
        """

        return HTMLEmailTemplates._get_base_template(content)

    @staticmethod
    def verification_email_template(user_name, verification_link):
        content = f"""
        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">Dear {user_name},</p>

        <div style="background-color: {HTMLEmailTemplates.SECONDARY_COLOR}; padding: 20px; border-radius: 6px; margin: 20px 0;">
            <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; margin: 0;">Thank you for joining CrowdNest! To get started, please verify your email address by clicking the button below.</p>
        </div>

        <div style="text-align: center; margin: 30px 0;">
            <a href="{verification_link}" style="background-color: {HTMLEmailTemplates.ACCENT_COLOR}; color: white; padding: 12px 30px; text-decoration: none; border-radius: 4px; font-weight: bold; display: inline-block;">Verify Email Address</a>
        </div>

        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 14px; line-height: 1.6; margin-top: 20px;">
            If the button doesn't work, you can copy and paste this link into your browser:<br>
            <span style="color: {HTMLEmailTemplates.PRIMARY_COLOR};">{verification_link}</span>
        </p>

        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 14px; line-height: 1.6; margin-top: 20px;">
            This verification link will expire in 24 hours. If you didn't create an account with CrowdNest, please ignore this email.
        </p>

        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">
            Best regards,<br>
            <span style="color: {HTMLEmailTemplates.PRIMARY_COLOR};">The CrowdNest Team</span>
        </p>
        """

        return HTMLEmailTemplates._get_base_template(content)

    @staticmethod
    def create_mime_message(subject, html_content, from_email, to_email):
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = from_email
        message['To'] = to_email
        
        html_part = MIMEText(html_content, 'html')
        message.attach(html_part)
        
        return message

    @staticmethod
    def generate_request_status_email(status, request_details):
        """
        Generate an HTML email template for donation request status updates
        
        :param status: Status of the request (approved/rejected)
        :param request_details: Dictionary containing request information
        :return: HTML email template as a string
        """
        # Extract request details with fallback values
        requester_name = request_details.get('requester_username', 'Valued Donor')
        donation_title = request_details.get('donation_title', 'Unnamed Donation')
        request_message = request_details.get('request_message', 'No additional details')
        
        if status.lower() == 'approved':
            return HTMLEmailTemplates.donation_request_accepted_template(
                requester_name,
                donation_title,
                request_details.get('donor_username', 'Donor'),
                request_details.get('donor_email', '')
            )
        elif status.lower() == 'rejected':
            return HTMLEmailTemplates.donation_request_rejected_template(
                requester_name,
                donation_title
            )
        else:
            content = f"""
            <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">Dear {requester_name},</p>
            
            <div style="background-color: {HTMLEmailTemplates.SECONDARY_COLOR}; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; margin: 0;">Your donation request for {donation_title} has been updated.</p>
            </div>
            
            <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid {HTMLEmailTemplates.PRIMARY_COLOR}; margin: 20px 0;">
                <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; margin: 0;">Status: {status.capitalize()}</p>
                <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; margin: 10px 0 0 0;">Your Request: {request_message}</p>
            </div>
            
            <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">
                If you have any questions, please don't hesitate to contact our support team.
            </p>
            
            <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">
                Best regards,<br>
                <span style="color: {HTMLEmailTemplates.PRIMARY_COLOR};">The CrowdNest Team</span>
            </p>
            """
            return HTMLEmailTemplates._get_base_template(content)

    @staticmethod
    def generate_request_status_plain_text(status, request_details):
        """
        Generate a plain text version of the email for email clients that don't support HTML
        
        :param status: Status of the request (approved/rejected)
        :param request_details: Dictionary containing request information
        :return: Plain text email content
        """
        # Determine message based on status
        if status.lower() == 'approved':
            status_message = 'Approved'
            additional_message = (
                "Great news! Your donation request has been carefully reviewed and approved. "
                "Our team will guide you through the next steps of the donation process."
            )
        elif status.lower() == 'rejected':
            status_message = 'Rejected'
            additional_message = (
                "We regret to inform you that your donation request could not be processed at this time. "
                "Our team carefully reviews each request to ensure the best match for community needs."
            )
        else:
            status_message = status.capitalize()
            additional_message = "Your donation request status has been updated."
        
        # Extract request details with fallback values
        requester_name = request_details.get('requester_username', 'Valued Donor')
        donation_title = request_details.get('donation_title', 'Unnamed Donation')
        request_message = request_details.get('request_message', 'No additional details')
        
        plain_text = f"""CrowdNest Donation Request Update

Dear {requester_name},

{additional_message}

Request Details:
- Donation: {donation_title}
- Your Request: {request_message}
- Status: {status_message}

If you have any questions or need further clarification, 
please contact our support team.

Best regards,
CrowdNest Team
&copy; 2025 CrowdNest. All rights reserved.
"""
        
        return plain_text

    @staticmethod
    def donation_request_accepted_template(requester_username, donation_title, donor_username, donor_email):
        """
        Create an HTML email template for accepted donation requests
        
        :param requester_username: Username of the requester
        :param donation_title: Title of the donation
        :param donor_username: Username of the donor
        :param donor_email: Email of the donor
        :return: HTML email content
        """
        content = f"""
        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">Dear {requester_username},</p>
        
        <div style="background-color: {HTMLEmailTemplates.ACCENT_COLOR}; color: white; padding: 20px; border-radius: 6px; margin: 20px 0;">
            <p style="margin: 0;">Great news! Your request for the donation "{donation_title}" has been accepted.</p>
        </div>
        
        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">
            The donor, {donor_username}, has accepted your request. You can contact them at {donor_email} to arrange the details of the donation.
        </p>
        
        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">
            Thank you for being part of the CrowdNest community!
        </p>
        
        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">
            Best regards,<br>
            <span style="color: {HTMLEmailTemplates.PRIMARY_COLOR};">The CrowdNest Team</span>
        </p>
        """
        
        return HTMLEmailTemplates._get_base_template(content)
    
    @staticmethod
    def donation_request_rejected_template(requester_username, donation_title):
        """
        Create an HTML email template for rejected donation requests
        
        :param requester_username: Username of the requester
        :param donation_title: Title of the donation
        :return: HTML email content
        """
        content = f"""
        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">Dear {requester_username},</p>
        
        <div style="background-color: #FF6B6B; color: white; padding: 20px; border-radius: 6px; margin: 20px 0;">
            <p style="margin: 0;">We regret to inform you that your request for the donation "{donation_title}" has been declined.</p>
        </div>
        
        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">
            Don't be discouraged! There are many other donations available on CrowdNest that might better suit your needs.
        </p>
        
        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">
            Thank you for being part of the CrowdNest community!
        </p>
        
        <p style="color: {HTMLEmailTemplates.TEXT_COLOR}; font-size: 16px; line-height: 1.6;">
            Best regards,<br>
            <span style="color: {HTMLEmailTemplates.PRIMARY_COLOR};">The CrowdNest Team</span>
        </p>
        """
        
        return HTMLEmailTemplates._get_base_template(content)
    
    @staticmethod
    def create_generic_email_template(title, message, sender_name='CrowdNest User'):
        """
        Create a generic HTML email template
        
        :param title: Email subject/title
        :param message: Main email body message
        :param sender_name: Name of the sender
        :return: HTML email content
        """
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .container {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .header {{
                    background-color: #4CAF50;
                    color: white;
                    text-align: center;
                    padding: 10px;
                    border-radius: 8px 8px 0 0;
                }}
                .content {{
                    margin-top: 20px;
                }}
                .footer {{
                    margin-top: 20px;
                    text-align: center;
                    font-size: 0.8em;
                    color: #777;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>CrowdNest Communication</h1>
                </div>
                <div class="content">
                    <h2>{title}</h2>
                    <p>{message}</p>
                </div>
                <div class="footer">
                    <p>Sent via CrowdNest by {sender_name}</p>
                    <p> {datetime.now().year} CrowdNest. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content

    @staticmethod
    def donation_request_accepted_template(requester_username, donation_title, donor_username, donor_email):
        """
        Generate HTML template for accepted donation request
        
        :param requester_username: Username of the requester
        :param donation_title: Title of the donation
        :param donor_username: Username of the donor
        :param donor_email: Email of the donor
        :return: HTML email template as string
        """
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
                .container {{ background-color: #f4f4f4; border-radius: 10px; padding: 20px; }}
                .header {{ background-color: #4CAF50; color: white; text-align: center; padding: 10px; border-radius: 5px; }}
                .content {{ background-color: white; padding: 20px; border-radius: 5px; margin-top: 10px; }}
                .footer {{ text-align: center; color: #777; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Donation Request Accepted!</h1>
                </div>
                <div class="content">
                    <p>Dear {requester_username},</p>
                    
                    <p>Great news! Your donation request for <strong>'{donation_title}'</strong> has been accepted by the donor.</p>
                    
                    <h3>Next Steps:</h3>
                    <ul>
                        <li>The donor will contact you with further details</li>
                        <li>Please be prepared to coordinate the donation pickup or delivery</li>
                    </ul>
                    
                    <h3>Donor Contact Information:</h3>
                    <p>
                        <strong>Username:</strong> {donor_username}<br>
                        <strong>Email:</strong> {donor_email}
                    </p>
                    
                    <p>We recommend reaching out to the donor soon to discuss the details of your donation.</p>
                    Best regards,<br>
                    <span style="color: {HTMLEmailTemplates.PRIMARY_COLOR};">The CrowdNest Team</span>
                
                </div>
                <div class="footer">
                    <p> 2024 CrowdNest. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

    @staticmethod
    def donation_request_rejected_template(requester_username, donation_title):
        """
        Generate HTML template for rejected donation request
        
        :param requester_username: Username of the requester
        :param donation_title: Title of the donation
        :return: HTML email template as string
        """
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
                .container {{ background-color: #f4f4f4; border-radius: 10px; padding: 20px; }}
                .header {{ background-color: #F44336; color: white; text-align: center; padding: 10px; border-radius: 5px; }}
                .content {{ background-color: white; padding: 20px; border-radius: 5px; margin-top: 10px; }}
                .footer {{ text-align: center; color: #777; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Donation Request Rejected</h1>
                </div>
                <div class="content">
                    <p>Dear {requester_username},</p>
                    
                    <p>We regret to inform you that your donation request for <strong>'{donation_title}'</strong> has been rejected by the donor.</p>
                    
                    <h3>Possible Reasons:</h3>
                    <ul>
                        <li>Donation no longer available</li>
                        <li>Donor's preference</li>
                        <li>Logistical constraints</li>
                    </ul>
                    
                    <p>We encourage you to continue exploring other available donations on CrowdNest. Our platform is constantly updated with new opportunities.</p>
                    
                    <p>Don't get discouraged! Keep searching and you'll find the perfect donation.</p>
                    Best regards,<br>
                    <span style="color: {HTMLEmailTemplates.PRIMARY_COLOR};">The CrowdNest Team</span>
                </div>
                <div class="footer">
                    <p> 2024 CrowdNest. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """