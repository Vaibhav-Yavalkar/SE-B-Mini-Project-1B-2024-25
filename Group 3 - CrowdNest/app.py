import tkinter as tk
from tkinter import messagebox, ttk
import os
from dotenv import load_dotenv
import sys
import traceback

# Import database handler
from src.database.database_handler import DatabaseHandler

# Import pages
from src.pages.dashboard_page import DashboardPage
from src.pages.login_page import LoginPage
from src.pages.register_page import RegisterPage
from src.pages.donation_form_page import DonationFormPage
from src.pages.donation_list_page import DonationListPage
from src.pages.profile_page import ProfilePage
from src.pages.donation_history_page import DonationHistoryPage
from src.pages.request_list_page import RequestListPage
from src.pages.accepted_requests_page import AcceptedRequestsPage
from src.ui.modern_ui import ModernUI
from src.ui.navigation import NavigationPane

class CrowdNestApp:
    def __init__(self, root):
        # Load environment variables
        load_dotenv()
        
        # Setup UI styles
        ModernUI.setup_styles()
        
        # Initialize database handler
        self.db = DatabaseHandler(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '12345678'),
            database=os.getenv('DB_NAME', 'CrowdNest')
        )
        
        # Set root window properties
        root.title("CrowdNest - Collective Resource Gathering")
        root.geometry("1024x768")  # Set a standard window size
        root.minsize(800, 600)  # Set minimum window size
        root.state('zoomed')  # Maximize the window
        
        # Root window setup
        self.root = root
        
        # User authentication state
        self.current_user = None
        self.user_info = None
        
        # Initialize frames dictionary
        self.frames = {}

        # Create main content frame with improved layout
        self.content_frame = ttk.Frame(root)
        self.content_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        # Create navigation pane
        self.nav_pane = NavigationPane(root, self.show_frame)
        self.nav_pane.logout_callback = self.logout  # Set the logout callback
        self.nav_pane.pack(side='left', fill='y')
        
        # Dictionary to map frame classes
        frame_classes = {
            'LoginPage': LoginPage,
            'RegisterPage': RegisterPage,
            'DashboardPage': DashboardPage,
            'DonationListPage': DonationListPage,
            'DonationFormPage': DonationFormPage,
            'DonationHistoryPage': DonationHistoryPage,
            'ProfilePage': ProfilePage,
            'RequestListPage': RequestListPage,
            'AcceptedRequestsPage': AcceptedRequestsPage
        }

        # Create frames dynamically
        for name, F in frame_classes.items():
            try:
                # Only create login and register pages initially
                if name in ['LoginPage', 'RegisterPage']:
                    frame = F(self.content_frame, 
                             self.login if name == 'LoginPage' else self.register, 
                             self.show_frame)
                    self.frames[name] = frame
                    if hasattr(frame, 'frame'):
                        frame.frame.pack_forget()
                    else:
                        print(f"Warning: {name} does not have a 'frame' attribute")

            except Exception as e:
                print(f"Error creating frame {name}: {e}")

        # Show login page initially
        self.show_frame('LoginPage')

    def show_frame(self, frame_name):
        """Show a specific frame, with authentication checks"""
        try:
            # List of frames that require authentication
            auth_required_frames = [
                'DashboardPage', 
                'DonationListPage', 
                'DonationFormPage', 
                'DonationHistoryPage', 
                'ProfilePage',
                'RequestListPage',
                'AcceptedRequestsPage'
            ]

            # Check if authentication is required for this frame
            if frame_name in auth_required_frames:
                if not self.current_user:
                    messagebox.showwarning("Login Required", f"You must be logged in to access {frame_name}")
                    frame_name = 'LoginPage'

            # Hide all frames
            for name, frame in self.frames.items():
                if hasattr(frame, 'frame'):
                    frame.frame.pack_forget()

            # Show the selected frame
            if frame_name in self.frames:
                frame = self.frames[frame_name]
                if hasattr(frame, 'frame'):
                    frame.frame.pack(fill='both', expand=True)

                # Update dashboard with user info if applicable
                if frame_name == 'DashboardPage' and self.current_user:
                    if hasattr(frame, 'update_user_info'):
                        frame.update_user_info(self.current_user)

            return frame_name

        except Exception as e:
            print(f"Error showing frame {frame_name}: {e}")
            messagebox.showerror("Navigation Error", f"Could not navigate to {frame_name}")

    def login(self, username, password):
        """Handle user login"""
        try:
            # Authenticate user via database
            user_info = self.db.authenticate_user(username, password)
            
            if user_info and 'unique_id' in user_info:
                # Successful authentication
                messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                
                # Initialize frames with authenticated user info
                if self.login_success(user_info):
                    # Explicitly show only the dashboard
                    self.show_frame('DashboardPage')
                else:
                    messagebox.showerror("Login Error", "Failed to initialize user session")
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        
        except Exception as e:
            messagebox.showerror("Login Error", str(e))

    def register(self, username, email, password, location):
        """Handle user registration"""
        try:
            # Validate inputs
            if not username or not email or not password or not location:
                messagebox.showerror("Registration Error", "All fields are required")
                return False
            
            # Register user via database
            user_id = self.db.register_user(username, email, password, location)
            
            if user_id:
                messagebox.showinfo("Registration Successful", "You can now log in!")
                self.show_frame('LoginPage')
                return True
            else:
                messagebox.showerror("Registration Failed", "Username or email might already exist")
                return False
        
        except Exception as e:
            messagebox.showerror("Registration Error", str(e))
            return False

    def submit_donation(self, title, description, category, condition, state, city, image_data, image_type=None):
        """Handle donation submission"""
        try:
            # Add donation to database
            success, message, donation_data = self.db.create_donation(
                donor_id=self.current_user['unique_id'],
                title=title,
                description=description,
                category=category,
                condition=condition,
                state=state,
                city=city,
                image_data=image_data,
                image_type=image_type
            )
            
            if success:
                messagebox.showinfo("Success", "Donation submitted successfully!")
                self.show_frame('DonationListPage')
                return True
            else:
                messagebox.showerror("Error", message)
                return False
                
        except Exception as e:
            messagebox.showerror("Error", f"Error submitting donation: {str(e)}")
            return False

    def logout(self):
        """Handle user logout"""
        try:
            # Clear user data
            self.current_user = None
            self.user_info = None
            
            # Clear all frames
            for name, frame in self.frames.items():
                if hasattr(frame, 'frame'):
                    frame.frame.pack_forget()
            
            # Show login page
            self.show_frame('LoginPage')
            
            # Show logout confirmation
            messagebox.showinfo("Logged Out", "You have been successfully logged out.")
            
            # Reset frames to initial state
            self.frames = {name: frame for name, frame in self.frames.items()
                           if name in ['LoginPage', 'RegisterPage']}
            
            # Ensure navigation pane remains visible
            if hasattr(self, 'nav_pane'):
                self.nav_pane.pack(side='left', fill='y')
            
        except Exception as e:
            print(f"Error in logout: {e}")
            messagebox.showerror("Logout Error", "An error occurred during logout")
    
    def login_success(self, user_info):
        """Handle successful login"""
        try:
            # Store user info
            self.current_user = user_info
            self.user_info = user_info
            
            # Initialize authenticated frames
            frame_classes = {
                'DashboardPage': DashboardPage,
                'DonationListPage': DonationListPage,
                'DonationFormPage': DonationFormPage,
                'DonationHistoryPage': DonationHistoryPage,
                'ProfilePage': ProfilePage,
                'RequestListPage': RequestListPage,
                'AcceptedRequestsPage': AcceptedRequestsPage
            }
            
            # Create authenticated frames with actual user data
            for name, F in frame_classes.items():
                try:
                    if name == 'DonationFormPage':
                        frame = F(self.content_frame, self.submit_donation, self.show_frame)
                    else:
                        frame = F(self.content_frame, user_info, self.show_frame)
                    self.frames[name] = frame
                    if hasattr(frame, 'frame'):
                        frame.frame.pack_forget()
                except Exception as e:
                    print(f"Error creating frame {name}: {e}")
            
            # Update navigation pane
            self.nav_pane.update_user_info(user_info)
            
            return True
            
        except Exception as e:
            print(f"Error in login_success: {e}")
            return False

if __name__ == '__main__':
    # Create and run Tkinter app
    root = tk.Tk()
    app = CrowdNestApp(root)
    root.mainloop()