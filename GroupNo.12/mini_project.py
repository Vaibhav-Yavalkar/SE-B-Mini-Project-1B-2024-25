#from itertools import product
import sqlite3
import tkinter as tk
import re
from tkinter import messagebox
from tkinter import messagebox, ttk
from datetime import datetime
from PIL import Image, ImageTk
from twilio.rest import Client
import requests
from tkinter import filedialog
import requests

#from tkintervideo import TkinterVideo # type: ignore

CART = []

conn = sqlite3.connect("nursery.db")
cursor = conn.cursor()
# ------------------- Database Tables -------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Reviews (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    username TEXT,
    review_text TEXT,
    rating INTEGER,
    FOREIGN KEY (product_id) REFERENCES Products (id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Orders (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    quantity INTEGER,
    total_price REAL,
    date TEXT,
    FOREIGN KEY (product_id) REFERENCES Products (id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Plantations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    planting_date TEXT,
    care_instructions TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Orders (
    id INTEGER PRIMARY KEY,
    username TEXT,
    product_id INTEGER,
    quantity INTEGER,
    total_price REAL,
    date TEXT,
    status TEXT,
    contact_no TEXT,
    FOREIGN KEY (product_id) REFERENCES Products (id)
)
""")
conn.commit()

# ------------------- Insert Default Data -------------------
cursor.execute("SELECT COUNT(*) FROM Products")
if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO Products (name, description, price, stock) 
    VALUES (?, ?, ?, ?)
    """, [
        ("Rose Plant", "Beautiful flowering plant.", 250.0, 50),
        ("Money Plant", "Low-maintenance indoor plant.", 350.0, 30),
        ("Tulsi", "Holy basil with medicinal properties.", 300.0, 100)
    ])
    conn.commit()

cursor.execute("SELECT COUNT(*) FROM Plantations")
if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO Plantations (name, planting_date, care_instructions)
    VALUES (?, ?, ?)
    """, [
        ("Rose Garden", "2023-05-15", "Water daily, provide sunlight"),
        ("Herb Section", "2023-06-20", "Trim regularly, water moderately"),
        ("Fruit Trees", "2023-07-10", "Fertilize monthly, protect from pests")
    ])
    conn.commit()

# Insert default admin account 
cursor.execute("SELECT * FROM Users WHERE username = ?", ("admin",))
if not cursor.fetchone():
    cursor.execute("INSERT INTO Users (username, password, role) VALUES (?, ?, ?)", ("admin", "123", "Admin"))
    conn.commit()

# ------------------- Color Settings -------------------
HEADER_COLOR = "#2e8b57"  # Sea green
BUTTON_COLOR = "#4682b4"  # Steel blue
TEXT_COLOR = "#ffffff"    # White
BG_COLOR = "#f0f8ff"      # Light blue

def send_sms_notification(contact_no, message_body):
    account_sid = 'acc_sid'
    auth_token = 'auth'
    twilio_number = 'twilo'
    
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message_body,
        from_=twilio_number,
        to=contact_no
    )
    return message.sid


def create_scrollable_frame(parent):
    outer_frame = tk.Frame(parent, bg=BG_COLOR)
    outer_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(outer_frame, bg=BG_COLOR, highlightthickness=0, borderwidth=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    return scrollable_frame


# ------------------- Admin Dashboard Function -------------------
def admin_dashboard():
    dashboard_window = tk.Toplevel()
    dashboard_window.title("Admin Dashboard")
    dashboard_window.geometry("800x600")
    dashboard_window.configure(bg=BG_COLOR)
    
    tk.Label(dashboard_window, text="Admin Dashboard", font=("Times New Roman", 20, "bold"),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=10).pack(fill=tk.X)
    
    total_orders = cursor.execute("SELECT COUNT(*) FROM Orders").fetchone()[0]
    total_withdrawal = cursor.execute("SELECT SUM(total_price) FROM Orders").fetchone()[0] or 0.0
    summary_frame = tk.Frame(dashboard_window, bg=BG_COLOR)
    summary_frame.pack(pady=10)
    
    tk.Label(summary_frame, text=f"Total Orders: {total_orders}", font=("Times New Roman", 14),
             bg=BG_COLOR).grid(row=0, column=0, padx=20)
    tk.Label(summary_frame, text=f"Total Withdrawal Amount: ₹{total_withdrawal:.2f}", font=("Times New Roman", 14),
             bg=BG_COLOR).grid(row=0, column=1, padx=20)
    
    tree_frame = tk.Frame(dashboard_window, bg=BG_COLOR)
    tree_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    columns = ("order_id", "product", "quantity", "total_price", "date", "status")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    
    tree.heading("order_id", text="Order ID")
    tree.column("order_id", anchor="center", width=80)
    
    tree.heading("product", text="Product")
    tree.column("product", anchor="center", width=120)
    
    tree.heading("quantity", text="Quantity")
    tree.column("quantity", anchor="center", width=80)
    
    tree.heading("total_price", text="Total Price")
    tree.column("total_price", anchor="center", width=100)
    
    tree.heading("date", text="Date")
    tree.column("date", anchor="center", width=150)
    
    tree.heading("status", text="Status")
    tree.column("status", anchor="center", width=100)
    
    tree.pack(fill=tk.BOTH, expand=True)
    
    # Fetch order history (including the actual status)
    cursor.execute("""
        SELECT o.id, p.name, o.quantity, o.total_price, o.date, o.status
        FROM Orders o 
        JOIN Products p ON o.product_id = p.id
        ORDER BY o.date DESC
    """)
    orders = cursor.fetchall()
    print("Orders found:", orders)  # Debug output
    
    for order in orders:
        # order[5] contains the actual status from the database
        tree.insert("", tk.END, values=(order[0], order[1], order[2], f"₹{order[3]:.2f}", order[4], order[5]))
    
    tk.Button(dashboard_window, text="Back", command=dashboard_window.destroy,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12), width=10).pack(pady=10)


def view_user_history(username):
    history_window = tk.Toplevel()
    history_window.title("My Order History")
    history_window.geometry("700x400")
    history_window.configure(bg=BG_COLOR)
    
    scrollable_frame = create_scrollable_frame(history_window)
    
    tk.Label(scrollable_frame, text="My Order History", font=("Times New Roman", 16, "bold"),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    
    columns = ("OrderID", "Product", "Quantity", "Price", "Date", "Status")
    tree = ttk.Treeview(scrollable_frame, columns=columns, show="headings", height=10)
    tree.heading("OrderID", text="Order ID")
    tree.heading("Product", text="Product")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Price", text="Price")
    tree.heading("Date", text="Date")
    tree.heading("Status", text="Status")
    
    tree.column("OrderID", anchor="center", width=80)
    tree.column("Product", anchor="center", width=150)
    tree.column("Quantity", anchor="center", width=80)
    tree.column("Price", anchor="center", width=100)
    tree.column("Date", anchor="center", width=150)
    tree.column("Status", anchor="center", width=100)
    
    tree.pack(fill=tk.BOTH, expand=True)
    
    def refresh_orders():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("""
        SELECT o.id, p.name, o.quantity, o.total_price, o.date, o.status
        FROM Orders o 
        JOIN Products p ON o.product_id = p.id
        WHERE o.username=?
        ORDER BY o.date DESC
        """, (username,))

        orders = cursor.fetchall()
        for od in orders:
            tree.insert("", tk.END, values=(od[0], od[1], od[2], f"₹{od[3]:.2f}", od[4], od[5]))
    
    refresh_orders()
    
    tk.Button(history_window, text="Refresh", command=refresh_orders,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12)).pack(pady=5)





# ------------------- Common Functions -------------------

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

def open_category_window(category, username):
    cat_window = tk.Toplevel()
    cat_window.title(category)
    cat_window.geometry("900x700")
    cat_window.configure(bg=BG_COLOR)

    header_frame = tk.Frame(cat_window, bg=HEADER_COLOR)
    header_frame.pack(fill=tk.X)
    tk.Label(header_frame, text=category, font=("Times New Roman", 20, "bold"),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=10).pack(side=tk.LEFT, padx=20)
    tk.Button(header_frame, text="🛒 Cart", font=("Times New Roman", 12, "bold"),
              bg=BUTTON_COLOR, fg=TEXT_COLOR, command=lambda: view_cart(username))\
              .pack(side=tk.RIGHT, padx=20, pady=5)

    products_frame = create_scrollable_frame(cat_window)
    
    cursor.execute("SELECT * FROM Products WHERE category = ?", (category,))
    products = cursor.fetchall()
    if not products:
        tk.Label(products_frame, text="No products available", font=("Times New Roman", 14),
                 bg=BG_COLOR, fg="red").pack(pady=20)
    else:
        for i, product in enumerate(products):     #grid view
            prod_frame = tk.Frame(products_frame, bg="white", bd=2, relief="groove", padx=10, pady=10)
            prod_frame.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky="nsew")
            
            try:
                if product[5]:
                    image_path = product[5].strip('"')
                    img = Image.open(image_path)
                    img = img.resize((150, 150))
                    photo = ImageTk.PhotoImage(img)
                    prod_frame.image = photo  
                    tk.Label(prod_frame, image=photo, bg="white").pack(pady=5)
                else:
                    tk.Label(prod_frame, text="No Image", font=("Times New Roman", 10), bg="white")\
                        .pack(pady=5)
            except Exception as e: 
                print("Error loading product image:", e)
                tk.Label(prod_frame, text="No Image", font=("Times New Roman", 10), bg="white")\
                    .pack(pady=5)
            
            tk.Label(prod_frame, text=product[1], font=("Times New Roman", 14, "bold"), bg="white")\
                .pack(pady=2)
            tk.Label(prod_frame, text=product[2], font=("Times New Roman", 10), bg="white", wraplength=150)\
                .pack(pady=2)
            tk.Label(prod_frame, text=f"Price: ₹{product[3]:.2f}", font=("Times New Roman", 12), bg="white")\
                .pack(pady=2)
            tk.Label(prod_frame, text=f"Stock: {product[4]}", font=("Times New Roman", 12), bg="white")\
                .pack(pady=2)
            
            btn_frame = tk.Frame(prod_frame, bg="white")
            btn_frame.pack(pady=5)
            tk.Button(btn_frame, text="Buy Now", font=("Times New Roman", 12, "bold"),
                      bg=BUTTON_COLOR, fg=TEXT_COLOR, width=10,
                      command=lambda p=product: buy_product(p, username))\
                      .grid(row=0, column=0, padx=5)
            tk.Button(btn_frame, text="Add to Cart", font=("Times New Roman", 12, "bold"),
                      bg=BUTTON_COLOR, fg=TEXT_COLOR, width=10,
                      command=lambda p=product: add_to_cart(p, username))\
                      .grid(row=0, column=1, padx=5)
        
        for col in range(3):
            products_frame.columnconfigure(col, weight=1)

def view_pots_by_category(username, role):
    pot_window = tk.Toplevel()
    pot_window.title("Pots By Category")
    pot_window.geometry("900x700")
    pot_window.configure(bg=BG_COLOR)

    header_frame = tk.Frame(pot_window, bg=HEADER_COLOR)
    header_frame.pack(fill=tk.X)

    tk.Label(header_frame, text="Pots By Category", font=("Times New Roman", 20, "bold"),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=10).pack(side=tk.LEFT, padx=20)
    
    tk.Button(header_frame, text="🛒 Cart", font=("Times New Roman", 12, "bold"),
              bg=BUTTON_COLOR, fg=TEXT_COLOR, command=lambda: view_cart(username))\
              .pack(side=tk.RIGHT, padx=20, pady=5)

    top_frame = tk.Frame(pot_window, bg=BG_COLOR)
    top_frame.pack(fill=tk.X, padx=20, pady=10)
    
    pot_categories = [
        ("Plastic Pots",  r"C:\Users\admin\Desktop\Mini\Images\plastic.jpeg"),
        ("Ceramic Pots",  r"C:\Users\admin\Desktop\Mini\Images\ceramic.jpg"),
        ("Designer Pots", r"C:\Users\admin\Desktop\Mini\Images\designer.jpg"),
        ("Earthen Pots",  r"C:\Users\admin\Desktop\Mini\Images\earthen.jpg"),
        ("Fiber Pots",    r"C:\Users\admin\Desktop\Mini\Images\fiber.jpg")
    ]
    
    cat_frame = tk.Frame(top_frame, bg=BG_COLOR)
    cat_frame.pack()

    def open_category_window(category):
        """
        Opens a new window that displays products for the given pot category.
        """
        cat_win = tk.Toplevel()
        cat_win.title(category)
        cat_win.geometry("900x700")
        cat_win.configure(bg=BG_COLOR)

        header_frame_cat = tk.Frame(cat_win, bg=HEADER_COLOR)
        header_frame_cat.pack(fill=tk.X)
        tk.Label(header_frame_cat, text=category, font=("Times New Roman", 20, "bold"),
                 bg=HEADER_COLOR, fg=TEXT_COLOR, pady=10).pack(side=tk.LEFT, padx=20)
        tk.Button(header_frame_cat, text="🛒 Cart", font=("Times New Roman", 12, "bold"),
                  bg=BUTTON_COLOR, fg=TEXT_COLOR, command=lambda: view_cart(username))\
                  .pack(side=tk.RIGHT, padx=20, pady=5)

        products_frame = create_scrollable_frame(cat_win)

        cursor.execute("SELECT * FROM Pots WHERE category = ?", (category,))
        products = cursor.fetchall()
        if not products:
            tk.Label(products_frame, text="No products available", font=("Times New Roman", 14),
                     bg=BG_COLOR, fg="red").pack(pady=20)
            return

        for i, product in enumerate(products):
            prod_frame = tk.Frame(products_frame, bg="white", bd=2, relief="groove", padx=10, pady=10)
            prod_frame.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky="nsew")
            
            try:
                if product[5]:
                    image_path = product[5].strip('"')
                    img = Image.open(image_path)
                    img = img.resize((150, 150))
                    photo = ImageTk.PhotoImage(img)
                    prod_frame.image = photo
                    tk.Label(prod_frame, image=photo, bg="white").pack(pady=5)
                else:
                    tk.Label(prod_frame, text="No Image", font=("Times New Roman", 10), bg="white")\
                        .pack(pady=5)
            except Exception as e:
                print("Error loading product image:", e)
                tk.Label(prod_frame, text="No Image", font=("Times New Roman", 10), bg="white")\
                    .pack(pady=5)

            tk.Label(prod_frame, text=product[1], font=("Times New Roman", 14, "bold"), bg="white")\
                .pack(pady=2)
            tk.Label(prod_frame, text=product[2], font=("Times New Roman", 10), bg="white", wraplength=150)\
                .pack(pady=2)
            tk.Label(prod_frame, text=f"Price: ₹{product[3]:.2f}", font=("Times New Roman", 12), bg="white")\
                .pack(pady=2)
            tk.Label(prod_frame, text=f"Stock: {product[4]}", font=("Times New Roman", 12), bg="white")\
                .pack(pady=2)

            btn_frame = tk.Frame(prod_frame, bg="white")
            btn_frame.pack(pady=5)
            tk.Button(btn_frame, text="Buy Now", font=("Times New Roman", 12, "bold"),
                      bg=BUTTON_COLOR, fg=TEXT_COLOR, width=10,
                      command=lambda p=product: buy_product(p, username))\
                      .grid(row=0, column=0, padx=5)
            tk.Button(btn_frame, text="Add to Cart", font=("Times New Roman", 12, "bold"),
                      bg=BUTTON_COLOR, fg=TEXT_COLOR, width=10,
                      command=lambda p=product: add_to_cart(p, username))\
                      .grid(row=0, column=1, padx=5)
        
        for col in range(3):
            products_frame.columnconfigure(col, weight=1)

    for idx, (cat_name, cat_image) in enumerate(pot_categories):
        r = idx // 4
        c = idx % 4

        card = tk.Frame(cat_frame, bg="white", bd=2, relief="raised", padx=5, pady=5)
        card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        try:
            img = Image.open(cat_image)
            img = img.resize((120, 120))
            photo = ImageTk.PhotoImage(img)
            card.image = photo  # keep reference
            tk.Label(card, image=photo, bg="white").pack(pady=5)
        except Exception as e:
            print("Error loading category image:", e)
            tk.Label(card, text="No Image", font=("Times New Roman", 10), bg="white")\
                .pack(pady=5)

        tk.Label(card, text=cat_name, font=("Times New Roman", 12, "bold"), bg="white")\
            .pack(pady=5)
        tk.Button(card, text="View", bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 10),
                  command=lambda name=cat_name: open_category_window(name))\
                  .pack(pady=5)

    max_cols = 4
    for col in range(max_cols):
        cat_frame.columnconfigure(col, weight=1)

    pot_window.mainloop()




def view_reviews():
    cursor.execute("""
    SELECT r.username, r.review_text, r.rating, p.name 
    FROM Reviews r JOIN Products p ON r.product_id = p.id
    """)
    reviews = cursor.fetchall()
    reviews_window = tk.Toplevel()
    reviews_window.title("Customer Reviews")
    reviews_window.geometry("600x400")
    reviews_window.configure(bg=BG_COLOR)
    tk.Label(reviews_window, text="Customer Reviews", font=("Times New Roman", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    frame = tk.Frame(reviews_window, bg=BG_COLOR)
    frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    for review in reviews:
        review_frame = tk.Frame(frame, bg="#ffffff", borderwidth=2, relief="groove", padx=10, pady=10)
        review_frame.pack(pady=5, fill=tk.X)
        tk.Label(review_frame, text=f"Product: {review[3]}", font=("Times New Roman", 12), bg="#ffffff").pack(anchor="w")
        tk.Label(review_frame, text=f"User: {review[0]}", font=("Times New Roman", 10), bg="#ffffff").pack(anchor="w")
        tk.Label(review_frame, text=f"Rating: {review[2]}/5", font=("Times New Roman", 10), bg="#ffffff").pack(anchor="w")
        tk.Label(review_frame, text=f"Review: {review[1]}", font=("Times New Roman", 10), bg="#ffffff", wraplength=500).pack(anchor="w")

def order_product(product):
    def submit_product_order():
        quantity = int(entry_quantity.get())
        if quantity > product[4]:
            messagebox.showerror("Error", "Insufficient stock!")
            return
        total_price = product[3] * quantity
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO Orders (product_id, quantity, total_price, date) VALUES (?, ?, ?, ?)",
                       (product[0], quantity, total_price, date))
        cursor.execute("UPDATE Products SET stock = stock - ? WHERE id = ?", (quantity, product[0]))
        conn.commit()
        messagebox.showinfo("Success", f"Order placed successfully! Total: ₹{total_price:.2f}")
        product_order_window.destroy()

    product_order_window = tk.Toplevel()
    product_order_window.title("Order Product")
    product_order_window.geometry("400x200")
    product_order_window.configure(bg=BG_COLOR)
    
    tk.Label(product_order_window, text=f"Order: {product[1]}", font=("Times New Roman", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    frame = tk.Frame(product_order_window, bg=BG_COLOR)
    frame.pack(pady=10)
    
    tk.Label(frame, text="Quantity:", bg=BG_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_quantity = tk.Entry(frame)
    entry_quantity.grid(row=0, column=1, pady=5)
    
    tk.Button(product_order_window, text="Submit", command=submit_product_order,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12), width=10).pack(pady=10)


from PIL import Image, ImageTk

def show_categories_window(username, role):
    cat_window = tk.Toplevel()
    cat_window.title("Top Categories")
    cat_window.geometry("900x600")
    cat_window.configure(bg=BG_COLOR)

    tk.Label(cat_window, text="Top Categories", font=("Times New Roman", 20, "bold"),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=10).pack(fill=tk.X)

    # List of categories: (Category Name, Image Path)
    categories = [
        ("Indoor Plants",     r"C:\Users\admin\Desktop\Mini\Images\indoor.jpg"),
        ("Outdoor Plants",    r"C:\Users\admin\Desktop\Mini\Images\oudoor.jpg"),
        ("Table Top Plants",  r"C:\Users\admin\Desktop\Mini\Images\table top plants.jpg"),
        ("Gifting Plants",    r"C:\Users\admin\Desktop\Mini\Images\gifting.jpg"),
        ("Flower Plants",     r"C:\Users\admin\Desktop\Mini\Images\flowers.jpg"),
        ("Green Wall Plants", r"C:\Users\admin\Desktop\Mini\Images\green wall.jpg"),
        ("Seasonal Plants",   r"C:\Users\admin\Desktop\Mini\Images\seasonal.jpg"),
        ("Hanging Plants",    r"C:\Users\admin\Desktop\Mini\Images\hanging.jpg")
    ]

    cat_frame = tk.Frame(cat_window, bg=BG_COLOR)
    cat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def on_category_click(cat_name):
        cat_window.destroy()
        view_plants_by_category(cat_name, username, role)

    rows = 2
    cols = 4
    for idx, (cat_name, cat_image) in enumerate(categories):
        r = idx // cols
        c = idx % cols
        frame = tk.Frame(cat_frame, bg="white", bd=2, relief="groove")
        frame.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")

        try:
            img = Image.open(cat_image)
            img = img.resize((150, 150))  
            photo = ImageTk.PhotoImage(img)
            frame.image = photo  
            tk.Label(frame, image=photo, bg="white").pack(pady=5)
        except Exception as e:
            print("Error loading image:", e)
            tk.Label(frame, text="No Image", bg="white", font=("Times New Roman", 10)).pack(pady=5)

        tk.Label(frame, text=cat_name, font=("Times New Roman", 14, "bold"), bg="white").pack(pady=5)
        tk.Button(frame, text="View", bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12),
                  width=10, command=lambda name=cat_name: on_category_click(name)).pack(pady=5)

    for r in range(rows):
        cat_frame.rowconfigure(r, weight=1)
    for c in range(cols):
        cat_frame.columnconfigure(c, weight=1)


def view_plants_by_category(category_name, username, role):
    cursor.execute("SELECT * FROM Products WHERE category = ?", (category_name,))
    products = cursor.fetchall()
    
    window = tk.Toplevel()
    window.title(f"{category_name} Plants")
    window.geometry("800x600")
    window.configure(bg=BG_COLOR)
    
    tk.Label(window, text=f"{category_name} Plants", font=("Times New Roman", 16, "bold"),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    
    if not products:
        tk.Label(window, text="No product right now", font=("Times New Roman", 14),
                 bg=BG_COLOR, fg="red").pack(pady=20)
        return

    scrollable_frame = create_scrollable_frame(window)
    
    for i, product in enumerate(products):
        product_frame = tk.Frame(scrollable_frame, bg="white", bd=2, relief="groove", padx=10, pady=10)
        product_frame.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky="nsew")
        
        try:
            if product[5]:
                image_path = product[5].strip('"')
                img = Image.open(image_path)
                img = img.resize((150, 150))  
                photo = ImageTk.PhotoImage(img)
                product_frame.image = photo  
                tk.Label(product_frame, image=photo, bg="white").pack(pady=5)
            else:
                tk.Label(product_frame, text="No Image", font=("Times New Roman", 10), bg="white").pack(pady=5)
        except Exception as e:
            print("Error loading image:", e)
            tk.Label(product_frame, text="No Image", font=("Times New Roman", 10), bg="white").pack(pady=5)
        
        tk.Label(product_frame, text=product[1], font=("Times New Roman", 14, "bold"), bg="white").pack(pady=2)
        tk.Label(product_frame, text=product[2], font=("Times New Roman", 10), bg="white", wraplength=150).pack(pady=2)
        tk.Label(product_frame, text=f"Price: ₹{product[3]:.2f}", font=("Times New Roman", 12), bg="white").pack(pady=2)
        tk.Label(product_frame, text=f"Stock: {product[4]}", font=("Times New Roman", 12), bg="white").pack(pady=2)
        
        btn_frame = tk.Frame(product_frame, bg="white")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Buy Now", font=("Times New Roman", 12, "bold"),
                  bg=BUTTON_COLOR, fg=TEXT_COLOR, width=10,
                  command=lambda p=product: buy_product(p, username)).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Add to Cart", font=("Times New Roman", 12, "bold"),
                  bg=BUTTON_COLOR, fg=TEXT_COLOR, width=10,
                  command=lambda p=product: add_to_cart(p, username)).grid(row=0, column=1, padx=5)
    
    for col in range(3):
        scrollable_frame.columnconfigure(col, weight=1)



import os
from tkinter import Tk, Toplevel, Frame, Label, Button

def nursery_tour():
    def play_video_external(video_path):
        """Plays the specified video in the default video player."""
        try:
            os.startfile(video_path) 
        except Exception as e:
            print("Error opening video:", e)

    nursery_window = Toplevel()
    nursery_window.title("Nursery Tour")
    nursery_window.geometry("800x600")

    nursery_window.configure(bg=BG_COLOR)
    
    scrollable_frame = create_scrollable_frame(nursery_window)
    
    Label(scrollable_frame, text="Nursery Tour", font=("Times New Roman", 16),
          bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill="x")
    
    cards = [
        ("Welcome to Our Nursery", "Experience a lush, green environment where plants thrive."),
        ("Our Greenhouse", "State-of-the-art greenhouse facilities to nurture delicate plants.")
    ]
    for title, content in cards:
        card = Frame(scrollable_frame, bg="white", bd=2, relief="raised")
        card.pack(fill="x", pady=10, padx=10)
        Label(card, text=title, font=("Times New Roman", 14, "bold"), bg="white", fg=TEXT_COLOR)\
            .pack(anchor="w", padx=10, pady=5)
        Label(card, text=content, font=("Times New Roman", 12), bg="white", fg="black", wraplength=700, justify="left")\
            .pack(anchor="w", padx=10, pady=5)
    
    video_cards = [
        ("Explore Our Nursery", "Watch a video tour of our nursery to explore all the beautiful plants and facilities!",
         r"C:\Users\admin\Desktop\Mini\Videos\nurserytour.webm"),
        ("Planting Techniques", "Learn about various techniques we use to ensure healthy plant growth.",
         r"C:\Users\admin\Desktop\Mini\Videos\plantingtechniques.mp4"),
        ("Seasonal Plant Care", "Watch how we take care of our plants during different seasons.",
         r"C:\Users\admin\Desktop\Mini\Videos\seasonalcare.mp4")
    ]
    for title, description, video_path in video_cards:
        video_card = Frame(scrollable_frame, bg="white", bd=2, relief="raised")
        video_card.pack(fill="x", pady=10, padx=10)
        Label(video_card, text=title, font=("Times New Roman", 14, "bold"),
              bg="white", fg=TEXT_COLOR).pack(anchor="w", padx=10, pady=5)
        Label(video_card, text=description, font=("Times New Roman", 12), bg="white", fg="black",
              wraplength=700, justify="left").pack(anchor="w", padx=10, pady=5)
        Button(video_card, text="Play Video", command=lambda path=video_path: play_video_external(path),
               bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12), width=10).pack(pady=10)


import tkinter as tk

def plantation():
    """Displays plantation blogs in a FAQ-style collapsible layout with chevrons (▶/▼)."""
    blogs = [
    ("🌹 How to Care for Roses", 
     "Roses thrive in well-drained soil and require plenty of sunlight to grow beautifully."
     "Water them deeply but infrequently to encourage strong and healthy root systems."
     "Regular pruning is essential to maintain their shape and remove dead or diseased growth."
     "Using organic fertilizers enhances their blooms and overall health."
     "Monitor for pests like aphids and treat them promptly with natural remedies or insecticidal soap. "
     "A little care ensures your roses will flourish and beautify your garden.",
        r"C:\Users\admin\Desktop\Mini\Images\ROSE.jpeg"),

    ("🥕 Growing Organic Vegetables", 
     "Organic vegetables require soil that is free from chemicals and rich in nutrients. "
     "Adding compost or natural fertilizers improves soil quality and boosts plant growth. "
     "Practicing crop rotation helps maintain soil health and reduces the risk of pests and diseases. "
     "Organic gardening produces healthier food, free of synthetic chemicals, and supports biodiversity in your garden. "
     "Regular watering and weeding ensure the vegetables grow without stress. "
     "Growing your own organic vegetables is a step toward sustainable living.",
     r"C:\Users\admin\Desktop\Mini\Images\veg.jpg"),

    ("🏠 Benefits of Indoor Plants", 
     "Indoor plants bring multiple benefits to your living space beyond their aesthetic appeal. "
     "They help purify the air by removing toxins and releasing oxygen. Plants like peace lilies, "
     "snake plants, and spider plants can boost humidity levels, which is beneficial for your skin "
     "and respiratory health. Caring for indoor plants has been shown to reduce stress and enhance mood."
     " They are also known to improve concentration and productivity, making them ideal for home offices. "
     "Adding greenery to your interiors transforms your space into a calm and inviting environment.",
     r"C:\Users\admin\Desktop\Mini\Images\money plant.jpg"),

    ("🌵 Succulent Care", 
     "Succulents are hardy plants that thrive with minimal care, "
     "making them perfect for busy individuals. "
     "They require bright, indirect sunlight for at least 4-6 hours a day to stay healthy. "
     "Plant them in well-draining soil to prevent water from pooling around their roots. Water them sparingly,"
     " allowing the soil to dry out completely between waterings. "
     "Overwatering is the most common mistake with succulents, so be cautious."
     " These versatile plants add charm to any space and are ideal for small pots or creative arrangements.",
     r"C:\Users\admin\Desktop\Mini\Images\succulent.jpg"),

    ("🌸 Caring for Orchids", 
     "Orchids are delicate plants that require a little extra attention but reward you with stunning blooms."
     "Place them in bright, indirect sunlight as direct sun can scorch their leaves. "
     "Water them once a week, allowing excess water to drain completely to avoid root rot."
     " Orchids thrive in moderate humidity levels, so consider using a humidifier or misting the leaves occasionally. "
     "Use a potting mix specifically designed for orchids, which usually includes bark and moss. "
     "With proper care, your orchids can bloom beautifully and last for years.",
     r"C:\Users\admin\Desktop\Mini\Images\orchid.jpg"),

    ("🌿 Herb Gardening Tips", 
     "Growing herbs at home is both rewarding and convenient for adding fresh flavors to your meals."
     " Most herbs prefer sunny locations with at least 6 hours of direct sunlight daily."
     " Use well-drained soil to prevent waterlogging and root rot."
     " Prune herbs regularly to promote bushier growth and prevent them from flowering too soon. "
     "Popular herbs like basil, mint, and thyme grow well in small pots or garden beds."
     " Water them consistently but avoid overwatering."
     " A home herb garden ensures a steady supply of fresh and organic ingredients for cooking.",
     r"C:\Users\admin\Desktop\Mini\Images\herb.jpg"),

    ("💜 Lavender Care", 
     "Lavender is a hardy and fragrant plant that adds beauty and a pleasant aroma to your garden. "
     "It thrives in full sunlight and requires well-drained, slightly alkaline soil to grow its best."
     " Water the plant sparingly, as overwatering can lead to root rot. "
     "Prune the plant annually after blooming to maintain its shape and encourage new growth."
     " Lavender is also resistant to pests and diseases, making it low-maintenance."
     " Its vibrant blooms and calming scent make it a favorite among gardeners.",
     r"C:\Users\admin\Desktop\Mini\Images\lavender.jpg"),

    ("🌱 Snake Plant Care", 
     "Snake plants are popular for their striking foliage and low-maintenance nature."
     " They tolerate a wide range of lighting conditions, including low light, but grow best in bright, "
     "indirect sunlight. Water the plant only when the soil is completely dry, "
     "as it is drought-tolerant and prone to overwatering. "
     "Snake plants are known for their air-purifying qualities,"
     " making them great additions to indoor spaces. They can also thrive in neglected areas, "
     "requiring minimal attention. Perfect for busy lifestyles, they make a stylish and functional addition to your decor.",
     r"C:\Users\admin\Desktop\Mini\Images\snake.jpg"),

    ("🌳 Bonsai Maintenance", 
     "Bonsais are miniature trees that require specialized care to maintain their beauty and health. "
     "They need bright light, so place them near a sunny window or in an outdoor space with filtered sunlight. "
     "Water them regularly to keep the soil moist but not soggy, as consistent hydration is key."
     " Prune the tree frequently to shape it and remove dead branches. Repot bonsais every few years "
     "to refresh the soil and support healthy root growth. With proper care, bonsais can become living "
     "works of art that last for generations.",
     r"C:\Users\admin\Desktop\Mini\Images\bonsai.jpg"),

    ("🍂 Compost Basics", 
     "Composting is an excellent way to recycle kitchen scraps and yard waste while enriching your garden soil."
     " Combine green materials like fruit peels and vegetable scraps with brown materials such as dry leaves and cardboard. "
     "Turn the compost pile regularly to aerate it and speed up the decomposition process."
     " Over time, the organic matter breaks down into a nutrient-rich soil amendment."
     " Compost improves soil structure, boosts plant growth, and reduces waste sent to landfills."
     " It’s an easy and sustainable practice for every gardener.",
     r"C:\Users\admin\Desktop\Mini\Images\composite.jpg")
]


    plantation_window = tk.Toplevel()
    plantation_window.title("Plantation Blogs")
    plantation_window.geometry("600x600")
    plantation_window.configure(bg="white")

    # Scrollable canvas setup
    canvas = tk.Canvas(plantation_window, bg="white")
    scrollbar = tk.Scrollbar(plantation_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Hold image references
    images = {}

    def toggle_faq(answer_frame, arrow_button):
        """Show/hide the answer frame and switch arrow icon."""
        if answer_frame.winfo_ismapped():
            answer_frame.pack_forget()
            arrow_button.config(text="▶")
        else:
            answer_frame.pack(fill="x", padx=10, pady=5)
            arrow_button.config(text="▼")

    for entry in blogs:
        # Unpack safely
        if len(entry) == 3:
            title, text, img_path = entry
        else:
            title, text = entry
            img_path = None

        container = tk.Frame(scrollable_frame, bg="white", bd=1, relief="solid")
        container.pack(fill="x", padx=10, pady=5)

        # Header row
        row_frame = tk.Frame(container, bg="white")
        row_frame.pack(fill="x")
        question_label = tk.Label(row_frame, text=title,
                                  font=("Times New Roman", 12, "bold"),
                                  bg="white", anchor="w")
        question_label.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        arrow_button = tk.Button(row_frame, text="▶",
                                 font=("Times New Roman", 12, "bold"),
                                 bg="white", bd=0, relief="flat")
        arrow_button.pack(side="right", padx=5)

        answer_frame = tk.Frame(container, bg="#F0F8FF")

        # Load image if path valid
        if img_path:
            if os.path.isfile(img_path):
                try:
                    pil_img = Image.open(img_path)
                    pil_img.thumbnail((550, 300))
                    photo = ImageTk.PhotoImage(pil_img)
                    images[img_path] = photo  # keep reference
                    img_label = tk.Label(answer_frame, image=photo, bg="#F0F8FF")
                    img_label.image = photo
                    img_label.pack(fill="x", padx=10, pady=(5, 0))
                except Exception as e:
                    print(f"Failed to load image at {img_path}: {e}")
            else:
                print(f"Image file not found: {img_path}")

        # Answer text
        answer_label = tk.Label(answer_frame, text=text,
                                font=("Times New Roman", 12), wraplength=550,
                                justify="left", bg="#F0F8FF")
        answer_label.pack(fill="both", expand=True, padx=10, pady=5)
        answer_frame.pack_forget()

        # Bind toggle
        def on_click(frame=answer_frame, arrow=arrow_button):
            toggle_faq(frame, arrow)
        question_label.bind("<Button-1>", lambda e: on_click())
        arrow_button.config(command=on_click)

def add_review():
    def submit_review():
        product_id = entry_product_id.get()
        username = entry_username.get()
        review_text = text_review.get("1.0", "end-1c")
        rating = entry_rating.get()
        cursor.execute("INSERT INTO Reviews (product_id, username, review_text, rating) VALUES (?, ?, ?, ?)",
                       (product_id, username, review_text, rating))
        conn.commit()
        messagebox.showinfo("Success", "Review added successfully!")
        review_window.destroy()

    review_window = tk.Toplevel()
    review_window.title("Add Review")
    review_window.geometry("400x300")
    review_window.configure(bg=BG_COLOR)
    
    tk.Label(review_window, text="Add a Review", font=("Times New Roman", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    
    frame = tk.Frame(review_window, bg=BG_COLOR)
    frame.pack(pady=10)
    
    tk.Label(frame, text="Product ID:", bg=BG_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_product_id = tk.Entry(frame)
    entry_product_id.grid(row=0, column=1, pady=5)
    
    tk.Label(frame, text="Username:", bg=BG_COLOR).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_username = tk.Entry(frame)
    entry_username.grid(row=1, column=1, pady=5)
    
    tk.Label(frame, text="Review:", bg=BG_COLOR).grid(row=2, column=0, sticky="nw", padx=10, pady=5)
    text_review = tk.Text(frame, height=5, width=30)
    text_review.grid(row=2, column=1, pady=5)
    
    tk.Label(frame, text="Rating (1-5):", bg=BG_COLOR).grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_rating = tk.Entry(frame)
    entry_rating.grid(row=3, column=1, pady=5)
    
    tk.Button(review_window, text="Submit", command=submit_review,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12), width=10).pack(pady=10)

def add_to_cart(product, username):
    global CART
    CART.append(product)
    messagebox.showinfo("Cart", f"{product[1]} added to cart.")

def view_cart(username):
    global CART
    cart_window = tk.Toplevel()
    cart_window.title("My Cart")
    cart_window.geometry("600x400")
    cart_window.configure(bg=BG_COLOR)
    
    container = tk.Frame(cart_window, bg=BG_COLOR)
    container.pack(fill=tk.BOTH, expand=True)
    
    scrollable_frame = create_scrollable_frame(container)
    
    tk.Label(scrollable_frame, text="My Cart", font=("Times New Roman", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    
    def normalize_cart_item(item):
        """
        Convert the item to a list and ensure the structure is:
        [id, name, price, quantity].
        Any extra data (like descriptions) is discarded.
        If quantity doesn't exist, default to 1.
        """
        if isinstance(item, tuple):
            item = list(item)
        
        if len(item) < 3:
            while len(item) < 3:
                item.append(0.0) 
            item.append(1)     
        else:
            try:
                float(item[2])  
                if len(item) == 3:
                    item.append(1)
                else:
                    item = item[:4]
            except ValueError:
                if len(item) >= 4:
                    price = item[3]
                    item = [item[0], item[1], price, 1]
                else:
                    item = [item[0], item[1], 0.0, 1]
        item[2] = float(item[2])
        item[3] = int(item[3])
        return item
    
    for i in range(len(CART)):
        CART[i] = normalize_cart_item(CART[i])
    
    def update_quantity(product, delta):
        product[3] += delta
        if product[3] <= 0:
            CART.remove(product)
        refresh_cart()

    def delete_product_from_cart(product):
        CART.remove(product)
        refresh_cart()

    def refresh_cart():
        cart_window.destroy()
        view_cart(username)
    
    if not CART:
        tk.Label(scrollable_frame, text="Your cart is empty.", font=("Times New Roman", 14),
                 bg=BG_COLOR).pack(pady=20)
    else:
        for product in CART:
            item_frame = tk.Frame(scrollable_frame, bg="white", bd=1, relief="solid", padx=5, pady=5)
            item_frame.pack(fill=tk.X, padx=10, pady=5)
            
            info = f"{product[1]} | Price: ₹{product[2]:.2f} | Qty: {product[3]}"
            tk.Label(item_frame, text=info, font=("Times New Roman", 14), bg="white")\
                .pack(side=tk.LEFT, padx=5)
            
            btn_frame = tk.Frame(item_frame, bg="white")
            btn_frame.pack(side=tk.RIGHT)
            
            tk.Button(btn_frame, text="-", font=("Times New Roman", 12, "bold"),
                      bg=BUTTON_COLOR, fg=TEXT_COLOR,
                      command=lambda p=product: update_quantity(p, -1))\
                      .pack(side=tk.LEFT, padx=2)
            
            tk.Button(btn_frame, text="+", font=("Times New Roman", 12, "bold"),
                      bg=BUTTON_COLOR, fg=TEXT_COLOR,
                      command=lambda p=product: update_quantity(p, 1))\
                      .pack(side=tk.LEFT, padx=2)
            
            tk.Button(btn_frame, text="🗑️", font=("Times New Roman", 12),
                      bg=BUTTON_COLOR, fg=TEXT_COLOR,
                      command=lambda p=product: delete_product_from_cart(p))\
                      .pack(side=tk.LEFT, padx=2)
    
    total = sum(p[2] * p[3] for p in CART)  
    
    def buy_now():
        if not CART:
            messagebox.showinfo("Cart Empty", "Your cart is empty. Please continue shopping.")
        else:
            cart_shipping_details(username, CART, len(CART), total)
    
    bottom_frame = tk.Frame(container, bg=BG_COLOR)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    tk.Label(bottom_frame, text=f"Total: ₹{total:.2f}", font=("Times New Roman", 14),
             bg=BG_COLOR, fg="black").pack(side=tk.LEFT, padx=10)
    
    tk.Button(bottom_frame, text="Buy Now", font=("Times New Roman", 12),
              bg=BUTTON_COLOR, fg=TEXT_COLOR, command=buy_now)\
              .pack(side=tk.RIGHT, padx=10)
    
    cart_window.mainloop()


def universal_process_payment(username, product, qty, total, full_name, address, state, city, zip_code, contact_no, method):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with sqlite3.connect("nursery.db", timeout=10) as local_conn:
            local_cursor = local_conn.cursor()

            # Insert the order using the local cursor
            local_cursor.execute("""
            INSERT INTO Orders (username, product_id, quantity, total_price, date, status, contact_no)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (username, product[0], qty, total, date, "Processing", contact_no))
            
            # Retrieve the newly created order ID
            order_id = local_cursor.lastrowid

            local_conn.commit()
            print("✅ Order placed successfully in the database!")

            # Fetch product name from the product details
            product_name = product[1]

            # Build success message with order details
            success_message = (
                f"Order placed successfully using {method}!\n\n"
                f"Shipping to:\n{full_name}\n{address}\n{state}, {city} - {zip_code}\n"
                f"Contact: {contact_no}"
                f"Total: ₹{total:.2f}\n"
                f"Status: Processing\n\n"
            )
            messagebox.showinfo("Success", success_message)

            # Build SMS body with order details
            if contact_no:
                sms_body = (
                    f"Your order has been placed!\n"
                    f"Order ID: {order_id}\n"
                    f"Product: {product_name}\n"
                    f"Quantity: {qty}\n"
                    f"Total: ₹{total:.2f}\n"
                    f"Status: Processing\n"
                    "Thank you for shopping with us!"
                )
                try:
                    sms_sid = send_sms_notification(contact_no, sms_body)
                    print("📩 SMS sent successfully, SID:", sms_sid)
                except Exception as e:
                    print("⚠️ Failed to send SMS:", e)

            global CART
            CART.clear()

    except sqlite3.Error as db_err:
        print(f"❌ Database Error: {db_err}")
        messagebox.showerror("Error", f"Failed to place order due to database error: {db_err}")

    except Exception as e:
        print(f"⚠️ Unexpected Error: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def cart_payment_method(username, product, qty, total_price, full_name, address, state, city, zip_code, contact_no):
    payment_window = tk.Toplevel()
    payment_window.title("Select Payment Method")
    payment_window.geometry("400x300")
    payment_window.configure(bg=BG_COLOR)
    
    tk.Label(payment_window, text=f"Total Amount: ₹{total_price:.2f}",
             font=("Helvetica", 16, "bold"), bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    
    tk.Label(payment_window, text="Choose Payment Method:",
             font=("Helvetica", 12, "bold"), bg=BG_COLOR).pack(pady=10)
    
    print(f"Debug: Received Total Price = {total_price}")


    def process_cart_payment(method):
        """Processes payment for all items in the cart at once."""
        print("inside proceaa")
        for prod in product:
            universal_process_payment(
                username, 
                prod, 
                prod[3],  
                prod[2] * prod[3],  
                full_name, 
                address, 
                state, 
                city, 
                zip_code, 
                contact_no, 
                method
            )
        # print("PID 3", {product[3]})
        # print("PID 2", {product[2]})
        # print("total", {total_price})
        # print("QTY",{qty})

        # universal_process_payment(
        #         username, 
        #         product, 
        #         qty,  
        #         total_price,  
        #         full_name, 
        #         address, 
        #         state, 
        #         city, 
        #         zip_code, 
        #         contact_no, 
        #         method
        #     )
        global CART
        CART.clear() 
        payment_window.destroy()
        messagebox.showinfo("Success", "All items ordered successfully!")

        def process_cart_payment_buynow(method):
            """Processes payment for all items in the cart at once."""
            print("inside proceaa")
            universal_process_payment(
                    username, 
                    product, 
                    qty,  
                    total_price,  
                    full_name, 
                    address, 
                    state, 
                    city, 
                    zip_code, 
                    contact_no, 
                    method
                )
            global CART
            CART.clear() 
            payment_window.destroy()
            messagebox.showinfo("Success", "All items ordered successfully!")

    def select_upi():
        if messagebox.askyesno("Confirm Payment", "Proceed with UPI payment?"):
            process_cart_payment("UPI")

    def select_card():
        """Handle credit/debit card payments separately."""
        payment_window.withdraw() 
        for prod in product:
            card_payment_window(username, prod, 1, prod[3], full_name, address, state, city, zip_code, contact_no)
        payment_window.destroy()  
    def select_cod():
        if messagebox.askyesno("Cash on Delivery", "Proceed with Cash on Delivery?"):
            process_cart_payment("Cash on Delivery")
    
    tk.Button(payment_window, text="UPI", command=select_upi,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Helvetica", 12, "bold"), width=20).pack(pady=5)

    tk.Button(payment_window, text="Credit/Debit/ATM Card", command=select_card,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Helvetica", 12, "bold"), width=20).pack(pady=5)

    tk.Button(payment_window, text="Cash on Delivery", command=select_cod,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Helvetica", 12, "bold"), width=20).pack(pady=5)

    payment_window.mainloop()

def cart_payment_method_buynow(username, product, qty, total_price, full_name, address, state, city, zip_code, contact_no):
    payment_window = tk.Toplevel()
    payment_window.title("Select Payment Method")
    payment_window.geometry("400x300")
    payment_window.configure(bg=BG_COLOR)
    
    tk.Label(payment_window, text=f"Total Amount: ₹{total_price:.2f}",
             font=("Helvetica", 16, "bold"), bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    
    tk.Label(payment_window, text="Choose Payment Method:",
             font=("Helvetica", 12, "bold"), bg=BG_COLOR).pack(pady=10)
    
    print(f"Debug: Received Total Price = {total_price}")


    def process_cart_payment(method):
        """Processes payment for all items in the cart at once."""
        print("inside proceaa")
        # for prod in product:
        #     print("PID ",{prod})
        #     universal_process_payment(
        #         username, 
        #         prod, 
        #         prod[3],  
        #         prod[2] * prod[3],  
        #         full_name, 
        #         address, 
        #         state, 
        #         city, 
        #         zip_code, 
        #         contact_no, 
        #         method
        #     )
        # print("PID 3", {product[3]})
        # print("PID 2", {product[2]})
        # print("total", {total_price})
        # print("QTY",{qty})

        universal_process_payment(
                username, 
                product, 
                qty,  
                total_price,  
                full_name, 
                address, 
                state, 
                city, 
                zip_code, 
                contact_no, 
                method
            )
        global CART
        CART.clear() 
        payment_window.destroy()
        messagebox.showinfo("Success", "All items ordered successfully!")

        # def process_cart_payment_buynow(method):
        #     """Processes payment for all items in the cart at once."""
        #     print("inside proceaa")
        #     universal_process_payment(
        #             username, 
        #             product, 
        #             qty,  
        #             total_price,  
        #             full_name, 
        #             address, 
        #             state, 
        #             city, 
        #             zip_code, 
        #             contact_no, 
        #             method
        #         )
        #     global CART
        #     CART.clear() 
        #     payment_window.destroy()
        #     messagebox.showinfo("Success", "All items ordered successfully!")

    def select_upi():
        if messagebox.askyesno("Confirm Payment", "Proceed with UPI payment?"):
            process_cart_payment("UPI")

    def select_card():
        """Handle credit/debit card payments separately for Buy Now."""
        payment_window.withdraw()
        # No loop needed for single product
        card_payment_window(username, product, qty, total_price, full_name, address, state, city, zip_code, contact_no)
        payment_window.destroy()

    def select_cod():
        if messagebox.askyesno("Cash on Delivery", "Proceed with Cash on Delivery?"):
            process_cart_payment("Cash on Delivery")
    
    tk.Button(payment_window, text="UPI", command=select_upi,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Helvetica", 12, "bold"), width=20).pack(pady=5)

    tk.Button(payment_window, text="Credit/Debit/ATM Card", command=select_card,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Helvetica", 12, "bold"), width=20).pack(pady=5)

    tk.Button(payment_window, text="Cash on Delivery", command=select_cod,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Helvetica", 12, "bold"), width=20).pack(pady=5)

    payment_window.mainloop()

def card_payment_window(username, product, qty, total, full_name, address, state, city, zip_code, contact_no):
    card_window = tk.Toplevel()
    card_window.title("Payment - Card")
    card_window.geometry("400x350")
    card_window.configure(bg=BG_COLOR)

    tk.Label(card_window, text=f"Total Amount: ₹{total:.2f}",
             font=("Helvetica", 16, "bold"), bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5)\
        .pack(fill=tk.X)
    
    frame_card = tk.Frame(card_window, bg=BG_COLOR)
    frame_card.pack(pady=10)
    
    tk.Label(frame_card, text="Card Holder Name:", font=("Helvetica", 12, "bold"), bg=BG_COLOR)\
        .grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entry_holder = tk.Entry(frame_card, width=30)
    entry_holder.grid(row=0, column=1, pady=5)
    
    tk.Label(frame_card, text="Card Number:", font=("Helvetica", 12, "bold"), bg=BG_COLOR)\
        .grid(row=1, column=0, sticky="w", padx=5, pady=5)
    entry_card_number = tk.Entry(frame_card, width=30)
    entry_card_number.grid(row=1, column=1, pady=5)
    
    tk.Label(frame_card, text="CVV:", font=("Helvetica", 12, "bold"), bg=BG_COLOR)\
        .grid(row=2, column=0, sticky="w", padx=5, pady=5)
    entry_cvv = tk.Entry(frame_card, width=30, show="*")
    entry_cvv.grid(row=2, column=1, pady=5)
    
    tk.Label(frame_card, text="Expiry Date (MM/YY):", font=("Helvetica", 12, "bold"), bg=BG_COLOR)\
        .grid(row=3, column=0, sticky="w", padx=5, pady=5)
    entry_expiry = tk.Entry(frame_card, width=30)
    entry_expiry.grid(row=3, column=1, pady=5)

    def format_expiry(event):
        text = entry_expiry.get().strip()
        if len(text) == 2 and '/' not in text:
            entry_expiry.insert(tk.END, "/")

    entry_expiry.bind("<KeyRelease>", format_expiry)

    def validate_card_number(event):
        card_no = entry_card_number.get().strip()
        if card_no and (not card_no.isdigit() or len(card_no) != 16):
            messagebox.showerror("Error", "Invalid card number! Please enter a 16-digit number.")
            entry_card_number.focus_set()

    def validate_cvv(event):
        cvv = entry_cvv.get().strip()
        if cvv and (not cvv.isdigit() or len(cvv) not in [3, 4]):
            messagebox.showerror("Error", "Invalid CVV! Please enter a 3 or 4-digit CVV.")
            entry_cvv.focus_set()

    def validate_expiry(event):
        expiry = entry_expiry.get().strip()
        pattern = r"^(0[1-9]|1[0-2])\/\d{2}$"
        if expiry and not re.match(pattern, expiry):
            messagebox.showerror("Error", "Invalid expiry date! Please enter in MM/YY format.")
            entry_expiry.focus_set()
        else:
            try:
                exp_month, exp_year = map(int, expiry.split('/'))
                current_year = int(datetime.now().strftime("%y"))
                current_month = datetime.now().month
                if exp_year < current_year or (exp_year == current_year and exp_month < current_month):
                    messagebox.showerror("Error", "Card expired! Please enter a valid expiry date.")
                    entry_expiry.focus_set()
            except:
                pass

    entry_card_number.bind("<FocusOut>", validate_card_number)
    entry_cvv.bind("<FocusOut>", validate_cvv)
    entry_expiry.bind("<FocusOut>", validate_expiry)
    
    def process_card_payment():
        holder = entry_holder.get().strip()
        card_no = entry_card_number.get().strip()
        cvv = entry_cvv.get().strip()
        expiry = entry_expiry.get().strip()
        
        if not holder:
            messagebox.showerror("Error", "Card Holder Name is required!")
            entry_holder.focus_set()
            return
        if not card_no:
            messagebox.showerror("Error", "Card Number is required!")
            entry_card_number.focus_set()
            return
        if not cvv:
            messagebox.showerror("Error", "CVV is required!")
            entry_cvv.focus_set()
            return
        if not expiry:
            messagebox.showerror("Error", "Expiry Date is required!")
            entry_expiry.focus_set()
            return
        
        if not (card_no.isdigit() and len(card_no) == 16):
            messagebox.showerror("Error", "Invalid card number! Please enter a 16-digit number.")
            entry_card_number.focus_set()
            return
        if not (cvv.isdigit() and len(cvv) in [3, 4]):
            messagebox.showerror("Error", "Invalid CVV! Please enter a 3 or 4-digit CVV.")
            entry_cvv.focus_set()
            return
        if not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", expiry):
            messagebox.showerror("Error", "Invalid expiry date! Please enter in MM/YY format.")
            entry_expiry.focus_set()
            return
        
        if messagebox.askyesno("Confirm Payment", "Are you sure you want to proceed with the payment?"):
            card_window.destroy()
            universal_process_payment(username, product, qty, total, full_name, address, state, city, zip_code, contact_no, "Credit/Debit/ATM Card")
    
    tk.Button(card_window, text="Pay Now", command=process_card_payment,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Helvetica", 12, "bold"), width=15)\
        .pack(pady=10)
    
API_KEY = "API_KEY"
HEADERS = {"X-CSCAPI-KEY": API_KEY}
state_iso_map = {}  

def get_states():
    global state_iso_map
    try:
        response = requests.get("https://api.countrystatecity.in/v1/countries/IN/states", headers=HEADERS)
        response.raise_for_status()
        states = response.json()
        state_iso_map = {state["name"]: state["iso2"] for state in states}
        return list(state_iso_map.keys())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch states: {e}")
        return []

def get_cities(state):
    if not state:
        return []
    iso_code = state_iso_map.get(state)
    if not iso_code:
        return []
    try:
        response = requests.get(f"https://api.countrystatecity.in/v1/countries/IN/states/{iso_code}/cities", headers=HEADERS)
        response.raise_for_status()
        cities = response.json()
        return [city["name"] for city in cities]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch cities for {state}: {e}")
        return []


def cart_shipping_details(username, product, qty, total_price):
    shipping_window = tk.Toplevel()
    shipping_window.title("Shipping Details")
    shipping_window.geometry("400x500")
    shipping_window.configure(bg=BG_COLOR)
    
    tk.Label(shipping_window, text=f"Total Amount: ₹{total_price:.2f}", 
             font=("Helvetica", 16, "bold"), bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5)\
             .pack(fill=tk.X)
    
    frame_addr = tk.Frame(shipping_window, bg=BG_COLOR)
    frame_addr.pack(pady=10)
    
    tk.Label(frame_addr, text="Full Name:", font=("Helvetica", 12, "bold"), bg=BG_COLOR)\
        .grid(row=0, column=0, sticky="w", padx=5, pady=2)
    entry_name = tk.Entry(frame_addr, width=30)
    entry_name.grid(row=0, column=1, pady=2)
    
    tk.Label(frame_addr, text="Address:", font=("Helvetica", 12, "bold"), bg=BG_COLOR)\
        .grid(row=1, column=0, sticky="nw", padx=5, pady=2)
    text_address = tk.Text(frame_addr, width=30, height=3)
    text_address.grid(row=1, column=1, pady=2)
    
    tk.Label(frame_addr, text="State:", font=("Helvetica", 12, "bold"), bg=BG_COLOR)\
        .grid(row=2, column=0, sticky="w", padx=5, pady=2)
    state_var = tk.StringVar()
    state_dropdown = ttk.Combobox(frame_addr, textvariable=state_var, width=27, state="readonly")
    state_dropdown.grid(row=2, column=1, pady=2)
    state_dropdown['values'] = get_states()  # Load states

    tk.Label(frame_addr, text="City:", font=("Helvetica", 12, "bold"), bg=BG_COLOR)\
        .grid(row=3, column=0, sticky="w", padx=5, pady=2)
    city_var = tk.StringVar()
    city_dropdown = ttk.Combobox(frame_addr, textvariable=city_var, width=27, state="readonly")
    city_dropdown.grid(row=3, column=1, pady=2)

    def update_cities(event):
        selected_state = state_var.get()
        city_dropdown['values'] = get_cities(selected_state)
        city_dropdown.current(0)  

    state_dropdown.bind("<<ComboboxSelected>>", update_cities)
    
    tk.Label(frame_addr, text="Zip Code:", font=("Helvetica", 12, "bold"), bg=BG_COLOR)\
        .grid(row=4, column=0, sticky="w", padx=5, pady=2)
    entry_zip = tk.Entry(frame_addr, width=30)
    entry_zip.grid(row=4, column=1, pady=2)
    
    tk.Label(frame_addr, text="Contact No:", font=("Helvetica", 12, "bold"), bg=BG_COLOR)\
        .grid(row=5, column=0, sticky="w", padx=5, pady=2)
    entry_contact = tk.Entry(frame_addr, width=30)
    entry_contact.grid(row=5, column=1, pady=2)
    
    def proceed_to_payment():
        full_name = entry_name.get().strip()
        address = text_address.get("1.0", "end-1c").strip()
        state = state_var.get().strip()
        city = city_var.get().strip()
        zip_code = entry_zip.get().strip()
        contact_no = entry_contact.get().strip()
    
        if not (full_name and address and state and city and zip_code and contact_no):
            messagebox.showerror("Error", "Please fill in all shipping details!")
            return
        cart_payment_method(username, product, qty, total_price, full_name, address, state, city, zip_code, contact_no)

    
    tk.Button(shipping_window, text="Proceed to Payment", font=("Helvetica", 12, "bold"),
              bg=BUTTON_COLOR, fg=TEXT_COLOR, command=proceed_to_payment)\
              .pack(pady=20)
    
    shipping_window.mainloop()



def buy_products(username):
    """Display all products (plants and pots) for placing an order with images, details, and action buttons."""
    plants = cursor.execute("SELECT * FROM Products").fetchall()
    try:
        pots = cursor.execute("SELECT * FROM Pots").fetchall()
    except sqlite3.Error as e:
        print("Error fetching pots:", e)
        pots = []
        
    all_products = plants + pots

    window = tk.Toplevel()
    window.title("Place Order")
    window.geometry("1100x700")  
    window.configure(bg=BG_COLOR)
    
    header_frame = tk.Frame(window, bg=BG_COLOR)
    header_frame.pack(fill=tk.X)
    
    tk.Label(header_frame, text="Available Products", font=("Times New Roman", 16, "bold"),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=10).pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    cart_button = tk.Button(header_frame, text="🛒 Cart", font=("Times New Roman", 12, "bold"),
                            bg=BUTTON_COLOR, fg=TEXT_COLOR,
                            command=lambda: view_cart(username))
    cart_button.pack(side=tk.RIGHT, padx=10, pady=10)
    
    scrollable_frame = create_scrollable_frame(window)
    
    for i, product in enumerate(all_products):
        product_frame = tk.Frame(scrollable_frame, bg="white", bd=2, relief="groove", padx=10, pady=10)
        product_frame.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky="nsew")
        
        try:
            if product[5]:
                image_path = product[5].strip('"') 
                img = Image.open(image_path)
                img = img.resize((130, 130))
                photo = ImageTk.PhotoImage(img)
                product_frame.image = photo 
                tk.Label(product_frame, image=photo, bg="white").pack(pady=5)
            else:
                tk.Label(product_frame, text="No Image", font=("Times New Roman", 10), bg="white").pack(pady=5)
        except Exception as e:
            print("Error loading image:", e)
            tk.Label(product_frame, text="No Image", font=("Times New Roman", 10), bg="white").pack(pady=5)
        
        tk.Label(product_frame, text=product[1], font=("Times New Roman", 14, "bold"), bg="white").pack(pady=2)
        tk.Label(product_frame, text=product[2], font=("Times New Roman", 10), bg="white", wraplength=150).pack(pady=2)
        tk.Label(product_frame, text=f"Price: ₹{product[3]:.2f}", font=("Times New Roman", 12), bg="white").pack(pady=2)
        tk.Label(product_frame, text=f"Stock: {product[4]}", font=("Times New Roman", 12), bg="white").pack(pady=2)
        
        btn_frame = tk.Frame(product_frame, bg="white")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Buy Now", font=("Times New Roman", 12, "bold"),
                  bg=BUTTON_COLOR, fg=TEXT_COLOR, width=10,
                  command=lambda p=product: buy_product(p, username))\
                  .grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Add to Cart", font=("Times New Roman", 12, "bold"),
                  bg=BUTTON_COLOR, fg=TEXT_COLOR, width=10,
                  command=lambda p=product: add_to_cart(p, username))\
                  .grid(row=0, column=1, padx=5)
    
    for col in range(3):
        scrollable_frame.columnconfigure(col, weight=1, minsize=330)



def buy_product(product, username):
    """Initiate the buying process for a single product with shipping details and then call the payment method window."""
    buy_window = tk.Toplevel()
    buy_window.title("Buy Product")
    buy_window.geometry("400x500")
    buy_window.configure(bg=BG_COLOR)
    
    parent_frame = buy_window 

    tk.Label(parent_frame, text=f"Buy Now: {product[1]}", font=("Times New Roman", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    tk.Label(parent_frame, text=product[2], font=("Times New Roman", 12), bg=BG_COLOR, wraplength=350).pack(pady=5)
    tk.Label(parent_frame, text=f"Price: ₹{product[3]:.2f}", font=("Times New Roman", 12), bg=BG_COLOR).pack(pady=5)
    
    frame_qty = tk.Frame(parent_frame, bg=BG_COLOR)
    frame_qty.pack(pady=5)
    tk.Label(frame_qty, text="Quantity:", font=("Times New Roman", 12, "bold"), bg=BG_COLOR)\
        .grid(row=0, column=0, padx=5)
    entry_qty = tk.Entry(frame_qty, width=5)
    entry_qty.grid(row=0, column=1)
    entry_qty.insert(0, "1")
    
    tk.Label(parent_frame, text="Shipping Details", font=("Times New Roman", 14),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X, pady=10)
    frame_addr = tk.Frame(parent_frame, bg=BG_COLOR)
    frame_addr.pack(pady=5)
    
    tk.Label(frame_addr, text="Full Name:", font=("Times New Roman", 12, "bold"), bg=BG_COLOR)\
        .grid(row=0, column=0, sticky="w", padx=5, pady=2)
    entry_name = tk.Entry(frame_addr, width=30)
    entry_name.grid(row=0, column=1, pady=2)
    
    tk.Label(frame_addr, text="Address:", font=("Times New Roman", 12, "bold"), bg=BG_COLOR)\
        .grid(row=1, column=0, sticky="nw", padx=5, pady=2)
    text_address = tk.Text(frame_addr, width=30, height=3)
    text_address.grid(row=1, column=1, pady=2)
    
    tk.Label(frame_addr, text="State:", font=("Times New Roman", 12, "bold"), bg=BG_COLOR)\
        .grid(row=2, column=0, sticky="w", padx=5, pady=2)
    state_var = tk.StringVar()
    state_dropdown = ttk.Combobox(frame_addr, textvariable=state_var, width=27, state="readonly")
    state_dropdown.grid(row=2, column=1, pady=2)
    state_dropdown['values'] = get_states()  

    tk.Label(frame_addr, text="City:", font=("Times New Roman", 12, "bold"), bg=BG_COLOR)\
        .grid(row=3, column=0, sticky="w", padx=5, pady=2)
    city_var = tk.StringVar()
    city_dropdown = ttk.Combobox(frame_addr, textvariable=city_var, width=27, state="readonly")
    city_dropdown.grid(row=3, column=1, pady=2)

    def update_cities(event):
        selected_state = state_var.get()
        city_dropdown['values'] = get_cities(selected_state)
        city_dropdown.current(0)  

    state_dropdown.bind("<<ComboboxSelected>>", update_cities)
    
    tk.Label(frame_addr, text="Zip Code:", font=("Times New Roman", 12, "bold"), bg=BG_COLOR)\
        .grid(row=4, column=0, sticky="w", padx=5, pady=2)
    entry_zip = tk.Entry(frame_addr, width=30)
    entry_zip.grid(row=4, column=1, pady=2)
    
    tk.Label(frame_addr, text="Contact No:", font=("Times New Roman", 12, "bold"), bg=BG_COLOR)\
        .grid(row=5, column=0, sticky="w", padx=5, pady=2)
    entry_contact = tk.Entry(frame_addr, width=30)
    entry_contact.grid(row=5, column=1, pady=2)
    
    def proceed_to_payment():
        try:
            qty = int(entry_qty.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity!")
            return
        
        full_name = entry_name.get().strip()
        address = text_address.get("1.0", "end-1c").strip()
        state = state_var.get().strip()
        city = city_var.get().strip()
        zip_code = entry_zip.get().strip()
        contact_no = entry_contact.get().strip()
        
        if not (full_name and address and state and city and zip_code and contact_no):
            messagebox.showerror("Error", "Please fill in all shipping details!")
            return
        
        total_price = product[3] * qty
        print({total_price},{product})
        cart_payment_method_buynow(username, product, qty, total_price, full_name, address, state, city, zip_code, contact_no)
        buy_window.destroy()
    
    tk.Button(parent_frame, text="Proceed to Payment", command=proceed_to_payment,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12), width=15).pack(pady=10)



def place_order_and_update(product, qty, total_price, username, full_name, address, city, zip_code, contact_no):
    from datetime import datetime
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        local_conn = sqlite3.connect("nursery.db", timeout=10)
        local_cursor = local_conn.cursor()
        local_cursor.execute("PRAGMA journal_mode=WAL;")
        
        local_cursor.execute("""
            INSERT INTO Orders (product_id, quantity, total_price, date, username, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (product[0], qty, total_price, date, username, "Processing"))
        
        local_cursor.execute("UPDATE Products SET stock = stock - ? WHERE id = ?", (qty, product[0]))
        
        local_conn.commit() 
        
        print("Order inserted, stock updated, and committed.")
        messagebox.showinfo("Success", f"Order placed successfully!\n\n"
                                       f"Name: {full_name}\nAddress: {address}\nCity: {city}\n"
                                       f"Zip Code: {zip_code}\nContact: {contact_no}")
        local_cursor.close()
        local_conn.close()
    except Exception as e:
        local_conn.rollback()
        print("Error inserting order:", e)
        messagebox.showerror("Database Error", f"Failed to place order: {e}")
        local_cursor.close()
        local_conn.close()


# ------------------- Admin Only Functions -------------------
def add_product():
    add_window = tk.Toplevel()
    add_window.title("Add New Product")
    add_window.geometry("400x450")
    add_window.configure(bg=BG_COLOR)
    
    tk.Label(add_window, text="Add New Product", font=("Times New Roman", 16, "bold"),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    
    frame = tk.Frame(add_window, bg=BG_COLOR)
    frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
    
    # Product Name
    tk.Label(frame, text="Name:", bg=BG_COLOR, font=("Times New Roman", 12, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_name = tk.Entry(frame, font=("Times New Roman", 12))
    entry_name.grid(row=0, column=1, pady=5)
    
    # Description
    tk.Label(frame, text="Description:", bg=BG_COLOR, font=("Times New Roman", 12, "bold")).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_description = tk.Entry(frame, font=("Times New Roman", 12))
    entry_description.grid(row=1, column=1, pady=5)
    
    # Price
    tk.Label(frame, text="Price:", bg=BG_COLOR, font=("Times New Roman", 12, "bold")).grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_price = tk.Entry(frame, font=("Times New Roman", 12))
    entry_price.grid(row=2, column=1, pady=5)
    
    # Stock
    tk.Label(frame, text="Stock:", bg=BG_COLOR, font=("Times New Roman", 12, "bold")).grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_stock = tk.Entry(frame, font=("Times New Roman", 12))
    entry_stock.grid(row=3, column=1, pady=5)
    
    # Type Dropdown (Plant or Pot)
    tk.Label(frame, text="Type:", bg=BG_COLOR, font=("Times New Roman", 12, "bold")).grid(row=4, column=0, sticky="w", padx=10, pady=5)
    types = ["Plant", "Pot"]
    selected_type = tk.StringVar(frame)
    selected_type.set(types[0])
    type_menu = tk.OptionMenu(frame, selected_type, *types)
    type_menu.config(font=("Times New Roman", 12))
    type_menu.grid(row=4, column=1, pady=5)
    
    tk.Label(frame, text="Category:", bg=BG_COLOR, font=("Times New Roman", 12, "bold")).grid(row=5, column=0, sticky="w", padx=10, pady=5)
    plant_categories = ["Indoor Plants", "Outdoor Plants", "Table Top Plants", "Gifting Plants", 
                        "Flower Plants", "Green Wall Plants", "Seasonal Plants", "Hanging Plants"]
    pot_categories = ["Plastic Pots", "Ceramic Pots", "Designer Pots", "Earthen Pots", "Fiber Pots"]
    
    selected_category = tk.StringVar(frame)
    selected_category.set(plant_categories[0]) 
    
    option_menu = tk.OptionMenu(frame, selected_category, *plant_categories)
    option_menu.config(font=("Times New Roman", 12))
    option_menu.grid(row=5, column=1, pady=5)
    
    def update_categories(*args):
        prod_type = selected_type.get()
        if prod_type == "Plant":
            options = plant_categories
        else:
            options = pot_categories
        menu = option_menu["menu"]
        menu.delete(0, "end")
        for option in options:
            menu.add_command(label=option, command=lambda value=option: selected_category.set(value))
        if options:
            selected_category.set(options[0])
    
    selected_type.trace("w", update_categories)
    
    tk.Label(frame, text="Image Path:", bg=BG_COLOR, font=("Times New Roman", 12, "bold")).grid(row=6, column=0, sticky="w", padx=10, pady=5)
    entry_image = tk.Entry(frame, font=("Times New Roman", 12))
    entry_image.grid(row=6, column=1, pady=5)
    
    def browse_image():
        filename = filedialog.askopenfilename(
            parent=add_window, 
            title="Select Image", 
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")]
        )
        if filename:
            entry_image.delete(0, tk.END)  
            entry_image.insert(0, filename)  

    
    tk.Button(frame, text="Browse", command=browse_image,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12)).grid(row=6, column=2, padx=5, pady=5)
    
    def submit_product():
        name = entry_name.get().strip()
        description = entry_description.get().strip()
        try:
            price = float(entry_price.get().strip())
            stock = int(entry_stock.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Invalid price or stock!")
            return
        product_type = selected_type.get().strip()
        category = selected_category.get().strip()
        image_path = entry_image.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        
        if product_type == "Plant":
            cursor.execute(
                "INSERT INTO Products (name, description, price, stock, image_path, category) VALUES (?, ?, ?, ?, ?, ?)",
                (name, description, price, stock, image_path, category)
            )
        else:
            cursor.execute(
                "INSERT INTO Pots (name, description, price, stock, image_path, category, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name, description, price, stock, image_path, category, "Available")
            )
        conn.commit()
        messagebox.showinfo("Success", "Product added successfully!")
        add_window.destroy()
    
    tk.Button(add_window, text="Add Product", command=submit_product,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12), width=10).pack(pady=10)
    tk.Button(add_window, text="Back", command=add_window.destroy,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12), width=10).pack(pady=5)



def delete_product():
    delete_window = tk.Toplevel()
    delete_window.title("Delete Product")
    delete_window.geometry("300x200")
    delete_window.configure(bg=BG_COLOR)
    
    tk.Label(delete_window, text="Delete Product", font=("Times New Roman", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    
    frame = tk.Frame(delete_window, bg=BG_COLOR)
    frame.pack(pady=20)
    
    tk.Label(frame, text="Product ID:", bg=BG_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_id = tk.Entry(frame)
    entry_id.grid(row=0, column=1, pady=5)
    
    def submit_delete():
        product_id = entry_id.get()
        cursor.execute("SELECT * FROM Products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        if not product:
            messagebox.showerror("Error", "Product not found!")
            return
        cursor.execute("DELETE FROM Products WHERE id = ?", (product_id,))
        conn.commit()
        messagebox.showinfo("Success", "Product deleted successfully!")
        delete_window.destroy()
    
    tk.Button(delete_window, text="Delete Product", command=submit_delete,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12), width=10).pack(pady=10)
    tk.Button(delete_window, text="Back", command=delete_window.destroy,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12), width=10).pack(pady=5)

def edit_product():
    edit_window = tk.Toplevel()
    edit_window.title("Edit Product")
    edit_window.geometry("400x500")
    edit_window.configure(bg=BG_COLOR)
    
    tk.Label(edit_window, text="Edit Product", font=("Times New Roman", 16, "bold"),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    
    frame_search = tk.Frame(edit_window, bg=BG_COLOR)
    frame_search.pack(pady=10)
    
    tk.Label(frame_search, text="Product ID:", bg=BG_COLOR, font=("Times New Roman", 12, "bold"))\
        .grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_id = tk.Entry(frame_search, font=("Times New Roman", 12))
    entry_id.grid(row=0, column=1, pady=5)
    
    tk.Label(frame_search, text="OR", bg=BG_COLOR, font=("Times New Roman", 12, "bold"))\
        .grid(row=1, column=0, columnspan=2, pady=5)
    
    tk.Label(frame_search, text="Product Name:", bg=BG_COLOR, font=("Times New Roman", 12, "bold"))\
        .grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_name_search = tk.Entry(frame_search, font=("Times New Roman", 12))
    entry_name_search.grid(row=2, column=1, pady=5)
    
    def load_product():
        prod_id_str = entry_id.get().strip()
        prod_name = entry_name_search.get().strip()
        
        if not prod_id_str and not prod_name:
            messagebox.showerror("Error", "Please enter a Product ID or Product Name!")
            return

        if prod_id_str:
            try:
                prod_id = int(prod_id_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid Product ID. Please enter a numeric value.")
                return
            cursor.execute("SELECT * FROM Products WHERE id = ?", (prod_id,))
        else:
            cursor.execute("SELECT * FROM Products WHERE name = ?", (prod_name,))
        
        product = cursor.fetchone()
        if not product:
            messagebox.showerror("Error", "Product not found!")
            return
        
        frame_edit = tk.Frame(edit_window, bg=BG_COLOR)
        frame_edit.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Name
        tk.Label(frame_edit, text="Name:", font=("Times New Roman", 12, "bold"), bg=BG_COLOR)\
            .grid(row=0, column=0, sticky="w", padx=10, pady=5)
        entry_name_edit = tk.Entry(frame_edit, font=("Times New Roman", 12))
        entry_name_edit.grid(row=0, column=1, pady=5)
        entry_name_edit.insert(0, product[1])
        
        # Description
        tk.Label(frame_edit, text="Description:", font=("Times New Roman", 12, "bold"), bg=BG_COLOR)\
            .grid(row=1, column=0, sticky="w", padx=10, pady=5)
        entry_description = tk.Entry(frame_edit, font=("Times New Roman", 12))
        entry_description.grid(row=1, column=1, pady=5)
        entry_description.insert(0, product[2])
        
        # Price
        tk.Label(frame_edit, text="Price:", font=("Times New Roman", 12, "bold"), bg=BG_COLOR)\
            .grid(row=2, column=0, sticky="w", padx=10, pady=5)
        entry_price = tk.Entry(frame_edit, font=("Times New Roman", 12))
        entry_price.grid(row=2, column=1, pady=5)
        entry_price.insert(0, product[3])
        
        # Stock
        tk.Label(frame_edit, text="Stock:", font=("Times New Roman", 12, "bold"), bg=BG_COLOR)\
            .grid(row=3, column=0, sticky="w", padx=10, pady=5)
        entry_stock = tk.Entry(frame_edit, font=("Times New Roman", 12))
        entry_stock.grid(row=3, column=1, pady=5)
        entry_stock.insert(0, product[4])
        
        # Image Path
        tk.Label(frame_edit, text="Image Path:", font=("Times New Roman", 12, "bold"), bg=BG_COLOR)\
            .grid(row=4, column=0, sticky="w", padx=10, pady=5)
        entry_image = tk.Entry(frame_edit, font=("Times New Roman", 12))
        entry_image.grid(row=4, column=1, pady=5)
        entry_image.insert(0, product[5] if product[5] else "")
        
        # Category Dropdown
        tk.Label(frame_edit, text="Category:", font=("Times New Roman", 12, "bold"), bg=BG_COLOR)\
            .grid(row=5, column=0, sticky="w", padx=10, pady=5)
        categories = ["Indoor Plants", "Outdoor Plants", "Table Top Plants", "Gifting Plants", 
                      "Flower Plants", "Green Wall Plants", "Seasonal Plants", "Hanging Plants"]
        selected_category = tk.StringVar(frame_edit)
        if len(product) > 6 and product[6]:
            selected_category.set(product[6])
        else:
            selected_category.set(categories[0])
        dropdown = tk.OptionMenu(frame_edit, selected_category, *categories)
        dropdown.config(font=("Times New Roman", 12))
        dropdown.grid(row=5, column=1, pady=5)
        
        def update_product():
            new_name = entry_name_edit.get().strip()
            new_description = entry_description.get().strip()
            try:
                new_price = float(entry_price.get().strip())
                new_stock = int(entry_stock.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Invalid price or stock!")
                return
            new_image = entry_image.get().strip()
            new_category = selected_category.get().strip()
            
            if not new_name:
                messagebox.showerror("Error", "Name cannot be empty!")
                return
            
            cursor.execute("""
                UPDATE Products
                SET name = ?, description = ?, price = ?, stock = ?, image_path = ?, category = ?
                WHERE id = ?
            """, (new_name, new_description, new_price, new_stock, new_image, new_category, product[0]))
            conn.commit()
            messagebox.showinfo("Success", "Product updated successfully!")
            edit_window.destroy()
        
        tk.Button(frame_edit, text="Update", command=update_product,
                  bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12), width=10)\
            .grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(frame_edit, text="Back", command=edit_window.destroy,
                  bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12), width=10)\
            .grid(row=7, column=0, columnspan=2, pady=5)
    
    tk.Button(frame_search, text="Load Product", command=load_product,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12), width=10)\
        .grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(frame_search, text="Back", command=edit_window.destroy,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12), width=10)\
        .grid(row=4, column=0, columnspan=2, pady=5)

   
def update_order_status():
    status_window = tk.Toplevel()
    status_window.title("Update Order Status")
    status_window.geometry("400x250")
    status_window.configure(bg=BG_COLOR)
    
    tk.Label(status_window, text="Update Order Status", font=("Times New Roman", 16, "bold"),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=10).pack(fill=tk.X)
    
    frame = tk.Frame(status_window, bg=BG_COLOR)
    frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
    
    # Order ID input
    tk.Label(frame, text="Order ID:", font=("Times New Roman", 12, "bold"), bg=BG_COLOR)\
        .grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_order_id = tk.Entry(frame, font=("Times New Roman", 12))
    entry_order_id.grid(row=0, column=1, pady=5)
    
    # Status dropdown 
    tk.Label(frame, text="New Status:", font=("Times New Roman", 12, "bold"), bg=BG_COLOR)\
        .grid(row=1, column=0, sticky="w", padx=10, pady=5)
    statuses = ["Processing", "Shipped", "Delivered", "Cancelled"]
    new_status = tk.StringVar(frame)
    new_status.set(statuses[0])  
    dropdown = tk.OptionMenu(frame, new_status, *statuses)
    dropdown.config(font=("Times New Roman", 12))
    dropdown.grid(row=1, column=1, pady=5)
    
    def update_status():
        order_id = entry_order_id.get().strip()
        status_value = new_status.get().strip()
        if not order_id:
            messagebox.showerror("Error", "Please enter an Order ID!")
            return
        try:
            cursor.execute("UPDATE Orders SET status = ? WHERE id = ?", (status_value, order_id))
            conn.commit()
            
            # Fetch order details
            cursor.execute("SELECT product_id, quantity, total_price, contact_no FROM Orders WHERE id = ?", (order_id,))
            order_details = cursor.fetchone()
            if order_details:
                product_id, quantity, total_price, contact_no = order_details
                # Get product name
                cursor.execute("SELECT name FROM Products WHERE id = ?", (product_id,))
                product = cursor.fetchone()
                product_name = product[0] if product else "Unknown Product"
                
                # Prepare SMS
                sms_body = (
                    f"Your order status has been updated.\n"
                    f"Order ID: {order_id}\n"
                    f"New Status: {status_value}\n"
                    f"Product: {product_name}\n"
                    f"Quantity: {quantity}\n"
                    f"Total: ₹{total_price:.2f}\n"
                    "Thank you for choosing us!"
                )
                if contact_no:
                    try:
                        send_sms_notification(contact_no, sms_body)
                        messagebox.showinfo("Success", f"Status updated and SMS sent to {contact_no}.")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to send SMS: {e}")
                else:
                    messagebox.showinfo("Success", "Status updated, but no contact number found.")
            else:
                messagebox.showerror("Error", "Order not found.")
            
            status_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update status: {e}")
    
    tk.Button(frame, text="Update Status", command=update_status,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12, "bold"), width=15)\
              .grid(row=2, column=0, columnspan=2, pady=15)

# ------------------- Login and Registration Functions -------------------
def is_valid_username(username):
    return re.fullmatch(r"\w{3,}", username)

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True


def show_register():
    register_window = tk.Toplevel()
    register_window.title("Register")
    register_window.geometry("400x350")
    register_window.configure(bg=BG_COLOR)
    
    tk.Label(register_window, text="Register", font=("Times New Roman", 16),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=5).pack(fill=tk.X)
    
    frame = tk.Frame(register_window, bg=BG_COLOR)
    frame.pack(pady=20)
    
    tk.Label(frame, text="Username:", font=("Times New Roman", 14), bg=BG_COLOR).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_reg_username = tk.Entry(frame, font=("Times New Roman", 14))
    entry_reg_username.grid(row=0, column=1, pady=5)
    
    tk.Label(frame, text="Password:", font=("Times New Roman", 14), bg=BG_COLOR).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_reg_password = tk.Entry(frame, show="*", font=("Times New Roman", 14))
    entry_reg_password.grid(row=1, column=1, pady=5)
    
    tk.Label(frame, text="Confirm Password:", font=("Times New Roman", 14), bg=BG_COLOR).grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_reg_confirm = tk.Entry(frame, show="*", font=("Times New Roman", 14))
    entry_reg_confirm.grid(row=2, column=1, pady=5)
    
    def submit_registration():
        username = entry_reg_username.get().strip()
        password = entry_reg_password.get()
        confirm = entry_reg_confirm.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty!")
            return
        
        if not is_valid_username(username):
            messagebox.showerror("Error", "Invalid username! It must be at least 3 characters long and contain only letters, numbers, or underscores.")
            return
        
        if not is_valid_password(password):
            messagebox.showerror("Error", "Password must be at least 8 characters long and include a lowercase letter, an uppercase letter, and a number!")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        try:
            cursor.execute("INSERT INTO Users (username, password, role) VALUES (?, ?, ?)", (username, password, "User"))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful! Please login.")
            register_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
    
    tk.Button(register_window, text="Register", command=submit_registration,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12), width=10).pack(pady=10)
    tk.Button(register_window, text="Back", command=register_window.destroy,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 12), width=10).pack(pady=5)

def show_admin_login():
    login_window = tk.Tk()
    login_window.title("Admin Login")
    login_window.geometry("400x350")
    login_window.configure(bg=BG_COLOR)
    # for denying users from resizing frames
    # login_window.resizable(False, False)

    tk.Label(login_window, text="Admin Login", font=("Times New Roman", 18, "bold"),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=10).pack(fill=tk.X)

    frame = tk.Frame(login_window, bg=BG_COLOR)
    frame.pack(pady=20, padx=20)

    tk.Label(frame, text="Username:", font=("Times New Roman", 14), bg=BG_COLOR)\
        .grid(row=0, column=0, sticky="w", padx=10, pady=10)
    entry_username = tk.Entry(frame, font=("Times New Roman", 14))
    entry_username.grid(row=0, column=1, pady=10)

    tk.Label(frame, text="Password:", font=("Times New Roman", 14), bg=BG_COLOR)\
        .grid(row=1, column=0, sticky="w", padx=10, pady=10)
    entry_password = tk.Entry(frame, show="*", font=("Times New Roman", 14))
    entry_password.grid(row=1, column=1, pady=10)

    def authenticate():
        username = entry_username.get().strip()
        password = entry_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Both fields are required!")
            return

        cursor.execute("SELECT * FROM Users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            if user[3] != "Admin":
                messagebox.showerror("Error", "This account is not an Admin!")
                return
            login_window.destroy()
            show_main_window("Admin", username)
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    tk.Button(login_window, text="Login", command=authenticate,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 14), width=10)\
              .pack(pady=10)
    tk.Button(login_window, text="Back", command=lambda: [login_window.destroy(), show_welcome()],
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 14), width=10)\
              .pack(pady=5)

    login_window.mainloop()

def show_user_login():
    login_window = tk.Tk()
    login_window.title("User Login")
    login_window.geometry("400x350")
    login_window.configure(bg=BG_COLOR)
    # 
    # login_window.resizable(False, False)

    tk.Label(login_window, text="User Login", font=("Times New Roman", 18, "bold"),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=10).pack(fill=tk.X)

    frame = tk.Frame(login_window, bg=BG_COLOR)
    frame.pack(pady=20, padx=20)

    tk.Label(frame, text="Username:", font=("Times New Roman", 14), bg=BG_COLOR)\
        .grid(row=0, column=0, sticky="w", padx=10, pady=10)
    entry_username = tk.Entry(frame, font=("Times New Roman", 14))
    entry_username.grid(row=0, column=1, pady=10)

    tk.Label(frame, text="Password:", font=("Times New Roman", 14), bg=BG_COLOR)\
        .grid(row=1, column=0, sticky="w", padx=10, pady=10)
    entry_password = tk.Entry(frame, show="*", font=("Times New Roman", 14))
    entry_password.grid(row=1, column=1, pady=10)

    def authenticate():
        username = entry_username.get().strip()
        password = entry_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Both fields are required!")
            return
        
        cursor.execute("SELECT * FROM Users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            if user[3] != "User":
                messagebox.showerror("Error", "This account is not a User account!")
                return
            login_window.destroy()
            show_main_window("User", username)
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    tk.Button(login_window, text="Login", command=authenticate,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 14), width=10)\
              .pack(pady=10)
    tk.Button(login_window, text="Register", command=show_register,
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 14), width=10)\
              .pack(pady=5)
    tk.Button(login_window, text="Back", command=lambda: [login_window.destroy(), show_welcome()],
              bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Times New Roman", 14), width=10)\
              .pack(pady=5)

    login_window.mainloop()

# ------------------- Main Window -------------------
def show_main_window(role, username):
    main_window = tk.Tk()
    main_window.title("Nursery Management System")
    main_window.geometry("800x600")
    main_window.configure(bg=BG_COLOR)

    header_frame = tk.Frame(main_window, bg=HEADER_COLOR)
    header_frame.pack(fill=tk.X)

    tk.Label(header_frame, text=f"Nursery Management System - {role}",
             font=("Times New Roman", 20, "bold"), bg=HEADER_COLOR, fg=TEXT_COLOR, pady=10)\
             .pack(side=tk.LEFT, padx=20)

    if role != "Admin":
        tk.Button(header_frame, text="🛒 Cart", font=("Times New Roman", 12, "bold"),
                  bg=BUTTON_COLOR, fg=TEXT_COLOR, command=lambda: view_cart(username))\
                  .pack(side=tk.RIGHT, padx=10)
        
    tk.Button(header_frame, text="Logout", font=("Times New Roman", 12, "bold"),
              command=lambda: [main_window.destroy(), show_welcome()],
              bg=BUTTON_COLOR, fg=TEXT_COLOR)\
              .pack(side=tk.RIGHT, padx=10)

    tk.Label(header_frame, text=f"Logged in as: {username}",
             font=("Times New Roman", 14), bg=HEADER_COLOR, fg=TEXT_COLOR)\
             .pack(side=tk.RIGHT, padx=10)

    button_frame = tk.Frame(main_window, bg=BG_COLOR)
    button_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    if role == "Admin":
        admin_buttons = [
            ("ADMIN DASHBOARD", admin_dashboard),
            ("ADD PRODUCT", add_product),
            ("EDIT PRODUCT", edit_product),
            ("DELETE PRODUCT", delete_product),
            ("UPDATE ORDER STATUS", update_order_status)
        ]
        for i, (text, command) in enumerate(admin_buttons):
            r = i // 2
            c = i % 2
            tk.Button(button_frame, text=text, command=command,
                      font=("Times New Roman", 14, "bold"), bg=BUTTON_COLOR, fg=TEXT_COLOR,
                      width=20, height=2).grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        for col in range(2):
            button_frame.columnconfigure(col, weight=1)
        for row in range((len(admin_buttons) + 1) // 2):
            button_frame.rowconfigure(row, weight=1)
    else:
        user_buttons = [
            ("Plants By Category", lambda: show_categories_window(username, role)),
            ("All Products", lambda: buy_products(username)),
            ("Nursery Tour", nursery_tour),
            ("Plantation Guide", plantation),
            ("Pots", lambda: view_pots_by_category(username, role)),
            ("Order History", lambda: view_user_history(username))
        ]
        for i, (text, command) in enumerate(user_buttons):
            r = i // 3
            c = i % 3
            tk.Button(button_frame, text=text, command=command,
                      font=("Times New Roman", 14, "bold"), bg=BUTTON_COLOR, fg=TEXT_COLOR,
                      width=20, height=2).grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        for col in range(3):
            button_frame.columnconfigure(col, weight=1)
        for row in range((len(user_buttons) + 2) // 3):
            button_frame.rowconfigure(row, weight=1)

    main_window.mainloop()




# ------------------- Welcome Screen -------------------
def show_welcome():
    welcome_window = tk.Tk()
    welcome_window.title("Welcome")
    welcome_window.geometry("300x200")
    welcome_window.configure(bg=BG_COLOR)
    
    tk.Label(welcome_window, text="Welcome", font=("Times New Roman", 18),
             bg=HEADER_COLOR, fg=TEXT_COLOR, pady=10).pack(fill=tk.X)
    
    tk.Button(welcome_window, text="Admin", command=lambda: [welcome_window.destroy(), show_admin_login()],
              bg=BUTTON_COLOR, fg=TEXT_COLOR, width=15, height=2).pack(pady=10)
    
    tk.Button(welcome_window, text="User", command=lambda: [welcome_window.destroy(), show_user_login()],
              bg=BUTTON_COLOR, fg=TEXT_COLOR, width=15, height=2).pack(pady=10)
    
    welcome_window.mainloop()

# ------------------- Start Application -------------------
show_welcome()
