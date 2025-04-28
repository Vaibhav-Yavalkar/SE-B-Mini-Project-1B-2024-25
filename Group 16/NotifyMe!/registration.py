# # from tkinter import Toplevel, Label, Button, messagebox
# # from tkinter import Entry
# # import tkinter as tk
# # import re
# # from db import save_registration_data
# #
# # class PlaceholderEntry(Entry):
# #     def __init__(self, parent, placeholder, *args, **kwargs):
# #         super().__init__(parent, *args, **kwargs)
# #         self.placeholder = placeholder
# #         self.placeholder_color = "grey"
# #         self.default_fg_color = "#E0E0E0"
# #         self.insert(0, placeholder)
# #         self.config(fg=self.placeholder_color, bg="#2D2D44", insertbackground="#00D4FF")
# #         self.bind("<FocusIn>", self.remove_placeholder)
# #         self.bind("<FocusOut>", self.add_placeholder)
# #
# #     def remove_placeholder(self, event=None):
# #         if self.get() == self.placeholder:
# #             self.delete(0, "end")
# #             self.config(fg=self.default_fg_color)
# #
# #     def add_placeholder(self, event=None):
# #         if not self.get().strip():
# #             self.insert(0, self.placeholder)
# #             self.config(fg=self.placeholder_color)
# #
# # def rwindow(root=None, prev_window=None):
# #     if prev_window:
# #         prev_window.destroy()
# #     mywindow = tk.Toplevel(root)
# #     mywindow.title("Registration")
# #     mywindow.configure(bg="#1E1E2F")
# #     mywindow.state('zoomed')
# #
# #     def on_submit():
# #         name = Name.get().strip()
# #         email = Email.get().strip()
# #         username = Username.get().strip()
# #         password = Password.get().strip()
# #         if name == "Enter Name":
# #             name = ""
# #         if email == "Enter Email":
# #             email = ""
# #         if username == "Enter Username":
# #             username = ""
# #         if password == "Enter Password":
# #             password = ""
# #         if not name or not email or not username or not password:
# #             messagebox.showwarning("Validation Error", "All fields are required!")
# #             return
# #         if not name.replace(" ", "").isalpha():
# #             messagebox.showwarning("Validation Error", "Name must contain only letters.")
# #             return
# #         if "@" not in email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
# #             messagebox.showwarning("Validation Error", "Invalid email! Email must contain '@' and a valid domain.")
# #             return
# #         if len(password) < 8:
# #             messagebox.showwarning("Validation Error", "Password must be at least 8 characters long.")
# #             return
# #         if not any(char.isupper() for char in password):
# #             messagebox.showwarning("Validation Error", "Password must contain at least one uppercase letter.")
# #             return
# #         if not any(char in "!@#$%^&*()_+={}[]|:;,.<>?/~" for char in password):
# #             messagebox.showwarning("Validation Error", "Password must contain at least one special character.")
# #             return
# #         save_registration_data(name, email, username, password)
# #         messagebox.showinfo("Success", "Registration Successful!")
# #         mywindow.destroy()
# #         if root:
# #             root.deiconify()
# #
# #     Label(mywindow, text="Name:", font=("Roboto", 16), bg="#1E1E2F", fg="#E0E0E0").place(x=100, y=100)
# #     Name = PlaceholderEntry(mywindow, "Enter Name", font=("Roboto", 16))
# #     Name.place(x=250, y=105)
# #
# #     Label(mywindow, text="Email:", font=("Roboto", 16), bg="#1E1E2F", fg="#E0E0E0").place(x=100, y=200)
# #     Email = PlaceholderEntry(mywindow, "Enter Email", font=("Roboto", 16))
# #     Email.place(x=250, y=205)
# #
# #     Label(mywindow, text="Password:", font=("Roboto", 16), bg="#1E1E2F", fg="#E0E0E0").place(x=100, y=300)
# #     Password = PlaceholderEntry(mywindow, "Enter Password", font=("Roboto", 16), show="*")
# #     Password.place(x=250, y=305)
# #
# #     Label(mywindow, text="Username:", font=("Roboto", 16), bg="#1E1E2F", fg="#E0E0E0").place(x=100, y=400)
# #     Username = PlaceholderEntry(mywindow, "Enter Username", font=("Roboto", 16))
# #     Username.place(x=250, y=405)
# #
# #     Button(mywindow, text="Submit", width=20, bg="#39FF14", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", command=on_submit).place(x=100, y=500)
# #     Button(mywindow, text="Back", width=20, bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", command=lambda: back_to_main(mywindow)).place(x=400, y=500)
# #
# #     def back_to_main(window):
# #         window.destroy()
# #         if root:
# #             root.deiconify()
# #
# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     rwindow(root)
# #     root.mainloop()
#
#
# from tkinter import Toplevel, Label, Button, messagebox
# from tkinter import Entry
# import tkinter as tk
# import re
# from db import save_registration_data
#
# class PlaceholderEntry(Entry):
#     def __init__(self, parent, placeholder, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#         self.placeholder = placeholder
#         self.placeholder_color = "grey"
#         self.default_fg_color = "#E0E0E0"
#         self.insert(0, placeholder)
#         self.config(fg=self.placeholder_color, bg="#3A3A3A", insertbackground="#4A90E2")
#         self.bind("<FocusIn>", self.remove_placeholder)
#         self.bind("<FocusOut>", self.add_placeholder)
#
#     def remove_placeholder(self, event=None):
#         if self.get() == self.placeholder:
#             self.delete(0, "end")
#             self.config(fg=self.default_fg_color)
#
#     def add_placeholder(self, event=None):
#         if not self.get().strip():
#             self.insert(0, self.placeholder)
#             self.config(fg=self.placeholder_color)
#
# def rwindow(root=None, prev_window=None):
#     if prev_window:
#         prev_window.destroy()
#     mywindow = tk.Toplevel(root)
#     mywindow.title("Registration")
#     mywindow.configure(bg="#2B2B2B")
#     mywindow.state('zoomed')
#
#     def on_submit():
#         name = Name.get().strip()
#         email = Email.get().strip()
#         username = Username.get().strip()
#         password = Password.get().strip()
#         if name == "Enter Name":
#             name = ""
#         if email == "Enter Email":
#             email = ""
#         if username == "Enter Username":
#             username = ""
#         if password == "Enter Password":
#             password = ""
#         if not name or not email or not username or not password:
#             messagebox.showwarning("Validation Error", "All fields are required!")
#             return
#         if not name.replace(" ", "").isalpha():
#             messagebox.showwarning("Validation Error", "Name must contain only letters.")
#             return
#         if "@" not in email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
#             messagebox.showwarning("Validation Error", "Invalid email! Email must contain '@' and a valid domain.")
#             return
#         if len(password) < 8:
#             messagebox.showwarning("Validation Error", "Password must be at least 8 characters long.")
#             return
#         if not any(char.isupper() for char in password):
#             messagebox.showwarning("Validation Error", "Password must contain at least one uppercase letter.")
#             return
#         if not any(char in "!@#$%^&*()_+={}[]|:;,.<>?/~" for char in password):
#             messagebox.showwarning("Validation Error", "Password must contain at least one special character.")
#             return
#         save_registration_data(name, email, username, password)
#         messagebox.showinfo("Success", "Registration Successful!")
#         mywindow.destroy()
#         if root:
#             root.deiconify()
#
#     Label(mywindow, text="Name:", font=("Roboto", 16), bg="#2B2B2B", fg="#E0E0E0").place(x=100, y=100)
#     Name = PlaceholderEntry(mywindow, "Enter Name", font=("Roboto", 16))
#     Name.place(x=250, y=105)
#
#     Label(mywindow, text="Email:", font=("Roboto", 16), bg="#2B2B2B", fg="#E0E0E0").place(x=100, y=200)
#     Email = PlaceholderEntry(mywindow, "Enter Email", font=("Roboto", 16))
#     Email.place(x=250, y=205)
#
#     Label(mywindow, text="Password:", font=("Roboto", 16), bg="#2B2B2B", fg="#E0E0E0").place(x=100, y=300)
#     Password = PlaceholderEntry(mywindow, "Enter Password", font=("Roboto", 16), show="*")
#     Password.place(x=250, y=305)
#
#     Label(mywindow, text="Username:", font=("Roboto", 16), bg="#2B2B2B", fg="#E0E0E0").place(x=100, y=400)
#     Username = PlaceholderEntry(mywindow, "Enter Username", font=("Roboto", 16))
#     Username.place(x=250, y=405)
#
#     Button(mywindow, text="Submit", width=20, bg="#50C878", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", command=on_submit).place(x=100, y=500)
#     Button(mywindow, text="Back", width=20, bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", command=lambda: back_to_main(mywindow)).place(x=400, y=500)
#
#     def back_to_main(window):
#         window.destroy()
#         if root:
#             root.deiconify()
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     rwindow(root)
#     root.mainloop()



# from tkinter import Toplevel, Label, Button, messagebox
# from tkinter import Entry
# import tkinter as tk
# import re
# from db import save_registration_data
#
# class PlaceholderEntry(Entry):
#     def __init__(self, parent, placeholder, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#         self.placeholder = placeholder
#         self.placeholder_color = "grey"
#         self.default_fg_color = "#E0E0E0"
#         self.insert(0, placeholder)
#         self.config(fg=self.placeholder_color, bg="#3A3A3A", insertbackground="#4A90E2")
#         self.bind("<FocusIn>", self.remove_placeholder)
#         self.bind("<FocusOut>", self.add_placeholder)
#
#     def remove_placeholder(self, event=None):
#         if self.get() == self.placeholder:
#             self.delete(0, "end")
#             self.config(fg=self.default_fg_color)
#
#     def add_placeholder(self, event=None):
#         if not self.get().strip():
#             self.insert(0, self.placeholder)
#             self.config(fg=self.placeholder_color)
#
# def rwindow(root=None, prev_window=None):
#     if prev_window:
#         prev_window.destroy()
#     mywindow = tk.Toplevel(root)
#     mywindow.title("Registration")
#     mywindow.configure(bg="#2B2B2B")
#     mywindow.state('zoomed')
#
#     Label(mywindow, text="Create Your NotifyMe Account", font=("Roboto", 36, "bold"), fg="#E0E0E0", bg="#2B2B2B").place(relx=0.5, y=50, anchor="center")
#     Label(mywindow, text="Enter your details below", font=("Roboto", 20), fg="#E0E0E0", bg="#2B2B2B").place(relx=0.5, y=100, anchor="center")
#
#     def on_submit():
#         name = Name.get().strip()
#         email = Email.get().strip()
#         username = Username.get().strip()
#         password = Password.get().strip()
#         if name == "Enter Name":
#             name = ""
#         if email == "Enter Email":
#             email = ""
#         if username == "Enter Username":
#             username = ""
#         if password == "Enter Password":
#             password = ""
#         if not name or not email or not username or not password:
#             messagebox.showwarning("Validation Error", "All fields are required!")
#             return
#         if not name.replace(" ", "").isalpha():
#             messagebox.showwarning("Validation Error", "Name must contain only letters.")
#             return
#         if "@" not in email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
#             messagebox.showwarning("Validation Error", "Invalid email! Email must contain '@' and a valid domain.")
#             return
#         if len(password) < 8:
#             messagebox.showwarning("Validation Error", "Password must be at least 8 characters long.")
#             return
#         if not any(char.isupper() for char in password):
#             messagebox.showwarning("Validation Error", "Password must contain at least one uppercase letter.")
#             return
#         if not any(char in "!@#$%^&*()_+={}[]|:;,.<>?/~" for char in password):
#             messagebox.showwarning("Validation Error", "Password must contain at least one special character.")
#             return
#         save_registration_data(name, email, username, password)
#         messagebox.showinfo("Success", "Registration Successful!")
#         mywindow.destroy()
#         if root:
#             root.deiconify()
#
#     Label(mywindow, text="Name:", font=("Roboto", 16), bg="#2B2B2B", fg="#E0E0E0").place(relx=0.5, y=150, anchor="center")
#     Name = PlaceholderEntry(mywindow, "Enter Name", font=("Roboto", 16))
#     Name.place(relx=0.5, y=190, anchor="center")
#
#     Label(mywindow, text="Email:", font=("Roboto", 16), bg="#2B2B2B", fg="#E0E0E0").place(relx=0.5, y=250, anchor="center")
#     Email = PlaceholderEntry(mywindow, "Enter Email", font=("Roboto", 16))
#     Email.place(relx=0.5, y=290, anchor="center")
#
#     Label(mywindow, text="Password:", font=("Roboto", 16), bg="#2B2B2B", fg="#E0E0E0").place(relx=0.5, y=350, anchor="center")
#     Password = PlaceholderEntry(mywindow, "Enter Password", font=("Roboto", 16), show="*")
#     Password.place(relx=0.5, y=390, anchor="center")
#
#     Label(mywindow, text="Username:", font=("Roboto", 16), bg="#2B2B2B", fg="#E0E0E0").place(relx=0.5, y=450, anchor="center")
#     Username = PlaceholderEntry(mywindow, "Enter Username", font=("Roboto", 16))
#     Username.place(relx=0.5, y=490, anchor="center")
#
#     Button(mywindow, text="Sign Up", width=20, bg="#50C878", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", command=on_submit).place(relx=0.4, y=550, anchor="center")
#     Button(mywindow, text="Back", width=20, bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", command=lambda: back_to_main(mywindow)).place(relx=0.6, y=550, anchor="center")
#
#     def back_to_main(window):
#         window.destroy()
#         if root:
#             root.deiconify()
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     rwindow(root)
#     root.mainloop()


from tkinter import Toplevel, Label, Button, messagebox, Entry
import re
from db import save_registration_data

class PlaceholderEntry(Entry):
    def __init__(self, parent, placeholder, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = "#666666"  # Medium grey from Code 1
        self.default_fg_color = "white"  # White text from Code 1

        self.insert(0, placeholder)
        self.config(fg=self.placeholder_color)

        self.bind("<FocusIn>", self.remove_placeholder)
        self.bind("<FocusOut>", self.add_placeholder)

    def remove_placeholder(self, event=None):
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self.config(fg=self.default_fg_color)

    def add_placeholder(self, event=None):
        if not self.get().strip():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)

class RegistrationUI(Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Sign Up - NotifyMe")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.configure(bg="#1a1a1a")  # Black background from Code 1
        self.state('zoomed')

        container = Label(self, bg="#1a1a1a")  # Black from Code 1
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Title and subtitle
        title_label = Label(container, text="Create Your NotifyMe Account",
                                    font=("Calibri", 28, "bold"), fg="#69dbc8", bg="#1a1a1a")  # Teal text from Code 1
        subtitle_label = Label(container, text="Enter your details below",
                                       font=("Calibri", 16), fg="#ffffff", bg="#1a1a1a")  # White text from Code 1
        title_label.pack(pady=10)
        subtitle_label.pack(pady=5)

        # Form fields
        self.create_form_entry(container, "Full Name:", "name", "Enter Name")
        self.create_form_entry(container, "Email Address:", "email", "Enter Email")
        self.create_form_entry(container, "Username:", "username", "Enter Username")
        self.create_form_entry(container, "Password:", "password", "Enter Password", show="*")

        # Buttons Frame
        button_frame = Label(container, bg="#1a1a1a")  # Black from Code 1
        button_frame.pack(pady=20)

        # Submit Button
        submit_button = Button(button_frame, text="Sign Up", font=("Calibri", 16, "bold"),
                                    fg="black", bg="#41d627", width=14, height=2,  # Green from Code 1
                                    borderwidth=2, relief="flat", command=self.on_submit,
                                    cursor="hand2", activebackground="#33aa1e")  # Darker green for hover
        submit_button.pack(side="left", padx=20)

        # Back Button
        back_button = Button(button_frame, text="Back", font=("Calibri", 16, "bold"),
                                  fg="black", bg="#69dbc8", width=14, height=2,  # Teal from Code 1
                                  borderwidth=2, relief="flat", command=self.destroy,
                                  cursor="hand2", activebackground="#54b0a0")  # Darker teal for hover
        back_button.pack(side="left", padx=20)

        # Add hover effects
        for btn, hover_color in [(submit_button, "#33aa1e"), (back_button, "#54b0a0")]:
            btn.bind("<Enter>", lambda e, b=btn, c=hover_color: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=btn.cget("bg"): b.config(bg=c))

    def create_form_entry(self, parent, label_text, field_name, placeholder, show=""):
        frame = Label(parent, bg="#1a1a1a")  # Black from Code 1
        frame.pack(pady=10)

        label = Label(frame, text=label_text, font=("Calibri", 14),
                            fg="#ffffff", bg="#1a1a1a", anchor="w")  # White text from Code 1
        label.pack(anchor="w")

        entry = PlaceholderEntry(frame, placeholder, font=("Calibri", 14),
                                        width=30, bg="#333333", fg="white", bd=2,  # Dark grey from Code 1
                                        relief="flat", show=show, insertbackground="white")
        entry.pack(ipady=5)
        setattr(self, f"{field_name}_entry", entry)

    def on_submit(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Remove placeholders before validation
        if name == "Enter Name":
            name = ""
        if email == "Enter Email":
            email = ""
        if username == "Enter Username":
            username = ""
        if password == "Enter Password":
            password = ""

        # Validation: Check if any field is empty
        if not name or not email or not username or not password:
            messagebox.showwarning("Validation Error", "All fields are required!")
            return

        # Name Validation: Only alphabetic characters allowed
        if not name.replace(" ", "").isalpha():
            messagebox.showwarning("Validation Error", "Name must contain only letters.")
            return

        # Email Validation
        if "@" not in email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showwarning("Validation Error", "Invalid email! Email must contain '@' and a valid domain.")
            return

        # Password Validation
        if len(password) < 8:
            messagebox.showwarning("Validation Error", "Password must be at least 8 characters long.")
            return
        if not any(char.isupper() for char in password):
            messagebox.showwarning("Validation Error", "Password must contain at least one uppercase letter.")
            return
        if not any(char in "!@#$%^&*()_+={}[]|:;,.<>?/~" for char in password):
            messagebox.showwarning("Validation Error", "Password must contain at least one special character.")
            return

        # Save user registration data
        save_registration_data(name, email, username, password)
        messagebox.showinfo("Success", "Registration Successful!")
        self.destroy()

def rwindow(root):
    RegistrationUI(root)