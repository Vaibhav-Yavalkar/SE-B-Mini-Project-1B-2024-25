import sqlite3

# Connect to the database
conn = sqlite3.connect("food_waste_tracker.db")
cursor = conn.cursor()

# Fetch and display waste logs
cursor.execute("SELECT * FROM waste_log")
waste_log_rows = cursor.fetchall()

print("Waste Log:")
for row in waste_log_rows:
    print(row)

# Fetch and display stock data
cursor.execute("SELECT * FROM stock")
stock_rows = cursor.fetchall()

print("\nStock:")
for row in stock_rows:
    print(row)

# Close the database connection
conn.close()
