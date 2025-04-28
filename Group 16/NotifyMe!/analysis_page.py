# import tkinter as tk
# from tkinter import ttk
# from collections import Counter
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from db import fetch_data
# from tkinter import messagebox
#
# class MatricsFrame:
#     def __init__(self, root, prev_window=None):
#         if prev_window:
#             prev_window.destroy()
#         self.root = tk.Toplevel(root)
#         self.root.title("Employee Data Analysis Dashboard")
#         self.root.configure(bg="#1E1E2F")
#         self.root.state("zoomed")
#         self.fields = {
#             "Services Provided": "service_provided",
#             "Company": "company",
#             "Designation": "designation",
#             "Department": "department"
#         }
#         self.sidebar_frame = tk.Frame(self.root, bg="#2D2D44", width=300, relief=tk.RIDGE, bd=2)
#         self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
#         self.content_frame = tk.Frame(self.root, bg="#1E1E2F")
#         self.content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
#         self.setup_sidebar()
#         self.canvas_frame = tk.Frame(self.content_frame, bg="#25253A", bd=3, relief=tk.GROOVE)
#         self.canvas_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
#         self.update_graph()
#
#     def setup_sidebar(self):
#         title_label = tk.Label(self.sidebar_frame, text="Analysis Dashboard", bg="#2D2D44", fg="#FFFFFF",
#                                font=("Roboto", 18, "bold"))
#         title_label.pack(pady=(20, 20))
#         dropdown_label = tk.Label(self.sidebar_frame, text="Select Category:", bg="#2D2D44", fg="#FFFFFF",
#                                   font=("Roboto", 14))
#         dropdown_label.pack(pady=(0, 10), padx=10, anchor=tk.W)
#         self.selected_field = tk.StringVar()
#         self.selected_field.set("Services Provided")
#         self.dropdown = ttk.Combobox(self.sidebar_frame, textvariable=self.selected_field,
#                                      values=list(self.fields.keys()), state="readonly", font=("Roboto", 12), width=22)
#         self.dropdown.pack(pady=10, padx=20)
#         self.dropdown.bind("<<ComboboxSelected>>", self.update_graph)
#         self.plot_button = tk.Button(self.sidebar_frame, text="Refresh Graph", command=self.update_graph,
#                                      font=("Roboto", 12, "bold"), bg="#00D4FF", fg="#FFFFFF", relief="flat", padx=10, pady=5)
#         self.plot_button.pack(pady=20, padx=20, fill="x")
#         self.back_button = tk.Button(self.sidebar_frame, text="Back", command=lambda: self.back_to_dashboard(),
#                                      font=("Roboto", 12, "bold"), bg="#FF5555", fg="#E0E0E0", relief="flat", padx=10, pady=5)
#         self.back_button.pack(pady=20, padx=20, fill="x")
#
#     def back_to_dashboard(self):
#         from dashboard import open_dashboard
#         self.root.destroy()
#         open_dashboard(root=self.root.master, prev_window=self.root, is_admin=True)
#
#     def update_graph(self, event=None):
#         field = self.fields[self.selected_field.get()]
#         try:
#             data = fetch_data(field)
#             if not data:
#                 messagebox.showwarning("No Data", f"No data found for {self.selected_field.get()}.")
#                 return
#             data_counts = Counter(data)
#             labels = [f"{key} ({value})" for key, value in data_counts.items()]
#             sizes = list(data_counts.values())
#             total_count = sum(sizes)
#             colors = plt.cm.Pastel1(range(len(labels)))
#             for widget in self.canvas_frame.winfo_children():
#                 widget.destroy()
#             fig, ax = plt.subplots(figsize=(10, 10))
#             wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors,
#                                               textprops={'fontsize': 12})
#             ax.set_title(f"Distribution of {self.selected_field.get()} (Total: {total_count})", fontsize=14, pad=10, color="#E0E0E0")
#             ax.set_facecolor("#25253A")
#             fig.set_facecolor("#25253A")
#             canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
#             canvas.draw()
#             canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to fetch or display data: {str(e)}")
#
# def matrics(root=None, prev_window=None):
#     app = MatricsFrame(root, prev_window)
#
# if __name__ == "__main__":
#     matrics()



# import tkinter as tk
# from tkinter import ttk
# from collections import Counter
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from db import fetch_data
# from tkinter import messagebox
#
# class MatricsFrame:
#     def __init__(self, root, prev_window=None):
#         if prev_window:
#             prev_window.destroy()
#         self.root = tk.Toplevel(root)
#         self.root.title("Employee Data Analysis Dashboard")
#         self.root.configure(bg="#2B2B2B")
#         self.root.state("zoomed")
#         self.fields = {
#             "Services Provided": "service_provided",
#             "Company": "company",
#             "Designation": "designation",
#             "Department": "department"
#         }
#         self.sidebar_frame = tk.Frame(self.root, bg="#3A3A3A", width=300, relief=tk.RIDGE, bd=2)
#         self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
#         self.content_frame = tk.Frame(self.root, bg="#2B2B2B")
#         self.content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
#         self.setup_sidebar()
#         self.canvas_frame = tk.Frame(self.content_frame, bg="#25253A", bd=3, relief=tk.GROOVE)
#         self.canvas_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
#         self.update_graph()
#
#     def setup_sidebar(self):
#         title_label = tk.Label(self.sidebar_frame, text="Analysis Dashboard", bg="#3A3A3A", fg="#E0E0E0",
#                                font=("Roboto", 18, "bold"))
#         title_label.pack(pady=(20, 20))
#         dropdown_label = tk.Label(self.sidebar_frame, text="Select Category:", bg="#3A3A3A", fg="#E0E0E0",
#                                   font=("Roboto", 14))
#         dropdown_label.pack(pady=(0, 10), padx=10, anchor=tk.W)
#         self.selected_field = tk.StringVar()
#         self.selected_field.set("Services Provided")
#         self.dropdown = ttk.Combobox(self.sidebar_frame, textvariable=self.selected_field,
#                                      values=list(self.fields.keys()), state="readonly", font=("Roboto", 12), width=22)
#         self.dropdown.pack(pady=10, padx=20)
#         self.dropdown.bind("<<ComboboxSelected>>", self.update_graph)
#         self.plot_button = tk.Button(self.sidebar_frame, text="Refresh Graph", command=self.update_graph,
#                                      font=("Roboto", 12, "bold"), bg="#4A90E2", fg="#E0E0E0", relief="flat", padx=10, pady=5)
#         self.plot_button.pack(pady=20, padx=20, fill="x")
#         self.back_button = tk.Button(self.sidebar_frame, text="Back", command=lambda: self.back_to_dashboard(),
#                                      font=("Roboto", 12, "bold"), bg="#FF5555", fg="#E0E0E0", relief="flat", padx=10, pady=5)
#         self.back_button.pack(pady=20, padx=20, fill="x")
#
#     def back_to_dashboard(self):
#         from dashboard import open_dashboard
#         self.root.destroy()
#         open_dashboard(root=self.root.master, prev_window=self.root, is_admin=True)
#
#     def update_graph(self, event=None):
#         field = self.fields[self.selected_field.get()]
#         try:
#             data = fetch_data(field)
#             if not data:
#                 messagebox.showwarning("No Data", f"No data found for {self.selected_field.get()}.")
#                 return
#             data_counts = Counter(data)
#             labels = [f"{key} ({value})" for key, value in data_counts.items()]
#             sizes = list(data_counts.values())
#             total_count = sum(sizes)
#             colors = plt.cm.Pastel1(range(len(labels)))
#             for widget in self.canvas_frame.winfo_children():
#                 widget.destroy()
#             fig, ax = plt.subplots(figsize=(10, 10))
#             wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors,
#                                               textprops={'fontsize': 12})
#             ax.set_title(f"Distribution of {self.selected_field.get()} (Total: {total_count})", fontsize=14, pad=10, color="#E0E0E0")
#             ax.set_facecolor("#25253A")
#             fig.set_facecolor("#25253A")
#             canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
#             canvas.draw()
#             canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to fetch or display data: {str(e)}")
#
# def matrics(root=None, prev_window=None):
#     app = MatricsFrame(root, prev_window)
#
# if __name__ == "__main__":
#     matrics()



# import tkinter as tk
# from tkinter import ttk
# from collections import Counter
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from db import fetch_data
# from tkinter import messagebox
#
# class MatricsFrame:
#     def __init__(self, root, prev_window=None):
#         if prev_window:
#             prev_window.destroy()
#         self.root = tk.Toplevel(root)
#         self.root.title("Employee Data Analysis Dashboard")
#         self.root.configure(bg="#2B2B2B")
#         self.root.state("zoomed")
#         self.fields = {
#             "Services Provided": "service_provided",
#             "Company": "company",
#             "Designation": "designation",
#             "Department": "department"
#         }
#         self.sidebar_frame = tk.Frame(self.root, bg="#3A3A3A", width=300, relief=tk.RIDGE, bd=2)
#         self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
#         self.content_frame = tk.Frame(self.root, bg="#2B2B2B")
#         self.content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
#         self.setup_sidebar()
#         self.canvas_frame = tk.Frame(self.content_frame, bg="#25253A", bd=3, relief=tk.GROOVE)
#         self.canvas_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
#         self.update_graph()
#
#     def setup_sidebar(self):
#         title_label = tk.Label(self.sidebar_frame, text="Analysis Dashboard", bg="#3A3A3A", fg="#E0E0E0",
#                                font=("Roboto", 18, "bold"))
#         title_label.pack(pady=(20, 20))
#         dropdown_label = tk.Label(self.sidebar_frame, text="Select Category:", bg="#3A3A3A", fg="#E0E0E0",
#                                   font=("Roboto", 14))
#         dropdown_label.pack(pady=(0, 10), padx=10, anchor=tk.W)
#         self.selected_field = tk.StringVar()
#         self.selected_field.set("Services Provided")
#         self.dropdown = ttk.Combobox(self.sidebar_frame, textvariable=self.selected_field,
#                                      values=list(self.fields.keys()), state="readonly", font=("Roboto", 12), width=22)
#         self.dropdown.pack(pady=10, padx=20)
#         self.dropdown.bind("<<ComboboxSelected>>", self.update_graph)
#         self.plot_button = tk.Button(self.sidebar_frame, text="Refresh Graph", command=self.update_graph,
#                                      font=("Roboto", 12, "bold"), bg="#4A90E2", fg="#E0E0E0", relief="flat", padx=10, pady=5)
#         self.plot_button.pack(pady=20, padx=20, fill="x")
#         self.back_button = tk.Button(self.sidebar_frame, text="Back", command=lambda: self.back_to_dashboard(),
#                                      font=("Roboto", 12, "bold"), bg="#FF5555", fg="#E0E0E0", relief="flat", padx=10, pady=5)
#         self.back_button.pack(pady=20, padx=20, fill="x")
#
#     def back_to_dashboard(self):
#         from dashboard import open_dashboard
#         self.root.destroy()
#         open_dashboard(root=self.root.master, prev_window=self.root, is_admin=True)
#
#     def update_graph(self, event=None):
#         field = self.fields[self.selected_field.get()]
#         try:
#             data = fetch_data(field)
#             if not data:
#                 messagebox.showwarning("No Data", f"No data found for {self.selected_field.get()}.")
#                 return
#             data_counts = Counter(data)
#             labels = [f"{key} ({value})" for key, value in data_counts.items()]
#             sizes = list(data_counts.values())
#             total_count = sum(sizes)
#             colors = plt.cm.Pastel1(range(len(labels)))
#             for widget in self.canvas_frame.winfo_children():
#                 widget.destroy()
#             fig, ax = plt.subplots(figsize=(10, 10))
#             wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors,
#                                               textprops={'fontsize': 12})
#             ax.set_title(f"Distribution of {self.selected_field.get()} (Total: {total_count})", fontsize=14, pad=10, color="#E0E0E0")
#             ax.set_facecolor("#25253A")
#             fig.set_facecolor("#25253A")
#             canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
#             canvas.draw()
#             canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to fetch or display data: {str(e)}")
#
# def matrics(root=None, prev_window=None):
#     app = MatricsFrame(root, prev_window)
#
# if __name__ == "__main__":
#     matrics()




import tkinter as tk
from tkinter import ttk
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db import fetch_data
from tkinter import messagebox

class MatricsFrame:
    def __init__(self, root, prev_window=None):
        if prev_window:
            prev_window.destroy()
        self.root = tk.Toplevel(root)
        self.root.title("Employee Data Analysis Dashboard")
        self.root.configure(bg="#2B2B2B")
        self.root.state("zoomed")
        self.fields = {
            "Services Provided": "service_provided",
            "Company": "company",
            "Designation": "designation",
            "Department": "department"
        }
        self.sidebar_frame = tk.Frame(self.root, bg="#3A3A3A", width=300, relief=tk.RIDGE, bd=2)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.content_frame = tk.Frame(self.root, bg="#2B2B2B")
        self.content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.setup_sidebar()
        self.canvas_frame = tk.Frame(self.content_frame, bg="#25253A", bd=3, relief=tk.GROOVE)
        self.canvas_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.update_graph()

    def setup_sidebar(self):
        title_label = tk.Label(self.sidebar_frame, text="Analysis Dashboard", bg="#3A3A3A", fg="#E0E0E0",
                               font=("Roboto", 18, "bold"))
        title_label.pack(pady=(20, 20))
        dropdown_label = tk.Label(self.sidebar_frame, text="Select Category:", bg="#3A3A3A", fg="#E0E0E0",
                                  font=("Roboto", 14))
        dropdown_label.pack(pady=(0, 10), padx=10, anchor=tk.W)
        self.selected_field = tk.StringVar()
        self.selected_field.set("Services Provided")
        self.dropdown = ttk.Combobox(self.sidebar_frame, textvariable=self.selected_field,
                                     values=list(self.fields.keys()), state="readonly", font=("Roboto", 12), width=22)
        self.dropdown.pack(pady=10, padx=20)
        self.dropdown.bind("<<ComboboxSelected>>", self.update_graph)
        self.plot_button = tk.Button(self.sidebar_frame, text="Refresh Graph", command=self.update_graph,
                                     font=("Roboto", 12, "bold"), bg="#4A90E2", fg="#E0E0E0", relief="flat", padx=10, pady=5)
        self.plot_button.pack(pady=20, padx=20, fill="x")
        self.back_button = tk.Button(self.sidebar_frame, text="Back", command=lambda: self.back_to_dashboard(),
                                     font=("Roboto", 12, "bold"), bg="#FF5555", fg="#E0E0E0", relief="flat", padx=10, pady=5)
        self.back_button.pack(pady=20, padx=20, fill="x")

    def back_to_dashboard(self):
        from dashboard import open_dashboard
        self.root.destroy()
        open_dashboard(root=self.root.master, prev_window=self.root, is_admin=True)

    def update_graph(self, event=None):
        field = self.fields[self.selected_field.get()]
        try:
            data = fetch_data(field)
            if not data:
                messagebox.showwarning("No Data", f"No data found for {self.selected_field.get()}.")
                return
            data_counts = Counter(data)
            labels = [f"{key} ({value})" for key, value in data_counts.items()]
            sizes = list(data_counts.values())
            total_count = sum(sizes)
            colors = plt.cm.Pastel1(range(len(labels)))
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            fig, ax = plt.subplots(figsize=(10, 10))
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors,
                                              textprops={'fontsize': 12, 'color': 'white'})  # Labels to white
            ax.set_title(f"Distribution of {self.selected_field.get()} (Total: {total_count})", fontsize=14, pad=10, color="white")  # Title to white
            ax.set_facecolor("#25253A")
            fig.set_facecolor("#25253A")
            # Set percentage text (autotexts) to black
            for autotext in autotexts:
                autotext.set_color('black')
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch or display data: {str(e)}")

def matrics(root=None, prev_window=None):
    app = MatricsFrame(root, prev_window)

if __name__ == "__main__":
    matrics()
