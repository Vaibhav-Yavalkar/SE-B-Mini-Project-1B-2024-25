import tkinter as tk
from db import Database
import re
# import messagebox
from datetime import datetime

# Initialize database connection
db = Database()

# Sample Data for Doctors (static data instead of database)
doctor_data = {
    'name': 'Dr. Smith',
    'age': 45,
    'qualification': 'MBBS, MD (General Medicine)',
    'experience': 20
}

def open_doctor_info():
    # Create a new window
    window = tk.Toplevel()
    window.title("Doctor Information")
    window.geometry("600x400")  # Adjusted size

    # Title
    title_label = tk.Label(window, text="Doctor Information", font=("Arial", 20, "bold"))
    title_label.pack(pady=10)

    # Doctor Information Section
    doctor_frame = tk.Frame(window)
    doctor_frame.pack(pady=10)

    tk.Label(doctor_frame, text="Name:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    tk.Label(doctor_frame, text=doctor_data['name']).grid(row=0, column=1, padx=10, pady=5, sticky="w")

    tk.Label(doctor_frame, text="Age:", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Label(doctor_frame, text=doctor_data['age']).grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Label(doctor_frame, text="Qualification:", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    tk.Label(doctor_frame, text=doctor_data['qualification']).grid(row=2, column=1, padx=10, pady=5, sticky="w")

    tk.Label(doctor_frame, text="Years of Experience:", font=("Arial", 12, "bold")).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    tk.Label(doctor_frame, text=doctor_data['experience']).grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Button frame for Close and Back buttons
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    close_button = tk.Button(button_frame, text="Close", command=window.destroy, bg="red", fg="white")
    close_button.pack(side=tk.LEFT, padx=5)

    back_button = tk.Button(button_frame, text="Back to Menu", command=window.destroy, bg="gray", fg="white")
    back_button.pack(side=tk.LEFT, padx=5)

def submit_details():
    name = name_entry.get().strip()
    specialization = specialization_entry.get().strip()
    experience = experience_entry.get().strip()
    contact = contact_entry.get().strip()
    email = email_entry.get().strip()

    # Validate name
    if not name:
        messagebox.showwarning("Input Error", "Please enter the doctor's name!")
        return
    if not re.match(r'^[a-zA-Z\s]{2,50}$', name):
        messagebox.showwarning("Input Error", "Name should only contain letters and spaces (2-50 characters)!")
        return

    # Validate specialization
    if not specialization:
        messagebox.showwarning("Input Error", "Please enter the specialization!")
        return
    if not re.match(r'^[a-zA-Z\s]{2,50}$', specialization):
        messagebox.showwarning("Input Error", "Specialization should only contain letters and spaces!")
        return

    # Validate experience
    if not experience:
        messagebox.showwarning("Input Error", "Please enter years of experience!")
        return
    try:
        exp_num = int(experience)
        if exp_num < 0 or exp_num > 50:
            messagebox.showwarning("Input Error", "Please enter a valid experience (0-50 years)!")
            return
    except ValueError:
        messagebox.showwarning("Input Error", "Experience must be a number!")
        return

    # Validate contact
    if not contact:
        messagebox.showwarning("Input Error", "Please enter contact number!")
        return
    if not contact.isdigit() or len(contact) != 10:
        messagebox.showwarning("Input Error", "Contact number must be exactly 10 digits!")
        return

    # Validate email
    if not email:
        messagebox.showwarning("Input Error", "Please enter email address!")
        return
    if not re.fullmatch(r"[a-zA-Z0-9._%+-]+@gmail\.com", email):
        messagebox.showwarning("Input Error", "Email must be in format ____@gmail.com!")
        return

    # Update labels with doctor information
    doctor_info_label.config(text=f"Doctor: {name}, {specialization}")
    experience_label.config(text=f"Experience: {experience} years")
    contact_info_label.config(text=f"Contact: {contact}, Email: {email}")

    # Hide form and show doctor profile
    form_frame.pack_forget()
    profile_frame.pack(pady=10)

def add_schedule():
    date = date_entry.get().strip()
    time = time_entry.get().strip()
    duration = duration_entry.get().strip()

    # Validate date
    if not date:
        messagebox.showwarning("Input Error", "Please enter the date!")
        return
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        messagebox.showwarning("Input Error", "Date must be in YYYY-MM-DD format!")
        return

    # Validate date is not in the past
    try:
        schedule_date = datetime.strptime(date, '%Y-%m-%d').date()
        if schedule_date < datetime.now().date():
            messagebox.showwarning("Input Error", "Cannot add schedules for past dates!")
            return
    except ValueError:
        messagebox.showwarning("Input Error", "Invalid date format!")
        return

    # Validate time
    if not time:
        messagebox.showwarning("Input Error", "Please enter the time!")
        return
    if not re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$', time):
        messagebox.showwarning("Input Error", "Time must be in HH:MM format!")
        return

    # Validate duration
    if not duration:
        messagebox.showwarning("Input Error", "Please enter the duration!")
        return
    try:
        duration_num = int(duration)
        if duration_num < 15 or duration_num > 120:
            messagebox.showwarning("Input Error", "Duration must be between 15 and 120 minutes!")
            return
    except ValueError:
        messagebox.showwarning("Input Error", "Duration must be a number!")
        return

    # Add to schedule tree
    schedule_tree.insert("", "end", values=(date, time, duration))
    messagebox.showinfo("Success", "Schedule added successfully!")

    # Clear form fields
    date_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)