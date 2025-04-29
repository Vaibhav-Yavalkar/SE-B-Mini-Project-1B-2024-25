import tkinter as tk
from tkinter import messagebox
from doctor_info import open_doctor_info
from patient_info import open_patient_info
from view_appointments import open_view_appointments
import subprocess
import re
from tkinter import scrolledtext, font, ttk
import random
from db import Database
from datetime import datetime
from tkcalendar import Calendar
from PIL import Image, ImageTk

# Initialize database connection
db = Database()

class ClinicManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("CarePlus : A Smart clinic")
        self.root.geometry("600x600")

        self.current_user = None
        self.create_welcome_page()

    def create_welcome_page(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Welcome to CarePlus : A Smart clinic", font=("Arial", 14, "bold")).pack(pady=20)

        tk.Button(self.root, text="Login", width=20, command=self.open_login_page).pack(pady=10)
        tk.Button(self.root, text="Signup", width=20, command=self.open_signup_page).pack(pady=10)
        tk.Button(self.root, text="Exit", width=20, command=self.root.quit, bg="red", fg="white").pack(pady=10)

    def open_login_page(self):
        self.login_page = tk.Toplevel(self.root)
        self.login_page.title("Login")
        self.login_page.geometry("400x300")

        tk.Label(self.login_page, text="Login", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.login_page, text="Username:").pack()
        self.username_entry = tk.Entry(self.login_page)
        self.username_entry.pack()

        tk.Label(self.login_page, text="Password:").pack()
        self.password_entry = tk.Entry(self.login_page, show="*")
        self.password_entry.pack()

        tk.Button(self.login_page, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.login_page, text="Back", command=self.login_page.destroy).pack(pady=5)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Validate empty fields
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        # Validate username format (alphanumeric, 4-20 characters)
        if not re.match(r'^[a-zA-Z0-9]{4,20}$', username):
            messagebox.showerror("Error", "Username must be 4-20 characters long and contain only letters and numbers!")
            return

        # Validate password length (minimum 6 characters)
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long!")
            return

        if db.verify_user(username, password):
            # Check for appointment notifications
            db.check_appointment_notifications()
            
            # Show login success message
            messagebox.showinfo("Success", "Login successful!")
            self.login_page.destroy()
            self.create_home_page(username)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def open_signup_page(self):
        self.signup_page = tk.Toplevel(self.root)
        self.signup_page.title("Signup")
        self.signup_page.geometry("400x400")

        tk.Label(self.signup_page, text="Signup", font=("Arial", 14, "bold")).pack(pady=10)

        # Username frame
        username_frame = tk.Frame(self.signup_page)
        username_frame.pack(pady=5)
        tk.Label(username_frame, text="Username:").pack()
        self.new_username_entry = tk.Entry(username_frame)
        self.new_username_entry.pack()
        tk.Label(username_frame, text="(4-20 characters, letters and numbers only)", 
                font=("Arial", 8)).pack()

        # Password frame
        password_frame = tk.Frame(self.signup_page)
        password_frame.pack(pady=5)
        tk.Label(password_frame, text="Password:").pack()
        self.new_password_entry = tk.Entry(password_frame, show="*")
        self.new_password_entry.pack()
        tk.Label(password_frame, text="(minimum 6 characters)", 
                font=("Arial", 8)).pack()

        # Confirm password frame
        confirm_frame = tk.Frame(self.signup_page)
        confirm_frame.pack(pady=5)
        tk.Label(confirm_frame, text="Confirm Password:").pack()
        self.confirm_password_entry = tk.Entry(confirm_frame, show="*")
        self.confirm_password_entry.pack()

        # Buttons frame
        button_frame = tk.Frame(self.signup_page)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Signup", command=self.signup, 
                 bg="green", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back", command=self.signup_page.destroy,
                 bg="gray", fg="white").pack(side=tk.LEFT, padx=5)

    def signup(self):
        username = self.new_username_entry.get().strip()
        password = self.new_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        # Validate empty fields
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        # Validate username format (alphanumeric, 4-20 characters)
        if not re.match(r'^[a-zA-Z0-9]{4,20}$', username):
            messagebox.showerror("Error", "Username must be 4-20 characters long and contain only letters and numbers!")
            return

        # Validate password length (minimum 6 characters)
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long!")
            return

        # Validate password match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Validate password strength (at least one uppercase, one lowercase, one number)
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', password):
            messagebox.showerror("Error", "Password must contain at least one uppercase letter, one lowercase letter, and one number!")
            return

        if db.add_user(username, password):
            messagebox.showinfo("Success", "Signup Successful!")
            self.signup_page.destroy()
            self.create_home_page(username)
        else:
            messagebox.showerror("Error", "Username already exists!")

    def create_home_page(self, username):
        self.current_user = username

        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Home Page layout
        tk.Label(self.root, text=f"Welcome, {username}", font=("Arial", 14, "bold")).pack(pady=10)

        features = [
            "User Profile", "Doctor's Profile", "Book Appointment",
            "View Appointments", "Feedback", "Notifications", "Chat Support"
        ]

        for feature in features:
            button = tk.Button(self.root, text=feature, width=25, height=2,
                               command=lambda f=feature: self.handle_home_page_click(f))
            button.pack(pady=5)

        # Add Logout button
        tk.Button(self.root, text="Logout", width=25, height=2,
                   command=self.create_welcome_page, bg="red", fg="white").pack(pady=5)

    def handle_home_page_click(self, feature):
        if feature == "User Profile":
            open_patient_info(self.current_user)
        elif feature == "Doctor's Profile":
            self.root.withdraw()  # Hide main window
            open_doctor_info()
            self.root.deiconify()  # Show main window again
        elif feature == "Book Appointment":
            self.open_book_appointment_page()
        elif feature == "View Appointments":
            open_view_appointments(self.current_user, self.root)
        elif feature == "Feedback":
            self.open_feedback_form()
        elif feature == "Notifications":
            self.open_notifications_page()
        elif feature == "Chat Support":
            self.open_chat_support()

    def open_book_appointment_page(self):
        self.appointment_page = tk.Toplevel(self.root)
        self.appointment_page.title("Book Appointment")
        self.appointment_page.geometry("500x350")
        self.appointment_page.transient(self.root)  # Make it a transient window
        self.appointment_page.grab_set()  # Make it modal

        tk.Label(self.appointment_page, text="Patient Information", font=("Arial", 14, "bold")).grid(row=0, column=0,columnspan=3,pady=20)

        # Patient Name
        tk.Label(self.appointment_page, text="Name:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.patient_name = tk.Entry(self.appointment_page)
        self.patient_name.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.appointment_page, text="Gender:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.patient_gender = tk.StringVar(value="Male")

        gender_frame = tk.Frame(self.appointment_page)
        gender_frame.grid(row=2, column=1, padx=5, pady=5)

        tk.Radiobutton(gender_frame, text="Male", variable=self.patient_gender, value="Male").pack(side="left", padx=5)
        tk.Radiobutton(gender_frame, text="Female", variable=self.patient_gender, value="Female").pack(side="left",
                                                                                                       padx=5)
        tk.Radiobutton(gender_frame, text="Other", variable=self.patient_gender, value="Other").pack(side="left",
                                                                                                     padx=5)

        tk.Label(self.appointment_page, text="Contact No:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.patient_contact = tk.Entry(self.appointment_page)
        self.patient_contact.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.appointment_page, text="Email Address:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.patient_email = tk.Entry(self.appointment_page)
        self.patient_email.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.appointment_page, text="Diagnosis (Short Description):").grid(row=5, column=0, sticky="e", padx=5,pady=5)
        self.patient_diagnosis = tk.Text(self.appointment_page, height=3, width=30, wrap="word")
        self.patient_diagnosis.grid(row=5, column=1, padx=5, pady=5)

        # Button frame for Next and Back buttons
        button_frame = tk.Frame(self.appointment_page)
        button_frame.grid(row=10, column=0, columnspan=3, pady=20)

        tk.Button(button_frame, text="Next", command=self.validate_input, bg="green", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back to Menu", command=lambda: [self.appointment_page.destroy(), self.create_home_page(self.current_user)], bg="gray", fg="white").pack(side=tk.LEFT, padx=5)

    def validate_input(self):
        # Get all input values
        name = self.patient_name.get().strip()
        contact_no = self.patient_contact.get().strip()
        email = self.patient_email.get().strip()
        diagnosis = self.patient_diagnosis.get("1.0", "end-1c").strip()

        # Validate name
        if not name:
            messagebox.showerror("Invalid Input", "Please enter your name.")
            return
        if not re.match(r'^[a-zA-Z\s]{2,50}$', name):
            messagebox.showerror("Invalid Input", "Name should only contain letters and spaces (2-50 characters).")
            return

        # Validate contact number
        if not contact_no:
            messagebox.showerror("Invalid Input", "Please enter your contact number.")
            return
        if not contact_no.isdigit() or len(contact_no) != 10:
            messagebox.showerror("Invalid Input", "Contact number must be exactly 10 digits.")
            return

        # Validate email
        if not email:
            messagebox.showerror("Invalid Input", "Please enter your email address.")
            return
        if not re.fullmatch(r"[a-zA-Z0-9._%+-]+@gmail\.com", email):
            messagebox.showerror("Invalid Input", "Email must be in format ____@gmail.com.")
            return

        # Validate diagnosis
        if not diagnosis:
            messagebox.showerror("Invalid Input", "Please enter a brief diagnosis.")
            return
        if len(diagnosis) > 500:
            messagebox.showerror("Invalid Input", "Diagnosis should not exceed 500 characters.")
            return

        self.show_slot_selection()

    def show_slot_selection(self):
        self.slot_window = tk.Toplevel(self.root)
        self.slot_window.title("Select Appointment Slot")
        self.slot_window.geometry("500x600")  # Reduced height
        self.slot_window.transient(self.root)
        self.slot_window.grab_set()

        # Create main frame with scrollbar
        main_frame = tk.Frame(self.slot_window)
        main_frame.pack(fill="both", expand=True)

        # Create canvas and scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Calendar widget
        tk.Label(scrollable_frame, text="Select Date:", font=("Arial", 12)).pack(pady=(10, 5))
        current_date = datetime.now()
        self.calendar = Calendar(scrollable_frame, 
                               selectmode='day',
                               year=current_date.year,
                               month=current_date.month,
                               day=current_date.day,
                               mindate=current_date,
                               date_pattern='yyyy-mm-dd')
        self.calendar.pack(pady=10, padx=10)

        # Digital clock frame
        clock_frame = tk.Frame(scrollable_frame)
        clock_frame.pack(pady=10)
        tk.Label(clock_frame, text="Current Time:", font=("Arial", 10)).pack()
        self.clock_label = tk.Label(clock_frame, font=("Arial", 20), fg="blue")
        self.clock_label.pack()
        self.update_clock()

        tk.Label(scrollable_frame, text="Select a Slot:", font=("Arial", 12)).pack(pady=10)

        self.slot_var = tk.StringVar()
        self.slot_var.set(None)
        slots = {
            "Morning": ["09:30", "10:00", "10:30", "11:00"],
            "Afternoon": ["12:00", "12:30", "13:00", "13:30", "14:00"],
            "Evening": ["17:00", "17:30", "18:00"]
        }

        # Create a frame for slots
        slots_frame = tk.Frame(scrollable_frame)
        slots_frame.pack(fill=tk.BOTH, padx=20)

        for period, times in slots.items():
            period_frame = tk.LabelFrame(slots_frame, text=period, font=("Arial", 10, "bold"))
            period_frame.pack(fill=tk.X, pady=5)

            for time in times:
                tk.Radiobutton(period_frame, text=time, variable=self.slot_var, value=time).pack(anchor="w", padx=10)

        # Button frame for Book Slot and Back buttons (outside scrollable frame)
        button_frame = tk.Frame(self.slot_window)
        button_frame.pack(pady=10, padx=20, fill="x")

        tk.Button(button_frame, text="Book Slot", command=self.book_slot, bg="green", fg="white").pack(side=tk.LEFT, padx=5, expand=True)
        tk.Button(button_frame, text="Back to Menu", command=lambda: [self.slot_window.destroy(), self.create_home_page(self.current_user)], bg="gray", fg="white").pack(side=tk.LEFT, padx=5, expand=True)

    def update_clock(self):
        current_time = datetime.now().strftime('%H:%M:%S')
        self.clock_label.config(text=current_time)
        self.slot_window.after(1000, self.update_clock)

    def book_slot(self):
        selected_slot = self.slot_var.get()
        selected_date = self.calendar.get_date()

        # Validate date
        if not selected_date:
            messagebox.showwarning("Warning", "Please select a date")
            return

        # Validate slot selection
        if not selected_slot:
            messagebox.showwarning("Warning", "Please select a slot")
            return

        # Check if slot is available
        if db.is_slot_available(selected_date, selected_slot):
            if db.add_appointment(
                self.current_user,
                self.patient_name.get(),
                self.patient_gender.get(),
                self.patient_contact.get(),
                self.patient_email.get(),
                self.patient_diagnosis.get("1.0", "end-1c"),
                selected_date,
                selected_slot,
                "Pending"  # Default status for new appointments
            ):
                messagebox.showinfo("Success", f"Successfully booked your appointment on {selected_date} at {selected_slot}")
                self.slot_window.destroy()
                self.appointment_page.destroy()  # Close both windows
            else:
                messagebox.showerror("Error", "Failed to book appointment. Please try again.")
        else:
            messagebox.showerror("Error", "This slot is already booked. Please select another slot.")

    def open_notifications_page(self):
        self.notifications_page = tk.Toplevel(self.root)
        self.notifications_page.title("Notifications")
        self.notifications_page.geometry("400x500")
        self.notifications_page.transient(self.root)  # Make it a transient window
        self.notifications_page.grab_set()  # Make it modal

        # Title with notification count
        notifications = db.get_unread_notifications(self.current_user)
        title_text = f"Your Notifications ({len(notifications)} unread)"
        tk.Label(self.notifications_page, text=title_text, font=("Arial", 14, "bold")).pack(pady=10)

        # Create a frame for notifications with scrollbar
        notifications_frame = tk.Frame(self.notifications_page)
        notifications_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create canvas and scrollbar
        canvas = tk.Canvas(notifications_frame)
        scrollbar = ttk.Scrollbar(notifications_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        if notifications:
            for notification in notifications:
                # Create a frame for each notification
                notif_frame = tk.Frame(scrollable_frame)
                notif_frame.pack(fill="x", pady=5, padx=5)
                
                # Add a colored dot for unread notifications
                dot = tk.Label(notif_frame, text="●", fg="blue", font=("Arial", 12))
                dot.pack(side="left", padx=5)
                
                # Message and timestamp
                message = notification['message']
                date = notification['created_at'].strftime("%Y-%m-%d %H:%M")
                
                # Message label with word wrap
                msg_label = tk.Label(notif_frame, text=message, wraplength=300, justify="left")
                msg_label.pack(side="left", padx=5)
                
                # Timestamp label
                time_label = tk.Label(notif_frame, text=date, fg="gray", font=("Arial", 8))
                time_label.pack(side="right", padx=5)
            
            # Mark notifications as read
            db.mark_notifications_as_read(self.current_user)
        else:
            tk.Label(scrollable_frame, text="No new notifications", fg="gray").pack(pady=20)

        # Back button
        tk.Button(self.notifications_page, text="Back to Menu", 
                 command=lambda: [self.notifications_page.destroy(), self.create_home_page(self.current_user)], 
                 bg="gray", fg="white").pack(pady=10)

    def open_feedback_form(self):
        self.feedback_page = tk.Toplevel(self.root)
        self.feedback_page.title("Feedback")
        self.feedback_page.geometry("500x650")
        self.feedback_page.transient(self.root)
        self.feedback_page.grab_set()

        # Create a main frame with scrollbar
        main_frame = tk.Frame(self.feedback_page)
        main_frame.pack(fill="both", expand=True)

        # Create canvas and scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Title
        tk.Label(scrollable_frame, text="Feedback Form", font=("Arial", 16, "bold")).pack(pady=20)

        # Star Rating Frame
        rating_frame = tk.Frame(scrollable_frame)
        rating_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(rating_frame, text="Rate your experience:", font=("Arial", 12)).pack(side="left")
        
        # Create star rating
        self.rating_var = tk.IntVar(value=0)
        stars_frame = tk.Frame(rating_frame)
        stars_frame.pack(side="right", padx=5)
        
        def update_rating(value):
            self.rating_var.set(value)
            # Update star colors
            for i in range(5):
                if i < value:
                    star_labels[i].config(text="★", fg="gold")
                else:
                    star_labels[i].config(text="☆", fg="gray")

        star_labels = []
        for i in range(5):
            star_label = tk.Label(stars_frame, text="☆", 
                                font=("Arial", 20), fg="gray",
                                cursor="hand2")
            star_label.pack(side="left", padx=2)
            star_label.bind("<Button-1>", lambda e, val=i+1: update_rating(val))
            star_label.bind("<Enter>", lambda e, val=i+1: [
                star_labels[j].config(text="★", fg="gold") for j in range(val)
            ] + [
                star_labels[j].config(text="☆", fg="gray") for j in range(val, 5)
            ])
            star_label.bind("<Leave>", lambda e: [
                star_labels[j].config(text="★", fg="gold") if j < self.rating_var.get() 
                else star_labels[j].config(text="☆", fg="gray") 
                for j in range(5)
            ])
            star_labels.append(star_label)

        # Department Selection
        dept_frame = tk.Frame(scrollable_frame)
        dept_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(dept_frame, text="Select Department:", font=("Arial", 12)).pack(side="left")
        self.department_var = tk.StringVar(value="General")
        department_combo = ttk.Combobox(dept_frame, textvariable=self.department_var, 
                                      values=["General", "Cardiology", "Orthopedics", "Pediatrics", "Dental", "Other"],
                                      width=20)
        department_combo.pack(side="right", padx=5)

        # Service Quality
        tk.Label(scrollable_frame, text="Service Quality:", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Service Quality Checkboxes with descriptions
        self.service_qualities = {
            "Staff Friendliness": ("How friendly and helpful was our staff?", tk.BooleanVar(value=False)),
            "Less Waiting Time": ("How satisfied were you with the waiting time?", tk.BooleanVar(value=False)),
            "Doctor Expertise": ("How would you rate the doctor's expertise?", tk.BooleanVar(value=False)),
            "Communication": ("How effective was the communication?", tk.BooleanVar(value=False)),
            "Facility Availability": ("How satisfied were you with the facilities?", tk.BooleanVar(value=False)),
        }

        # Create a frame for checkboxes with descriptions
        checkbox_frame = tk.Frame(scrollable_frame)
        checkbox_frame.pack(fill="x", padx=20)

        for quality, (description, var) in self.service_qualities.items():
            # Create a frame for each checkbox and its description
            check_container = tk.Frame(checkbox_frame)
            check_container.pack(fill="x", pady=3)  # Reduced padding from 5 to 3
            
            # Add checkbox
            tk.Checkbutton(check_container, text=quality, variable=var, 
                          font=("Arial", 10, "bold")).pack(anchor="w")
            
            # Add description
            tk.Label(check_container, text=description, 
                    font=("Arial", 9), fg="gray").pack(anchor="w", padx=20)

        # Comments
        tk.Label(scrollable_frame, text="Your Comments:", font=("Arial", 12, "bold")).pack(pady=10)
        self.comments_text = tk.Text(scrollable_frame, height=5, width=40)  # Reduced height from 6 to 5
        self.comments_text.pack(pady=5)
        
        # Add placeholder text
        self.comments_text.insert("1.0", "Please share your experience with us...")
        self.comments_text.bind("<FocusIn>", lambda e: self.on_comments_focus_in())
        self.comments_text.bind("<FocusOut>", lambda e: self.on_comments_focus_out())

        # Submit Button (outside scrollable frame)
        submit_btn = tk.Button(self.feedback_page, text="Submit Feedback", 
                             command=self.submit_feedback,
                             bg="#4a90e2", fg="white", font=("Arial", 11),
                             width=20, height=2)
        submit_btn.pack(pady=10)  # Reduced padding from 20 to 10

    def on_comments_focus_in(self):
        if self.comments_text.get("1.0", "end-1c") == "Please share your experience with us...":
            self.comments_text.delete("1.0", tk.END)

    def on_comments_focus_out(self):
        if not self.comments_text.get("1.0", "end-1c").strip():
            self.comments_text.insert("1.0", "Please share your experience with us...")

    def submit_feedback(self):
        # Get feedback data
        rating = self.rating_var.get()
        department = self.department_var.get()
        comments = self.comments_text.get("1.0", "end-1c").strip()
        
        # Validate rating
        if not rating:
            messagebox.showerror("Error", "Please select a rating.")
            return
        try:
            rating_num = int(rating)
            if rating_num < 1 or rating_num > 5:
                messagebox.showerror("Error", "Rating must be between 1 and 5.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid rating value.")
            return

        # Validate department
        if not department:
            messagebox.showerror("Error", "Please select a department.")
            return
        valid_departments = ["General", "Cardiology", "Orthopedics", "Pediatrics", "Dental", "Other"]
        if department not in valid_departments:
            messagebox.showerror("Error", "Invalid department selected.")
            return

        # Validate comments
        if not comments or comments == "Please share your experience with us...":
            messagebox.showerror("Error", "Please provide your comments.")
            return
        if len(comments) > 1000:
            messagebox.showerror("Error", "Comments should not exceed 1000 characters.")
            return
        
        # Get selected service qualities
        selected_qualities = [quality for quality, (_, var) in self.service_qualities.items() if var.get()]
        if not selected_qualities:
            messagebox.showerror("Error", "Please select at least one service quality.")
            return

        # Format feedback with more structure
        formatted_comments = f"""Rating: {rating}/5
Department: {department}

Service Qualities Selected:
{chr(10).join(f"- {quality}" for quality in selected_qualities)}

Comments:
{comments}"""

        if db.add_feedback(self.current_user, int(rating), formatted_comments, department):
            messagebox.showinfo("Success", "Thank you for your valuable feedback!")
            self.feedback_page.destroy()
        else:
            messagebox.showerror("Error", "Failed to submit feedback. Please try again.")

    def open_chat_support(self):
        self.chat_page = tk.Toplevel(self.root)
        self.chat_page.title("Chat Support")
        self.chat_page.geometry("500x700")
        self.chat_page.transient(self.root)
        self.chat_page.grab_set()

        # Title
        tk.Label(self.chat_page, text="Chat Support", font=("Arial", 16, "bold")).pack(pady=10)

        # Chat display area with custom colors
        self.chat_display = scrolledtext.ScrolledText(self.chat_page, wrap=tk.WORD, height=20)
        self.chat_display.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Configure text colors and tags
        self.chat_display.tag_configure("user", foreground="#0000FF")  # Blue for user messages
        self.chat_display.tag_configure("bot", foreground="#008000")   # Green for bot messages

        # Message input area
        input_frame = tk.Frame(self.chat_page)
        input_frame.pack(padx=10, pady=5, fill="x")

        self.message_entry = tk.Entry(input_frame)
        self.message_entry.pack(side="left", fill="x", expand=True)

        send_button = tk.Button(input_frame, text="Send", command=self.send_chat_message,
                              bg="#4a90e2", fg="white")
        send_button.pack(side="right", padx=5)

        # Quick Help section
        tk.Label(self.chat_page, text="Quick Help", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Quick help buttons frame
        quick_help_frame = tk.Frame(self.chat_page)
        quick_help_frame.pack(pady=10, padx=10)

        # Quick help buttons
        quick_help_buttons = [
            ("Appointment Book", self.quick_help_appointment),
            ("Cancellation", self.quick_help_cancellation),
            ("Contact Info", self.quick_help_contact)
        ]

        for text, command in quick_help_buttons:
            btn = tk.Button(quick_help_frame, text=text, command=command,
                          bg="white", fg="#4a90e2", relief="solid", width=15)
            btn.pack(side="left", padx=5, pady=5)

        # Load chat history
        self.display_chat_messages()

        # Bind Enter key to send message
        self.message_entry.bind("<Return>", lambda e: self.send_chat_message())

    def quick_help_appointment(self):
        self.message_entry.insert(0, "How do I book an appointment?")
        self.send_chat_message()

    def quick_help_cancellation(self):
        self.message_entry.insert(0, "What is the cancellation policy?")
        self.send_chat_message()

    def quick_help_contact(self):
        self.message_entry.insert(0, "How can I contact the clinic?")
        self.send_chat_message()

    def display_user_message(self, message):
        self.chat_display.insert(tk.END, f"\naryan: {message}\n", "user")
        self.chat_display.see(tk.END)

    def display_chatbot_message(self, message):
        self.chat_display.insert(tk.END, f"\nChatbot: {message}\n", "bot")
        self.chat_display.see(tk.END)

    def handle_chatbot_response(self, user_message):
        # Basic chatbot responses
        user_message = user_message.lower().strip()
        
        # Validate message length
        if len(user_message) > 100:
            return "Your message is too long. Please keep it brief and clear."
        
        # Check for common spam patterns
        if re.match(r'^[a-zA-Z0-9]{20,}$', user_message):
            return "Please use proper spacing and punctuation in your message."
        
        # Check for repeated characters
        if re.match(r'(.)\1{4,}', user_message):
            return "Please avoid using repeated characters."
        
        if "hello" in user_message or "hi" in user_message:
            return "Hello! How can I help you today?"
        elif "appointment" in user_message:
            return "To book an appointment:\n1. Click on 'Book Appointment'\n2. Fill in your details\n3. Select a date and time slot\n4. Submit the form"
        elif "cancel" in user_message:
            return "To cancel an appointment:\n1. Go to 'View Appointments'\n2. Select the appointment\n3. Click 'Cancel'\n4. Confirm cancellation"
        elif "bill" in user_message:
            return "For billing assistance:\n1. Go to 'Billing'\n2. View your current bill\n3. Choose payment method\n4. Complete payment"
        elif "bye" in user_message:
            return "Goodbye! Have a great day!"
        else:
            return "I'm here to help! What would you like to know?"

    def display_chat_messages(self):
        # Get chat history
        messages = db.get_chat_history(self.current_user)
        
        # Display messages
        for message in messages:
            if message['is_bot']:
                self.display_chatbot_message(message['message'])
            else:
                self.display_user_message(message['message'])

    def send_chat_message(self):
        message = self.message_entry.get().strip()
        
        # Validate message
        if not message:
            messagebox.showwarning("Warning", "Please enter a message.")
            return
            
        if len(message) > 500:
            messagebox.showerror("Error", "Message should not exceed 500 characters.")
            return
            
        # Validate message content (no special characters or scripts)
        if not re.match(r'^[a-zA-Z0-9\s.,!?-]+$', message):
            messagebox.showerror("Error", "Message contains invalid characters.")
            return

        # Validate message frequency (prevent spam)
        current_time = datetime.now()
        if hasattr(self, 'last_message_time'):
            time_diff = (current_time - self.last_message_time).total_seconds()
            if time_diff < 1:  # Minimum 1 second between messages
                messagebox.showwarning("Warning", "Please wait a moment before sending another message.")
                return
        self.last_message_time = current_time

        # Add user message to chat
        self.display_user_message(message)
        db.add_chat_message(self.current_user, message)
        
        # Clear input
        self.message_entry.delete(0, tk.END)
        
        # Get and display chatbot response
        response = self.handle_chatbot_response(message)
        self.display_chatbot_message(response)
        db.add_chat_message(self.current_user, response, is_bot=True)

def main():
    root = tk.Tk()
    app = ClinicManagementSystem(root)
    
    # Center the window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 600
    window_height = 600
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
