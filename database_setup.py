import sqlite3

# Connect to the database file (creates the file if it doesn't exist)
conn = sqlite3.connect("nursery.db")
cursor = conn.cursor()

# ------------------- Create Database Tables -------------------
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
    username TEXT,
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
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Admin', 'User'))
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

cursor.execute("SELECT * FROM Users WHERE username = ?", ("admin",))
if not cursor.fetchone():
    cursor.execute("INSERT INTO Users (username, password, role) VALUES (?, ?, ?)", ("admin", "123", "Admin"))
    conn.commit()

print("Database 'nursery.db' created and populated successfully!")

conn.close()
