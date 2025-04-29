import tkinter as tk
from tkinter import ttk, messagebox
from db import Database
from datetime import datetime

# Initialize database connection
db = Database()

def open_view_appointments(username, root):
    # Create a new window
    window = tk.Toplevel(root)
    window.title("View Appointments")
    window.geometry("1200x600")
    window.transient(root)  
    window.grab_set()  # Make it modal

    # Title at the top
    title_label = tk.Label(window, text="Your Appointments", font=("Arial", 24, "bold"))
    title_label.pack(pady=10)

    # Create a frame for the treeview and buttons
    main_frame = tk.Frame(window)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create Treeview
    columns = ("Date", "Time", "Patient Name", "Doctor", "Diagnosis", "Status")
    appointments_tree = ttk.Treeview(main_frame, columns=columns, show="headings")

    # Set column headings
    for col in columns:
        appointments_tree.heading(col, text=col)
        appointments_tree.column(col, width=100)  # Default width

    # Set specific column widths
    appointments_tree.column("Date", width=100)
    appointments_tree.column("Time", width=100)
    appointments_tree.column("Patient Name", width=150)
    appointments_tree.column("Doctor", width=150)
    appointments_tree.column("Diagnosis", width=300)
    appointments_tree.column("Status", width=100)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=appointments_tree.yview)
    appointments_tree.configure(yscrollcommand=scrollbar.set)

    # Pack the treeview and scrollbar
    appointments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a frame for buttons
    button_frame = tk.Frame(window)
    button_frame.pack(fill=tk.X, padx=10, pady=5)

    def refresh_appointments():
        # Clear existing items
        for item in appointments_tree.get_children():
            appointments_tree.delete(item)

        # Get appointments from database
        appointments = db.get_user_appointments(username)
        
        if not appointments:
            messagebox.showinfo("No Appointments", "You have no appointments scheduled.")
            return

        # Sort appointments by date and time
        sorted_appointments = sorted(appointments, key=lambda x: (x['appointment_date'], x['appointment_time']))

        # Insert appointments into treeview
        for appt in sorted_appointments:
            # Validate appointment data
            try:
                # Validate date format
                datetime.strptime(str(appt['appointment_date']), '%Y-%m-%d')
                # Validate time format
                datetime.strptime(str(appt['appointment_time']), '%H:%M:%S')
            except ValueError:
                messagebox.showerror("Error", f"Invalid date/time format in appointment for {appt['patient_name']}")
                continue

            # Remove "Dr. Smith" from diagnosis if present
            diagnosis = appt['diagnosis']
            if diagnosis and "Dr. Smith" in diagnosis:
                diagnosis = diagnosis.replace("Dr. Smith", "").strip()

            # Validate diagnosis length
            if diagnosis and len(diagnosis) > 500:
                diagnosis = diagnosis[:497] + "..."

            appointments_tree.insert("", "end", values=(
                appt['appointment_date'],
                appt['appointment_time'],
                appt['patient_name'],
                "Dr. Smith",  # Default doctor
                diagnosis or "No diagnosis provided",
                appt['status']
            ))

    def delete_selected_appointment():
        # Get selected item
        selected_item = appointments_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an appointment to delete.")
            return

        # Get appointment details
        values = appointments_tree.item(selected_item)['values']
        date = values[0]
        time = values[1]
        patient_name = values[2]
        doctor = values[3]
        diagnosis = values[4]
        status = values[5]

        # Validate appointment status
        if status == "Confirmed":
            messagebox.showwarning("Cannot Delete", "Confirmed appointments cannot be deleted. Please contact the clinic for cancellation.")
            return

        # Validate appointment date
        try:
            appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
            if appointment_date < datetime.now().date():
                messagebox.showwarning("Cannot Delete", "Past appointments cannot be deleted.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid date format in appointment.")
            return

        # Confirm deletion with detailed information
        if messagebox.askyesno("Confirm Deletion", 
                             f"Are you sure you want to delete this appointment?\n\n"
                             f"Date: {date}\n"
                             f"Time: {time}\n"
                             f"Patient: {patient_name}\n"
                             f"Doctor: {doctor}\n"
                             f"Diagnosis: {diagnosis}\n"
                             f"Status: {status}"):
            # Delete from database
            if db.delete_appointment(username, date, time):
                messagebox.showinfo("Success", "Appointment deleted successfully!")
                refresh_appointments()  # Refresh the display
            else:
                messagebox.showerror("Error", "Failed to delete appointment. Please try again.")

    # Add buttons
    tk.Button(button_frame, text="Refresh", command=refresh_appointments, 
             bg="blue", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Delete Selected", command=delete_selected_appointment, 
             bg="red", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Back to Menu", command=window.destroy, 
             bg="gray", fg="white").pack(side=tk.LEFT, padx=5)


    refresh_appointments()

    
    window.transient(root)
    window.grab_set()

    window.mainloop() 