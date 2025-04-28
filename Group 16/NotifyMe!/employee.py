# # # # # employee.py
# # # # import tkinter as tk
# # # # from tkinter import messagebox
# # # # import webbrowser
# # # # from db import fetch_employees, insert_employee, delete_employee, update_employee, fetch_companies
# # # #
# # # # class EmployeeApp:
# # # #     def __init__(self, root):
# # # #         self.root = root
# # # #         self.root.title("Employee Management")
# # # #         self.root.configure(bg="#2c3e50")
# # # #
# # # #         # Frame for the employee list (with Scrollbar)
# # # #         self.employee_frame = tk.Frame(self.root, bg="#ecf0f1")
# # # #         self.employee_frame.pack(pady=10, fill="both", expand=True)
# # # #
# # # #         # Create a Canvas for Scrollable List
# # # #         self.canvas = tk.Canvas(self.employee_frame, bg="#ecf0f1")
# # # #         self.scroll_y = tk.Scrollbar(self.employee_frame, orient="vertical", command=self.canvas.yview)
# # # #         self.scroll_y.pack(side="right", fill="y")
# # # #
# # # #         self.inner_frame = tk.Frame(self.canvas, bg="#ecf0f1")
# # # #         self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
# # # #
# # # #         self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
# # # #         self.canvas.configure(yscrollcommand=self.scroll_y.set)
# # # #         self.canvas.pack(side="left", fill="both", expand=True)
# # # #
# # # #         # Button Frame
# # # #         self.button_frame = tk.Frame(self.root, bg="#2c3e50")
# # # #         self.button_frame.pack(pady=10, fill="x")
# # # #
# # # #         self.add_button = tk.Button(self.button_frame, text="Add New Employee", command=self.show_form,
# # # #                                     bg="#3498db", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
# # # #         self.add_button.pack(side="left", padx=10)
# # # #
# # # #         self.update_button = tk.Button(self.button_frame, text="Update", command=self.handle_update,
# # # #                                        bg="#f1c40f", fg="black", font=("Arial", 12, "bold"), padx=10, pady=5)
# # # #         self.update_button.pack(side="left", padx=10)
# # # #
# # # #         self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.handle_delete,
# # # #                                        bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
# # # #         self.delete_button.pack(side="left", padx=10)
# # # #
# # # #         self.linkedin_button = tk.Button(self.button_frame, text="LinkedIn", command=self.open_linkedin,
# # # #                                          bg="#0077b5", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
# # # #         self.linkedin_button.pack(side="left", padx=10)
# # # #
# # # #         self.back_button = tk.Button(self.button_frame, text="Back", command=self.root.destroy,
# # # #                                      bg="#f39c12", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
# # # #         self.back_button.pack(side="right", padx=10)
# # # #
# # # #         self.selected_employee = None
# # # #         self.employee_frames = {}
# # # #
# # # #         self.display_employees()
# # # #
# # # #     def display_employees(self):
# # # #         """Displays employee records with 3 frames per row."""
# # # #         for widget in self.inner_frame.winfo_children():
# # # #             widget.destroy()
# # # #         self.employee_frames.clear()
# # # #         self.selected_employee = None
# # # #
# # # #         employees = fetch_employees()
# # # #         num_employees = len(employees)
# # # #         num_rows = (num_employees + 2) // 3  # Ceiling division to determine rows
# # # #
# # # #         CARD_WIDTH = 380
# # # #         CARD_HEIGHT = 380
# # # #
# # # #         for row in range(num_rows):
# # # #             row_frame = tk.Frame(self.inner_frame, bg="#ecf0f1")
# # # #             row_frame.pack(pady=10, fill="x")
# # # #
# # # #             for col in range(3):
# # # #                 employee_idx = row * 3 + col
# # # #                 if employee_idx >= num_employees:
# # # #                     tk.Frame(row_frame, width=CARD_WIDTH, height=CARD_HEIGHT, bg="#ecf0f1").pack(side="left", padx=5)
# # # #                     continue
# # # #
# # # #                 employee = employees[employee_idx]
# # # #                 frame = tk.Frame(row_frame, relief="solid", bd=2, bg="#ffffff",
# # # #                                width=CARD_WIDTH, height=CARD_HEIGHT)
# # # #                 frame.pack(side="left", padx=5)
# # # #                 frame.pack_propagate(False)
# # # #
# # # #                 label_text = (
# # # #                     f"ID: {employee.get('id', 'N/A')}\n"
# # # #                     f"Name: {employee.get('name', 'N/A')}\n"
# # # #                     f"Department: {employee.get('department', 'N/A')}\n"
# # # #                     f"Phone No 1: {employee.get('phone_no1', 'N/A')}\n"
# # # #                     f"Phone No 2: {employee.get('phone_no2', 'N/A')}\n"
# # # #                     f"Designation: {employee.get('designation', 'N/A')}\n"
# # # #                     f"LinkedIn: {employee.get('linkedin_link', 'N/A')}\n"
# # # #                     f"Service: {employee.get('service_provided', 'N/A')}\n"
# # # #                     f"Company: {employee.get('company', 'N/A')}"
# # # #                 )
# # # #
# # # #                 label = tk.Label(frame, text=label_text, justify="left", anchor="nw",
# # # #                                font=("Arial", 9), bg="#ffffff", wraplength=CARD_WIDTH-20)
# # # #                 label.pack(padx=5, pady=5, fill="both", expand=True)
# # # #
# # # #                 frame.bind("<Button-1>", lambda e, emp=employee: self.select_employee(emp))
# # # #                 label.bind("<Button-1>", lambda e, emp=employee: self.select_employee(emp))
# # # #                 self.employee_frames[employee['id']] = frame
# # # #
# # # #         self.canvas.update_idletasks()
# # # #         self.canvas.configure(scrollregion=self.canvas.bbox("all"))
# # # #         self.scroll_y.config(bg="#3498db", troughcolor="#2980b9", activebackground="#1f618d")
# # # #
# # # #     def select_employee(self, employee):
# # # #         if self.selected_employee:
# # # #             prev_frame = self.employee_frames[self.selected_employee['id']]
# # # #             prev_frame.config(relief="solid", bd=2)
# # # #         self.selected_employee = employee
# # # #         selected_frame = self.employee_frames[employee['id']]
# # # #         selected_frame.config(relief="solid", bd=4, highlightbackground="#3498db")
# # # #
# # # #     def open_linkedin(self):
# # # #         if not self.selected_employee:
# # # #             messagebox.showwarning("Selection Error", "Please select an employee to view their LinkedIn profile!")
# # # #             return
# # # #         linkedin_url = self.selected_employee.get('linkedin_link', 'N/A')
# # # #         if linkedin_url and linkedin_url != 'N/A' and linkedin_url.strip():
# # # #             try:
# # # #                 webbrowser.open(linkedin_url)
# # # #             except Exception as e:
# # # #                 messagebox.showerror("Error", f"Failed to open LinkedIn profile: {str(e)}")
# # # #         else:
# # # #             messagebox.showwarning("No LinkedIn", "The selected employee has no LinkedIn profile link provided!")
# # # #
# # # #     def handle_update(self):
# # # #         if not self.selected_employee:
# # # #             messagebox.showwarning("Selection Error", "Please select an employee to update!")
# # # #             return
# # # #         self.open_edit_form(self.selected_employee)
# # # #
# # # #     def handle_delete(self):
# # # #         if not self.selected_employee:
# # # #             messagebox.showwarning("Selection Error", "Please select an employee to delete!")
# # # #             return
# # # #         self.delete_employee(self.selected_employee['id'])
# # # #
# # # #     def delete_employee(self, id):
# # # #         if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
# # # #             if delete_employee(id):
# # # #                 messagebox.showinfo("Success", "Employee deleted successfully!")
# # # #                 self.display_employees()
# # # #             else:
# # # #                 messagebox.showerror("Error", "Failed to delete employee.")
# # # #
# # # #     def show_form(self):
# # # #         self.create_form(None, "Add Employee", self.submit_add)
# # # #
# # # #     def open_edit_form(self, employee):
# # # #         self.create_form(employee, "Edit Employee", lambda data: self.submit_edit(data, self.selected_employee['id']))
# # # #
# # # #     def create_form(self, employee, title, submit_action):
# # # #         form_window = tk.Toplevel(self.root)
# # # #         form_window.title(title)
# # # #         form_window.geometry("400x500")
# # # #         form_window.configure(bg="#ffffff")
# # # #
# # # #         tk.Label(form_window, text=title, font=("Arial", 12, "bold"), bg="#ffffff", fg="#2980b9").pack(pady=10)
# # # #
# # # #         fields = ["id", "name", "department", "phone_no1", "phone_no2", "designation", "linkedin_link",
# # # #                   "service_provided", "company"]
# # # #         values = employee or {}
# # # #         entries = {}
# # # #
# # # #         for field in fields:
# # # #             tk.Label(form_window, text=field, bg="#ffffff", fg="#2980b9").pack()
# # # #             entry = tk.Entry(form_window)
# # # #             entry.insert(0, values.get(field.lower().replace(" ", ""), ""))
# # # #             entry.pack(pady=5, ipadx=5, ipady=2, fill="x")
# # # #             entries[field] = entry
# # # #
# # # #         button_frame = tk.Frame(form_window, bg="#ffffff")
# # # #         button_frame.pack(pady=10)
# # # #
# # # #         # Single submit/update button that closes the window on success
# # # #         def on_submit():
# # # #             data = {field: entries[field].get() for field in fields}
# # # #             if submit_action(data):
# # # #                 form_window.destroy()
# # # #
# # # #         tk.Button(button_frame, text="Submit" if title == "Add Employee" else "Update",
# # # #                   command=on_submit, bg="#27ae60", fg="white", padx=10, pady=5).pack(side="left", padx=5)
# # # #         tk.Button(button_frame, text="Cancel", command=form_window.destroy,
# # # #                   bg="#e74c3c", fg="white", padx=10, pady=5).pack(side="left", padx=5)
# # # #
# # # #     def submit_add(self, data):
# # # #         companies = fetch_companies()
# # # #         company_names = [company['company_name'] for company in companies]
# # # #
# # # #         if data["company"] not in company_names:
# # # #             messagebox.showwarning("Validation Error",
# # # #                                  "The company name does not exist. Please create the company first!")
# # # #             return False
# # # #
# # # #         if not all([data["id"], data["name"], data["department"], data["phone_no1"], data["company"]]):
# # # #             messagebox.showwarning("Validation Error", "Required fields are missing!")
# # # #             return False
# # # #
# # # #         if insert_employee(**data):
# # # #             messagebox.showinfo("Success", "Employee added successfully!")
# # # #             self.display_employees()
# # # #             return True
# # # #         else:
# # # #             messagebox.showerror("Error", "Failed to add employee.")
# # # #             return False
# # # #
# # # #     def submit_edit(self, data, employee_id):
# # # #         companies = fetch_companies()
# # # #         company_names = [company['company_name'] for company in companies]
# # # #
# # # #         if data["company"] not in company_names:
# # # #             messagebox.showwarning("Validation Error",
# # # #                                  "The company name does not exist. Please create the company first!")
# # # #             return False
# # # #
# # # #         if not all([data["id"], data["name"], data["department"], data["phone_no1"], data["company"]]):
# # # #             messagebox.showwarning("Validation Error", "Required fields are missing!")
# # # #             return False
# # # #
# # # #         # Update the database
# # # #         success = update_employee(
# # # #             id=data["id"],
# # # #             name=data["name"],
# # # #             department=data["department"],
# # # #             phone_no1=data["phone_no1"],
# # # #             phone_no2=data["phone_no2"],
# # # #             designation=data["designation"],
# # # #             linkedin_link=data["linkedin_link"],
# # # #             service_provided=data["service_provided"],
# # # #             company=data["company"]
# # # #         )
# # # #
# # # #         if success:
# # # #             messagebox.showinfo("Success", "Employee updated successfully!")
# # # #             self.selected_employee.update(data)
# # # #             self.display_employees()
# # # #             return True
# # # #         else:
# # # #             messagebox.showerror("Error", "Failed to update employee.")
# # # #             return False
# # # #
# # # # def employee(master=None):
# # # #     if master is None:
# # # #         root = tk.Tk()
# # # #         root.state("zoomed")
# # # #         app = EmployeeApp(root)
# # # #         root.mainloop()
# # # #     else:
# # # #         app = EmployeeApp(master)
# # # #
# # # # if __name__ == "__main__":
# # # #     employee()
# # #
# # # import tkinter as tk
# # # from tkinter import messagebox
# # # import webbrowser
# # # from db import fetch_employees, insert_employee, delete_employee, update_employee, fetch_companies
# # #
# # # class EmployeeApp:
# # #     def __init__(self, root, prev_window=None):
# # #         if prev_window:
# # #             prev_window.destroy()  # Close previous window (dashboard)
# # #         self.root = tk.Toplevel(root)
# # #         self.root.title("Employee Management")
# # #         self.root.configure(bg="#2c3e50")
# # #         self.root.state("zoomed")
# # #         self.selected_employee = None
# # #         self.employee_frames = {}  # Initialize here before display_employees
# # #         self.setup_ui()
# # #         self.display_employees()
# # #
# # #     def setup_ui(self):
# # #         self.employee_frame = tk.Frame(self.root, bg="#ecf0f1")
# # #         self.employee_frame.pack(pady=10, fill="both", expand=True)
# # #
# # #         self.canvas = tk.Canvas(self.employee_frame, bg="#ecf0f1")
# # #         self.scroll_y = tk.Scrollbar(self.employee_frame, orient="vertical", command=self.canvas.yview)
# # #         self.scroll_y.pack(side="right", fill="y")
# # #
# # #         self.inner_frame = tk.Frame(self.canvas, bg="#ecf0f1")
# # #         self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
# # #
# # #         self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
# # #         self.canvas.configure(yscrollcommand=self.scroll_y.set)
# # #         self.canvas.pack(side="left", fill="both", expand=True)
# # #
# # #         self.button_frame = tk.Frame(self.root, bg="#2c3e50")
# # #         self.button_frame.pack(pady=10, fill="x")
# # #
# # #         self.add_button = tk.Button(self.button_frame, text="Add New Employee", command=self.show_form,
# # #                                     bg="#3498db", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
# # #         self.add_button.pack(side="left", padx=10)
# # #
# # #         self.update_button = tk.Button(self.button_frame, text="Update", command=self.handle_update,
# # #                                        bg="#f1c40f", fg="black", font=("Arial", 12, "bold"), padx=10, pady=5)
# # #         self.update_button.pack(side="left", padx=10)
# # #
# # #         self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.handle_delete,
# # #                                        bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
# # #         self.delete_button.pack(side="left", padx=10)
# # #
# # #         self.linkedin_button = tk.Button(self.button_frame, text="LinkedIn", command=self.open_linkedin,
# # #                                          bg="#0077b5", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
# # #         self.linkedin_button.pack(side="left", padx=10)
# # #
# # #         self.lusha_button = tk.Button(self.button_frame, text="Lusha", command=self.open_lusha,
# # #                                       bg="#00c4cc", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
# # #         self.lusha_button.pack(side="left", padx=10)
# # #
# # #         self.salesql_button = tk.Button(self.button_frame, text="SalesQL", command=self.open_salesql,
# # #                                         bg="#ff5733", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
# # #         self.salesql_button.pack(side="left", padx=10)
# # #
# # #         self.back_button = tk.Button(self.button_frame, text="Back", command=lambda: self.back_to_dashboard(),
# # #                                      bg="#f39c12", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
# # #         self.back_button.pack(side="right", padx=10)
# # #
# # #     def back_to_dashboard(self):
# # #         from dashboard import open_dashboard  # Moved import here
# # #         self.root.destroy()
# # #         open_dashboard(root=self.root.master, prev_window=self.root)
# # #
# # #     def display_employees(self):
# # #         for widget in self.inner_frame.winfo_children():
# # #             widget.destroy()
# # #         self.employee_frames.clear()
# # #         self.selected_employee = None
# # #         employees = fetch_employees()
# # #         num_employees = len(employees)
# # #         num_rows = (num_employees + 2) // 3  # 3 cards per row
# # #         CARD_WIDTH = 380
# # #         CARD_HEIGHT = 380
# # #         for row in range(num_rows):
# # #             row_frame = tk.Frame(self.inner_frame, bg="#ecf0f1")
# # #             row_frame.pack(pady=10, fill="x")
# # #             for col in range(3):
# # #                 employee_idx = row * 3 + col
# # #                 if employee_idx >= num_employees:
# # #                     tk.Frame(row_frame, width=CARD_WIDTH, height=CARD_HEIGHT, bg="#ecf0f1").pack(side="left", padx=5)
# # #                     continue
# # #                 employee = employees[employee_idx]
# # #                 frame = tk.Frame(row_frame, relief="solid", bd=2, bg="#ffffff",
# # #                                  width=CARD_WIDTH, height=CARD_HEIGHT)
# # #                 frame.pack(side="left", padx=5)
# # #                 frame.pack_propagate(False)
# # #                 label_text = (
# # #                     f"ID: {employee.get('id', 'N/A')}\n"
# # #                     f"Name: {employee.get('name', 'N/A')}\n"
# # #                     f"Department: {employee.get('department', 'N/A')}\n"
# # #                     f"Phone No 1: {employee.get('phone_no1', 'N/A')}\n"
# # #                     f"Phone No 2: {employee.get('phone_no2', 'N/A')}\n"
# # #                     f"Designation: {employee.get('designation', 'N/A')}\n"
# # #                     f"LinkedIn: {employee.get('linkedin_link', 'N/A')}\n"
# # #                     f"Service: {employee.get('service_provided', 'N/A')}\n"
# # #                     f"Company: {employee.get('company', 'N/A')}"
# # #                 )
# # #                 label = tk.Label(frame, text=label_text, justify="left", anchor="nw",
# # #                                  font=("Arial", 9), bg="#ffffff", wraplength=CARD_WIDTH-20)
# # #                 label.pack(padx=5, pady=5, fill="both", expand=True)
# # #                 frame.bind("<Button-1>", lambda e, emp=employee: self.select_employee(emp))
# # #                 label.bind("<Button-1>", lambda e, emp=employee: self.select_employee(emp))
# # #                 self.employee_frames[employee['id']] = frame
# # #         self.canvas.update_idletasks()
# # #         self.canvas.configure(scrollregion=self.canvas.bbox("all"))
# # #         self.scroll_y.config(bg="#3498db", troughcolor="#2980b9", activebackground="#1f618d")
# # #
# # #     def select_employee(self, employee):
# # #         if self.selected_employee:
# # #             prev_frame = self.employee_frames[self.selected_employee['id']]
# # #             prev_frame.config(relief="solid", bd=2)
# # #         self.selected_employee = employee
# # #         selected_frame = self.employee_frames[employee['id']]
# # #         selected_frame.config(relief="solid", bd=4, highlightbackground="#3498db")
# # #
# # #     def open_linkedin(self):
# # #         if not self.selected_employee:
# # #             messagebox.showwarning("Selection Error", "Please select an employee to view their LinkedIn profile!")
# # #             return
# # #         linkedin_url = self.selected_employee.get('linkedin_link', 'N/A')
# # #         if linkedin_url and linkedin_url != 'N/A' and linkedin_url.strip():
# # #             try:
# # #                 webbrowser.open(linkedin_url)
# # #             except Exception as e:
# # #                 messagebox.showerror("Error", f"Failed to open LinkedIn profile: {str(e)}")
# # #         else:
# # #             messagebox.showwarning("No LinkedIn", "The selected employee has no LinkedIn profile link provided!")
# # #
# # #     def open_lusha(self):
# # #         try:
# # #             webbrowser.open("https://www.lusha.com")
# # #         except Exception as e:
# # #             messagebox.showerror("Error", f"Failed to open Lusha: {str(e)}")
# # #
# # #     def open_salesql(self):
# # #         try:
# # #             webbrowser.open("https://www.salesql.com")
# # #         except Exception as e:
# # #             messagebox.showerror("Error", f"Failed to open SalesQL: {str(e)}")
# # #
# # #     def handle_update(self):
# # #         if not self.selected_employee:
# # #             messagebox.showwarning("Selection Error", "Please select an employee to update!")
# # #             return
# # #         self.open_edit_form(self.selected_employee)
# # #
# # #     def handle_delete(self):
# # #         if not self.selected_employee:
# # #             messagebox.showwarning("Selection Error", "Please select an employee to delete!")
# # #             return
# # #         self.delete_employee(self.selected_employee['id'])
# # #
# # #     def delete_employee(self, id):
# # #         if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
# # #             if delete_employee(id):
# # #                 messagebox.showinfo("Success", "Employee deleted successfully!")
# # #                 self.display_employees()
# # #             else:
# # #                 messagebox.showerror("Error", "Failed to delete employee.")
# # #
# # #     def show_form(self):
# # #         self.create_form(None, "Add Employee", self.submit_add)
# # #
# # #     def open_edit_form(self, employee):
# # #         self.create_form(employee, "Edit Employee", lambda data: self.submit_edit(data, self.selected_employee['id']))
# # #
# # #     def create_form(self, employee, title, submit_action):
# # #         form_window = tk.Toplevel(self.root)
# # #         form_window.title(title)
# # #         form_window.geometry("400x500")
# # #         form_window.configure(bg="#ffffff")
# # #         tk.Label(form_window, text=title, font=("Arial", 12, "bold"), bg="#ffffff", fg="#2980b9").pack(pady=10)
# # #         fields = ["id", "name", "department", "phone_no1", "phone_no2", "designation", "linkedin_link",
# # #                   "service_provided", "company"]
# # #         values = employee or {}
# # #         entries = {}
# # #         for field in fields:
# # #             tk.Label(form_window, text=field, bg="#ffffff", fg="#2980b9").pack()
# # #             entry = tk.Entry(form_window)
# # #             entry.insert(0, values.get(field.lower().replace(" ", ""), ""))
# # #             entry.pack(pady=5, ipadx=5, ipady=2, fill="x")
# # #             entries[field] = entry
# # #         button_frame = tk.Frame(form_window, bg="#ffffff")
# # #         button_frame.pack(pady=10)
# # #
# # #         def on_submit():
# # #             data = {field: entries[field].get() for field in fields}
# # #             if submit_action(data):
# # #                 form_window.destroy()
# # #
# # #         tk.Button(button_frame, text="Submit" if title == "Add Employee" else "Update",
# # #                   command=on_submit, bg="#27ae60", fg="white", padx=10, pady=5).pack(side="left", padx=5)
# # #         tk.Button(button_frame, text="Cancel", command=form_window.destroy,
# # #                   bg="#e74c3c", fg="white", padx=10, pady=5).pack(side="left", padx=5)
# # #
# # #     def submit_add(self, data):
# # #         companies = fetch_companies()
# # #         company_names = [company['company_name'] for company in companies]
# # #         if data["company"] not in company_names:
# # #             messagebox.showwarning("Validation Error",
# # #                                  "The company name does not exist. Please create the company first!")
# # #             return False
# # #         if not all([data["id"], data["name"], data["department"], data["phone_no1"], data["company"]]):
# # #             messagebox.showwarning("Validation Error", "Required fields are missing!")
# # #             return False
# # #         if insert_employee(**data):
# # #             messagebox.showinfo("Success", "Employee added successfully!")
# # #             self.display_employees()
# # #             return True
# # #         else:
# # #             messagebox.showerror("Error", "Failed to add employee.")
# # #             return False
# # #
# # #     def submit_edit(self, data, employee_id):
# # #         companies = fetch_companies()
# # #         company_names = [company['company_name'] for company in companies]
# # #         if data["company"] not in company_names:
# # #             messagebox.showwarning("Validation Error",
# # #                                  "The company name does not exist. Please create the company first!")
# # #             return False
# # #         if not all([data["id"], data["name"], data["department"], data["phone_no1"], data["company"]]):
# # #             messagebox.showwarning("Validation Error", "Required fields are missing!")
# # #             return False
# # #         success = update_employee(
# # #             id=data["id"],
# # #             name=data["name"],
# # #             department=data["department"],
# # #             phone_no1=data["phone_no1"],
# # #             phone_no2=data["phone_no2"],
# # #             designation=data["designation"],
# # #             linkedin_link=data["linkedin_link"],
# # #             service_provided=data["service_provided"],
# # #             company=data["company"]
# # #         )
# # #         if success:
# # #             messagebox.showinfo("Success", "Employee updated successfully!")
# # #             self.selected_employee.update(data)
# # #             self.display_employees()
# # #             return True
# # #         else:
# # #             messagebox.showerror("Error", "Failed to update employee.")
# # #             return False
# # #
# # # def employee(root=None, prev_window=None):
# # #     app = EmployeeApp(root, prev_window)
# # #
# # # if __name__ == "__main__":
# # #     root = tk.Tk()
# # #     employee(root)
# # #     root.mainloop()
# #
# # import tkinter as tk
# # from tkinter import messagebox
# # import webbrowser
# # from db import fetch_employees, insert_employee, delete_employee, update_employee, fetch_companies
# #
# # class EmployeeApp:
# #     def __init__(self, root, prev_window=None):
# #         if prev_window:
# #             prev_window.destroy()
# #         self.root = tk.Toplevel(root)
# #         self.root.title("Employee Management")
# #         self.root.configure(bg="#1E1E2F")
# #         self.root.state("zoomed")
# #         self.selected_employee = None
# #         self.employee_frames = {}
# #         self.setup_ui()
# #         self.display_employees()
# #
# #     def setup_ui(self):
# #         self.employee_frame = tk.Frame(self.root, bg="#2D2D44")
# #         self.employee_frame.pack(pady=10, fill="both", expand=True)
# #
# #         self.canvas = tk.Canvas(self.employee_frame, bg="#2D2D44")
# #         self.scroll_y = tk.Scrollbar(self.employee_frame, orient="vertical", command=self.canvas.yview, bg="#00D4FF", troughcolor="#2D2D44")
# #         self.scroll_y.pack(side="right", fill="y")
# #
# #         self.inner_frame = tk.Frame(self.canvas, bg="#2D2D44")
# #         self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
# #
# #         self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
# #         self.canvas.configure(yscrollcommand=self.scroll_y.set)
# #         self.canvas.pack(side="left", fill="both", expand=True)
# #
# #         self.button_frame = tk.Frame(self.root, bg="#1E1E2F")
# #         self.button_frame.pack(pady=10, fill="x")
# #
# #         self.add_button = tk.Button(self.button_frame, text="Add New Employee", command=self.show_form,
# #                                     bg="#00D4FF", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
# #         self.add_button.pack(side="left", padx=10)
# #
# #         self.update_button = tk.Button(self.button_frame, text="Update", command=self.handle_update,
# #                                        bg="#00D4FF", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
# #         self.update_button.pack(side="left", padx=10)
# #
# #         self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.handle_delete,
# #                                        bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
# #         self.delete_button.pack(side="left", padx=10)
# #
# #         self.linkedin_button = tk.Button(self.button_frame, text="LinkedIn", command=self.open_linkedin,
# #                                          bg="#0077B5", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
# #         self.linkedin_button.pack(side="left", padx=10)
# #
# #         self.lusha_button = tk.Button(self.button_frame, text="Lusha", command=self.open_lusha,
# #                                       bg="#00C4CC", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
# #         self.lusha_button.pack(side="left", padx=10)
# #
# #         self.salesql_button = tk.Button(self.button_frame, text="SalesQL", command=self.open_salesql,
# #                                         bg="#FF5733", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
# #         self.salesql_button.pack(side="left", padx=10)
# #
# #         self.back_button = tk.Button(self.button_frame, text="Back", command=lambda: self.back_to_dashboard(),
# #                                      bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
# #         self.back_button.pack(side="right", padx=10)
# #
# #     def back_to_dashboard(self):
# #         from dashboard import open_dashboard
# #         self.root.destroy()
# #         open_dashboard(root=self.root.master, prev_window=self.root)
# #
# #     def display_employees(self):
# #         for widget in self.inner_frame.winfo_children():
# #             widget.destroy()
# #         self.employee_frames.clear()
# #         self.selected_employee = None
# #         employees = fetch_employees()
# #         num_employees = len(employees)
# #         num_rows = (num_employees + 2) // 3
# #         CARD_WIDTH = 380
# #         CARD_HEIGHT = 380
# #         for row in range(num_rows):
# #             row_frame = tk.Frame(self.inner_frame, bg="#2D2D44")
# #             row_frame.pack(pady=10, fill="x")
# #             for col in range(3):
# #                 employee_idx = row * 3 + col
# #                 if employee_idx >= num_employees:
# #                     tk.Frame(row_frame, width=CARD_WIDTH, height=CARD_HEIGHT, bg="#2D2D44").pack(side="left", padx=5)
# #                     continue
# #                 employee = employees[employee_idx]
# #                 frame = tk.Frame(row_frame, relief="solid", bd=2, bg="#25253A",
# #                                  width=CARD_WIDTH, height=CARD_HEIGHT)
# #                 frame.pack(side="left", padx=5)
# #                 frame.pack_propagate(False)
# #                 label_text = (
# #                     f"ID: {employee.get('id', 'N/A')}\n"
# #                     f"Name: {employee.get('name', 'N/A')}\n"
# #                     f"Department: {employee.get('department', 'N/A')}\n"
# #                     f"Phone No 1: {employee.get('phone_no1', 'N/A')}\n"
# #                     f"Phone No 2: {employee.get('phone_no2', 'N/A')}\n"
# #                     f"Designation: {employee.get('designation', 'N/A')}\n"
# #                     f"LinkedIn: {employee.get('linkedin_link', 'N/A')}\n"
# #                     f"Service: {employee.get('service_provided', 'N/A')}\n"
# #                     f"Company: {employee.get('company', 'N/A')}"
# #                 )
# #                 label = tk.Label(frame, text=label_text, justify="left", anchor="nw",
# #                                  font=("Roboto", 9), bg="#25253A", fg="#E0E0E0", wraplength=CARD_WIDTH-20)
# #                 label.pack(padx=5, pady=5, fill="both", expand=True)
# #                 frame.bind("<Button-1>", lambda e, emp=employee: self.select_employee(emp))
# #                 label.bind("<Button-1>", lambda e, emp=employee: self.select_employee(emp))
# #                 self.employee_frames[employee['id']] = frame
# #         self.canvas.update_idletasks()
# #         self.canvas.configure(scrollregion=self.canvas.bbox("all"))
# #
# #     def select_employee(self, employee):
# #         if self.selected_employee:
# #             prev_frame = self.employee_frames[self.selected_employee['id']]
# #             prev_frame.config(relief="solid", bd=2)
# #         self.selected_employee = employee
# #         selected_frame = self.employee_frames[employee['id']]
# #         selected_frame.config(relief="solid", bd=4, highlightbackground="#00D4FF")
# #
# #     def open_linkedin(self):
# #         if not self.selected_employee:
# #             messagebox.showwarning("Selection Error", "Please select an employee to view their LinkedIn profile!")
# #             return
# #         linkedin_url = self.selected_employee.get('linkedin_link', 'N/A')
# #         if linkedin_url and linkedin_url != 'N/A' and linkedin_url.strip():
# #             try:
# #                 webbrowser.open(linkedin_url)
# #             except Exception as e:
# #                 messagebox.showerror("Error", f"Failed to open LinkedIn profile: {str(e)}")
# #         else:
# #             messagebox.showwarning("No LinkedIn", "The selected employee has no LinkedIn profile link provided!")
# #
# #     def open_lusha(self):
# #         try:
# #             webbrowser.open("https://www.lusha.com")
# #         except Exception as e:
# #             messagebox.showerror("Error", f"Failed to open Lusha: {str(e)}")
# #
# #     def open_salesql(self):
# #         try:
# #             webbrowser.open("https://www.salesql.com")
# #         except Exception as e:
# #             messagebox.showerror("Error", f"Failed to open SalesQL: {str(e)}")
# #
# #     def handle_update(self):
# #         if not self.selected_employee:
# #             messagebox.showwarning("Selection Error", "Please select an employee to update!")
# #             return
# #         self.open_edit_form(self.selected_employee)
# #
# #     def handle_delete(self):
# #         if not self.selected_employee:
# #             messagebox.showwarning("Selection Error", "Please select an employee to delete!")
# #             return
# #         self.delete_employee(self.selected_employee['id'])
# #
# #     def delete_employee(self, id):
# #         if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
# #             if delete_employee(id):
# #                 messagebox.showinfo("Success", "Employee deleted successfully!")
# #                 self.display_employees()
# #             else:
# #                 messagebox.showerror("Error", "Failed to delete employee.")
# #
# #     def show_form(self):
# #         self.create_form(None, "Add Employee", self.submit_add)
# #
# #     def open_edit_form(self, employee):
# #         self.create_form(employee, "Edit Employee", lambda data: self.submit_edit(data, self.selected_employee['id']))
# #
# #     def create_form(self, employee, title, submit_action):
# #         form_window = tk.Toplevel(self.root)
# #         form_window.title(title)
# #         form_window.geometry("400x500")
# #         form_window.configure(bg="#1E1E2F")
# #         tk.Label(form_window, text=title, font=("Roboto", 12, "bold"), bg="#1E1E2F", fg="#00D4FF").pack(pady=10)
# #         fields = ["id", "name", "department", "phone_no1", "phone_no2", "designation", "linkedin_link",
# #                   "service_provided", "company"]
# #         values = employee or {}
# #         entries = {}
# #         for field in fields:
# #             tk.Label(form_window, text=field, bg="#1E1E2F", fg="#E0E0E0").pack()
# #             entry = tk.Entry(form_window, bg="#2D2D44", fg="#E0E0E0", insertbackground="#00D4FF")
# #             entry.insert(0, values.get(field.lower().replace(" ", ""), ""))
# #             entry.pack(pady=5, ipadx=5, ipady=2, fill="x")
# #             entries[field] = entry
# #         button_frame = tk.Frame(form_window, bg="#1E1E2F")
# #         button_frame.pack(pady=10)
# #
# #         def on_submit():
# #             data = {field: entries[field].get() for field in fields}
# #             if submit_action(data):
# #                 form_window.destroy()
# #
# #         tk.Button(button_frame, text="Submit" if title == "Add Employee" else "Update",
# #                   command=on_submit, bg="#39FF14", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(side="left", padx=5)
# #         tk.Button(button_frame, text="Cancel", command=form_window.destroy,
# #                   bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(side="left", padx=5)
# #
# #     def submit_add(self, data):
# #         companies = fetch_companies()
# #         company_names = [company['company_name'] for company in companies]
# #         if data["company"] not in company_names:
# #             messagebox.showwarning("Validation Error",
# #                                  "The company name does not exist. Please create the company first!")
# #             return False
# #         if not all([data["id"], data["name"], data["department"], data["phone_no1"], data["company"]]):
# #             messagebox.showwarning("Validation Error", "Required fields are missing!")
# #             return False
# #         if insert_employee(**data):
# #             messagebox.showinfo("Success", "Employee added successfully!")
# #             self.display_employees()
# #             return True
# #         else:
# #             messagebox.showerror("Error", "Failed to add employee.")
# #             return False
# #
# #     def submit_edit(self, data, employee_id):
# #         companies = fetch_companies()
# #         company_names = [company['company_name'] for company in companies]
# #         if data["company"] not in company_names:
# #             messagebox.showwarning("Validation Error",
# #                                  "The company name does not exist. Please create the company first!")
# #             return False
# #         if not all([data["id"], data["name"], data["department"], data["phone_no1"], data["company"]]):
# #             messagebox.showwarning("Validation Error", "Required fields are missing!")
# #             return False
# #         success = update_employee(
# #             id=data["id"],
# #             name=data["name"],
# #             department=data["department"],
# #             phone_no1=data["phone_no1"],
# #             phone_no2=data["phone_no2"],
# #             designation=data["designation"],
# #             linkedin_link=data["linkedin_link"],
# #             service_provided=data["service_provided"],
# #             company=data["company"]
# #         )
# #         if success:
# #             messagebox.showinfo("Success", "Employee updated successfully!")
# #             self.selected_employee.update(data)
# #             self.display_employees()
# #             return True
# #         else:
# #             messagebox.showerror("Error", "Failed to update employee.")
# #             return False
# #
# # def employee(root=None, prev_window=None):
# #     app = EmployeeApp(root, prev_window)
# #
# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     employee(root)
# #     root.mainloop()
#
#
# import tkinter as tk
# from tkinter import messagebox
# import webbrowser
# from db import fetch_employees, insert_employee, delete_employee, update_employee, fetch_companies
#
# class EmployeeApp:
#     def __init__(self, root, prev_window=None):
#         if prev_window:
#             prev_window.destroy()
#         self.root = tk.Toplevel(root)
#         self.root.title("Employee Management")
#         self.root.configure(bg="#2B2B2B")
#         self.root.state("zoomed")
#         self.selected_employee = None
#         self.employee_frames = {}
#         self.setup_ui()
#         self.display_employees()
#
#     def setup_ui(self):
#         self.employee_frame = tk.Frame(self.root, bg="#3A3A3A")
#         self.employee_frame.pack(pady=10, fill="both", expand=True)
#
#         self.canvas = tk.Canvas(self.employee_frame, bg="#3A3A3A")
#         self.scroll_y = tk.Scrollbar(self.employee_frame, orient="vertical", command=self.canvas.yview, bg="#4A90E2", troughcolor="#3A3A3A")
#         self.scroll_y.pack(side="right", fill="y")
#
#         self.inner_frame = tk.Frame(self.canvas, bg="#3A3A3A")
#         self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
#
#         self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
#         self.canvas.configure(yscrollcommand=self.scroll_y.set)
#         self.canvas.pack(side="left", fill="both", expand=True)
#
#         self.button_frame = tk.Frame(self.root, bg="#2B2B2B")
#         self.button_frame.pack(pady=10, fill="x")
#
#         self.add_button = tk.Button(self.button_frame, text="Add New Employee", command=self.show_form,
#                                     bg="#4A90E2", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.add_button.pack(side="left", padx=10)
#
#         self.update_button = tk.Button(self.button_frame, text="Update", command=self.handle_update,
#                                        bg="#4A90E2", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.update_button.pack(side="left", padx=10)
#
#         self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.handle_delete,
#                                        bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.delete_button.pack(side="left", padx=10)
#
#         self.linkedin_button = tk.Button(self.button_frame, text="LinkedIn", command=self.open_linkedin,
#                                          bg="#0077B5", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.linkedin_button.pack(side="left", padx=10)
#
#         self.lusha_button = tk.Button(self.button_frame, text="Lusha", command=self.open_lusha,
#                                       bg="#00C4CC", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.lusha_button.pack(side="left", padx=10)
#
#         self.salesql_button = tk.Button(self.button_frame, text="SalesQL", command=self.open_salesql,
#                                         bg="#FF5733", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.salesql_button.pack(side="left", padx=10)
#
#         self.back_button = tk.Button(self.button_frame, text="Back", command=lambda: self.back_to_dashboard(),
#                                      bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.back_button.pack(side="right", padx=10)
#
#     def back_to_dashboard(self):
#         from dashboard import open_dashboard
#         self.root.destroy()
#         open_dashboard(root=self.root.master, prev_window=self.root)
#
#     def display_employees(self):
#         for widget in self.inner_frame.winfo_children():
#             widget.destroy()
#         self.employee_frames.clear()
#         self.selected_employee = None
#         employees = fetch_employees()
#         num_employees = len(employees)
#         num_rows = (num_employees + 2) // 3
#         CARD_WIDTH = 380
#         CARD_HEIGHT = 380
#         for row in range(num_rows):
#             row_frame = tk.Frame(self.inner_frame, bg="#3A3A3A")
#             row_frame.pack(pady=10, fill="x")
#             for col in range(3):
#                 employee_idx = row * 3 + col
#                 if employee_idx >= num_employees:
#                     tk.Frame(row_frame, width=CARD_WIDTH, height=CARD_HEIGHT, bg="#3A3A3A").pack(side="left", padx=5)
#                     continue
#                 employee = employees[employee_idx]
#                 frame = tk.Frame(row_frame, relief="solid", bd=2, bg="#25253A",
#                                  width=CARD_WIDTH, height=CARD_HEIGHT)
#                 frame.pack(side="left", padx=5)
#                 frame.pack_propagate(False)
#                 label_text = (
#                     f"ID: {employee.get('id', 'N/A')}\n"
#                     f"Name: {employee.get('name', 'N/A')}\n"
#                     f"Department: {employee.get('department', 'N/A')}\n"
#                     f"Phone No 1: {employee.get('phone_no1', 'N/A')}\n"
#                     f"Phone No 2: {employee.get('phone_no2', 'N/A')}\n"
#                     f"Designation: {employee.get('designation', 'N/A')}\n"
#                     f"LinkedIn: {employee.get('linkedin_link', 'N/A')}\n"
#                     f"Service: {employee.get('service_provided', 'N/A')}\n"
#                     f"Company: {employee.get('company', 'N/A')}"
#                 )
#                 label = tk.Label(frame, text=label_text, justify="left", anchor="nw",
#                                  font=("Roboto", 9), bg="#25253A", fg="#E0E0E0", wraplength=CARD_WIDTH-20)
#                 label.pack(padx=5, pady=5, fill="both", expand=True)
#                 frame.bind("<Button-1>", lambda e, emp=employee: self.select_employee(emp))
#                 label.bind("<Button-1>", lambda e, emp=employee: self.select_employee(emp))
#                 self.employee_frames[employee['id']] = frame
#         self.canvas.update_idletasks()
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#
#     def select_employee(self, employee):
#         if self.selected_employee:
#             prev_frame = self.employee_frames[self.selected_employee['id']]
#             prev_frame.config(relief="solid", bd=2)
#         self.selected_employee = employee
#         selected_frame = self.employee_frames[employee['id']]
#         selected_frame.config(relief="solid", bd=4, highlightbackground="#4A90E2")
#
#     def open_linkedin(self):
#         if not self.selected_employee:
#             messagebox.showwarning("Selection Error", "Please select an employee to view their LinkedIn profile!")
#             return
#         linkedin_url = self.selected_employee.get('linkedin_link', 'N/A')
#         if linkedin_url and linkedin_url != 'N/A' and linkedin_url.strip():
#             try:
#                 webbrowser.open(linkedin_url)
#             except Exception as e:
#                 messagebox.showerror("Error", f"Failed to open LinkedIn profile: {str(e)}")
#         else:
#             messagebox.showwarning("No LinkedIn", "The selected employee has no LinkedIn profile link provided!")
#
#     def open_lusha(self):
#         try:
#             webbrowser.open("https://www.lusha.com")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to open Lusha: {str(e)}")
#
#     def open_salesql(self):
#         try:
#             webbrowser.open("https://www.salesql.com")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to open SalesQL: {str(e)}")
#
#     def handle_update(self):
#         if not self.selected_employee:
#             messagebox.showwarning("Selection Error", "Please select an employee to update!")
#             return
#         self.open_edit_form(self.selected_employee)
#
#     def handle_delete(self):
#         if not self.selected_employee:
#             messagebox.showwarning("Selection Error", "Please select an employee to delete!")
#             return
#         self.delete_employee(self.selected_employee['id'])
#
#     def delete_employee(self, id):
#         if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
#             if delete_employee(id):
#                 messagebox.showinfo("Success", "Employee deleted successfully!")
#                 self.display_employees()
#             else:
#                 messagebox.showerror("Error", "Failed to delete employee.")
#
#     def show_form(self):
#         self.create_form(None, "Add Employee", self.submit_add)
#
#     def open_edit_form(self, employee):
#         self.create_form(employee, "Edit Employee", lambda data: self.submit_edit(data, self.selected_employee['id']))
#
#     def create_form(self, employee, title, submit_action):
#         form_window = tk.Toplevel(self.root)
#         form_window.title(title)
#         form_window.geometry("400x500")
#         form_window.configure(bg="#2B2B2B")
#         tk.Label(form_window, text=title, font=("Roboto", 12, "bold"), bg="#2B2B2B", fg="#4A90E2").pack(pady=10)
#         fields = ["id", "name", "department", "phone_no1", "phone_no2", "designation", "linkedin_link",
#                   "service_provided", "company"]
#         values = employee or {}
#         entries = {}
#         for field in fields:
#             tk.Label(form_window, text=field, bg="#2B2B2B", fg="#E0E0E0").pack()
#             entry = tk.Entry(form_window, bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#             entry.insert(0, values.get(field.lower().replace(" ", ""), ""))
#             entry.pack(pady=5, ipadx=5, ipady=2, fill="x")
#             entries[field] = entry
#         button_frame = tk.Frame(form_window, bg="#2B2B2B")
#         button_frame.pack(pady=10)
#
#         def on_submit():
#             data = {field: entries[field].get() for field in fields}
#             if submit_action(data):
#                 form_window.destroy()
#
#         tk.Button(button_frame, text="Submit" if title == "Add Employee" else "Update",
#                   command=on_submit, bg="#50C878", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(side="left", padx=5)
#         tk.Button(button_frame, text="Cancel", command=form_window.destroy,
#                   bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(side="left", padx=5)
#
#     def submit_add(self, data):
#         companies = fetch_companies()
#         company_names = [company['company_name'] for company in companies]
#         if data["company"] not in company_names:
#             messagebox.showwarning("Validation Error",
#                                  "The company name does not exist. Please create the company first!")
#             return False
#         if not all([data["id"], data["name"], data["department"], data["phone_no1"], data["company"]]):
#             messagebox.showwarning("Validation Error", "Required fields are missing!")
#             return False
#         if insert_employee(**data):
#             messagebox.showinfo("Success", "Employee added successfully!")
#             self.display_employees()
#             return True
#         else:
#             messagebox.showerror("Error", "Failed to add employee.")
#             return False
#
#     def submit_edit(self, data, employee_id):
#         companies = fetch_companies()
#         company_names = [company['company_name'] for company in companies]
#         if data["company"] not in company_names:
#             messagebox.showwarning("Validation Error",
#                                  "The company name does not exist. Please create the company first!")
#             return False
#         if not all([data["id"], data["name"], data["department"], data["phone_no1"], data["company"]]):
#             messagebox.showwarning("Validation Error", "Required fields are missing!")
#             return False
#         success = update_employee(
#             id=data["id"],
#             name=data["name"],
#             department=data["department"],
#             phone_no1=data["phone_no1"],
#             phone_no2=data["phone_no2"],
#             designation=data["designation"],
#             linkedin_link=data["linkedin_link"],
#             service_provided=data["service_provided"],
#             company=data["company"]
#         )
#         if success:
#             messagebox.showinfo("Success", "Employee updated successfully!")
#             self.selected_employee.update(data)
#             self.display_employees()
#             return True
#         else:
#             messagebox.showerror("Error", "Failed to update employee.")
#             return False
#
# def employee(root=None, prev_window=None):
#     app = EmployeeApp(root, prev_window)
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     employee(root)
#     root.mainloop()



# import tkinter as tk
# from tkinter import messagebox, filedialog
# import webbrowser
# import pandas as pd  # For reading Excel files
# from db import fetch_employees, insert_employee, delete_employee, update_employee, fetch_companies, insert_bulk_employee_data  # Add insert_bulk_employee_data
#
# class EmployeeApp:
#     def __init__(self, root, prev_window=None):
#         if prev_window:
#             prev_window.destroy()
#         self.root = tk.Toplevel(root)
#         self.root.title("Employee Management")
#         self.root.configure(bg="#2B2B2B")
#         self.root.state("zoomed")
#         self.selected_employee = None
#         self.employee_frames = {}
#         self.setup_ui()
#         self.display_employees()
#
#     def setup_ui(self):
#         self.employee_frame = tk.Frame(self.root, bg="#3A3A3A")
#         self.employee_frame.pack(pady=10, fill="both", expand=True)
#
#         self.canvas = tk.Canvas(self.employee_frame, bg="#3A3A3A")
#         self.scroll_y = tk.Scrollbar(self.employee_frame, orient="vertical", command=self.canvas.yview, bg="#4A90E2", troughcolor="#3A3A3A")
#         self.scroll_y.pack(side="right", fill="y")
#
#         self.inner_frame = tk.Frame(self.canvas, bg="#3A3A3A")
#         self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
#
#         self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
#         self.canvas.configure(yscrollcommand=self.scroll_y.set)
#         self.canvas.pack(side="left", fill="both", expand=True)
#
#         self.button_frame = tk.Frame(self.root, bg="#2B2B2B")
#         self.button_frame.pack(pady=10, fill="x")
#
#         self.add_button = tk.Button(self.button_frame, text="Add New Employee", command=self.show_form,
#                                     bg="#4A90E2", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.add_button.pack(side="left", padx=10)
#
#         self.update_button = tk.Button(self.button_frame, text="Update", command=self.handle_update,
#                                        bg="#4A90E2", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.update_button.pack(side="left", padx=10)
#
#         self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.handle_delete,
#                                        bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.delete_button.pack(side="left", padx=10)
#
#         self.linkedin_button = tk.Button(self.button_frame, text="LinkedIn", command=self.open_linkedin,
#                                          bg="#0077B5", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.linkedin_button.pack(side="left", padx=10)
#
#         self.lusha_button = tk.Button(self.button_frame, text="Lusha", command=self.open_lusha,
#                                       bg="#00C4CC", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.lusha_button.pack(side="left", padx=10)
#
#         self.salesql_button = tk.Button(self.button_frame, text="SalesQL", command=self.open_salesql,
#                                         bg="#FF5733", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.salesql_button.pack(side="left", padx=10)
#
#         # New Bulk Data Button
#         self.bulk_data_button = tk.Button(self.button_frame, text="Bulk Data", command=self.show_bulk_data_form,
#                                           bg="#50C878", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.bulk_data_button.pack(side="left", padx=10)
#
#         self.back_button = tk.Button(self.button_frame, text="Back", command=lambda: self.back_to_dashboard(),
#                                      bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.back_button.pack(side="right", padx=10)
#
#     def back_to_dashboard(self):
#         from dashboard import open_dashboard
#         self.root.destroy()
#         open_dashboard(root=self.root.master, prev_window=self.root)
#
#     def display_employees(self):
#         for widget in self.inner_frame.winfo_children():
#             widget.destroy()
#         self.employee_frames.clear()
#         self.selected_employee = None
#         employees = fetch_employees()
#         num_employees = len(employees)
#         num_rows = (num_employees + 2) // 3
#         CARD_WIDTH = 380
#         CARD_HEIGHT = 380
#         for row in range(num_rows):
#             row_frame = tk.Frame(self.inner_frame, bg="#3A3A3A")
#             row_frame.pack(pady=10, fill="x")
#             for col in range(3):
#                 employee_idx = row * 3 + col
#                 if employee_idx >= num_employees:
#                     tk.Frame(row_frame, width=CARD_WIDTH, height=CARD_HEIGHT, bg="#3A3A3A").pack(side="left", padx=5)
#                     continue
#                 employee = employees[employee_idx]
#                 frame = tk.Frame(row_frame, relief="solid", bd=2, bg="#25253A",
#                                  width=CARD_WIDTH, height=CARD_HEIGHT)
#                 frame.pack(side="left", padx=5)
#                 frame.pack_propagate(False)
#                 label_text = (
#                     f"ID: {employee.get('id', 'N/A')}\n"
#                     f"Name: {employee.get('name', 'N/A')}\n"
#                     f"Department: {employee.get('department', 'N/A')}\n"
#                     f"Phone No 1: {employee.get('phone_no1', 'N/A')}\n"
#                     f"Phone No 2: {employee.get('phone_no2', 'N/A')}\n"
#                     f"Designation: {employee.get('designation', 'N/A')}\n"
#                     f"LinkedIn: {employee.get('linkedin_link', 'N/A')}\n"
#                     f"Service: {employee.get('service_provided', 'N/A')}\n"
#                     f"Company: {employee.get('company', 'N/A')}"
#                 )
#                 label = tk.Label(frame, text=label_text, justify="left", anchor="nw",
#                                  font=("Roboto", 9), bg="#25253A", fg="#E0E0E0", wraplength=CARD_WIDTH-20)
#                 label.pack(padx=5, pady=5, fill="both", expand=True)
#                 frame.bind("<Button-1>", lambda e, emp=employee: self.select_employee(emp))
#                 label.bind("<Button-1>", lambda e, emp=employee: self.select_employee(emp))
#                 self.employee_frames[employee['id']] = frame
#         self.canvas.update_idletasks()
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#
#     def select_employee(self, employee):
#         if self.selected_employee:
#             prev_frame = self.employee_frames[self.selected_employee['id']]
#             prev_frame.config(relief="solid", bd=2)
#         self.selected_employee = employee
#         selected_frame = self.employee_frames[employee['id']]
#         selected_frame.config(relief="solid", bd=4, highlightbackground="#4A90E2")
#
#     def open_linkedin(self):
#         if not self.selected_employee:
#             messagebox.showwarning("Selection Error", "Please select an employee to view their LinkedIn profile!")
#             return
#         linkedin_url = self.selected_employee.get('linkedin_link', 'N/A')
#         if linkedin_url and linkedin_url != 'N/A' and linkedin_url.strip():
#             try:
#                 webbrowser.open(linkedin_url)
#             except Exception as e:
#                 messagebox.showerror("Error", f"Failed to open LinkedIn profile: {str(e)}")
#         else:
#             messagebox.showwarning("No LinkedIn", "The selected employee has no LinkedIn profile link provided!")
#
#     def open_lusha(self):
#         try:
#             webbrowser.open("https://www.lusha.com")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to open Lusha: {str(e)}")
#
#     def open_salesql(self):
#         try:
#             webbrowser.open("https://www.salesql.com")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to open SalesQL: {str(e)}")
#
#     def handle_update(self):
#         if not self.selected_employee:
#             messagebox.showwarning("Selection Error", "Please select an employee to update!")
#             return
#         self.open_edit_form(self.selected_employee)
#
#     def handle_delete(self):
#         if not self.selected_employee:
#             messagebox.showwarning("Selection Error", "Please select an employee to delete!")
#             return
#         self.delete_employee(self.selected_employee['id'])
#
#     def delete_employee(self, id):
#         if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
#             if delete_employee(id):
#                 messagebox.showinfo("Success", "Employee deleted successfully!")
#                 self.display_employees()
#             else:
#                 messagebox.showerror("Error", "Failed to delete employee.")
#
#     def show_form(self):
#         self.create_form(None, "Add Employee", self.submit_add)
#
#     def open_edit_form(self, employee):
#         self.create_form(employee, "Edit Employee", lambda data: self.submit_edit(data, self.selected_employee['id']))
#
#     def create_form(self, employee, title, submit_action):
#         form_window = tk.Toplevel(self.root)
#         form_window.title(title)
#         form_window.geometry("400x500")
#         form_window.configure(bg="#2B2B2B")
#         tk.Label(form_window, text=title, font=("Roboto", 12, "bold"), bg="#2B2B2B", fg="#4A90E2").pack(pady=10)
#         fields = ["id", "name", "department", "phone_no1", "phone_no2", "designation", "linkedin_link",
#                   "service_provided", "company"]
#         values = employee or {}
#         entries = {}
#         for field in fields:
#             tk.Label(form_window, text=field, bg="#2B2B2B", fg="#E0E0E0").pack()
#             entry = tk.Entry(form_window, bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#             entry.insert(0, values.get(field.lower().replace(" ", ""), ""))
#             entry.pack(pady=5, ipadx=5, ipady=2, fill="x")
#             entries[field] = entry
#         button_frame = tk.Frame(form_window, bg="#2B2B2B")
#         button_frame.pack(pady=10)
#
#         def on_submit():
#             data = {field: entries[field].get() for field in fields}
#             if submit_action(data):
#                 form_window.destroy()
#
#         tk.Button(button_frame, text="Submit" if title == "Add Employee" else "Update",
#                   command=on_submit, bg="#50C878", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(side="left", padx=5)
#         tk.Button(button_frame, text="Cancel", command=form_window.destroy,
#                   bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(side="left", padx=5)
#
#     def submit_add(self, data):
#         companies = fetch_companies()
#         company_names = [company['company_name'] for company in companies]
#         if data["company"] not in company_names:
#             messagebox.showwarning("Validation Error",
#                                  "The company name does not exist. Please create the company first!")
#             return False
#         if not all([data["id"], data["name"], data["department"], data["phone_no1"], data["company"]]):
#             messagebox.showwarning("Validation Error", "Required fields are missing!")
#             return False
#         if insert_employee(**data):
#             messagebox.showinfo("Success", "Employee added successfully!")
#             self.display_employees()
#             return True
#         else:
#             messagebox.showerror("Error", "Failed to add employee.")
#             return False
#
#     def submit_edit(self, data, employee_id):
#         companies = fetch_companies()
#         company_names = [company['company_name'] for company in companies]
#         if data["company"] not in company_names:
#             messagebox.showwarning("Validation Error",
#                                  "The company name does not exist. Please create the company first!")
#             return False
#         if not all([data["id"], data["name"], data["department"], data["phone_no1"], data["company"]]):
#             messagebox.showwarning("Validation Error", "Required fields are missing!")
#             return False
#         success = update_employee(
#             id=data["id"],
#             name=data["name"],
#             department=data["department"],
#             phone_no1=data["phone_no1"],
#             phone_no2=data["phone_no2"],
#             designation=data["designation"],
#             linkedin_link=data["linkedin_link"],
#             service_provided=data["service_provided"],
#             company=data["company"]
#         )
#         if success:
#             messagebox.showinfo("Success", "Employee updated successfully!")
#             self.selected_employee.update(data)
#             self.display_employees()
#             return True
#         else:
#             messagebox.showerror("Error", "Failed to update employee.")
#             return False
#
#     def show_bulk_data_form(self):
#         bulk_window = tk.Toplevel(self.root)
#         bulk_window.title("Bulk Data Upload")
#         bulk_window.geometry("400x200")
#         bulk_window.configure(bg="#2B2B2B")
#
#         tk.Label(bulk_window, text="Upload Excel File", bg="#2B2B2B", font=("Roboto", 12, "bold"), fg="#E0E0E0").pack(pady=10)
#         file_label = tk.Label(bulk_window, text="No file selected", bg="#2B2B2B", fg="#E0E0E0")
#         file_label.pack(pady=5)
#
#         def select_file():
#             file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
#             if file_path:
#                 file_label.config(text=file_path)
#                 bulk_window.file_path = file_path  # Store file path in window object
#
#         tk.Button(bulk_window, text="Browse", command=select_file, bg="#4A90E2", fg="#E0E0E0",
#                   font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(pady=10)
#
#         def submit_bulk():
#             if hasattr(bulk_window, 'file_path'):
#                 try:
#                     df = pd.read_excel(bulk_window.file_path)
#                     required_columns = ["id", "name", "department", "phone_no1", "company"]
#                     if not all(col in df.columns for col in required_columns):
#                         messagebox.showerror("Error", "Excel file must contain 'id', 'name', 'department', 'phone_no1', and 'company' columns!")
#                         return
#                     companies = fetch_companies()
#                     company_names = [company['company_name'] for company in companies]
#                     invalid_companies = [emp["company"] for emp in df.to_dict(orient="records") if emp["company"] not in company_names]
#                     if invalid_companies:
#                         messagebox.showerror("Error", f"Invalid company names found: {', '.join(set(invalid_companies))}. Please create these companies first!")
#                         return
#                     employees = df.to_dict(orient="records")
#                     success = insert_bulk_employee_data(employees)
#                     if success:
#                         messagebox.showinfo("Success", "All employee data entered successfully!")
#                         bulk_window.destroy()
#                         self.display_employees()
#                     else:
#                         messagebox.showerror("Error", "Failed to add bulk employee data!")
#                 except Exception as e:
#                     messagebox.showerror("Error", f"Failed to process file: {str(e)}")
#             else:
#                 messagebox.showwarning("Selection Error", "Please select an Excel file!")
#
#         tk.Button(bulk_window, text="Submit", command=submit_bulk, bg="#50C878", fg="#E0E0E0",
#                   font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(side="left", padx=20, pady=20)
#         tk.Button(bulk_window, text="Back", command=bulk_window.destroy, bg="#FF5555", fg="#E0E0E0",
#                   font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(side="right", padx=20, pady=20)
#
# def employee(root=None, prev_window=None):
#     app = EmployeeApp(root, prev_window)
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     employee(root)
#     root.mainloop()



# import tkinter as tk
# from tkinter import messagebox, filedialog
# import webbrowser
# import pandas as pd
# from db import fetch_employees, insert_employee, delete_employee, update_employee, fetch_companies, insert_bulk_employee_data
#
# class EmployeeApp:
#     def __init__(self, root, prev_window=None):
#         if prev_window:
#             prev_window.destroy()
#         self.root = tk.Toplevel(root)
#         self.root.title("Employee Management")
#         self.root.configure(bg="#2B2B2B")
#         self.root.state("zoomed")
#         self.selected_employee = None
#         self.employee_frames = {}
#         self.setup_ui()
#         self.display_employees()
#
#     def setup_ui(self):
#         self.employee_frame = tk.Frame(self.root, bg="#3A3A3A")
#         self.employee_frame.pack(pady=10, fill="both", expand=True)
#
#         self.canvas = tk.Canvas(self.employee_frame, bg="#3A3A3A")
#         self.scroll_y = tk.Scrollbar(self.employee_frame, orient="vertical", command=self.canvas.yview, bg="#4A90E2", troughcolor="#3A3A3A")
#         self.scroll_y.pack(side="right", fill="y")
#
#         self.inner_frame = tk.Frame(self.canvas, bg="#3A3A3A")
#         self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
#
#         self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
#         self.canvas.configure(yscrollcommand=self.scroll_y.set)
#         self.canvas.pack(side="left", fill="both", expand=True)
#
#         self.button_frame = tk.Frame(self.root, bg="#2B2B2B")
#         self.button_frame.pack(pady=10, fill="x")
#
#         self.add_button = tk.Button(self.button_frame, text="Add New Employee", command=self.show_form,
#                                     bg="#4A90E2", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.add_button.pack(side="left", padx=10)
#
#         self.update_button = tk.Button(self.button_frame, text="Update", command=self.handle_update,
#                                        bg="#4A90E2", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.update_button.pack(side="left", padx=10)
#
#         self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.handle_delete,
#                                        bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.delete_button.pack(side="left", padx=10)
#
#         self.linkedin_button = tk.Button(self.button_frame, text="LinkedIn", command=self.open_linkedin,
#                                          bg="#0077B5", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.linkedin_button.pack(side="left", padx=10)
#
#         self.lusha_button = tk.Button(self.button_frame, text="Lusha", command=self.open_lusha,
#                                       bg="#00C4CC", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.lusha_button.pack(side="left", padx=10)
#
#         self.salesql_button = tk.Button(self.button_frame, text="SalesQL", command=self.open_salesql,
#                                         bg="#FF5733", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.salesql_button.pack(side="left", padx=10)
#
#         self.bulk_data_button = tk.Button(self.button_frame, text="Bulk Data", command=self.show_bulk_data_form,
#                                           bg="#50C878", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.bulk_data_button.pack(side="left", padx=10)
#
#         self.back_button = tk.Button(self.button_frame, text="Back", command=lambda: self.back_to_dashboard(),
#                                      bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.back_button.pack(side="right", padx=10)
#
#     def back_to_dashboard(self):
#         from dashboard import open_dashboard
#         self.root.destroy()
#         open_dashboard(root=self.root.master, prev_window=self.root)
#
#     def display_employees(self):
#         for widget in self.inner_frame.winfo_children():
#             widget.destroy()
#         self.employee_frames.clear()
#         self.selected_employee = None
#         employees = fetch_employees()
#         num_employees = len(employees)
#         num_rows = (num_employees + 2) // 3
#         CARD_WIDTH = 380
#         CARD_HEIGHT = 380
#         for row in range(num_rows):
#             row_frame = tk.Frame(self.inner_frame, bg="#3A3A3A")
#             row_frame.pack(pady=10, fill="x")
#             for col in range(3):
#                 employee_idx = row * 3 + col
#                 if employee_idx >= num_employees:
#                     tk.Frame(row_frame, width=CARD_WIDTH, height=CARD_HEIGHT, bg="#3A3A3A").pack(side="left", padx=5)
#                     continue
#                 employee = employees[employee_idx]
#                 frame = tk.Frame(row_frame, relief="solid", bd=2, bg="#25253A",
#                                  width=CARD_WIDTH, height=CARD_HEIGHT)
#                 frame.pack(side="left", padx=5)
#                 frame.pack_propagate(False)
#                 label_text = (
#                     f"ID: {employee.get('id', 'N/A')}\n"
#                     f"Name: {employee.get('name', 'N/A')}\n"
#                     f"Department: {employee.get('department', 'N/A')}\n"
#                     f"Phone No 1: {employee.get('phone_no1', 'N/A')}\n"
#                     f"Phone No 2: {employee.get('phone_no2', 'N/A')}\n"
#                     f"Designation: {employee.get('designation', 'N/A')}\n"
#                     f"LinkedIn: {employee.get('linkedin_link', 'N/A')}\n"
#                     f"Service: {employee.get('service_provided', 'N/A')}\n"
#                     f"Company: {employee.get('company', 'N/A')}"
#                 )
#                 label = tk.Label(frame, text=label_text, justify="left", anchor="nw",
#                                  font=("Roboto", 9), bg="#25253A", fg="#E0E0E0", wraplength=CARD_WIDTH-20)
#                 label.pack(padx=5, pady=5, fill="both", expand=True)
#                 frame.bind("<Button-1>", lambda e, emp=employee: self.select_employee(emp))
#                 label.bind("<Button-1>", lambda e, emp=employee: self.select_employee(emp))
#                 self.employee_frames[employee['id']] = frame
#         self.canvas.update_idletasks()
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#
#     def select_employee(self, employee):
#         if self.selected_employee:
#             prev_frame = self.employee_frames[self.selected_employee['id']]
#             prev_label = prev_frame.winfo_children()[0]
#             prev_frame.config(bg="#25253A", relief="solid", bd=2)
#             prev_label.config(bg="#25253A")
#         self.selected_employee = employee
#         selected_frame = self.employee_frames[employee['id']]
#         selected_label = selected_frame.winfo_children()[0]
#         selected_frame.config(bg="#4A90E2", relief="solid", bd=4)
#         selected_label.config(bg="#4A90E2")
#
#     def open_linkedin(self):
#         if not self.selected_employee:
#             messagebox.showwarning("Selection Error", "Please select an employee to view their LinkedIn profile!")
#             return
#         linkedin_url = self.selected_employee.get('linkedin_link', 'N/A')
#         if linkedin_url and linkedin_url != 'N/A' and linkedin_url.strip():
#             try:
#                 webbrowser.open(linkedin_url)
#             except Exception as e:
#                 messagebox.showerror("Error", f"Failed to open LinkedIn profile: {str(e)}")
#         else:
#             messagebox.showwarning("No LinkedIn", "The selected employee has no LinkedIn profile link provided!")
#
#     def open_lusha(self):
#         try:
#             webbrowser.open("https://www.lusha.com")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to open Lusha: {str(e)}")
#
#     def open_salesql(self):
#         try:
#             webbrowser.open("https://www.salesql.com")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to open SalesQL: {str(e)}")
#
#     def handle_update(self):
#         if not self.selected_employee:
#             messagebox.showwarning("Selection Error", "Please select an employee to update!")
#             return
#         self.open_edit_form(self.selected_employee)
#
#     def handle_delete(self):
#         if not self.selected_employee:
#             messagebox.showwarning("Selection Error", "Please select an employee to delete!")
#             return
#         self.delete_employee(self.selected_employee['id'])
#
#     def delete_employee(self, id):
#         if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
#             if delete_employee(id):
#                 messagebox.showinfo("Success", "Employee deleted successfully!")
#                 self.display_employees()
#             else:
#                 messagebox.showerror("Error", "Failed to delete employee.")
#
#     def show_form(self):
#         self.create_form(None, "Add Employee", self.submit_add)
#
#     def open_edit_form(self, employee):
#         self.create_form(employee, "Edit Employee", lambda data: self.submit_edit(data, self.selected_employee['id']))
#
#     def create_form(self, employee, title, submit_action):
#         form_window = tk.Toplevel(self.root)
#         form_window.title(title)
#         form_window.geometry("400x500")
#         form_window.configure(bg="#2B2B2B")
#         tk.Label(form_window, text=title, font=("Roboto", 12, "bold"), bg="#2B2B2B", fg="#4A90E2").pack(pady=10)
#         fields = ["id", "name", "department", "phone_no1", "phone_no2", "designation", "linkedin_link",
#                   "service_provided", "company"]
#         values = employee or {}
#         entries = {}
#         for field in fields:
#             tk.Label(form_window, text=field, bg="#2B2B2B", fg="#E0E0E0").pack()
#             entry = tk.Entry(form_window, bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#             entry.insert(0, values.get(field.lower().replace(" ", ""), ""))
#             entry.pack(pady=5, ipadx=5, ipady=2, fill="x")
#             entries[field] = entry
#         button_frame = tk.Frame(form_window, bg="#2B2B2B")
#         button_frame.pack(pady=10)
#
#         def on_submit():
#             data = {field: entries[field].get() for field in fields}
#             if submit_action(data):
#                 form_window.destroy()
#
#         tk.Button(button_frame, text="Submit" if title == "Add Employee" else "Update",
#                   command=on_submit, bg="#50C878", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(side="left", padx=5)
#         tk.Button(button_frame, text="Cancel", command=form_window.destroy,
#                   bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(side="left", padx=5)
#
#     def submit_add(self, data):
#         companies = fetch_companies()
#         company_names = [company['company_name'] for company in companies]
#         if data["company"] not in company_names:
#             messagebox.showwarning("Validation Error",
#                                  "The company name does not exist. Please create the company first!")
#             return False
#         if not all([data["id"], data["name"], data["department"], data["phone_no1"], data["company"]]):
#             messagebox.showwarning("Validation Error", "Required fields are missing!")
#             return False
#         if insert_employee(**data):
#             messagebox.showinfo("Success", "Employee added successfully!")
#             self.display_employees()
#             return True
#         else:
#             messagebox.showerror("Error", "Failed to add employee.")
#             return False
#
#     def submit_edit(self, data, employee_id):
#         companies = fetch_companies()
#         company_names = [company['company_name'] for company in companies]
#         if data["company"] not in company_names:
#             messagebox.showwarning("Validation Error",
#                                  "The company name does not exist. Please create the company first!")
#             return False
#         if not all([data["id"], data["name"], data["department"], data["phone_no1"], data["company"]]):
#             messagebox.showwarning("Validation Error", "Required fields are missing!")
#             return False
#         success = update_employee(
#             id=data["id"],
#             name=data["name"],
#             department=data["department"],
#             phone_no1=data["phone_no1"],
#             phone_no2=data["phone_no2"],
#             designation=data["designation"],
#             linkedin_link=data["linkedin_link"],
#             service_provided=data["service_provided"],
#             company=data["company"]
#         )
#         if success:
#             messagebox.showinfo("Success", "Employee updated successfully!")
#             self.selected_employee.update(data)
#             self.display_employees()
#             return True
#         else:
#             messagebox.showerror("Error", "Failed to update employee.")
#             return False
#
#     def show_bulk_data_form(self):
#         bulk_window = tk.Toplevel(self.root)
#         bulk_window.title("Bulk Data Upload")
#         bulk_window.geometry("400x200")
#         bulk_window.configure(bg="#2B2B2B")
#
#         tk.Label(bulk_window, text="Upload Excel File", bg="#2B2B2B", font=("Roboto", 12, "bold"), fg="#E0E0E0").pack(pady=10)
#         file_label = tk.Label(bulk_window, text="No file selected", bg="#2B2B2B", fg="#E0E0E0")
#         file_label.pack(pady=5)
#
#         def select_file():
#             file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
#             if file_path:
#                 file_label.config(text=file_path)
#                 bulk_window.file_path = file_path
#
#         tk.Button(bulk_window, text="Browse", command=select_file, bg="#4A90E2", fg="#E0E0E0",
#                   font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(pady=10)
#
#         def submit_bulk():
#             if hasattr(bulk_window, 'file_path'):
#                 try:
#                     df = pd.read_excel(bulk_window.file_path)
#                     required_columns = ["id", "name", "department", "phone_no1", "company"]
#                     if not all(col in df.columns for col in required_columns):
#                         messagebox.showerror("Error", "Excel file must contain 'id', 'name', 'department', 'phone_no1', and 'company' columns!")
#                         return
#                     companies = fetch_companies()
#                     company_names = [company['company_name'] for company in companies]
#                     invalid_companies = [emp["company"] for emp in df.to_dict(orient="records") if emp["company"] not in company_names]
#                     if invalid_companies:
#                         messagebox.showerror("Error", f"Invalid company names found: {', '.join(set(invalid_companies))}. Please create these companies first!")
#                         return
#                     employees = df.to_dict(orient="records")
#                     success = insert_bulk_employee_data(employees)
#                     if success:
#                         messagebox.showinfo("Success", "All employee data entered successfully!")
#                         bulk_window.destroy()
#                         self.display_employees()
#                     else:
#                         messagebox.showerror("Error", "Failed to add bulk employee data!")
#                 except Exception as e:
#                     messagebox.showerror("Error", f"Failed to process file: {str(e)}")
#             else:
#                 messagebox.showwarning("Selection Error", "Please select an Excel file!")
#
#         tk.Button(bulk_window, text="Submit", command=submit_bulk, bg="#50C878", fg="#E0E0E0",
#                   font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(side="left", padx=20, pady=20)
#         tk.Button(bulk_window, text="Back", command=bulk_window.destroy, bg="#FF5555", fg="#E0E0E0",
#                   font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(side="right", padx=20, pady=20)
#
# def employee(root=None, prev_window=None):
#     app = EmployeeApp(root, prev_window)
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     employee(root)
#     root.mainloop()




import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser
import pandas as pd
from db import fetch_employees, insert_employee, delete_employee, update_employee, fetch_companies, \
    insert_bulk_employee_data


class EmployeeApp:
    def __init__(self, root, prev_window=None):
        if prev_window:
            prev_window.destroy()
        self.root = tk.Toplevel(root)
        self.root.title("Employee Management")
        self.root.configure(bg="#2B2B2B")
        self.root.state("zoomed")
        self.selected_employee = None
        self.employee_frames = {}
        self.setup_ui()
        self.display_employees()

    def setup_ui(self):
        self.employee_frame = tk.Frame(self.root, bg="#3A3A3A")
        self.employee_frame.pack(pady=10, fill="both", expand=True)

        self.canvas = tk.Canvas(self.employee_frame, bg="#3A3A3A")
        self.scroll_y = tk.Scrollbar(self.employee_frame, orient="vertical", command=self.canvas.yview, bg="#4A90E2",
                                     troughcolor="#3A3A3A")
        self.scroll_y.pack(side="right", fill="y")

        self.inner_frame = tk.Frame(self.canvas, bg="#3A3A3A")
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.button_frame = tk.Frame(self.root, bg="#2B2B2B")
        self.button_frame.pack(pady=10, fill="x")

        self.add_button = tk.Button(self.button_frame, text="Add New Employee", command=self.show_form,
                                    bg="#4A90E2", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10,
                                    pady=5)
        self.add_button.pack(side="left", padx=10)

        self.update_button = tk.Button(self.button_frame, text="Update", command=self.handle_update,
                                       bg="#4A90E2", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10,
                                       pady=5)
        self.update_button.pack(side="left", padx=10)

        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.handle_delete,
                                       bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10,
                                       pady=5)
        self.delete_button.pack(side="left", padx=10)

        self.linkedin_button = tk.Button(self.button_frame, text="LinkedIn", command=self.open_linkedin,
                                         bg="#0077B5", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat",
                                         padx=10, pady=5)
        self.linkedin_button.pack(side="left", padx=10)

        self.lusha_button = tk.Button(self.button_frame, text="Lusha", command=self.open_lusha,
                                      bg="#00C4CC", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10,
                                      pady=5)
        self.lusha_button.pack(side="left", padx=10)

        self.salesql_button = tk.Button(self.button_frame, text="SalesQL", command=self.open_salesql,
                                        bg="#FF5733", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10,
                                        pady=5)
        self.salesql_button.pack(side="left", padx=10)

        self.bulk_data_button = tk.Button(self.button_frame, text="Bulk Data", command=self.show_bulk_data_form,
                                          bg="#50C878", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat",
                                          padx=10, pady=5)
        self.bulk_data_button.pack(side="left", padx=10)

        self.back_button = tk.Button(self.button_frame, text="Back", command=lambda: self.back_to_dashboard(),
                                     bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10,
                                     pady=5)
        self.back_button.pack(side="right", padx=10)

    def back_to_dashboard(self):
        from dashboard import open_dashboard
        self.root.destroy()
        open_dashboard(root=self.root.master, prev_window=self.root)

    def display_employees(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.employee_frames.clear()
        self.selected_employee = None
        employees = fetch_employees()
        num_employees = len(employees)
        num_rows = (num_employees + 2) // 3
        CARD_WIDTH = 380
        CARD_HEIGHT = 380
        for row in range(num_rows):
            row_frame = tk.Frame(self.inner_frame, bg="#3A3A3A")
            row_frame.pack(pady=10, fill="x")
            for col in range(3):
                employee_idx = row * 3 + col
                if employee_idx >= num_employees:
                    tk.Frame(row_frame, width=CARD_WIDTH, height=CARD_HEIGHT, bg="#3A3A3A").pack(side="left", padx=5)
                    continue
                employee = employees[employee_idx]
                frame = tk.Frame(row_frame, relief="solid", bd=2, bg="#25253A",
                                 width=CARD_WIDTH, height=CARD_HEIGHT)
                frame.pack(side="left", padx=5)
                frame.pack_propagate(False)
                label_text = (
                    f"ID: {employee.get('id', 'N/A')}\n"
                    f"Name: {employee.get('name', 'N/A')}\n"
                    f"Department: {employee.get('department', 'N/A')}\n"
                    f"Phone No 1: {employee.get('phone_no1', 'N/A')}\n"
                    f"Phone No 2: {employee.get('phone_no2', 'N/A')}\n"
                    f"Designation: {employee.get('designation', 'N/A')}\n"
                    f"LinkedIn: {employee.get('linkedin_link', 'N/A')}\n"
                    f"Service: {employee.get('service_provided', 'N/A')}\n"
                    f"Company: {employee.get('company', 'N/A')}"
                )
                label = tk.Label(frame, text=label_text, justify="left", anchor="nw",
                                 font=("Roboto", 9), bg="#25253A", fg="#E0E0E0", wraplength=CARD_WIDTH - 20)
                label.pack(padx=5, pady=5, fill="both", expand=True)
                frame.bind("<Button-1>", lambda e, emp=employee: self.select_employee(emp))
                label.bind("<Button-1>", lambda e, emp=employee: self.select_employee(emp))
                self.employee_frames[employee['id']] = frame
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def select_employee(self, employee):
        if self.selected_employee:
            prev_frame = self.employee_frames[self.selected_employee['id']]
            prev_label = prev_frame.winfo_children()[0]
            prev_frame.config(bg="#25253A", relief="solid", bd=2)
            prev_label.config(bg="#25253A")
        self.selected_employee = employee
        selected_frame = self.employee_frames[employee['id']]
        selected_label = selected_frame.winfo_children()[0]
        selected_frame.config(bg="#4A90E2", relief="solid", bd=4)
        selected_label.config(bg="#4A90E2")

    def open_linkedin(self):
        if not self.selected_employee:
            messagebox.showwarning("Selection Error", "Please select an employee to view their LinkedIn profile!")
            return
        linkedin_url = self.selected_employee.get('linkedin_link', 'N/A')
        if linkedin_url and linkedin_url != 'N/A' and linkedin_url.strip():
            try:
                webbrowser.open(linkedin_url)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open LinkedIn profile: {str(e)}")
        else:
            messagebox.showwarning("No LinkedIn", "The selected employee has no LinkedIn profile link provided!")

    def open_lusha(self):
        try:
            webbrowser.open("https://www.lusha.com")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Lusha: {str(e)}")

    def open_salesql(self):
        try:
            webbrowser.open("https://www.salesql.com")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open SalesQL: {str(e)}")

    def handle_update(self):
        if not self.selected_employee:
            messagebox.showwarning("Selection Error", "Please select an employee to update!")
            return
        self.open_edit_form(self.selected_employee)

    def handle_delete(self):
        if not self.selected_employee:
            messagebox.showwarning("Selection Error", "Please select an employee to delete!")
            return
        self.delete_employee(self.selected_employee['id'])

    def delete_employee(self, id):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
            if delete_employee(id):
                messagebox.showinfo("Success", "Employee deleted successfully!")
                self.display_employees()
            else:
                messagebox.showerror("Error", "Failed to delete employee.")

    def show_form(self):
        self.create_form(None, "Add Employee", self.submit_add)

    def open_edit_form(self, employee):
        self.create_form(employee, "Edit Employee", lambda data: self.submit_edit(data, self.selected_employee['id']))

    def create_form(self, employee, title, submit_action):
        form_window = tk.Toplevel(self.root)
        form_window.title(title)
        form_window.geometry("400x500")
        form_window.configure(bg="#2B2B2B")
        tk.Label(form_window, text=title, font=("Roboto", 12, "bold"), bg="#2B2B2B", fg="#4A90E2").pack(pady=10)
        fields = ["id", "name", "department", "phone_no1", "phone_no2", "designation", "linkedin_link",
                  "service_provided", "company"]
        values = employee or {}
        entries = {}
        for field in fields:
            tk.Label(form_window, text=field, bg="#2B2B2B", fg="#E0E0E0").pack()
            entry = tk.Entry(form_window, bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
            entry.insert(0, str(values.get(field.lower().replace(" ", ""), "")))
            entry.pack(pady=5, ipadx=5, ipady=2, fill="x")
            entries[field] = entry
        button_frame = tk.Frame(form_window, bg="#2B2B2B")
        button_frame.pack(pady=10)

        def on_submit():
            data = {field: entries[field].get() for field in fields}
            if submit_action(data):
                form_window.destroy()

        if title == "Add Employee":
            tk.Button(button_frame, text="Submit", command=on_submit, bg="#50C878", fg="#E0E0E0",
                      font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(side="left", padx=5)
        elif title == "Edit Employee":
            tk.Button(button_frame, text="Submit", command=on_submit, bg="#50C878", fg="#E0E0E0",
                      font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(side="left", padx=5)

        tk.Button(button_frame, text="Cancel", command=form_window.destroy,
                  bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(
            side="left", padx=5)

    def submit_add(self, data):
        companies = fetch_companies()
        company_names = [company['company_name'] for company in companies]
        if data["company"] not in company_names:
            messagebox.showwarning("Validation Error",
                                   "The company name does not exist. Please create the company first!")
            return False
        if not all([data["id"], data["name"], data["department"], data["phone_no1"], data["company"]]):
            messagebox.showwarning("Validation Error", "Required fields are missing!")
            return False
        if insert_employee(**data):
            messagebox.showinfo("Success", "Employee added successfully!")
            self.display_employees()
            return True
        else:
            messagebox.showerror("Error", "Failed to add employee.")
            return False

    def submit_edit(self, data, employee_id):
        companies = fetch_companies()
        company_names = [company['company_name'] for company in companies]
        if data["company"] not in company_names:
            messagebox.showwarning("Validation Error",
                                   "The company name does not exist. Please create the company first!")
            return False
        if not all([data["id"], data["name"], data["department"], data["phone_no1"], data["company"]]):
            messagebox.showwarning("Validation Error", "Required fields are missing!")
            return False
        success = update_employee(
            id=data["id"],
            name=data["name"],
            department=data["department"],
            phone_no1=data["phone_no1"],
            phone_no2=data["phone_no2"],
            designation=data["designation"],
            linkedin_link=data["linkedin_link"],
            service_provided=data["service_provided"],
            company=data["company"]
        )
        if success:
            messagebox.showinfo("Success", "Employee updated successfully!")
            self.selected_employee.update(data)
            self.display_employees()
            return True
        else:
            messagebox.showerror("Error", "Failed to update employee.")
            return False

    def show_bulk_data_form(self):
        bulk_window = tk.Toplevel(self.root)
        bulk_window.title("Bulk Data Upload")
        bulk_window.geometry("400x200")
        bulk_window.configure(bg="#2B2B2B")

        tk.Label(bulk_window, text="Upload Excel File", bg="#2B2B2B", font=("Roboto", 12, "bold"), fg="#E0E0E0").pack(
            pady=10)
        file_label = tk.Label(bulk_window, text="No file selected", bg="#2B2B2B", fg="#E0E0E0")
        file_label.pack(pady=5)

        def select_file():
            file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
            if file_path:
                file_label.config(text=file_path)
                bulk_window.file_path = file_path

        tk.Button(bulk_window, text="Browse", command=select_file, bg="#4A90E2", fg="#E0E0E0",
                  font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(pady=10)

        def submit_bulk():
            if hasattr(bulk_window, 'file_path'):
                try:
                    df = pd.read_excel(bulk_window.file_path)
                    required_columns = ["id", "name", "department", "phone_no1", "company"]
                    if not all(col in df.columns for col in required_columns):
                        messagebox.showerror("Error",
                                             "Excel file must contain 'id', 'name', 'department', 'phone_no1', and 'company' columns!")
                        return
                    companies = fetch_companies()
                    company_names = [company['company_name'] for company in companies]
                    invalid_companies = [emp["company"] for emp in df.to_dict(orient="records") if
                                         emp["company"] not in company_names]
                    if invalid_companies:
                        messagebox.showerror("Error",
                                             f"Invalid company names found: {', '.join(set(invalid_companies))}. Please create these companies first!")
                        return
                    employees = df.to_dict(orient="records")
                    success = insert_bulk_employee_data(employees)
                    if success:
                        messagebox.showinfo("Success", "All employee data entered successfully!")
                        bulk_window.destroy()
                        self.display_employees()
                    else:
                        messagebox.showerror("Error", "Failed to add bulk employee data!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to process file: {str(e)}")
            else:
                messagebox.showwarning("Selection Error", "Please select an Excel file!")

        tk.Button(bulk_window, text="Submit", command=submit_bulk, bg="#50C878", fg="#E0E0E0",
                  font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(side="left", padx=20, pady=20)
        tk.Button(bulk_window, text="Back", command=bulk_window.destroy, bg="#FF5555", fg="#E0E0E0",
                  font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(side="right", padx=20, pady=20)


def employee(root=None, prev_window=None):
    app = EmployeeApp(root, prev_window)


if __name__ == "__main__":
    root = tk.Tk()
    employee(root)
    root.mainloop()