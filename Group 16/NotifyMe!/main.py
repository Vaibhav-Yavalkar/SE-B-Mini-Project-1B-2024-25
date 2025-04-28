# # from tkinter import Tk, ttk
# # from login import lwindow
# # from registration import rwindow
# #
# # root = Tk()
# # root.title("NotifyMe!")
# # root.state('zoomed')
# #
# # style = ttk.Style()
# # style.configure("Custom.TButton", font=("Roboto", 28, "bold"), background="#00D4FF", foreground="black")
# #
# # lbutton = ttk.Button(root, text="Login", width=15, command=lambda: lwindow(root), style="Custom.TButton")
# # lbutton.pack(side="left", padx=150, pady=6)
# #
# # sbutton = ttk.Button(root, text="Sign-up", width=15, command=lambda: rwindow(root), style="Custom.TButton")
# # sbutton.pack(side="right", padx=150, pady=6)
# #
# # root.configure(bg="#1E1E2F")
# # root.mainloop()
#
# # from tkinter import Tk, ttk
# # from login import lwindow
# # from registration import rwindow
# #
# # root = Tk()
# # root.title("NotifyMe!")
# # root.state('zoomed')
# #
# # style = ttk.Style()
# # style.configure("Custom.TButton", font=("Roboto", 28, "bold"), background="#4A90E2", foreground="black")
# #
# # lbutton = ttk.Button(root, text="Login", width=15, command=lambda: lwindow(root), style="Custom.TButton")
# # lbutton.pack(side="left", padx=150, pady=6)
# #
# # sbutton = ttk.Button(root, text="Sign-up", width=15, command=lambda: rwindow(root), style="Custom.TButton")
# # sbutton.pack(side="right", padx=150, pady=6)
# #
# # root.configure(bg="#2B2B2B")
# # root.mainloop()
#
#
#
# from tkinter import Tk, ttk, Label
# from login import lwindow
# from registration import rwindow
#
# root = Tk()
# root.title("NotifyMe!")
# root.state('zoomed')
#
# Label(root, text="NotifyMe!", font=("Roboto", 36, "bold"), fg="#E0E0E0", bg="#2B2B2B").place(relx=0.5, y=200, anchor="center")
# Label(root, text="Streamline Your Business Communication", font=("Roboto", 20), fg="#E0E0E0", bg="#2B2B2B").place(relx=0.5, y=250, anchor="center")
#
# style = ttk.Style()
# style.configure("Custom.TButton", font=("Roboto", 28, "bold"), background="#4A90E2", foreground="black")
#
# lbutton = ttk.Button(root, text="Login", width=15, command=lambda: lwindow(root), style="Custom.TButton")
# lbutton.pack(side="left", padx=150, pady=6)
#
# sbutton = ttk.Button(root, text="Sign-up", width=15, command=lambda: rwindow(root), style="Custom.TButton")
# sbutton.pack(side="right", padx=150, pady=6)
#
# root.configure(bg="#2B2B2B")
# root.mainloop()



from tkinter import Tk, ttk, Label
from login import lwindow
from registration import rwindow

class MainUI(Tk):
    def __init__(self):
        super().__init__()
        self.title("NotifyMe! - CRM System")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.configure(bg="#1a1a1a")  # Black background from Code 1
        self.state('zoomed')

        container = ttk.Frame(self, style="Dark.TFrame")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Configure styles
        self.style = ttk.Style()
        self.style.configure("Dark.TFrame", background="#1a1a1a")  # Black from Code 1
        self.style.configure("Title.TLabel", font=("Calibri", 34, "bold"), foreground="#69dbc8", background="#1a1a1a")  # Teal text from Code 1
        self.style.configure("Subtitle.TLabel", font=("Calibri", 16), foreground="#ffffff", background="#1a1a1a")  # White text from Code 1
        self.style.configure("Glow.TButton",
                            font=("Calibri", 18, "bold"),
                            foreground="black",
                            background="#69dbc8",  # Teal from Code 1 for buttons
                            width=14,
                            borderwidth=2,
                            relief="flat")
        self.style.map("Glow.TButton",
                       background=[("active", "#54b0a0"), ("!active", "#69dbc8")])  # Darker teal for hover

        # Title and subtitle
        title_label = ttk.Label(container, text="NotifyMe !", style="Title.TLabel")
        subtitle_label = ttk.Label(container, text="Streamline Your Business Communication", style="Subtitle.TLabel")
        title_label.pack(pady=20)
        subtitle_label.pack(pady=5)

        # Button frame
        button_frame = ttk.Frame(container, style="Dark.TFrame")
        button_frame.pack()

        # Buttons
        login_button = ttk.Button(button_frame, text="Login", style="Glow.TButton", command=lambda: lwindow(self))
        login_button.pack(side="left", padx=20, pady=20)

        signup_button = ttk.Button(button_frame, text="Sign Up", style="Glow.TButton", command=lambda: rwindow(self))
        signup_button.pack(side="left", padx=20, pady=20)

if __name__ == "__main__":
    app = MainUI()
    app.mainloop()
