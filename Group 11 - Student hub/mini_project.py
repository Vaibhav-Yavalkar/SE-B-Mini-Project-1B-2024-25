import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
# from database import create_table, insert_student_data


USERNAME = "admin"
PASSWORD = "1234"
data = None

def authenticate():
    if username_entry.get() == USERNAME and password_entry.get() == PASSWORD:
        login_window.destroy()
        open_main_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def open_main_dashboard():
    global root
    root = tk.Tk()
    root.title("Student Hub - Dashboard")
    root.configure(bg="#2c2f33")
    
    tk.Label(root, text="Student Hub", font=("Arial", 20, "bold"), bg="#7289da", fg="white", pady=15).grid(row=0, column=0, columnspan=2, pady=15, padx=20, sticky="ew")
    
    buttons = [
        ("Upload & Process CSV", upload_file),
        ("Search Student", search_student),
        ("Sort Students", sort_students),
        ("Top Performers", show_top_students),
        ("Visualize Data", show_graph),
        ("Save Processed Data", save_file),
        ("View All Results", view_all_results)
    ]
    
    for i, (text, command) in enumerate(buttons):
        tk.Button(root, text=text, command=command, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=25, height=2).grid(row=(i//2)+1, column=i%2, padx=20, pady=10)
    
    tk.Button(root, text="Exit", command=root.quit, font=("Arial", 12, "bold"), bg="#f44336", fg="white", width=25, height=2).grid(row=(len(buttons)//2)+2, column=0, columnspan=2, padx=20, pady=20)
    
    root.mainloop()


def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        messagebox.showwarning("Warning", "No file selected!")
        return
    
    try:
        global data
        data = pd.read_csv(file_path)
        required_columns = {'Name', 'Marks1', 'Marks2', 'Marks3', 'Marks4', 'Marks5'}
        if not required_columns.issubset(data.columns):
            messagebox.showerror("Error", "CSV must contain: Name, Marks1-5")
            return
        
        data['Marks Obtained'] = data[['Marks1', 'Marks2', 'Marks3', 'Marks4', 'Marks5']].sum(axis=1)
        data['Total Marks'] = 500
        data['Percentage'] = round((data['Marks Obtained'] / data['Total Marks']) * 100, 2)
        data['Grade'] = data['Percentage'].apply(calculate_grade)
        data['Status'] = data['Percentage'].apply(lambda x: "Pass" if x >= 40 else "Fail")
        
        messagebox.showinfo("Success", "CSV Processed Successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file: {e}")


def calculate_grade(percentage):
    if percentage >= 90: return "A+"
    elif percentage >= 80: return "A"
    elif percentage >= 70: return "B"
    elif percentage >= 60: return "C"
    elif percentage >= 50: return "D"
    else: return "F"

def create_table_window(title, dataset):
    table_window = tk.Toplevel(root)
    table_window.title(title)
    table_window.configure(bg="#23272a")
    
    tree = ttk.Treeview(table_window, columns=list(dataset.columns), show="headings")
    for col in dataset.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    
    for _, row in dataset.iterrows():
        tree.insert("", "end", values=tuple(row))
    
    tree.pack(expand=True, fill="both")

def view_all_results():
    if data is None:
        messagebox.showwarning("Warning", "No data available! Please upload a CSV first.")
        return
    create_table_window("All Student Results", data)

def search_student():
    if data is None:
        messagebox.showwarning("Warning", "No data available! Please upload a CSV first.")
        return
    search_window = tk.Toplevel(root)
    search_window.title("Search Student")
    search_window.configure(bg="#23272a")
    
    tk.Label(search_window, text="Enter Student Name:", font=("Arial", 12), bg="#23272a", fg="white").pack()
    search_entry = tk.Entry(search_window, font=("Arial", 12))
    search_entry.pack()
    
    def find_student():
        name = search_entry.get().strip()
        student = data[data['Name'].str.lower() == name.lower()]
        if student.empty:
            messagebox.showinfo("Not Found", "Student not found!")
        else:
            create_table_window("Search Result", student)
    
    tk.Button(search_window, text="Search", command=find_student, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

def sort_students():
    global data
    if data is None:
        messagebox.showwarning("Warning", "No data available! Please upload a CSV first.")
        return
    data = data.sort_values(by='Percentage', ascending=False)
    messagebox.showinfo("Sorted", "Students sorted by percentage!")

def show_top_students():
    if data is None:
        messagebox.showwarning("Warning", "No data available! Please upload a CSV first.")
        return
    top_students = data.nlargest(3, 'Percentage')
    create_table_window("Top 3 Students", top_students)

def show_graph():
    if data is None:
        messagebox.showwarning("Warning", "No data available! Please upload a CSV first.")
        return
    plt.figure(figsize=(10, 5))
    plt.bar(data['Name'], data['Percentage'], color='blue')
    plt.xlabel("Students")
    plt.ylabel("Percentage")
    plt.title("Student Performance")
    plt.xticks(rotation=45)
    plt.show()

def save_file():
    if data is None:
        messagebox.showwarning("Warning", "No data available! Please upload a CSV first.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        data.to_csv(file_path, index=False)
        messagebox.showinfo("Success", "File saved successfully!")

login_window = tk.Tk()
login_window.title("Login")
login_window.configure(bg="#2c2f33")

tk.Label(login_window, text="Username:", font=("Arial", 12), bg="#2c2f33", fg="white").grid(row=0, column=0)
username_entry = tk.Entry(login_window, font=("Arial", 12))
username_entry.grid(row=0, column=1)

tk.Label(login_window, text="Password:", font=("Arial", 12), bg="#2c2f33", fg="white").grid(row=1, column=0)
password_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
password_entry.grid(row=1, column=1)

tk.Button(login_window, text="Login", command=authenticate, font=("Arial", 12), bg="#4CAF50", fg="white").grid(row=2, column=0, columnspan=2, pady=10)
login_window.mainloop()
