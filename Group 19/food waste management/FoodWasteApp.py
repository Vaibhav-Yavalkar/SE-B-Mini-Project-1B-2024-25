import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk, ImageEnhance

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
        self.food_waste_log = []
        self.food_stock = {}

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
        tk.Button(
            buttons_frame,
            text="View Stock",
            font=("Verdana", 12),
            bg="#ffc107",
            fg="#343a40",
            activebackground="#e0a800",
            activeforeground="#343a40",
            command=self.view_stock,
        ).grid(row=0, column=3, padx=5, pady=5)

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
            text="Generate Statistical Report",
            font=("Verdana", 14),
            bg="#007bff",
            fg="white",
            activebackground="#0056b3",
            activeforeground="white",
            command=self.generate_statistical_report,
        ).pack(side=tk.LEFT, padx=5, pady=5)

    def log_food_waste(self):
        food_item = self.food_entry.get()
        quantity = self.quantity_entry.get()
        reason = self.reason_var.get()
        if food_item and quantity.isdigit() and reason:
            quantity = int(quantity)
            self.food_waste_log.append((food_item, quantity, reason))
            if food_item in self.food_stock:
                self.food_stock[food_item] -= quantity
                if self.food_stock[food_item] <= 0:
                    del self.food_stock[food_item]
            self.clear_entries()
            messagebox.showinfo("Success", "Food waste logged successfully!")
        else:
            messagebox.showwarning("Input Error", "Please enter a valid food item, quantity, and reason.")

    def add_to_stock(self):
        food_item = self.food_entry.get()
        quantity = self.quantity_entry.get()
        if food_item and quantity.isdigit():
            quantity = int(quantity)
            if food_item in self.food_stock:
                self.food_stock[food_item] += quantity
            else:
                self.food_stock[food_item] = quantity
            self.clear_entries()
            messagebox.showinfo("Success", "Food item added to stock successfully!")
        else:
            messagebox.showwarning("Input Error", "Please enter a valid food item and quantity.")

    def clear_entries(self):
        self.food_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.reason_var.set("expired")

    def view_stock(self):
        if self.food_stock:
            stock_report = "\n".join([f"{item}: {quantity}" for item, quantity in self.food_stock.items()])
            messagebox.showinfo("Current Stock", f"Your Current Food Stock:\n{stock_report}")
        else:
            messagebox.showinfo("No Data", "No food items in stock yet.")

    def generate_report(self):
        if self.food_waste_log:
            report = "\n".join([f"{item} ({quantity}) - {reason}" for item, quantity, reason in self.food_waste_log])
            messagebox.showinfo("Food Waste Report", f"Your Food Waste Log:\n{report}")
        else:
            messagebox.showinfo("No Data", "No food waste logged yet.")

    def generate_statistical_report(self):
        if self.food_waste_log or self.food_stock:
            waste_data = {}
            saved_data = {}

            for item, quantity, _ in self.food_waste_log:
                waste_data[item] = waste_data.get(item, 0) + quantity

            for item, quantity in self.food_stock.items():
                saved_data[item] = saved_data.get(item, 0) + quantity

            items = list(set(waste_data.keys()).union(set(saved_data.keys())))
            wasted = [waste_data.get(item, 0) for item in items]
            saved = [saved_data.get(item, 0) for item in items]

            plt.figure(figsize=(10, 6))
            bar_width = 0.4
            x_indices = range(len(items))

            plt.bar(x_indices, wasted, bar_width, label="Wasted", color="#ff6f61")
            plt.bar([x + bar_width for x in x_indices], saved, bar_width, label="Saved", color="#6fbf73")

            plt.xlabel("Food Items")
            plt.ylabel("Quantity")
            plt.title("Food Wasted vs Saved", fontsize=16)
            plt.xticks([x + bar_width / 2 for x in x_indices], items, rotation=45)
            plt.legend()
            plt.tight_layout()

            plt.show()
        else:
            messagebox.showinfo("No Data", "Not enough data to generate a statistical report.")

if __name__ == "__main__":
    root = tk.Tk()
    landing_page = LandingPage(root)
    root.mainloop()