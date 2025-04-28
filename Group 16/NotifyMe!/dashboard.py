# import tkinter as tk
# from PIL import Image, ImageTk, ImageSequence
#
# GIF_PATH = "GIF1.gif"
#
# def open_dashboard(is_admin=False, root=None, prev_window=None):
#     if prev_window:
#         prev_window.destroy()
#     dashboard = tk.Toplevel(root)
#     dashboard.title("Dashboard")
#     dashboard.state("zoomed")
#     dashboard.configure(bg="#1E1E2F")
#
#     sidebar = tk.Frame(dashboard, bg="#2D2D44", width=250, height=dashboard.winfo_screenheight())
#     sidebar.pack(side="left", fill="y")
#
#     label_frame = tk.Frame(sidebar, bg="#2D2D44", pady=50)
#     label_frame.pack(fill="x", pady=(10, 20))
#
#     notify_label = tk.Label(label_frame, text="NotifyMe!", font=("Roboto", 18, "bold"), fg="#00D4FF", bg="#2D2D44", pady=50)
#     notify_label.pack(pady=10, padx=10)
#
#     button_style = {
#         "font": ("Roboto", 16, "bold"),
#         "width": 20,
#         "height": 2,
#         "fg": "#E0E0E0",
#         "bg": "#00D4FF",
#         "relief": "flat",
#         "bd": 0
#     }
#
#     def create_button(parent, text, command):
#         btn = tk.Button(parent, text=text, command=command, **button_style)
#         btn.pack(pady=15, padx=10, fill="x")
#
#     def open_company_app():
#         from company import company
#         dashboard.destroy()
#         company(root=root, prev_window=dashboard)
#
#     def open_employee_app():
#         from employee import employee
#         dashboard.destroy()
#         employee(root=root, prev_window=dashboard)
#
#     def open_sms_gui():
#         from sms import SMSNotifierGUI
#         dashboard.destroy()
#         SMSNotifierGUI(tk.Toplevel(root))
#
#     def open_metrics():
#         from analysis_page import matrics
#         dashboard.destroy()
#         matrics(root=root, prev_window=dashboard)
#
#     def logout():
#         from login import lwindow
#         dashboard.destroy()
#         lwindow(root=root, prev_window=dashboard)
#
#     create_button(sidebar, "Company", open_company_app)
#     create_button(sidebar, "Employee", open_employee_app)
#     create_button(sidebar, "Send Message", open_sms_gui)
#     if is_admin:
#         create_button(sidebar, "Metrics", open_metrics)
#     create_button(sidebar, "Logout", logout)
#
#     main_frame = tk.Frame(dashboard, bg="#1E1E2F", padx=50, pady=50)
#     main_frame.pack(expand=True, fill="both")
#
#     gif_label = tk.Label(dashboard, bg="#1E1E2F")
#     gif_label.pack(side="right", expand=True, padx=50, pady=50)
#
#     def animate_gif(label, gif_path):
#         try:
#             gif_image = Image.open(gif_path)
#             frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif_image)]
#
#             def update(index=0):
#                 frame = frames[index]
#                 label.config(image=frame)
#                 label.image = frame
#                 dashboard.after(100, update, (index + 1) % len(frames))
#
#             update()
#         except Exception as e:
#             print("Error loading GIF:", e)
#
#     animate_gif(gif_label, GIF_PATH)
#
#     dashboard.protocol("WM_DELETE_WINDOW", lambda: root.deiconify() if root else dashboard.destroy())
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.withdraw()
#     open_dashboard()
#     root.mainloop()
# #
# #
# # import tkinter as tk
# # from PIL import Image, ImageTk, ImageSequence
# #
# # GIF_PATH = "GIF1.gif"
# #
# # def open_dashboard(is_admin=False, root=None, prev_window=None):
# #     if prev_window:
# #         prev_window.destroy()
# #     dashboard = tk.Toplevel(root)
# #     dashboard.title("Dashboard")
# #     dashboard.state("zoomed")
# #     dashboard.configure(bg="#2B2B2B")
# #
# #     sidebar = tk.Frame(dashboard, bg="#3A3A3A", width=250, height=dashboard.winfo_screenheight())
# #     sidebar.pack(side="left", fill="y")
# #
# #     label_frame = tk.Frame(sidebar, bg="#3A3A3A", pady=50)
# #     label_frame.pack(fill="x", pady=(10, 20))
# #
# #     notify_label = tk.Label(label_frame, text="NotifyMe!", font=("Roboto", 18, "bold"), fg="#4A90E2", bg="#3A3A3A", pady=50)
# #     notify_label.pack(pady=10, padx=10)
# #
# #     button_style = {
# #         "font": ("Roboto", 16, "bold"),
# #         "width": 20,
# #         "height": 2,
# #         "fg": "#E0E0E0",
# #         "bg": "#4A90E2",
# #         "relief": "flat",
# #         "bd": 0
# #     }
# #
# #     def create_button(parent, text, command):
# #         btn = tk.Button(parent, text=text, command=command, **button_style)
# #         btn.pack(pady=15, padx=10, fill="x")
# #
# #     def open_company_app():
# #         from company import company
# #         dashboard.destroy()
# #         company(root=root, prev_window=dashboard)
# #
# #     def open_employee_app():
# #         from employee import employee
# #         dashboard.destroy()
# #         employee(root=root, prev_window=dashboard)
# #
# #     def open_sms_gui():
# #         from sms import SMSNotifierGUI
# #         dashboard.destroy()
# #         SMSNotifierGUI(tk.Toplevel(root))
# #
# #     def open_metrics():
# #         from analysis_page import matrics
# #         dashboard.destroy()
# #         matrics(root=root, prev_window=dashboard)
# #
# #     def logout():
# #         from login import lwindow
# #         dashboard.destroy()
# #         lwindow(root=root, prev_window=dashboard)
# #
# #     create_button(sidebar, "Company", open_company_app)
# #     create_button(sidebar, "Employee", open_employee_app)
# #     create_button(sidebar, "Send Message", open_sms_gui)
# #     if is_admin:
# #         create_button(sidebar, "Metrics", open_metrics)
# #     create_button(sidebar, "Logout", logout)
# #
# #     main_frame = tk.Frame(dashboard, bg="#2B2B2B", padx=50, pady=50)
# #     main_frame.pack(expand=True, fill="both")
# #
# #     gif_label = tk.Label(dashboard, bg="#2B2B2B")
# #     gif_label.pack(side="right", expand=True, padx=50, pady=50)
# #
# #     def animate_gif(label, gif_path):
# #         try:
# #             gif_image = Image.open(gif_path)
# #             frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif_image)]
# #
# #             def update(index=0):
# #                 frame = frames[index]
# #                 label.config(image=frame)
# #                 label.image = frame
# #                 dashboard.after(100, update, (index + 1) % len(frames))
# #
# #             update()
# #         except Exception as e:
# #             print("Error loading GIF:", e)
# #
# #     animate_gif(gif_label, GIF_PATH)
# #
# #     dashboard.protocol("WM_DELETE_WINDOW", lambda: root.deiconify() if root else dashboard.destroy())
# #
# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     root.withdraw()
# #     open_dashboard()
# #     root.mainloop()
#
#
#
# import tkinter as tk
# from PIL import Image, ImageTk
#
# # Path to your image (you'll need to save the provided image locally and specify its path)
# IMAGE_PATH = "notifyme_logo.jpeg"  # Replace with the actual path where you save the image
#
# def open_dashboard(is_admin=False, root=None, prev_window=None):
#     if prev_window:
#         prev_window.destroy()
#     dashboard = tk.Toplevel(root)
#     dashboard.title("Dashboard")
#     dashboard.state("zoomed")
#     dashboard.configure(bg="#2B2B2B")
#
#     sidebar = tk.Frame(dashboard, bg="#3A3A3A", width=250, height=dashboard.winfo_screenheight())
#     sidebar.pack(side="left", fill="y")
#
#     label_frame = tk.Frame(sidebar, bg="#3A3A3A", pady=50)
#     label_frame.pack(fill="x", pady=(10, 20))
#
#     notify_label = tk.Label(label_frame, text="NotifyMe!", font=("Roboto", 18, "bold"), fg="#4A90E2", bg="#3A3A3A", pady=50)
#     notify_label.pack(pady=10, padx=10)
#
#     button_style = {
#         "font": ("Roboto", 16, "bold"),
#         "width": 20,
#         "height": 2,
#         "fg": "#E0E0E0",
#         "bg": "#4A90E2",
#         "relief": "flat",
#         "bd": 0
#     }
#
#     def create_button(parent, text, command):
#         btn = tk.Button(parent, text=text, command=command, **button_style)
#         btn.pack(pady=15, padx=10, fill="x")
#
#     def open_company_app():
#         from company import company
#         dashboard.destroy()
#         company(root=root, prev_window=dashboard)
#
#     def open_employee_app():
#         from employee import employee
#         dashboard.destroy()
#         employee(root=root, prev_window=dashboard)
#
#     def open_sms_gui():
#         from sms import SMSNotifierGUI
#         dashboard.destroy()
#         SMSNotifierGUI(tk.Toplevel(root))
#
#     def open_metrics():
#         from analysis_page import matrics
#         dashboard.destroy()
#         matrics(root=root, prev_window=dashboard)
#
#     def logout():
#         from login import lwindow
#         dashboard.destroy()
#         lwindow(root=root, prev_window=dashboard)
#
#     create_button(sidebar, "Company", open_company_app)
#     create_button(sidebar, "Employee", open_employee_app)
#     create_button(sidebar, "Send Message", open_sms_gui)
#     if is_admin:
#         create_button(sidebar, "Metrics", open_metrics)
#     create_button(sidebar, "Logout", logout)
#
#     main_frame = tk.Frame(dashboard, bg="#2B2B2B", padx=50, pady=50)
#     main_frame.pack(expand=True, fill="both")
#
#     # Load and display the static image instead of GIF
#     image_label = tk.Label(dashboard, bg="#2B2B2B")
#     image_label.pack(side="right", expand=True, padx=50, pady=50)
#
#     try:
#         # Load the image
#         image = Image.open(IMAGE_PATH)
#         # Optionally resize the image if needed (adjust dimensions as necessary)
#         image = image.resize((300, 300), Image.Resampling.LANCZOS)  # Adjust size as needed
#         photo = ImageTk.PhotoImage(image)
#         image_label.config(image=photo)
#         image_label.image = photo  # Keep a reference to avoid garbage collection
#     except Exception as e:
#         print("Error loading image:", e)
#
#     dashboard.protocol("WM_DELETE_WINDOW", lambda: root.deiconify() if root else dashboard.destroy())
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.withdraw()
#     open_dashboard()
#     root.mainloop()


import tkinter as tk
from PIL import Image, ImageTk

# Path to your image (update with the actual path)
IMAGE_PATH = "notifyme_logo.png"  # Replace with the correct path


def open_dashboard(is_admin=False, root=None, prev_window=None):
    if prev_window:
        prev_window.destroy()

    dashboard = tk.Toplevel(root)
    dashboard.title("Dashboard")
    dashboard.state("zoomed")
    dashboard.configure(bg="#2B2B2B")

    # Sidebar
    sidebar = tk.Frame(dashboard, bg="#3A3A3A", width=250, height=dashboard.winfo_screenheight())
    sidebar.pack(side="left", fill="y")

    label_frame = tk.Frame(sidebar, bg="#3A3A3A", pady=50)
    label_frame.pack(fill="x", pady=(10, 20))

    notify_label = tk.Label(label_frame, text="NotifyMe!", font=("Roboto", 18, "bold"), fg="#4A90E2", bg="#3A3A3A",
                            pady=50)
    notify_label.pack(pady=10, padx=10)

    button_style = {
        "font": ("Roboto", 16, "bold"),
        "width": 20,
        "height": 2,
        "fg": "#E0E0E0",
        "bg": "#4A90E2",
        "relief": "flat",
        "bd": 0
    }

    def create_button(parent, text, command):
        btn = tk.Button(parent, text=text, command=command, **button_style)
        btn.pack(pady=15, padx=10, fill="x")

    def open_company_app():
        from company import company
        dashboard.destroy()
        company(root=root, prev_window=dashboard)

    def open_employee_app():
        from employee import employee
        dashboard.destroy()
        employee(root=root, prev_window=dashboard)

    def open_sms_gui():
        from sms import SMSNotifierGUI
        dashboard.destroy()
        SMSNotifierGUI(tk.Toplevel(root))

    def open_metrics():
        from analysis_page import matrics
        dashboard.destroy()
        matrics(root=root, prev_window=dashboard)

    def logout():
        from login import lwindow
        dashboard.destroy()
        lwindow(root=root, prev_window=dashboard)

    create_button(sidebar, "Company", open_company_app)
    create_button(sidebar, "Employee", open_employee_app)
    create_button(sidebar, "Send Message", open_sms_gui)

    if is_admin:
        create_button(sidebar, "Metrics", open_metrics)

    create_button(sidebar, "Logout", logout)

    # Main content area
    main_frame = tk.Frame(dashboard, bg="#2B2B2B", padx=50, pady=50)
    main_frame.pack(expand=True, fill="both")

    # Centering the image
    image_frame = tk.Frame(main_frame, bg="#2B2B2B")
    image_frame.pack(expand=True)

    image_label = tk.Label(image_frame, bg="#2B2B2B")
    image_label.pack(expand=True)  # Center the image

    try:
        # Load and resize the image
        image = Image.open(IMAGE_PATH)
        image = image.resize((450, 450), Image.Resampling.LANCZOS)  # Adjust as needed
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo  # Prevent garbage collection
    except Exception as e:
        print("Error loading image:", e)

    dashboard.protocol("WM_DELETE_WINDOW", lambda: root.deiconify() if root else dashboard.destroy())


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_dashboard()
    root.mainloop()





