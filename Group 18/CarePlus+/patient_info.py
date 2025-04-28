import tkinter as tk
from tkinter import ttk, messagebox
from db import Database
import re
from datetime import datetime
from tkcalendar import Calendar

# Initialize database connection
db = Database()

def open_patient_info(username):
    # Store patient information
    patient_info = {
        'name': '',
        'gender': '',
        'contact': '',
        'email': ''
    }

    def submit_details():
        name = name_entry.get().strip()
        age = age_entry.get().strip()
        gender = gender_dropdown.get().strip()
        contact = contact_entry.get().strip()
        email = email_entry.get().strip()

        # Validate name
        if not name:
            messagebox.showwarning("Input Error", "Please enter your name!")
            return
        if not re.match(r'^[a-zA-Z\s]{2,50}$', name):
            messagebox.showwarning("Input Error", "Name should only contain letters and spaces (2-50 characters)!")
            return

        # Validate age
        if not age:
            messagebox.showwarning("Input Error", "Please enter your age!")
            return
        try:
            age_num = int(age)
            if age_num < 0 or age_num > 100:
                messagebox.showwarning("Input Error", "Please enter a valid age (0-100)!")
                return
        except ValueError:
            messagebox.showwarning("Input Error", "Age must be a number!")
            return

        # Validate gender
        if not gender:
            messagebox.showwarning("Input Error", "Please select your gender!")
            return

        # Validate contact
        if not contact:
            messagebox.showwarning("Input Error", "Please enter your contact number!")
            return
        if not contact.isdigit() or len(contact) != 10:
            messagebox.showwarning("Input Error", "Contact number must be exactly 10 digits!")
            return

        # Validate email
        if not email:
            messagebox.showwarning("Input Error", "Please enter your email address!")
            return
        if not re.fullmatch(r"[a-zA-Z0-9._%+-]+@gmail\.com", email):
            messagebox.showwarning("Input Error", "Email must be in format ____@gmail.com!")
            return

        # Store patient information
        patient_info['name'] = name
        patient_info['gender'] = gender
        patient_info['contact'] = contact
        patient_info['email'] = email

        # Update labels with user input
        patient_info_label.config(text=f"Patient: {name}, {age}, Gender: {gender}")
        contact_info_label.config(text=f"Contact: {contact}, Email: {email}")

        # Hide form and show patient profile
        form_frame.pack_forget()
        profile_frame.pack(pady=10)

    def update_clock():
        current_time = datetime.now().strftime('%H:%M:%S')
        clock_label.config(text=current_time)
        window.after(1000, update_clock)

    def add_appointment():
        # Get selected appointment from treeview
        selected_item = appointments_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an appointment to cancel!")
            return
        
        # Get the appointment details
        appointment = appointments_tree.item(selected_item)['values']
        
        # Confirm cancellation
        confirm = messagebox.askyesno("Confirm Cancellation", 
                                    f"Are you sure you want to cancel the appointment on {appointment[0]} at {appointment[1]}?")
        if confirm:
            # Update the appointment status in the database
            db.update_appointment_status(username, appointment[0], appointment[1], "Cancelled")
            
            # Update the treeview
            appointments_tree.set(selected_item, 'Status', "Cancelled")
            messagebox.showinfo("Success", "Appointment cancelled successfully!")

    def update_clock():
        current_time = datetime.now().strftime('%H:%M:%S')
        clock_label.config(text=current_time)
        window.after(1000, update_clock)

    # Main window
    window = tk.Toplevel()  # Changed from Tk() to Toplevel()
    window.title("Patient Profile")
    window.grab_set()  # Make it modal
    
    # Create main frame with scrollbar
    main_frame = tk.Frame(window)
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

    # Form Frame
    form_frame = tk.Frame(scrollable_frame)
    form_frame.pack(pady=10, padx=20)

    tk.Label(form_frame, text="Patient Details", font=("Arial", 20)).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(form_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
    name_entry = tk.Entry(form_frame)
    name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Age:").grid(row=2, column=0, padx=5, pady=5)
    age_entry = tk.Entry(form_frame)
    age_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Gender:").grid(row=3, column=0, padx=5, pady=5)
    gender_dropdown = ttk.Combobox(form_frame, values=["Male", "Female", "Other"])
    gender_dropdown.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Contact:").grid(row=4, column=0, padx=5, pady=5)
    contact_entry = tk.Entry(form_frame)
    contact_entry.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Email:").grid(row=5, column=0, padx=5, pady=5)
    email_entry = tk.Entry(form_frame)
    email_entry.grid(row=5, column=1, padx=5, pady=5)

    submit_button = tk.Button(form_frame, text="Submit", command=submit_details)
    submit_button.grid(row=6, column=0, columnspan=2, pady=10)

    # Profile Frame (Hidden initially)
    profile_frame = tk.Frame(scrollable_frame)

    patient_info_label = tk.Label(profile_frame, text="", font=("Arial", 16))
    patient_info_label.pack(pady=5)

    contact_info_label = tk.Label(profile_frame, text="", font=("Arial", 12))
    contact_info_label.pack(pady=5)

    # Appointments Section
    appointments_label = tk.Label(profile_frame, text="Booked Appointments", font=("Arial", 20))
    appointments_label.pack(pady=10)

    # Add tree with horizontal scrollbar
    tree_frame = tk.Frame(profile_frame)
    tree_frame.pack(fill=tk.X, padx=20)
    
    appointments_tree = ttk.Treeview(tree_frame, columns=("Date", "Time", "Doctor", "Status"), show="headings", height=6)
    appointments_tree.heading("Date", text="Date")
    appointments_tree.heading("Time", text="Time")
    appointments_tree.heading("Doctor", text="Doctor")
    appointments_tree.heading("Status", text="Status")
    
    # Configure column widths
    appointments_tree.column("Date", width=100)
    appointments_tree.column("Time", width=100)
    appointments_tree.column("Doctor", width=150)
    appointments_tree.column("Status", width=100)
    
    # Add vertical and horizontal scrollbars for the tree
    tree_vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=appointments_tree.yview)
    tree_hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=appointments_tree.xview)
    appointments_tree.configure(yscrollcommand=tree_vsb.set, xscrollcommand=tree_hsb.set)
    
    # Grid layout for tree and scrollbars
    appointments_tree.grid(row=0, column=0, sticky="nsew")
    tree_vsb.grid(row=0, column=1, sticky="ns")
    tree_hsb.grid(row=1, column=0, sticky="ew")
    tree_frame.grid_columnconfigure(0, weight=1)

    # Calendar and time selection frame
    calendar_time_frame = tk.Frame(profile_frame)
    calendar_time_frame.pack(pady=10)

    # Right side frame
    right_frame = tk.Frame(calendar_time_frame)
    right_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)

    # Button frame at the bottom of right frame
    button_frame = tk.Frame(right_frame)
    button_frame.pack(pady=10)

    add_appt_button = tk.Button(button_frame, text="Cancel Appointment", command=add_appointment, 
                               bg="red", fg="white", width=15, height=1)
    add_appt_button.pack(pady=(0, 5))

    back_button = tk.Button(button_frame, text="Back to Menu", command=window.destroy, 
                           bg="gray", fg="white", width=15, height=1)
    back_button.pack()

    # Load existing appointments from database
    appointments = db.get_user_appointments(username)
    for appt in appointments:
        appointments_tree.insert("", "end", values=(
            appt['appointment_date'],
            appt['appointment_time'],
            "Dr. Smith",
            appt['status']
        ))

    # Configure window size based on content
    window.update_idletasks()  # Update geometry
    window_width = scrollable_frame.winfo_reqwidth() + scrollbar.winfo_reqwidth() + 40
    window_height = scrollable_frame.winfo_reqheight() + 40
    
    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calculate position for center of screen
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    # Set window size and position
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Start Main Loop
    window.mainloop()