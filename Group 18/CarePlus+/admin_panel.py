import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from db import Database
from datetime import datetime, timedelta

# Initialize database connection
db = Database()

class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("CarePlus Admin Panel")
        self.root.geometry("1200x800")
        
        # Create main container
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(self.main_container, text="CarePlus Admin Panel", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create tabs
        self.appointments_tab = ttk.Frame(self.notebook)
        self.users_tab = ttk.Frame(self.notebook)
        self.reports_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.appointments_tab, text="Appointments")
        self.notebook.add(self.users_tab, text="Users")
        self.notebook.add(self.reports_tab, text="Reports")
        
        # Initialize tabs
        self.setup_appointments_tab()
        self.setup_users_tab()
        self.setup_reports_tab()

    def setup_appointments_tab(self):
        # Appointments management section
        tk.Label(self.appointments_tab, text="Appointments Management", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Search frame
        search_frame = tk.Frame(self.appointments_tab)
        search_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_appointments)
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=5)
        
        # Filter frame
        filter_frame = tk.Frame(self.appointments_tab)
        filter_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(filter_frame, text="Status:").pack(side=tk.LEFT, padx=5)
        self.status_var = tk.StringVar(value="All")
        status_menu = ttk.Combobox(filter_frame, textvariable=self.status_var, 
                                 values=["All", "Pending", "Confirmed", "Cancelled"])
        status_menu.pack(side=tk.LEFT, padx=5)
        status_menu.bind('<<ComboboxSelected>>', lambda e: self.filter_appointments())
        
        # Date range
        tk.Label(filter_frame, text="Date Range:").pack(side=tk.LEFT, padx=5)
        self.date_var = tk.StringVar(value="All")
        date_menu = ttk.Combobox(filter_frame, textvariable=self.date_var,
                               values=["All", "Today", "This Week", "This Month"])
        date_menu.pack(side=tk.LEFT, padx=5)
        date_menu.bind('<<ComboboxSelected>>', lambda e: self.filter_appointments())
        
        # Create Treeview for appointments
        columns = ("Date", "Time", "Patient Name", "Doctor", "Status", "Username")
        self.appointments_tree = ttk.Treeview(self.appointments_tab, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=100)
            
        # Hide the Username column (we'll use it for internal reference)
        self.appointments_tree.column("Username", width=0, stretch=False)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.appointments_tab, orient=tk.VERTICAL, 
                                command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.appointments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.appointments_tab)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(buttons_frame, text="Confirm Selected", command=self.confirm_appointment,
                 bg="green", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Cancel Selected", command=self.cancel_appointment,
                 bg="red", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Remove Test Data", command=self.remove_test_data,
                 bg="red", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Refresh", command=self.refresh_appointments,
                 bg="blue", fg="white").pack(side=tk.LEFT, padx=5)

    def setup_users_tab(self):
        # Users management section
        tk.Label(self.users_tab, text="Users Management", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Search frame
        search_frame = tk.Frame(self.users_tab)
        search_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(search_frame, text="Search Users:").pack(side=tk.LEFT, padx=5)
        self.user_search_var = tk.StringVar()
        self.user_search_var.trace('w', self.filter_users)
        tk.Entry(search_frame, textvariable=self.user_search_var, width=30).pack(side=tk.LEFT, padx=5)
        
        # Create Treeview for users
        columns = ("Username", "Created Date", "Total Appointments", "Actions")
        self.users_tree = ttk.Treeview(self.users_tab, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.users_tab, orient=tk.VERTICAL, 
                                command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.users_tab)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(buttons_frame, text="View Details", command=self.view_user_details,
                 bg="blue", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Delete User", command=self.delete_user,
                 bg="red", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Refresh", command=self.refresh_users,
                 bg="gray", fg="white").pack(side=tk.LEFT, padx=5)

    def setup_reports_tab(self):
        # Reports section
        tk.Label(self.reports_tab, text="Reports & Analytics", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Report types frame
        report_frame = tk.Frame(self.reports_tab)
        report_frame.pack(fill=tk.X, pady=10)
        
        # Report selection
        tk.Label(report_frame, text="Select Report:").pack(side=tk.LEFT, padx=5)
        self.report_var = tk.StringVar(value="Appointments Summary")
        report_menu = ttk.Combobox(report_frame, textvariable=self.report_var,
                                 values=["Appointments Summary", "User Statistics", 
                                        "Department Analytics"])
        report_menu.pack(side=tk.LEFT, padx=5)
        
        # Date range
        tk.Label(report_frame, text="Time Period:").pack(side=tk.LEFT, padx=5)
        self.report_period_var = tk.StringVar(value="This Month")
        period_menu = ttk.Combobox(report_frame, textvariable=self.report_period_var,
                                 values=["Today", "This Week", "This Month", "This Year"])
        period_menu.pack(side=tk.LEFT, padx=5)
        
        # Generate report button
        tk.Button(report_frame, text="Generate Report", command=self.generate_report,
                 bg="blue", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Report display area
        self.report_display = scrolledtext.ScrolledText(self.reports_tab, height=20, width=80)
        self.report_display.pack(pady=10, fill=tk.BOTH, expand=True)

    def filter_appointments(self, *args):
        # Clear current items
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
            
        # Get all appointments
        appointments = db.get_all_appointments()
        if not appointments:
            return
            
        search_term = self.search_var.get().lower()
        status_filter = self.status_var.get()
        date_filter = self.date_var.get()
        
        # Get date range for filter
        today = datetime.now().date()
        if date_filter == "Today":
            start_date = today
            end_date = today
        elif date_filter == "This Week":
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        elif date_filter == "This Month":
            start_date = today.replace(day=1)
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        else:
            start_date = None
            end_date = None
            
        # Filter and add appointments
        for appt in appointments:
            appt_date = datetime.strptime(appt['appointment_date'], '%Y-%m-%d').date()
            
            # Apply date filter
            if date_filter != "All" and not (start_date <= appt_date <= end_date):
                continue
                
            # Apply status filter
            if status_filter != "All" and appt['status'] != status_filter:
                continue
                
            # Apply search filter
            if search_term and search_term not in appt['patient_name'].lower():
                continue
                
            # Add to treeview
            self.appointments_tree.insert("", "end", values=(
                appt['appointment_date'],
                appt['appointment_time'],
                appt['patient_name'],
                "Dr. Smith",
                appt['status'],
                appt['username']  # Add username as the last column
            ))

    def filter_users(self, *args):
        # Clear current items
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Get search text
        search_text = self.user_search_var.get().lower()
        
        # Get users from database
        users = db.get_all_users()
        
        # Apply filter and update treeview
        for user in users:
            if search_text and search_text not in user['username'].lower():
                continue
                
            # Get appointment count for user
            appointments = db.get_user_appointments(user['username'])
            
            self.users_tree.insert("", "end", values=(
                user['username'],
                user['created_at'].strftime('%Y-%m-%d'),
                len(appointments),
                "View/Edit"
            ))

    def confirm_appointment(self):
        selected_item = self.appointments_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an appointment to confirm.")
            return
            
        values = self.appointments_tree.item(selected_item)['values']
        if values[4] == "Confirmed":
            messagebox.showinfo("Already Confirmed", "This appointment is already confirmed.")
            return
            
        if messagebox.askyesno("Confirm Appointment", 
                             f"Confirm appointment for {values[2]} on {values[0]} at {values[1]}?"):
            # Update appointment status using username
            if db.update_appointment_status(values[5], values[0], values[1], "Confirmed"):
                messagebox.showinfo("Success", "Appointment confirmed successfully!")
                self.refresh_appointments()
            else:
                messagebox.showerror("Error", "Failed to confirm appointment.")

    def cancel_appointment(self):
        selected_item = self.appointments_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an appointment to cancel.")
            return
            
        values = self.appointments_tree.item(selected_item)['values']
        if values[4] == "Cancelled":
            messagebox.showinfo("Already Cancelled", "This appointment is already cancelled.")
            return
            
        if messagebox.askyesno("Cancel Appointment", 
                             f"Cancel appointment for {values[2]} on {values[0]} at {values[1]}?"):
            # Update appointment status using username
            if db.update_appointment_status(values[5], values[0], values[1], "Cancelled"):
                messagebox.showinfo("Success", "Appointment cancelled successfully!")
                self.refresh_appointments()
            else:
                messagebox.showerror("Error", "Failed to cancel appointment.")

    def remove_test_data(self):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to remove patient appointments?"):
            if db.delete_test_appointments():
                messagebox.showinfo("Success", "Test appointments removed successfully!")
                self.refresh_appointments()
            else:
                messagebox.showerror("Error", "Failed to remove appointments.")

    def refresh_appointments(self):
        self.filter_appointments()

    def view_user_details(self):
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a user to view details.")
            return
            
        username = self.users_tree.item(selected_item)['values'][0]
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"User Details - {username}")
        details_window.geometry("600x400")
        
        # Get user details and appointments
        user_details = db.get_user_details(username)
        appointments = db.get_user_appointments(username)
        
        # Display user information
        tk.Label(details_window, text=f"User Details: {username}", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        details_frame = tk.Frame(details_window)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # User details
        tk.Label(details_frame, text=f"Created: {user_details['created_at']}").pack(anchor="w")
        tk.Label(details_frame, text=f"Total Appointments: {len(appointments)}").pack(anchor="w")
        
        # Appointments list
        tk.Label(details_frame, text="\nAppointment History:", 
                font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
        
        for appt in appointments:
            tk.Label(details_frame, 
                    text=f"{appt['appointment_date']} at {appt['appointment_time']} - {appt['status']}").pack(anchor="w")

    def delete_user(self):
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a user to delete.")
            return
            
        username = self.users_tree.item(selected_item)['values'][0]
        
        if messagebox.askyesno("Confirm Delete", 
                             f"Are you sure you want to delete user {username}?\nThis action cannot be undone."):
            if db.delete_user(username):
                messagebox.showinfo("Success", f"User {username} deleted successfully!")
                self.refresh_users()
            else:
                messagebox.showerror("Error", "Failed to delete user.")

    def refresh_users(self):
        self.filter_users()

    def generate_report(self):
        report_type = self.report_var.get()
        time_period = self.report_period_var.get()
        
        # Clear current report
        self.report_display.delete(1.0, tk.END)
        
        # Get date range
        end_date = datetime.now()
        if time_period == "Today":
            start_date = end_date
        elif time_period == "This Week":
            start_date = end_date - timedelta(days=7)
        elif time_period == "This Month":
            start_date = end_date.replace(day=1)
        else:  # This Year
            start_date = end_date.replace(month=1, day=1)
        
        # Generate report based on type
        if report_type == "Appointments Summary":
            appointments = db.get_appointments_in_range(start_date, end_date)
            
            total = len(appointments)
            confirmed = sum(1 for a in appointments if a['status'] == "Confirmed")
            cancelled = sum(1 for a in appointments if a['status'] == "Cancelled")
            pending = sum(1 for a in appointments if a['status'] == "Pending")
            
            report = f"""Appointments Summary ({time_period})
            
Total Appointments: {total}
Confirmed: {confirmed}
Cancelled: {cancelled}
Pending: {pending}

Daily Breakdown:
"""
            # Add daily breakdown
            current = start_date
            while current <= end_date:
                day_appointments = [a for a in appointments 
                                 if a['appointment_date'] == current.date()]
                report += f"{current.strftime('%Y-%m-%d')}: {len(day_appointments)} appointments\n"
                current += timedelta(days=1)
                
        elif report_type == "User Statistics":
            users = db.get_all_users()
            appointments = db.get_all_appointments()
            
            report = f"""User Statistics ({time_period})
            
Total Users: {len(users)}
Total Appointments: {len(appointments)}
Average Appointments per User: {len(appointments)/len(users):.2f}

Top Users by Appointments:
"""
            # Add user breakdown
            user_appointments = {}
            for appt in appointments:
                user_appointments[appt['username']] = user_appointments.get(appt['username'], 0) + 1
                
            sorted_users = sorted(user_appointments.items(), key=lambda x: x[1], reverse=True)
            for username, count in sorted_users[:5]:
                report += f"{username}: {count} appointments\n"
                
        else:  # Department Analytics
            appointments = db.get_appointments_in_range(start_date, end_date)
            
            report = f"""Department Analytics ({time_period})
            
Appointments by Department:
"""
            # Add department breakdown
            dept_counts = {}
            for appt in appointments:
                dept = "General"  # You might want to add department field to appointments
                dept_counts[dept] = dept_counts.get(dept, 0) + 1
                
            for dept, count in dept_counts.items():
                report += f"{dept}: {count} appointments\n"
        
        # Display report
        self.report_display.insert(tk.END, report)

def main():
    root = tk.Tk()
    admin_panel = AdminPanel(root)
    root.mainloop()

if __name__ == "__main__":
    main()