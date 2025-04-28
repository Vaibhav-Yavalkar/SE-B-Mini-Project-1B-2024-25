# # from tkinter import Toplevel, Label, Button, messagebox, Text
# # import tkinter as tk
# # from tkinter import Entry
# # from db import validate_login
# #
# # class PlaceholderEntry(Entry):
# #     def __init__(self, parent, placeholder, *args, **kwargs):
# #         super().__init__(parent, *args, **kwargs)
# #         self.placeholder = placeholder
# #         self.placeholder_color = "black"
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
# # def lwindow(root=None, prev_window=None):
# #     if prev_window:
# #         prev_window.destroy()
# #     newwindow = tk.Toplevel(root)
# #     newwindow.title("Login")
# #     newwindow.configure(bg="#1E1E2F")
# #     newwindow.state('zoomed')
# #
# #     def on_login():
# #         from dashboard import open_dashboard
# #         entered_username = Username.get().strip()
# #         entered_password = Password.get().strip()
# #         if not entered_username or not entered_password:
# #             messagebox.showwarning("Validation Error", "Username and Password are required!")
# #             return
# #         user = validate_login(entered_username, entered_password)
# #         if user:
# #             messagebox.showinfo("Login Success", "Login successful!")
# #             is_admin = entered_username == "sid@123445" and entered_password == "sid@12345"
# #             newwindow.destroy()
# #             open_dashboard(is_admin=is_admin, root=root, prev_window=newwindow)
# #         else:
# #             messagebox.showerror("Login Failed", "Invalid username or password.")
# #
# #     Label(newwindow, text="Username:", font=("Roboto", 16), fg="#E0E0E0", bg="#1E1E2F").place(x=100, y=100)
# #     Username = Entry(newwindow, width=20, font=("Roboto", 16), bg="#2D2D44", fg="#E0E0E0", insertbackground="#00D4FF")
# #     Username.place(x=250, y=105)
# #
# #     Label(newwindow, text="Password:", font=("Roboto", 16), fg="#E0E0E0", bg="#1E1E2F").place(x=100, y=200)
# #     Password = Entry(newwindow, width=20, font=("Roboto", 16), show="*", bg="#2D2D44", fg="#E0E0E0", insertbackground="#00D4FF")
# #     Password.place(x=250, y=205)
# #
# #     Button(newwindow, text="Submit", width=20, bg="#39FF14", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", command=on_login).place(x=100, y=300)
# #     Button(newwindow, text="Back", width=20, bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", command=lambda: back_to_main(newwindow)).place(x=400, y=300)
# #
# #     def back_to_main(window):
# #         window.destroy()
# #         if root:
# #             root.deiconify()
# #
# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     lwindow(root)
# #     root.mainloop()
#
#
# from tkinter import Toplevel, Label, Button, messagebox, Text
# import tkinter as tk
# from tkinter import Entry
# from db import validate_login
#
# class PlaceholderEntry(Entry):
#     def __init__(self, parent, placeholder, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#         self.placeholder = placeholder
#         self.placeholder_color = "black"
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
# def lwindow(root=None, prev_window=None):
#     if prev_window:
#         prev_window.destroy()
#     newwindow = tk.Toplevel(root)
#     newwindow.title("Login")
#     newwindow.configure(bg="#2B2B2B")
#     newwindow.state('zoomed')
#
#     def on_login():
#         from dashboard import open_dashboard
#         entered_username = Username.get().strip()
#         entered_password = Password.get().strip()
#         if not entered_username or not entered_password:
#             messagebox.showwarning("Validation Error", "Username and Password are required!")
#             return
#         user = validate_login(entered_username, entered_password)
#         if user:
#             messagebox.showinfo("Login Success", "Login successful!")
#             is_admin = entered_username == "sid@123445" and entered_password == "sid@12345"
#             newwindow.destroy()
#             open_dashboard(is_admin=is_admin, root=root, prev_window=newwindow)
#         else:
#             messagebox.showerror("Login Failed", "Invalid username or password.")
#
#     Label(newwindow, text="Username:", font=("Roboto", 16), fg="#E0E0E0", bg="#2B2B2B").place(x=100, y=100)
#     Username = Entry(newwindow, width=20, font=("Roboto", 16), bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#     Username.place(x=250, y=105)
#
#     Label(newwindow, text="Password:", font=("Roboto", 16), fg="#E0E0E0", bg="#2B2B2B").place(x=100, y=200)
#     Password = Entry(newwindow, width=20, font=("Roboto", 16), show="*", bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#     Password.place(x=250, y=205)
#
#     Button(newwindow, text="Submit", width=20, bg="#50C878", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", command=on_login).place(x=100, y=300)
#     Button(newwindow, text="Back", width=20, bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", command=lambda: back_to_main(newwindow)).place(x=400, y=300)
#
#     def back_to_main(window):
#         window.destroy()
#         if root:
#             root.deiconify()
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     lwindow(root)
#     root.mainloop()



# from tkinter import Toplevel, Label, Button, messagebox, Text
# import tkinter as tk
# from tkinter import Entry
# from db import validate_login
#
# class PlaceholderEntry(Entry):
#     def __init__(self, parent, placeholder, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#         self.placeholder = placeholder
#         self.placeholder_color = "black"
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
# def lwindow(root=None, prev_window=None):
#     if prev_window:
#         prev_window.destroy()
#     newwindow = tk.Toplevel(root)
#     newwindow.title("Login")
#     newwindow.configure(bg="#2B2B2B")
#     newwindow.state('zoomed')
#
#     Label(newwindow, text="Login to NotifyMe", font=("Roboto", 36, "bold"), fg="#E0E0E0", bg="#2B2B2B").place(relx=0.5, y=50, anchor="center")
#     Label(newwindow, text="Secure Business Login", font=("Roboto", 20), fg="#E0E0E0", bg="#2B2B2B").place(relx=0.5, y=100, anchor="center")
#
#     def on_login():
#         from dashboard import open_dashboard
#         entered_username = Username.get().strip()
#         entered_password = Password.get().strip()
#         if not entered_username or not entered_password:
#             messagebox.showwarning("Validation Error", "Username and Password are required!")
#             return
#         user = validate_login(entered_username, entered_password)
#         if user:
#             messagebox.showinfo("Login Success", "Login successful!")
#             is_admin = entered_username == "sid@123445" and entered_password == "sid@12345"
#             newwindow.destroy()
#             open_dashboard(is_admin=is_admin, root=root, prev_window=newwindow)
#         else:
#             messagebox.showerror("Login Failed", "Invalid username or password.")
#
#     Label(newwindow, text="Username:", font=("Roboto", 16), fg="#E0E0E0", bg="#2B2B2B").place(relx=0.5, y=150, anchor="center")
#     Username = Entry(newwindow, width=20, font=("Roboto", 16), bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#     Username.place(relx=0.5, y=190, anchor="center")
#
#     Label(newwindow, text="Password:", font=("Roboto", 16), fg="#E0E0E0", bg="#2B2B2B").place(relx=0.5, y=250, anchor="center")
#     Password = Entry(newwindow, width=20, font=("Roboto", 16), show="*", bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#     Password.place(relx=0.5, y=290, anchor="center")
#
#     Button(newwindow, text="Login", width=20, bg="#50C878", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", command=on_login).place(relx=0.4, y=350, anchor="center")
#     Button(newwindow, text="Back", width=20, bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", command=lambda: back_to_main(newwindow)).place(relx=0.6, y=350, anchor="center")
#
#     def back_to_main(window):
#         window.destroy()
#         if root:
#             root.deiconify()
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     lwindow(root)
#     root.mainloop()


# import tkinter as tk
# from tkinter import Entry, Label, Button, messagebox
# from db import validate_login
#
#
# class PlaceholderEntry(Entry):
#     def __init__(self, parent, placeholder, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#         self.placeholder = placeholder
#         self.placeholder_color = "black"
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
#
# def lwindow(root=None, prev_window=None):
#     if prev_window:
#         prev_window.destroy()
#
#     newwindow = tk.Toplevel(root)
#     newwindow.title("Login")
#     newwindow.configure(bg="#2B2B2B")
#     newwindow.state('zoomed')
#
#     container = tk.Frame(newwindow, bg="#2B2B2B")
#     container.place(relx=0.5, rely=0.5, anchor="center")
#
#     Label(container, text="Login to NotifyMe", font=("Roboto", 36, "bold"), fg="#E0E0E0", bg="#2B2B2B").pack(
#         pady=(0, 10))
#     Label(container, text="Secure Business Login", font=("Roboto", 20), fg="#E0E0E0", bg="#2B2B2B").pack(pady=(0, 20))
#
#     form_frame = tk.Frame(container, bg="#2B2B2B")
#     form_frame.pack()
#
#     Label(form_frame, text="Username:", font=("Roboto", 16), fg="#E0E0E0", bg="#2B2B2B").pack(anchor="w", pady=(0, 5))
#     Username = Entry(form_frame, width=25, font=("Roboto", 16), bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#     Username.pack(pady=(0, 15))
#
#     Label(form_frame, text="Password:", font=("Roboto", 16), fg="#E0E0E0", bg="#2B2B2B").pack(anchor="w", pady=(0, 5))
#     Password = Entry(form_frame, width=25, font=("Roboto", 16), show="*", bg="#3A3A3A", fg="#E0E0E0",
#                      insertbackground="#4A90E2")
#     Password.pack(pady=(0, 20))
#
#     button_frame = tk.Frame(container, bg="#2B2B2B")
#     button_frame.pack()
#
#     def on_login():
#         from dashboard import open_dashboard
#         entered_username = Username.get().strip()
#         entered_password = Password.get().strip()
#         if not entered_username or not entered_password:
#             messagebox.showwarning("Validation Error", "Username and Password are required!")
#             return
#         user = validate_login(entered_username, entered_password)
#         if user:
#             messagebox.showinfo("Login Success", "Login successful!")
#             is_admin = entered_username == "sid@123445" and entered_password == "sid@12345"
#             newwindow.destroy()
#             open_dashboard(is_admin=is_admin, root=root, prev_window=newwindow)
#         else:
#             messagebox.showerror("Login Failed", "Invalid username or password.")
#
#     Button(button_frame, text="Login", width=20, bg="#50C878", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat",
#            command=on_login).pack(side="left", padx=10)
#     Button(button_frame, text="Back", width=20, bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat",
#            command=lambda: back_to_main(newwindow)).pack(side="left", padx=10)
#
#     def back_to_main(window):
#         window.destroy()
#         if root:
#             root.deiconify()
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     lwindow(root)
#     root.mainloop()



from tkinter import Toplevel, Label, Button, messagebox, Entry
from dashboard import open_dashboard
from db import validate_login

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

class LoginUI(Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Login - NotifyMe")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.configure(bg="#1a1a1a")  # Black background from Code 1
        self.state('zoomed')

        container = Label(self, bg="#1a1a1a")  # Black from Code 1
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Title and subtitle
        title_label = Label(container, text="Login to NotifyMe", font=("Calibri", 28, "bold"),
                                    fg="#69dbc8", bg="#1a1a1a")  # Teal text from Code 1
        subtitle_label = Label(container, text="Secure Business Login", font=("Calibri", 16),
                                       fg="#ffffff", bg="#1a1a1a")  # White text from Code 1
        title_label.pack(pady=10)
        subtitle_label.pack(pady=5)

        # Username field
        Label(container, text="Username:", font=("Calibri", 14),
                    fg="#ffffff", bg="#1a1a1a").pack(anchor="w")  # White text from Code 1
        self.username_entry = PlaceholderEntry(container, "Enter username", font=("Calibri", 14), width=30,
                                                bg="#333333", fg="white", bd=2, relief="flat",  # Dark grey from Code 1
                                                insertbackground="white")
        self.username_entry.pack(ipady=5, pady=5)

        # Password field
        Label(container, text="Password:", font=("Calibri", 14),
                    fg="#ffffff", bg="#1a1a1a").pack(anchor="w")  # White text from Code 1
        self.password_entry = PlaceholderEntry(container, "Enter password", font=("Calibri", 14), width=30,
                                                bg="#333333", fg="white", bd=2, relief="flat", show="*",  # Dark grey from Code 1
                                                insertbackground="white")
        self.password_entry.pack(ipady=5, pady=5)

        # Error Label (Hidden by Default)
        self.error_label = Label(container, text="", font=("Calibri", 12),
                                    fg="#ff0000", bg="#1a1a1a")  # Red error text from Code 1
        self.error_label.pack()

        # Buttons Frame
        button_frame = Label(container, bg="#1a1a1a")  # Black from Code 1
        button_frame.pack(pady=20)

        # Login Button
        login_button = Button(button_frame, text="Login", font=("Calibri", 16, "bold"),
                                    fg="black", bg="#41d627", width=14, height=2,  # Green from Code 1
                                    borderwidth=2, relief="flat", command=self.on_login,
                                    cursor="hand2", activebackground="#33aa1e")  # Darker green for hover
        login_button.pack(side="left", padx=20)

        # Back Button
        back_button = Button(button_frame, text="Back", font=("Calibri", 16, "bold"),
                                  fg="black", bg="#69dbc8", width=14, height=2,  # Teal from Code 1
                                  borderwidth=2, relief="flat", command=self.destroy,
                                  cursor="hand2", activebackground="#54b0a0")  # Darker teal for hover
        back_button.pack(side="left", padx=20)

        # Add hover effects
        for btn, hover_color in [(login_button, "#33aa1e"), (back_button, "#54b0a0")]:
            btn.bind("<Enter>", lambda e, b=btn, c=hover_color: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=btn.cget("bg"): b.config(bg=c))

    def on_login(self):
        entered_username = self.username_entry.get().strip()
        entered_password = self.password_entry.get().strip()

        if entered_username == self.username_entry.placeholder or entered_password == self.password_entry.placeholder:
            self.error_label.config(text="Username and Password are required!")
            return

        if not entered_username or not entered_password:
            self.error_label.config(text="Username and Password are required!")
            return

        user = validate_login(entered_username, entered_password)

        if user:
            messagebox.showinfo("Login Success", "Login successful!")
            self.destroy()
            is_admin = entered_username == "sid@123445" and entered_password == "sid@12345"
            open_dashboard(is_admin)
        else:
            self.error_label.config(text="Invalid username or password.")

def lwindow(root):
    LoginUI(root)
