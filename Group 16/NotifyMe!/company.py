# # import tkinter as tk
# # from tkinter import messagebox
# # import webbrowser
# # from db import fetch_companies, insert_company_data, delete_company, update_company
# #
# # class CompanyApp:
# #     def __init__(self, root, prev_window=None):
# #         if prev_window:
# #             prev_window.destroy()
# #         self.root = tk.Toplevel(root)
# #         self.root.title("Company Management")
# #         self.root.configure(bg="#1E1E2F")
# #         self.root.state("zoomed")
# #         self.selected_company = None
# #         self.company_frames = {}
# #         self.setup_ui()
# #         self.display_companies()
# #
# #     def setup_ui(self):
# #         self.company_frame = tk.Frame(self.root, bg="#2D2D44")
# #         self.company_frame.pack(pady=10, fill="both", expand=True)
# #
# #         self.canvas = tk.Canvas(self.company_frame, bg="#2D2D44")
# #         self.scroll_y = tk.Scrollbar(self.company_frame, orient="vertical", command=self.canvas.yview, bg="#00D4FF", troughcolor="#2D2D44")
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
# #         self.add_button = tk.Button(self.button_frame, text="Add New Company", command=self.show_form,
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
# #         self.website_button = tk.Button(self.button_frame, text="Website", command=self.open_website,
# #                                         bg="#FFAA00", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
# #         self.website_button.pack(side="left", padx=10)
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
# #     def display_companies(self):
# #         for widget in self.inner_frame.winfo_children():
# #             widget.destroy()
# #         self.company_frames.clear()
# #         self.selected_company = None
# #         companies = fetch_companies()
# #         num_companies = len(companies)
# #         num_rows = (num_companies + 2) // 3
# #         CARD_WIDTH, CARD_HEIGHT = 380, 380
# #         for row in range(num_rows):
# #             row_frame = tk.Frame(self.inner_frame, bg="#2D2D44")
# #             row_frame.pack(pady=10, fill="x")
# #             for col in range(3):
# #                 company_idx = row * 3 + col
# #                 if company_idx >= num_companies:
# #                     tk.Frame(row_frame, width=CARD_WIDTH, height=CARD_HEIGHT, bg="#2D2D44").pack(side="left", padx=5)
# #                     continue
# #                 company = companies[company_idx]
# #                 frame = tk.Frame(row_frame, relief="solid", bd=2, bg="#25253A", width=CARD_WIDTH, height=CARD_HEIGHT)
# #                 frame.pack(side="left", padx=5)
# #                 frame.pack_propagate(False)
# #                 label_text = (
# #                     f"ID: {company.get('company_id', 'N/A')}\n"
# #                     f"Name: {company.get('company_name', 'N/A')}\n"
# #                     f"Contact No: {company.get('contact_no', 'N/A')}\n"
# #                     f"Primary Business: {company.get('primary_business', 'N/A')}\n"
# #                     f"Secondary Business: {company.get('secondary_business', 'N/A')}\n"
# #                     f"Since: {company.get('since', 'N/A')}\n"
# #                     f"Email: {company.get('email', 'N/A')}\n"
# #                     f"Website: {company.get('website', 'N/A')}"
# #                 )
# #                 label = tk.Label(frame, text=label_text, justify="left", anchor="nw",
# #                                  font=("Roboto", 9), bg="#25253A", fg="#E0E0E0", wraplength=CARD_WIDTH - 20)
# #                 label.pack(padx=5, pady=5, fill="both", expand=True)
# #                 frame.bind("<Button-1>", lambda e, comp=company: self.select_company(comp))
# #                 label.bind("<Button-1>", lambda e, comp=company: self.select_company(comp))
# #                 self.company_frames[company['company_id']] = frame
# #         self.canvas.update_idletasks()
# #         self.canvas.configure(scrollregion=self.canvas.bbox("all"))
# #
# #     def select_company(self, company):
# #         if self.selected_company:
# #             self.company_frames[self.selected_company['company_id']].config(relief="solid", bd=2)
# #         self.selected_company = company
# #         self.company_frames[company['company_id']].config(relief="solid", bd=4, highlightbackground="#00D4FF")
# #
# #     def open_website(self):
# #         if not self.selected_company:
# #             messagebox.showwarning("Selection Error", "Please select a company to view their website!")
# #             return
# #         website_url = self.selected_company.get('website', '').strip()
# #         if website_url and website_url != 'N/A':
# #             try:
# #                 webbrowser.open(website_url)
# #             except Exception as e:
# #                 messagebox.showerror("Error", f"Failed to open website: {str(e)}")
# #         else:
# #             messagebox.showwarning("No Website", "The selected company has no website link provided!")
# #
# #     def handle_update(self):
# #         if not self.selected_company:
# #             messagebox.showwarning("Selection Error", "Please select a company to update!")
# #             return
# #         self.show_update_form(self.selected_company)
# #
# #     def handle_delete(self):
# #         if not self.selected_company:
# #             messagebox.showwarning("Selection Error", "Please select a company to delete!")
# #             return
# #         if messagebox.askyesno("Confirm", "Are you sure you want to delete this company?"):
# #             if delete_company(self.selected_company['company_id']):
# #                 messagebox.showinfo("Success", "Company deleted successfully!")
# #                 self.display_companies()
# #             else:
# #                 messagebox.showerror("Error", "Failed to delete company.")
# #
# #     def show_form(self):
# #         self.create_form(None, "Add Company", self.submit_add)
# #
# #     def show_update_form(self, company):
# #         update_window = tk.Toplevel(self.root)
# #         update_window.title("Update Company")
# #         update_window.geometry("400x500")
# #         update_window.configure(bg="#1E1E2F")
# #         fields = [
# #             ("Company ID", company['company_id'], True),
# #             ("Company Name", company['company_name'], False),
# #             ("Contact No", company['contact_no'], False),
# #             ("Primary Business", company['primary_business'], False),
# #             ("Secondary Business", company['secondary_business'], False),
# #             ("Since", company['since'], False),
# #             ("Email", company['email'], False),
# #             ("Website", company['website'], False)
# #         ]
# #         entries = {}
# #         for idx, (label, value, disabled) in enumerate(fields):
# #             tk.Label(update_window, text=label, bg="#1E1E2F", font=("Roboto", 10, "bold"), fg="#E0E0E0").grid(row=idx, column=0, padx=10, pady=5, sticky="w")
# #             entry = tk.Entry(update_window, width=40, bg="#2D2D44", fg="#E0E0E0", insertbackground="#00D4FF")
# #             entry.grid(row=idx, column=1, padx=10, pady=5)
# #             entry.insert(0, value or "")
# #             if disabled:
# #                 entry.config(state="disabled")
# #             entries[label] = entry
# #
# #         def save_update():
# #             company_data = {label: entries[label].get() for label, _, _ in fields}
# #             success = update_company(
# #                 company_data["Company ID"],
# #                 company_data["Company Name"],
# #                 company_data["Contact No"],
# #                 company_data["Primary Business"],
# #                 company_data["Secondary Business"],
# #                 company_data["Since"],
# #                 company_data["Email"],
# #                 company_data["Website"]
# #             )
# #             if success:
# #                 messagebox.showinfo("Success", "Company updated successfully!")
# #                 update_window.destroy()
# #                 self.display_companies()
# #             else:
# #                 messagebox.showerror("Error", "Failed to update company!")
# #
# #         tk.Button(update_window, text="Save", command=save_update, bg="#39FF14", fg="#E0E0E0",
# #                   font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).grid(row=len(fields), column=0, columnspan=2, pady=20)
# #
# #     def create_form(self, company, title, submit_action):
# #         form_window = tk.Toplevel(self.root)
# #         form_window.title(title)
# #         form_window.geometry("400x500")
# #         form_window.configure(bg="#1E1E2F")
# #         fields = ["company_id", "company_name", "contact_no", "primary_business", "secondary_business", "since", "email", "website"]
# #         labels = ["Company ID", "Company Name", "Contact No", "Primary Business", "Secondary Business", "Since", "Email", "Website"]
# #         values = company or {}
# #         entries = {}
# #         for idx, (field, label) in enumerate(zip(fields, labels)):
# #             tk.Label(form_window, text=label, bg="#1E1E2F", font=("Roboto", 10), fg="#E0E0E0").grid(row=idx, column=0, padx=10, pady=5, sticky="w")
# #             entry = tk.Entry(form_window, width=40, bg="#2D2D44", fg="#E0E0E0", insertbackground="#00D4FF")
# #             entry.grid(row=idx, column=1, padx=10, pady=5)
# #             entry.insert(0, values.get(field, ""))
# #             if company and field == "company_id":
# #                 entry.config(state="disabled")
# #             entries[field] = entry
# #
# #         def submit():
# #             data = {field: entries[field].get() for field in fields}
# #             if submit_action(data):
# #                 form_window.destroy()
# #
# #         tk.Button(form_window, text="Submit" if not company else "Update", command=submit,
# #                   bg="#39FF14", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).grid(row=len(fields), column=0, columnspan=2, pady=20)
# #
# #     def submit_add(self, data):
# #         if not all([data["company_id"], data["company_name"], data["contact_no"]]):
# #             messagebox.showwarning("Validation Error", "Required fields (ID, Name, Contact No) are missing!")
# #             return False
# #         success = insert_company_data(**data)
# #         if success:
# #             messagebox.showinfo("Success", "Company added successfully!")
# #             self.display_companies()
# #             return True
# #         else:
# #             messagebox.showerror("Error", "Failed to add company!")
# #             return False
# #
# # def company(root=None, prev_window=None):
# #     app = CompanyApp(root, prev_window)
# #
# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     company(root)
# #     root.mainloop()
#
#
#
# import tkinter as tk
# from tkinter import messagebox
# import webbrowser
# from db import fetch_companies, insert_company_data, delete_company, update_company
#
# class CompanyApp:
#     def __init__(self, root, prev_window=None):
#         if prev_window:
#             prev_window.destroy()
#         self.root = tk.Toplevel(root)
#         self.root.title("Company Management")
#         self.root.configure(bg="#2B2B2B")
#         self.root.state("zoomed")
#         self.selected_company = None
#         self.company_frames = {}
#         self.setup_ui()
#         self.display_companies()
#
#     def setup_ui(self):
#         self.company_frame = tk.Frame(self.root, bg="#3A3A3A")
#         self.company_frame.pack(pady=10, fill="both", expand=True)
#
#         self.canvas = tk.Canvas(self.company_frame, bg="#3A3A3A")
#         self.scroll_y = tk.Scrollbar(self.company_frame, orient="vertical", command=self.canvas.yview, bg="#4A90E2", troughcolor="#3A3A3A")
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
#         self.add_button = tk.Button(self.button_frame, text="Add New Company", command=self.show_form,
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
#         self.website_button = tk.Button(self.button_frame, text="Website", command=self.open_website,
#                                         bg="#FFAA00", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.website_button.pack(side="left", padx=10)
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
#     def display_companies(self):
#         for widget in self.inner_frame.winfo_children():
#             widget.destroy()
#         self.company_frames.clear()
#         self.selected_company = None
#         companies = fetch_companies()
#         num_companies = len(companies)
#         num_rows = (num_companies + 2) // 3
#         CARD_WIDTH, CARD_HEIGHT = 380, 380
#         for row in range(num_rows):
#             row_frame = tk.Frame(self.inner_frame, bg="#3A3A3A")
#             row_frame.pack(pady=10, fill="x")
#             for col in range(3):
#                 company_idx = row * 3 + col
#                 if company_idx >= num_companies:
#                     tk.Frame(row_frame, width=CARD_WIDTH, height=CARD_HEIGHT, bg="#3A3A3A").pack(side="left", padx=5)
#                     continue
#                 company = companies[company_idx]
#                 frame = tk.Frame(row_frame, relief="solid", bd=2, bg="#25253A", width=CARD_WIDTH, height=CARD_HEIGHT)
#                 frame.pack(side="left", padx=5)
#                 frame.pack_propagate(False)
#                 label_text = (
#                     f"ID: {company.get('company_id', 'N/A')}\n"
#                     f"Name: {company.get('company_name', 'N/A')}\n"
#                     f"Contact No: {company.get('contact_no', 'N/A')}\n"
#                     f"Primary Business: {company.get('primary_business', 'N/A')}\n"
#                     f"Secondary Business: {company.get('secondary_business', 'N/A')}\n"
#                     f"Since: {company.get('since', 'N/A')}\n"
#                     f"Email: {company.get('email', 'N/A')}\n"
#                     f"Website: {company.get('website', 'N/A')}"
#                 )
#                 label = tk.Label(frame, text=label_text, justify="left", anchor="nw",
#                                  font=("Roboto", 9), bg="#25253A", fg="#E0E0E0", wraplength=CARD_WIDTH - 20)
#                 label.pack(padx=5, pady=5, fill="both", expand=True)
#                 frame.bind("<Button-1>", lambda e, comp=company: self.select_company(comp))
#                 label.bind("<Button-1>", lambda e, comp=company: self.select_company(comp))
#                 self.company_frames[company['company_id']] = frame
#         self.canvas.update_idletasks()
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#
#     def select_company(self, company):
#         if self.selected_company:
#             self.company_frames[self.selected_company['company_id']].config(relief="solid", bd=2)
#         self.selected_company = company
#         self.company_frames[company['company_id']].config(relief="solid", bd=4, highlightbackground="#4A90E2")
#
#     def open_website(self):
#         if not self.selected_company:
#             messagebox.showwarning("Selection Error", "Please select a company to view their website!")
#             return
#         website_url = self.selected_company.get('website', '').strip()
#         if website_url and website_url != 'N/A':
#             try:
#                 webbrowser.open(website_url)
#             except Exception as e:
#                 messagebox.showerror("Error", f"Failed to open website: {str(e)}")
#         else:
#             messagebox.showwarning("No Website", "The selected company has no website link provided!")
#
#     def handle_update(self):
#         if not self.selected_company:
#             messagebox.showwarning("Selection Error", "Please select a company to update!")
#             return
#         self.show_update_form(self.selected_company)
#
#     def handle_delete(self):
#         if not self.selected_company:
#             messagebox.showwarning("Selection Error", "Please select a company to delete!")
#             return
#         if messagebox.askyesno("Confirm", "Are you sure you want to delete this company?"):
#             if delete_company(self.selected_company['company_id']):
#                 messagebox.showinfo("Success", "Company deleted successfully!")
#                 self.display_companies()
#             else:
#                 messagebox.showerror("Error", "Failed to delete company.")
#
#     def show_form(self):
#         self.create_form(None, "Add Company", self.submit_add)
#
#     def show_update_form(self, company):
#         update_window = tk.Toplevel(self.root)
#         update_window.title("Update Company")
#         update_window.geometry("400x500")
#         update_window.configure(bg="#2B2B2B")
#         fields = [
#             ("Company ID", company['company_id'], True),
#             ("Company Name", company['company_name'], False),
#             ("Contact No", company['contact_no'], False),
#             ("Primary Business", company['primary_business'], False),
#             ("Secondary Business", company['secondary_business'], False),
#             ("Since", company['since'], False),
#             ("Email", company['email'], False),
#             ("Website", company['website'], False)
#         ]
#         entries = {}
#         for idx, (label, value, disabled) in enumerate(fields):
#             tk.Label(update_window, text=label, bg="#2B2B2B", font=("Roboto", 10, "bold"), fg="#E0E0E0").grid(row=idx, column=0, padx=10, pady=5, sticky="w")
#             entry = tk.Entry(update_window, width=40, bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#             entry.grid(row=idx, column=1, padx=10, pady=5)
#             entry.insert(0, value or "")
#             if disabled:
#                 entry.config(state="disabled")
#             entries[label] = entry
#
#         def save_update():
#             company_data = {label: entries[label].get() for label, _, _ in fields}
#             success = update_company(
#                 company_data["Company ID"],
#                 company_data["Company Name"],
#                 company_data["Contact No"],
#                 company_data["Primary Business"],
#                 company_data["Secondary Business"],
#                 company_data["Since"],
#                 company_data["Email"],
#                 company_data["Website"]
#             )
#             if success:
#                 messagebox.showinfo("Success", "Company updated successfully!")
#                 update_window.destroy()
#                 self.display_companies()
#             else:
#                 messagebox.showerror("Error", "Failed to update company!")
#
#         tk.Button(update_window, text="Save", command=save_update, bg="#50C878", fg="#E0E0E0",
#                   font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).grid(row=len(fields), column=0, columnspan=2, pady=20)
#
#     def create_form(self, company, title, submit_action):
#         form_window = tk.Toplevel(self.root)
#         form_window.title(title)
#         form_window.geometry("400x500")
#         form_window.configure(bg="#2B2B2B")
#         fields = ["company_id", "company_name", "contact_no", "primary_business", "secondary_business", "since", "email", "website"]
#         labels = ["Company ID", "Company Name", "Contact No", "Primary Business", "Secondary Business", "Since", "Email", "Website"]
#         values = company or {}
#         entries = {}
#         for idx, (field, label) in enumerate(zip(fields, labels)):
#             tk.Label(form_window, text=label, bg="#2B2B2B", font=("Roboto", 10), fg="#E0E0E0").grid(row=idx, column=0, padx=10, pady=5, sticky="w")
#             entry = tk.Entry(form_window, width=40, bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#             entry.grid(row=idx, column=1, padx=10, pady=5)
#             entry.insert(0, values.get(field, ""))
#             if company and field == "company_id":
#                 entry.config(state="disabled")
#             entries[field] = entry
#
#         def submit():
#             data = {field: entries[field].get() for field in fields}
#             if submit_action(data):
#                 form_window.destroy()
#
#         tk.Button(form_window, text="Submit" if not company else "Update", command=submit,
#                   bg="#50C878", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).grid(row=len(fields), column=0, columnspan=2, pady=20)
#
#     def submit_add(self, data):
#         if not all([data["company_id"], data["company_name"], data["contact_no"]]):
#             messagebox.showwarning("Validation Error", "Required fields (ID, Name, Contact No) are missing!")
#             return False
#         success = insert_company_data(**data)
#         if success:
#             messagebox.showinfo("Success", "Company added successfully!")
#             self.display_companies()
#             return True
#         else:
#             messagebox.showerror("Error", "Failed to add company!")
#             return False
#
# def company(root=None, prev_window=None):
#     app = CompanyApp(root, prev_window)
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     company(root)
#     root.mainloop()

# from datetime import datetime
# import tkinter as tk
# from tkinter import messagebox, filedialog
# import webbrowser
# import pandas as pd  # For reading Excel files
# from db import fetch_companies, insert_company_data, delete_company, update_company, insert_bulk_company_data  # Add insert_bulk_company_data
#
# class CompanyApp:
#     def __init__(self, root, prev_window=None):
#         if prev_window:
#             prev_window.destroy()
#         self.root = tk.Toplevel(root)
#         self.root.title("Company Management")
#         self.root.configure(bg="#2B2B2B")
#         self.root.state("zoomed")
#         self.selected_company = None
#         self.company_frames = {}
#         self.setup_ui()
#         self.display_companies()
#
#     def setup_ui(self):
#         self.company_frame = tk.Frame(self.root, bg="#3A3A3A")
#         self.company_frame.pack(pady=10, fill="both", expand=True)
#
#         self.canvas = tk.Canvas(self.company_frame, bg="#3A3A3A")
#         self.scroll_y = tk.Scrollbar(self.company_frame, orient="vertical", command=self.canvas.yview, bg="#4A90E2", troughcolor="#3A3A3A")
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
#         self.add_button = tk.Button(self.button_frame, text="Add New Company", command=self.show_form,
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
#         self.website_button = tk.Button(self.button_frame, text="Website", command=self.open_website,
#                                         bg="#FFAA00", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.website_button.pack(side="left", padx=10)
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
#     def display_companies(self):
#         for widget in self.inner_frame.winfo_children():
#             widget.destroy()
#         self.company_frames.clear()
#         self.selected_company = None
#         companies = fetch_companies()
#         num_companies = len(companies)
#         num_rows = (num_companies + 2) // 3
#         CARD_WIDTH, CARD_HEIGHT = 380, 380
#         for row in range(num_rows):
#             row_frame = tk.Frame(self.inner_frame, bg="#3A3A3A")
#             row_frame.pack(pady=10, fill="x")
#             for col in range(3):
#                 company_idx = row * 3 + col
#                 if company_idx >= num_companies:
#                     tk.Frame(row_frame, width=CARD_WIDTH, height=CARD_HEIGHT, bg="#3A3A3A").pack(side="left", padx=5)
#                     continue
#                 company = companies[company_idx]
#                 frame = tk.Frame(row_frame, relief="solid", bd=2, bg="#25253A", width=CARD_WIDTH, height=CARD_HEIGHT)
#                 frame.pack(side="left", padx=5)
#                 frame.pack_propagate(False)
#                 label_text = (
#                     f"ID: {company.get('company_id', 'N/A')}\n"
#                     f"Name: {company.get('company_name', 'N/A')}\n"
#                     f"Contact No: {company.get('contact_no', 'N/A')}\n"
#                     f"Primary Business: {company.get('primary_business', 'N/A')}\n"
#                     f"Secondary Business: {company.get('secondary_business', 'N/A')}\n"
#                     f"Since: {company.get('since', 'N/A')}\n"
#                     f"Email: {company.get('email', 'N/A')}\n"
#                     f"Website: {company.get('website', 'N/A')}"
#                 )
#                 label = tk.Label(frame, text=label_text, justify="left", anchor="nw",
#                                  font=("Roboto", 9), bg="#25253A", fg="#E0E0E0", wraplength=CARD_WIDTH - 20)
#                 label.pack(padx=5, pady=5, fill="both", expand=True)
#                 frame.bind("<Button-1>", lambda e, comp=company: self.select_company(comp))
#                 label.bind("<Button-1>", lambda e, comp=company: self.select_company(comp))
#                 self.company_frames[company['company_id']] = frame
#         self.canvas.update_idletasks()
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#
#     def select_company(self, company):
#         if self.selected_company:
#             self.company_frames[self.selected_company['company_id']].config(relief="solid", bd=2)
#         self.selected_company = company
#         self.company_frames[company['company_id']].config(relief="solid", bd=4, highlightbackground="#4A90E2")
#
#     def open_website(self):
#         if not self.selected_company:
#             messagebox.showwarning("Selection Error", "Please select a company to view their website!")
#             return
#         website_url = self.selected_company.get('website', '').strip()
#         if website_url and website_url != 'N/A':
#             try:
#                 webbrowser.open(website_url)
#             except Exception as e:
#                 messagebox.showerror("Error", f"Failed to open website: {str(e)}")
#         else:
#             messagebox.showwarning("No Website", "The selected company has no website link provided!")
#
#     def handle_update(self):
#         if not self.selected_company:
#             messagebox.showwarning("Selection Error", "Please select a company to update!")
#             return
#         self.show_update_form(self.selected_company)
#
#     def handle_delete(self):
#         if not self.selected_company:
#             messagebox.showwarning("Selection Error", "Please select a company to delete!")
#             return
#         if messagebox.askyesno("Confirm", "Are you sure you want to delete this company?"):
#             if delete_company(self.selected_company['company_id']):
#                 messagebox.showinfo("Success", "Company deleted successfully!")
#                 self.display_companies()
#             else:
#                 messagebox.showerror("Error", "Failed to delete company.")
#
#     def show_form(self):
#         self.create_form(None, "Add Company", self.submit_add)
#
#     def show_update_form(self, company):
#         update_window = tk.Toplevel(self.root)
#         update_window.title("Update Company")
#         update_window.geometry("400x500")
#         update_window.configure(bg="#2B2B2B")
#         fields = [
#             ("Company ID", company['company_id'], True),
#             ("Company Name", company['company_name'], False),
#             ("Contact No", company['contact_no'], False),
#             ("Primary Business", company['primary_business'], False),
#             ("Secondary Business", company['secondary_business'], False),
#             ("Since", company['since'], False),
#             ("Email", company['email'], False),
#             ("Website", company['website'], False)
#         ]
#         entries = {}
#         for idx, (label, value, disabled) in enumerate(fields):
#             tk.Label(update_window, text=label, bg="#2B2B2B", font=("Roboto", 10, "bold"), fg="#E0E0E0").grid(row=idx, column=0, padx=10, pady=5, sticky="w")
#             entry = tk.Entry(update_window, width=40, bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#             entry.grid(row=idx, column=1, padx=10, pady=5)
#             entry.insert(0, value or "")
#             if disabled:
#                 entry.config(state="disabled")
#             entries[label] = entry
#
#         def save_update():
#             company_data = {label: entries[label].get() for label, _, _ in fields}
#             success = update_company(
#                 company_data["Company ID"],
#                 company_data["Company Name"],
#                 company_data["Contact No"],
#                 company_data["Primary Business"],
#                 company_data["Secondary Business"],
#                 company_data["Since"],
#                 company_data["Email"],
#                 company_data["Website"]
#             )
#             if success:
#                 messagebox.showinfo("Success", "Company updated successfully!")
#                 update_window.destroy()
#                 self.display_companies()
#             else:
#                 messagebox.showerror("Error", "Failed to update company!")
#
#         tk.Button(update_window, text="Save", command=save_update, bg="#50C878", fg="#E0E0E0",
#                   font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).grid(row=len(fields), column=0, columnspan=2, pady=20)
#
#     def create_form(self, company, title, submit_action):
#         form_window = tk.Toplevel(self.root)
#         form_window.title(title)
#         form_window.geometry("400x500")
#         form_window.configure(bg="#2B2B2B")
#         fields = ["company_id", "company_name", "contact_no", "primary_business", "secondary_business", "since", "email", "website"]
#         labels = ["Company ID", "Company Name", "Contact No", "Primary Business", "Secondary Business", "Since", "Email", "Website"]
#         values = company or {}
#         entries = {}
#         for idx, (field, label) in enumerate(zip(fields, labels)):
#             tk.Label(form_window, text=label, bg="#2B2B2B", font=("Roboto", 10), fg="#E0E0E0").grid(row=idx, column=0, padx=10, pady=5, sticky="w")
#             entry = tk.Entry(form_window, width=40, bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#             entry.grid(row=idx, column=1, padx=10, pady=5)
#             entry.insert(0, values.get(field, ""))
#             if company and field == "company_id":
#                 entry.config(state="disabled")
#             entries[field] = entry
#
#         def submit():
#             data = {field: entries[field].get() for field in fields}
#             if submit_action(data):
#                 form_window.destroy()
#
#         tk.Button(form_window, text="Submit" if not company else "Update", command=submit,
#                   bg="#50C878", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).grid(row=len(fields), column=0, columnspan=2, pady=20)
#
#     def submit_add(self, data):
#         if not all([data["company_id"], data["company_name"], data["contact_no"]]):
#             messagebox.showwarning("Validation Error", "Required fields (ID, Name, Contact No) are missing!")
#             return False
#         success = insert_company_data(**data)
#         if success:
#             messagebox.showinfo("Success", "Company added successfully!")
#             self.display_companies()
#             return True
#         else:
#             messagebox.showerror("Error", "Failed to add company!")
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
#                     required_columns = ["company_id", "company_name", "contact_no"]
#                     df['since'] = pd.to_datetime(df['since']).dt.date
#                     if not all(col in df.columns for col in required_columns):
#                         messagebox.showerror("Error", "Excel file must contain 'company_id', 'company_name', and 'contact_no' columns!")
#                         return
#                     companies = df.to_dict(orient="records")
#                     success = insert_bulk_company_data(companies)
#                     if success:
#                         messagebox.showinfo("Success", "All data entered successfully!")
#                         bulk_window.destroy()
#                         self.display_companies()
#                     else:
#                         messagebox.showerror("Error", "Failed to add bulk data!")
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
# def company(root=None, prev_window=None):
#     app = CompanyApp(root, prev_window)
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     company(root)
#     root.mainloop()



import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser
import pandas as pd
from db import fetch_companies, insert_company_data, delete_company, update_company, insert_bulk_company_data

class CompanyApp:
    def __init__(self, root, prev_window=None):
        if prev_window:
            prev_window.destroy()
        self.root = tk.Toplevel(root)
        self.root.title("Company Management")
        self.root.configure(bg="#1a1a1a")
        self.root.state("zoomed")
        self.selected_company = None
        self.company_frames = {}
        self.setup_ui()
        self.display_companies()

    def setup_ui(self):
        self.company_frame = tk.Frame(self.root, bg="#333333")
        self.company_frame.pack(pady=10, fill="both", expand=True)

        self.canvas = tk.Canvas(self.company_frame, bg="#333333")
        self.scroll_y = tk.Scrollbar(self.company_frame, orient="vertical", command=self.canvas.yview, bg="#69dbc8", troughcolor="#5192ed")
        self.scroll_y.pack(side="right", fill="y")

        self.inner_frame = tk.Frame(self.canvas, bg="#333333")
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.button_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.button_frame.pack(pady=10, fill="x")

        button_style = {
            "font": ("Times New Roman", 12, "bold"),
            "fg": "black",
            "bg": "#69dbc8",
            "relief": "raised",
            "bd": 3,
            "padx": 10,
            "pady": 5,
            "activebackground": "#54b0a0"
        }

        def create_button(parent, text, command):
            btn = tk.Button(parent, text=text, command=command, **button_style)
            btn.pack(side="left", padx=10)
            btn.bind("<Enter>", lambda e: btn.config(bg="#54b0a0"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#69dbc8"))
            return btn

        def create_delete_button(parent, text, command):
            btn = tk.Button(parent, text=text, command=command, font=("Times New Roman", 12, "bold"), fg="white", bg="#ff0000", relief="raised", bd=3, padx=10, pady=5, activebackground="#cc0000")
            btn.pack(side="left", padx=10)
            btn.bind("<Enter>", lambda e: btn.config(bg="#cc0000"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#ff0000"))
            return btn

        def create_website_button(parent, text, command):
            btn = tk.Button(parent, text=text, command=command, font=("Times New Roman", 12, "bold"), fg="white", bg="#5192ed", relief="raised", bd=3, padx=10, pady=5, activebackground="#406fb3")
            btn.pack(side="left", padx=10)
            btn.bind("<Enter>", lambda e: btn.config(bg="#406fb3"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#5192ed"))
            return btn

        self.add_button = create_button(self.button_frame, "Add New Company", self.show_form)
        self.update_button = create_button(self.button_frame, "Update", self.handle_update)
        self.delete_button = create_delete_button(self.button_frame, "Delete", self.handle_delete)
        self.website_button = create_website_button(self.button_frame, "Website", self.open_website)

        self.bulk_data_button = create_button(self.button_frame, "Bulk Data", self.show_bulk_data_form)
        self.back_button = create_delete_button(self.button_frame, "Back", lambda: self.back_to_dashboard())

    def back_to_dashboard(self):
        from dashboard import open_dashboard
        self.root.destroy()
        open_dashboard(root=self.root.master, prev_window=self.root)

    def display_companies(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.company_frames.clear()
        self.selected_company = None
        companies = fetch_companies()
        num_companies = len(companies)
        num_rows = (num_companies + 2) // 3
        CARD_WIDTH, CARD_HEIGHT = 380, 380
        for row in range(num_rows):
            row_frame = tk.Frame(self.inner_frame, bg="#333333")
            row_frame.pack(pady=10, fill="x")
            for col in range(3):
                company_idx = row * 3 + col
                if company_idx >= num_companies:
                    tk.Frame(row_frame, width=CARD_WIDTH, height=CARD_HEIGHT, bg="#333333").pack(side="left", padx=5)
                    continue
                company = companies[company_idx]
                frame = tk.Frame(row_frame, relief="solid", bd=2, bg="#404040", width=CARD_WIDTH, height=CARD_HEIGHT)
                frame.pack(side="left", padx=5)
                frame.pack_propagate(False)
                label_text = (
                    f"ID: {company.get('company_id', 'N/A')}\n"
                    f"Name: {company.get('company_name', 'N/A')}\n"
                    f"Contact No: {company.get('contact_no', 'N/A')}\n"
                    f"Primary Business: {company.get('primary_business', 'N/A')}\n"
                    f"Secondary Business: {company.get('secondary_business', 'N/A')}\n"
                    f"Since: {company.get('since', 'N/A')}\n"
                    f"Email: {company.get('email', 'N/A')}\n"
                    f"Website: {company.get('website', 'N/A')}"
                )
                label = tk.Label(frame, text=label_text, justify="left", anchor="nw",
                                 font=("Arial", 9), bg="#404040", fg="white", wraplength=CARD_WIDTH - 20)
                label.pack(padx=5, pady=5, fill="both", expand=True)

                frame.bind("<Button-1>", lambda e, comp=company: self.select_company(comp))
                label.bind("<Button-1>", lambda e, comp=company: self.select_company(comp))
                self.company_frames[company['company_id']] = frame
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def select_company(self, company):
        if self.selected_company:
            prev_frame = self.company_frames[self.selected_company['company_id']]
            prev_label = prev_frame.winfo_children()[0]
            prev_frame.config(bg="#404040", relief="solid", bd=2)
            prev_label.config(bg="#404040")
        self.selected_company = company
        selected_frame = self.company_frames[company['company_id']]
        selected_label = selected_frame.winfo_children()[0]
        selected_frame.config(bg="#5192ed", relief="solid", bd=4)
        selected_label.config(bg="#5192ed")

    def open_website(self):
        if not self.selected_company:
            messagebox.showwarning("Selection Error", "Please select a company to view their website!")
            return
        website_url = self.selected_company.get('website', '').strip()
        if website_url and website_url != 'N/A':
            try:
                webbrowser.open(website_url)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open website: {str(e)}")
        else:
            messagebox.showwarning("No Website", "The selected company has no website link provided!")

    def handle_update(self):
        if not self.selected_company:
            messagebox.showwarning("Selection Error", "Please select a company to update!")
            return
        self.show_update_form(self.selected_company)

    def handle_delete(self):
        if not self.selected_company:
            messagebox.showwarning("Selection Error", "Please select a company to delete!")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this company?"):
            if delete_company(self.selected_company['company_id']):
                messagebox.showinfo("Success", "Company deleted successfully!")
                self.display_companies()
            else:
                messagebox.showerror("Error", "Failed to delete company.")

    def show_form(self):
        self.create_form(None, "Add Company", self.submit_add)

    def show_update_form(self, company):
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Company")
        update_window.geometry("400x500")
        update_window.configure(bg="#1a1a1a")
        fields = [
            ("Company ID", company['company_id'], True),
            ("Company Name", company['company_name'], False),
            ("Contact No", company['contact_no'], False),
            ("Primary Business", company['primary_business'], False),
            ("Secondary Business", company['secondary_business'], False),
            ("Since", company['since'], False),
            ("Email", company['email'], False),
            ("Website", company['website'], False)
        ]
        entries = {}
        for idx, (label, value, disabled) in enumerate(fields):
            tk.Label(update_window, text=label, bg="#1a1a1a", font=("Arial", 10), fg="white").grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(update_window, width=40, bg="#333333", fg="white", insertbackground="white")
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entry.insert(0, value or "")
            if disabled:
                entry.config(state="disabled", bg="#404040")
            entries[label] = entry

        def save_update():
            company_data = {label: entries[label].get() for label, _, _ in fields}
            success = update_company(
                company_data["Company ID"],
                company_data["Company Name"],
                company_data["Contact No"],
                company_data["Primary Business"],
                company_data["Secondary Business"],
                company_data["Since"],
                company_data["Email"],
                company_data["Website"]
            )
            if success:
                messagebox.showinfo("Success", "Company updated successfully!")
                update_window.destroy()
                self.display_companies()
            else:
                messagebox.showerror("Error", "Failed to update company!")

        tk.Button(update_window, text="Save", command=save_update, bg="#69dbc8", fg="black", font=("Times New Roman", 12, "bold"), relief="raised", bd=3, padx=10, pady=5, activebackground="#54b0a0").grid(row=len(fields), column=0, columnspan=2, pady=20)

    def create_form(self, company, title, submit_action):
        form_window = tk.Toplevel(self.root)
        form_window.title(title)
        form_window.geometry("400x500")
        form_window.configure(bg="#1a1a1a")
        fields = ["company_id", "company_name", "contact_no", "primary_business", "secondary_business", "since", "email", "website"]
        labels = ["Company ID", "Company Name", "Contact No", "Primary Business", "Secondary Business", "Since", "Email", "Website"]
        values = company or {}
        entries = {}
        for idx, (field, label) in enumerate(zip(fields, labels)):
            tk.Label(form_window, text=label, bg="#1a1a1a", font=("Arial", 10), fg="white").grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(form_window, width=40, bg="#333333", fg="white", insertbackground="white")
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entry.insert(0, values.get(field, ""))
            if company and field == "company_id":
                entry.config(state="disabled", bg="#404040")
            entries[field] = entry

        def submit():
            data = {field: entries[field].get() for field in fields}
            if submit_action(data):
                form_window.destroy()

        tk.Button(form_window, text="Submit" if not company else "Update", command=submit, bg="#69dbc8", fg="black", font=("Times New Roman", 12, "bold"), relief="raised", bd=3, padx=10, pady=5, activebackground="#54b0a0").grid(row=len(fields), column=0, columnspan=2, pady=20)

    def submit_add(self, data):
        if not all([data["company_id"], data["company_name"], data["contact_no"]]):
            messagebox.showwarning("Validation Error", "Required fields (ID, Name, Contact No) are missing!")
            return False
        success = insert_company_data(**data)
        if success:
            messagebox.showinfo("Success", "Company added successfully!")
            self.display_companies()
            return True
        else:
            messagebox.showerror("Error", "Failed to add company!")
            return False

    def show_bulk_data_form(self):
        bulk_window = tk.Toplevel(self.root)
        bulk_window.title("Bulk Data Upload")
        bulk_window.geometry("400x200")
        bulk_window.configure(bg="#1a1a1a")

        tk.Label(bulk_window, text="Upload Excel File", bg="#1a1a1a", font=("Arial", 12, "bold"), fg="#69dbc8").pack(pady=10)
        file_label = tk.Label(bulk_window, text="No file selected", bg="#1a1a1a", fg="white")
        file_label.pack(pady=5)

        def select_file():
            file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
            if file_path:
                file_label.config(text=file_path)
                bulk_window.file_path = file_path

        tk.Button(bulk_window, text="Browse", command=select_file, bg="#69dbc8", fg="black", font=("Times New Roman", 12, "bold"), relief="raised", bd=3, padx=10, pady=5, activebackground="#54b0a0").pack(pady=10)

        def submit_bulk():
            if hasattr(bulk_window, 'file_path'):
                try:
                    df = pd.read_excel(bulk_window.file_path)
                    required_columns = ["company_id", "company_name", "contact_no"]
                    df['since'] = pd.to_datetime(df['since']).dt.date
                    if not all(col in df.columns for col in required_columns):
                        messagebox.showerror("Error", "Excel file must contain 'company_id', 'company_name', and 'contact_no' columns!")
                        return
                    companies = df.to_dict(orient="records")
                    success = insert_bulk_company_data(companies)
                    if success:
                        messagebox.showinfo("Success", "All data entered successfully!")
                        bulk_window.destroy()
                        self.display_companies()
                    else:
                        messagebox.showerror("Error", "Failed to add bulk data!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to process file: {str(e)}")
            else:
                messagebox.showwarning("Selection Error", "Please select an Excel file!")

        tk.Button(bulk_window, text="Submit", command=submit_bulk, bg="#69dbc8", fg="black", font=("Times New Roman", 12, "bold"), relief="raised", bd=3, padx=10, pady=5, activebackground="#54b0a0").pack(side="left", padx=20, pady=20)
        tk.Button(bulk_window, text="Back", command=bulk_window.destroy, bg="#ff0000", fg="white", font=("Times New Roman", 12, "bold"), relief="raised", bd=3, padx=10, pady=5, activebackground="#cc0000").pack(side="right", padx=20, pady=20)

def company(root=None, prev_window=None):
    app = CompanyApp(root, prev_window)

if __name__ == "__main__":
    root = tk.Tk()
    company(root)
    root.mainloop()