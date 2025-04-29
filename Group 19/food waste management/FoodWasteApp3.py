import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from PIL import Image, ImageTk, ImageEnhance

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("food_waste_tracker.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS waste_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                food_item TEXT,
                quantity INTEGER,
                reason TEXT,
                timestamp DATETIME
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                food_item TEXT UNIQUE,
                quantity INTEGER
            )
        """)

        self.conn.commit()

    def insert_log(self, food_item, quantity, reason):
        timestamp = datetime.now()
        self.cursor.execute("""
            INSERT INTO waste_log (food_item, quantity, reason, timestamp)
            VALUES (?, ?, ?, ?)
        """, (food_item, quantity, reason, timestamp))
        self.conn.commit()

    def get_logs_for_current_and_previous_month(self):
        current_date = datetime.now()
        first_day_of_current_month = current_date.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

        self.cursor.execute("""
            SELECT food_item, quantity, reason, timestamp
            FROM waste_log
            WHERE timestamp >= ? AND timestamp < ?
        """, (first_day_of_previous_month, first_day_of_current_month))
        previous_month_logs = self.cursor.fetchall()

        self.cursor.execute("""
            SELECT food_item, quantity, reason, timestamp
            FROM waste_log
            WHERE timestamp >= ? AND timestamp < ?
        """, (first_day_of_current_month, current_date))
        current_month_logs = self.cursor.fetchall()

        return previous_month_logs, current_month_logs

    def get_stock(self):
        self.cursor.execute("SELECT food_item, quantity FROM stock")
        return self.cursor.fetchall()

    def add_to_stock(self, food_item, quantity):
        self.cursor.execute("SELECT quantity FROM stock WHERE food_item=?", (food_item,))
        result = self.cursor.fetchone()

        if result:
            new_quantity = result[0] + quantity
            self.cursor.execute("UPDATE stock SET quantity=? WHERE food_item=?", (new_quantity, food_item))
        else:
            self.cursor.execute("INSERT INTO stock (food_item, quantity) VALUES (?, ?)", (food_item, quantity))

        self.conn.commit()

    def reduce_stock(self, food_item, quantity):
        self.cursor.execute("SELECT quantity FROM stock WHERE food_item=?", (food_item,))
        result = self.cursor.fetchone()
        if result:
            new_quantity = result[0] - quantity
            if new_quantity <= 0:
                self.cursor.execute("DELETE FROM stock WHERE food_item=?", (food_item,))
            else:
                self.cursor.execute("UPDATE stock SET quantity=? WHERE food_item=?", (new_quantity, food_item))
            self.conn.commit()

    def close(self):
        self.conn.close()

class LandingPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Waste Tracker")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f2f5")

        self.bg_image = Image.open("food_waste_bg.webp")
        self.bg_image = self.bg_image.resize((900, 600), Image.LANCZOS)
        enhancer = ImageEnhance.Brightness(self.bg_image)
        self.bg_image = enhancer.enhance(1.0)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(root, width=900, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        self.canvas.create_rectangle(0, 0, 900, 600, fill="white", stipple="gray50")

        self.canvas.create_text(
            450, 200,
            text="Food Waste Tracker",
            font=("Helvetica", 40, "bold"),
            fill="black",
        )

        self.canvas.create_text(
            450, 260,
            text="Track, Reduce, and Manage Food Waste",
            font=("Helvetica", 18),
            fill="black",
        )

        start_button = tk.Button(
            root,
            text="Get Started",
            font=("Verdana", 18),
            bg="#28a745",
            fg="white",
            activebackground="#218838",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=10,
            command=self.launch_app,
        )
        self.canvas.create_window(450, 350, window=start_button)

    def launch_app(self):
        self.root.destroy()
        main_root = tk.Tk()
        app = FoodWasteApp(main_root)
        main_root.mainloop()

class FoodWasteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Waste Tracker")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f2f5")

        self.db = Database()

        tk.Label(
            root,
            text="Food Waste Tracking System",
            font=("Helvetica", 28, "bold"),
            bg="#343a40",
            fg="white",
            pady=20,
        ).pack(fill=tk.X)

        self.main_frame = tk.Frame(root, bg="#f0f2f5", padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        input_frame = tk.Frame(self.main_frame, bg="#f0f2f5")
        input_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            input_frame,
            text="Food Item:",
            font=("Arial", 14),
            bg="#f0f2f5",
            fg="#343a40",
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.food_entry = tk.Entry(input_frame, font=("Arial", 14), width=25)
        self.food_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(
            input_frame,
            text="Quantity:",
            font=("Arial", 14),
            bg="#f0f2f5",
            fg="#343a40",
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.quantity_entry = tk.Entry(input_frame, font=("Arial", 14), width=25)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(
            input_frame,
            text="Reason:",
            font=("Arial", 14),
            bg="#f0f2f5",
            fg="#343a40",
        ).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.reason_var = tk.StringVar(value="expired")
        self.reason_dropdown = ttk.Combobox(
            input_frame,
            textvariable=self.reason_var,
            values=["expired", "leftover", "spoiled", "other"],
            font=("Arial", 14),
            width=23,
            state="readonly",
        )
        self.reason_dropdown.grid(row=2, column=1, padx=10, pady=5)

        buttons_frame = tk.Frame(self.main_frame, bg="#f0f2f5")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(
            buttons_frame,
            text="Log Food Waste",
            font=("Verdana", 12),
            bg="#28a745",
            fg="white",
            activebackground="#218838",
            activeforeground="white",
            command=self.log_food_waste,
        ).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(
            buttons_frame,
            text="Add to Stock",
            font=("Verdana", 12),
            bg="#17a2b8",
            fg="white",
            activebackground="#117a8b",
            activeforeground="white",
            command=self.add_to_stock,
        ).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(
            buttons_frame,
            text="Clear Entries",
            font=("Verdana", 12),
            bg="#6c757d",
            fg="white",
            activebackground="#5a6268",
            activeforeground="white",
            command=self.clear_entries,
        ).grid(row=0, column=2, padx=5, pady=5)

        report_frame = tk.Frame(self.main_frame, bg="#f0f2f5")
        report_frame.pack(fill=tk.X, pady=10)

        tk.Button(
            report_frame,
            text="Generate Waste Report",
            font=("Verdana", 14),
            bg="#dc3545",
            fg="white",
            activebackground="#bd2130",
            activeforeground="white",
            command=self.generate_report,
        ).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(
            report_frame,
            text="View Stock",
            font=("Verdana", 14),
            bg="#007bff",
            fg="white",
            activebackground="#0056b3",
            activeforeground="white",
            command=self.view_stock,
        ).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(
            report_frame,
            text="View Waste Statistics (Bar Chart)",
            font=("Verdana", 14),
            bg="#007bff",
            fg="white",
            activebackground="#0056b3",
            activeforeground="white",
            command=self.generate_bar_chart,
        ).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(
            report_frame,
            text="View Waste Statistics (Pie Chart)",
            font=("Verdana", 14),
            bg="#007bff",
            fg="white",
            activebackground="#0056b3",
            activeforeground="white",
            command=self.generate_pie_chart,
        ).pack(side=tk.LEFT, padx=5, pady=5)

    def log_food_waste(self):
        food_item = self.food_entry.get()
        quantity = self.quantity_entry.get()
        reason = self.reason_var.get()
        if food_item and quantity.isdigit() and reason:
            quantity = int(quantity)
            self.db.insert_log(food_item, quantity, reason)
            self.db.reduce_stock(food_item, quantity)
            self.clear_entries()
            messagebox.showinfo("Success", "Food waste logged and stock updated successfully!")
        else:
            messagebox.showwarning("Input Error", "Please enter a valid food item, quantity, and reason.")

    def add_to_stock(self):
        food_item = self.food_entry.get()
        quantity = self.quantity_entry.get()

        if food_item and quantity.isdigit():
            quantity = int(quantity)
            self.db.add_to_stock(food_item, quantity)
            self.clear_entries()
            messagebox.showinfo("Success", f"{quantity} {food_item}(s) added to stock!")
        else:
            messagebox.showwarning("Input Error", "Please enter a valid food item and quantity.")

    def clear_entries(self):
        self.food_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.reason_var.set("expired")

    def generate_report(self):
        previous_month_logs, current_month_logs = self.db.get_logs_for_current_and_previous_month()

        if previous_month_logs or current_month_logs:
            report = "Food Waste Report:\n"
            report += "Previous Month Logs:\n"
            for item, quantity, reason, timestamp in previous_month_logs:
                report += f"{item} ({quantity}) - {reason} - {timestamp}\n"

            report += "\nCurrent Month Logs:\n"
            for item, quantity, reason, timestamp in current_month_logs:
                report += f"{item} ({quantity}) - {reason} - {timestamp}\n"

            messagebox.showinfo("Food Waste Report", report)
        else:
            messagebox.showinfo("No Data", "No food waste logs for the current or previous month.")

    def view_stock(self):
        stock_items = self.db.get_stock()
        stock_report = "Current Food Stock:\n"

        if stock_items:
            for food_item, quantity in stock_items:
                stock_report += f"{food_item}: {quantity}\n"
            messagebox.showinfo("Food Stock", stock_report)
        else:
            messagebox.showinfo("No Stock", "No items in stock.")

    def generate_bar_chart(self):
        previous_month_logs, current_month_logs = self.db.get_logs_for_current_and_previous_month()

        food_data = {}
        for item, quantity, _, _ in previous_month_logs + current_month_logs:
            if item in food_data:
                food_data[item] += quantity
            else:
                food_data[item] = quantity

        items = list(food_data.keys())
        quantities = list(food_data.values())

        plt.bar(items, quantities)
        plt.xlabel("Food Items")
        plt.ylabel("Quantity")
        plt.title("Food Waste Bar Chart")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    def generate_pie_chart(self):
        previous_month_logs, current_month_logs = self.db.get_logs_for_current_and_previous_month()

        food_data = {}
        for item, quantity, _, _ in previous_month_logs + current_month_logs:
            if item in food_data:
                food_data[item] += quantity
            else:
                food_data[item] = quantity

        items = list(food_data.keys())
        quantities = list(food_data.values())

        plt.pie(quantities, labels=items, autopct="%1.1f%%", startangle=90)
        plt.title("Food Waste Pie Chart")
        plt.axis("equal")  # Equal aspect ratio ensures that pie chart is drawn as a circle.
        plt.show()

    def close_db(self):
        self.db.close()


if __name__ == "__main__":
    root = tk.Tk()
    landing_page = LandingPage(root)
    root.mainloop()
