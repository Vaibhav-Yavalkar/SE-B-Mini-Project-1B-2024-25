import tkinter as tk
from tkinter import messagebox, ttk
import os
import time
import subprocess
import sys
from datetime import datetime, timedelta
import mysql.connector
import uuid
from parking_data import occupy_space, load_parking_data

def show_payment_page():
    payment_window = tk.Tk()
    payment_window.title("ParkWatch - Secure Parking Payment")
    payment_window.geometry("500x700")
    payment_window.state('zoomed')
    payment_window.configure(bg="#0F172A")  # Dark background

    # Default values
    selected_space = "Unknown"
    location_type = "Unknown"
    
    if os.path.exists("selected_space.txt"):
        with open("selected_space.txt", "r") as f:
            selected_space = f.read().strip()
    
    if os.path.exists("parking_type.txt"):
        with open("parking_type.txt", "r") as f:
            location_type = f.read().strip()
    else:
        # Determine location type based on the first letter of the space
        location_type = "shopping_mall" if selected_space[0] in ['P', 'Q', 'R', 'S'] else "college"
    
    # Format location type for display
    display_location = "Shopping Mall" if location_type == "shopping_mall" else "College Campus"
    
    current_time = datetime.now()
    default_hours = 1
    departure_time = current_time + timedelta(hours=default_hours)
    rate_per_hour = 100
    total_cost = default_hours * rate_per_hour

    def get_db_connection():
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="Tanay@26",
                database="parkwatch"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Connection Error", f"Could not connect to database: {err}")
            return None
    
    def process_payment():
        vehicle_number = vehicle_entry.get().strip()
        if not vehicle_number:
            messagebox.showerror("Error", "Please enter your vehicle number")
            return
        
        # Card details validation
        card_number = card_entry.get().replace(" ", "")
        if len(card_number) < 16:
            messagebox.showerror("Error", "Please enter a valid card number")
            return
        
        if not exp_entry.get() or "/" not in exp_entry.get():
            messagebox.showerror("Error", "Please enter a valid expiry date (MM/YY)")
            return
        
        if len(cvv_entry.get()) < 3:
            messagebox.showerror("Error", "Please enter a valid CVV")
            return
        
        hours = float(hours_var.get())
        cost = hours * rate_per_hour
        transaction_id = str(uuid.uuid4())[:8].upper()
        
        entry_time = current_time
        departure_time = current_time + timedelta(hours=hours)
        
        try:
            # Mark the space as occupied in the parking data
            success = occupy_space(selected_space, hours, vehicle_number)
            if not success:
                messagebox.showerror("Error", "Failed to reserve the parking space. Please try again.")
                return
                
            # Determine which table to use based on the parking type
            db_table = "shopping_mall" if location_type == "shopping_mall" else "college_parking"
            
            conn = get_db_connection()
            if not conn:
                return
                
            try:
                cursor = conn.cursor()
                
                query = f'''
                INSERT INTO {db_table} (
                    space_number, entry_time, exit_time, duration, amount, 
                    transaction_id, transaction_time, payment_method, vehicle_number,
                    card_number
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                
                # Mask card number except last 4 digits for storage
                masked_card = "*" * (len(card_number) - 4) + card_number[-4:]
                
                values = (
                    selected_space,
                    entry_time.strftime("%Y-%m-%d %H:%M:%S"), 
                    departure_time.strftime("%Y-%m-%d %H:%M:%S"), 
                    hours, 
                    cost,
                    transaction_id,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Card",
                    vehicle_number,
                    masked_card
                )
                
                cursor.execute(query, values)
                conn.commit()
                
                # Get the last inserted ID
                last_id = cursor.lastrowid
                
                # Close cursor and connection
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Payment Successful", 
                                  f"Payment of ₹{cost:.2f} processed successfully!\n\n" +
                                  f"Transaction ID: {transaction_id}\n" +
                                  f"Space: {selected_space}\n" +
                                  f"Duration: {hours} hours\n" +
                                  f"Please vacate the space by {departure_time.strftime('%I:%M %p')}")
                
                # Save transaction info for receipt generation
                with open("transaction_info.txt", "w") as f:
                    f.write(f"{last_id},{db_table}")
                
                payment_window.destroy()
                
                # Launch receipt generation
                try:
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    receipt_path = os.path.join(current_dir, "receipt.py")
                    
                    if os.path.exists(receipt_path):
                        if sys.platform.startswith('win'):
                            subprocess.Popen(["python", receipt_path])
                        else:
                            subprocess.Popen(["python3", receipt_path])
                    else:
                        messagebox.showinfo("Info", "Receipt generation is not available.")
                        # Go back to main dashboard
                        go_to_dashboard()
                except Exception as e:
                    messagebox.showerror("Error", f"Could not open receipt: {str(e)}")
                    # Go back to main dashboard as fallback
                    go_to_dashboard()
            
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Could not save payment: {str(err)}")
                # If database error, still try to rollback the parking space reservation
                # This would require a function to free the space in parking_data.py
            
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        
        except Exception as e:
            messagebox.showerror("System Error", f"Could not complete booking: {str(e)}")

    def go_to_dashboard():
        payment_window.destroy()
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dashboard_path = os.path.join(current_dir, "dashboard.py")
            
            if os.path.exists(dashboard_path):
                if sys.platform.startswith('win'):
                    subprocess.Popen(["python", dashboard_path])
                else:
                    subprocess.Popen(["python3", dashboard_path])
        except Exception as e:
            print(f"Error launching dashboard: {e}")

    # Main Container
    main_container = tk.Frame(payment_window, bg="#0F172A")
    main_container.pack(fill="both", expand=True, padx=20, pady=20)

    # Header
    header_label = tk.Label(main_container, text="PARKWATCH", 
                            font=("Arial", 24, "bold"), 
                            bg="#0F172A", fg="#60A5FA")
    header_label.pack(pady=(0, 10))

    subtitle_label = tk.Label(main_container, text="Secure Parking Payment", 
                              font=("Arial", 12), 
                              bg="#0F172A", fg="white")
    subtitle_label.pack(pady=(0, 20))

    # Location Details Frame
    location_frame = tk.Frame(main_container, bg="#1E293B", borderwidth=1)
    location_frame.pack(fill="x", pady=10)

    location_details = [
        ("Location:", display_location),
        ("Space Number:", selected_space)
    ]

    for label, value in location_details:
        row_frame = tk.Frame(location_frame, bg="#1E293B")
        row_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(row_frame, text=label, font=("Arial", 12), 
                 bg="#1E293B", fg="white", anchor="w").pack(side="left")
        tk.Label(row_frame, text=value, font=("Arial", 12), 
                 bg="#1E293B", fg="#60A5FA", anchor="e").pack(side="left")

    # Duration Details Frame
    duration_frame = tk.Frame(main_container, bg="#1E293B", borderwidth=1)
    duration_frame.pack(fill="x", pady=10)

    entry_time_str = current_time.strftime("%I:%M %p")
    exit_time_str = departure_time.strftime("%I:%M %p")

    # Create exit time label variable
    exit_time_label = None

    # Duration Details
    entry_row_frame = tk.Frame(duration_frame, bg="#1E293B")
    entry_row_frame.pack(fill="x", padx=10, pady=5)
    tk.Label(entry_row_frame, text="Entry Time:", font=("Arial", 12), 
             bg="#1E293B", fg="white", anchor="w").pack(side="left")
    tk.Label(entry_row_frame, text=entry_time_str, font=("Arial", 12), 
             bg="#1E293B", fg="#0eed16", anchor="e").pack(side="left")

    hours_row_frame = tk.Frame(duration_frame, bg="#1E293B")
    hours_row_frame.pack(fill="x", padx=10, pady=5)
    tk.Label(hours_row_frame, text="Number of Hours:", font=("Arial", 12), 
             bg="#1E293B", fg="white", anchor="w").pack(side="left")
    
    hours_var = tk.StringVar(value="1")
    hours_dropdown = ttk.Combobox(hours_row_frame, textvariable=hours_var, 
                                  values=["0.5", "1", "2", "3", "4", "5", "6"], 
                                  width=9, state="readonly")
    hours_dropdown.pack(side="left")

    exit_row_frame = tk.Frame(duration_frame, bg="#1E293B")
    exit_row_frame.pack(fill="x", padx=10, pady=5)
    tk.Label(exit_row_frame, text="Exit Time:", font=("Arial", 12), 
             bg="#1E293B", fg="white", anchor="w").pack(side="left")
    exit_time_label = tk.Label(exit_row_frame, text=exit_time_str, font=("Arial", 12), 
                               bg="#1E293B", fg="#f70f17", anchor="e")
    exit_time_label.pack(side="left")

    def update_total_cost_and_exit_time(*args):
        hours = float(hours_var.get())
        total_cost = hours * rate_per_hour
        
        # Update total amount
        total_amount_label.config(text=f"₹{total_cost:.2f}")
        pay_button.config(text=f"Pay ₹{total_cost:.2f}")
        
        # Update exit time
        new_departure_time = current_time + timedelta(hours=hours)
        exit_time_label.config(text=new_departure_time.strftime("%I:%M %p"))

    # Bind the update function to the hours dropdown
    hours_dropdown.bind("<<ComboboxSelected>>", update_total_cost_and_exit_time)

    # Payment Details Frame
    payment_frame = tk.Frame(main_container, bg="#1E293B", borderwidth=1)
    payment_frame.pack(fill="x", pady=10)

    rate_row_frame = tk.Frame(payment_frame, bg="#1E293B")
    rate_row_frame.pack(fill="x", padx=10, pady=5)
    
    tk.Label(rate_row_frame, text="Rate:", font=("Arial", 12), 
             bg="#1E293B", fg="white", anchor="w").pack(side="left")
    tk.Label(rate_row_frame, text="₹100.00 per hour", font=("Arial", 12), 
             bg="#1E293B", fg="#60A5FA", anchor="e").pack(side="left")

    total_row_frame = tk.Frame(payment_frame, bg="#1E293B")
    total_row_frame.pack(fill="x", padx=10, pady=5)
    
    tk.Label(total_row_frame, text="Total Amount:", font=("Arial", 12), 
             bg="#1E293B", fg="white", anchor="w").pack(side="left")
    total_amount_label = tk.Label(total_row_frame, text="₹100.00", font=("Arial", 12, "bold"), 
                                  bg="#1E293B", fg="#60A5FA", anchor="e")
    total_amount_label.pack(side="left")

    # Card Details
    card_details_frame = tk.Frame(main_container, bg="#1E293B", borderwidth=1)
    card_details_frame.pack(fill="x", pady=10)

    tk.Label(card_details_frame, text="Card Details", font=("Arial", 14, "bold"), 
             bg="#1E293B", fg="white").pack(pady=10)

    # Card Number
    card_number_frame = tk.Frame(card_details_frame, bg="#1E293B")
    card_number_frame.pack(fill="x", padx=10, pady=5)
    tk.Label(card_number_frame, text="Card Number: ", font=("Arial", 12), 
             bg="#1E293B", fg="white").pack(side="left")
    card_entry = tk.Entry(card_number_frame, font=("Arial", 12), width=20)
    card_entry.pack(side="left")

    # Expiry Date
    expiry_frame = tk.Frame(card_details_frame, bg="#1E293B")
    expiry_frame.pack(fill="x", padx=10, pady=5)
    tk.Label(expiry_frame, text="Expiry (MM/YY): ", font=("Arial", 12), 
             bg="#1E293B", fg="white").pack(side="left")
    exp_entry = tk.Entry(expiry_frame, font=("Arial", 12), width=10)
    exp_entry.pack(side="left")

    # CVV
    cvv_frame = tk.Frame(card_details_frame, bg="#1E293B")
    cvv_frame.pack(fill="x", padx=10, pady=5)
    tk.Label(cvv_frame, text="CVV: ", font=("Arial", 12), 
             bg="#1E293B", fg="white").pack(side="left")
    cvv_entry = tk.Entry(cvv_frame, font=("Arial", 12), width=5, show="*")
    cvv_entry.pack(side="left")

    # Vehicle Number
    vehicle_frame = tk.Frame(main_container, bg="#0F172A")
    vehicle_frame.pack(fill="x", pady=10)

    tk.Label(vehicle_frame, text="Vehicle Number: ", font=("Arial", 12), 
             bg="#0F172A", fg="white").pack(side="left")
    vehicle_entry = tk.Entry(vehicle_frame, font=("Arial", 12), width=20)
    vehicle_entry.pack(side="left")

    # Buttons
    button_frame = tk.Frame(main_container, bg="#0F172A")
    button_frame.pack(fill="x", pady=20)

    cancel_button = tk.Button(button_frame, text="Cancel", 
                              font=("Arial", 14), 
                              bg="#334155", fg="white", 
                              command=lambda: go_to_dashboard())
    cancel_button.pack(side="left", expand=True, padx=10)

    pay_button = tk.Button(button_frame, text="Pay ₹100.00", 
                           font=("Arial", 14, "bold"), 
                           bg="#10B981", fg="white", 
                           command=process_payment)
    pay_button.pack(side="right", expand=True, padx=10)

    # Start the Tkinter event loop
    payment_window.mainloop()

if __name__ == "__main__":
    show_payment_page()