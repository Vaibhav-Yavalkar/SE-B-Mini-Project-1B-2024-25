import tkinter as tk
from tkinter import messagebox
import os
import mysql.connector
from datetime import datetime
import qrcode
from PIL import Image, ImageTk
import tempfile

def show_receipt():
    # Create receipt window
    receipt_window = tk.Tk()
    receipt_window.title("ParkWatch - Receipt")
    receipt_window.geometry("500x700")
    receipt_window.configure(bg="#F8FAFC")
    
    # Database connection function
    def get_db_connection():
        # Replace with your MySQL connection details
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Tanay@26",
            database="parkwatch"
        )
        return conn
    
    # Get transaction ID and table name from file
    transaction_id = None
    table_name = None
    
    if os.path.exists("transaction_info.txt"):
        with open("transaction_info.txt", "r") as f:
            data = f.read().strip().split(',')
            if len(data) >= 2:
                transaction_id = data[0]
                table_name = data[1]
    
    if not transaction_id or not table_name:
        messagebox.showerror("Error", "Transaction information not found")
        receipt_window.destroy()
        return
    
    # Fetch transaction details from database
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Return results as dictionaries
        
        # Using parameterized query with MySQL syntax
        query = f"SELECT * FROM {table_name} WHERE id = %s"
        cursor.execute(query, (transaction_id,))
        transaction = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not transaction:
            messagebox.showerror("Error", "Transaction not found in database")
            receipt_window.destroy()
            return
            
    except Exception as e:
        messagebox.showerror("Database Error", f"Could not fetch transaction: {str(e)}")
        receipt_window.destroy()
        return
    
    # Header with logo
    header_frame = tk.Frame(receipt_window, bg="#F8FAFC")
    header_frame.pack(fill="x", pady=10)
    
    logo_label = tk.Label(header_frame, text="PARKWATCH", font=("Verdana", 24, "bold"), 
                        bg="#F8FAFC", fg="#0F172A")
    logo_label.pack()
    
    # Receipt title
    title = tk.Label(header_frame, text="PARKING RECEIPT", 
                    font=("Arial", 16, "bold"), bg="#F8FAFC", fg="#334155")
    title.pack(pady=5)
    
    # Divider
    divider1 = tk.Frame(receipt_window, height=2, bg="#CBD5E1")
    divider1.pack(fill="x", padx=20, pady=5)
    
    # Location info
    location_text = "Shopping Mall" if table_name == "shopping_mall" else "College Campus"
    location_frame = tk.Frame(receipt_window, bg="#F8FAFC")
    location_frame.pack(fill="x", padx=30, pady=5)
    
    location_label = tk.Label(location_frame, text=f"Location: {location_text}", 
                            font=("Arial", 12, "bold"), bg="#F8FAFC", fg="#0F172A")
    location_label.pack(anchor="w")
    
    # Transaction details
    details_frame = tk.Frame(receipt_window, bg="#F8FAFC")
    details_frame.pack(fill="x", padx=30, pady=10)
    
    # Format dates for display
    entry_time = datetime.strptime(transaction['entry_time'].strftime("%Y-%m-%d %H:%M:%S") if isinstance(transaction['entry_time'], datetime) else transaction['entry_time'], "%Y-%m-%d %H:%M:%S")
    exit_time = datetime.strptime(transaction['exit_time'].strftime("%Y-%m-%d %H:%M:%S") if isinstance(transaction['exit_time'], datetime) else transaction['exit_time'], "%Y-%m-%d %H:%M:%S")
    transaction_time = datetime.strptime(transaction['transaction_time'].strftime("%Y-%m-%d %H:%M:%S") if isinstance(transaction['transaction_time'], datetime) else transaction['transaction_time'], "%Y-%m-%d %H:%M:%S")
    
    # Details grid
    details = [
        ("Transaction ID:", transaction['transaction_id']),
        ("Date:", transaction_time.strftime("%d-%m-%Y")),
        ("Time:", transaction_time.strftime("%I:%M %p")),
        ("Space Number:", transaction['space_number']),
        ("Vehicle Number:", transaction['vehicle_number']),
        ("Entry Time:", entry_time.strftime("%d-%m-%Y %I:%M %p")),
        ("Exit Time:", exit_time.strftime("%d-%m-%Y %I:%M %p")),
        ("Duration:", f"{transaction['duration']} hours"),
    ]
    
    row = 0
    for label_text, value_text in details:
        tk.Label(details_frame, text=label_text, font=("Arial", 11), 
               bg="#F8FAFC", fg="#64748B").grid(row=row, column=0, sticky="w", pady=3)
        
        tk.Label(details_frame, text=value_text, font=("Arial", 11, "bold"), 
               bg="#F8FAFC", fg="#0F172A").grid(row=row, column=1, sticky="w", padx=10, pady=3)
        row += 1
    
    # Divider
    divider2 = tk.Frame(receipt_window, height=2, bg="#CBD5E1")
    divider2.pack(fill="x", padx=20, pady=10)
    
    # Payment details
    payment_frame = tk.Frame(receipt_window, bg="#F8FAFC")
    payment_frame.pack(fill="x", padx=30, pady=5)
    
    payment_header = tk.Label(payment_frame, text="Payment Details", 
                            font=("Arial", 14, "bold"), bg="#F8FAFC", fg="#334155")
    payment_header.pack(anchor="w", pady=5)
    
    # Payment method
    method_frame = tk.Frame(payment_frame, bg="#F8FAFC")
    method_frame.pack(fill="x", pady=3)
    
    method_label = tk.Label(method_frame, text="Payment Method:", 
                          font=("Arial", 11), bg="#F8FAFC", fg="#64748B")
    method_label.pack(side="left")
    
    method_value = tk.Label(method_frame, text=transaction['payment_method'].title(), 
                          font=("Arial", 11, "bold"), bg="#F8FAFC", fg="#0F172A")
    method_value.pack(side="left", padx=10)
    
    # Card number if applicable
    if transaction['payment_method'] == 'card' and transaction['card_number']:
        card_frame = tk.Frame(payment_frame, bg="#F8FAFC")
        card_frame.pack(fill="x", pady=3)
        
        card_label = tk.Label(card_frame, text="Card Number:", 
                            font=("Arial", 11), bg="#F8FAFC", fg="#64748B")
        card_label.pack(side="left")
        
        # Mask the card number except last 4 digits
        masked_card = 'XXXX-XXXX-XXXX-' + transaction['card_number'][-4:]
        card_value = tk.Label(card_frame, text=masked_card, 
                            font=("Arial", 11, "bold"), bg="#F8FAFC", fg="#0F172A")
        card_value.pack(side="left", padx=10)
    
    # Amount
    amount_frame = tk.Frame(payment_frame, bg="#F8FAFC")
    amount_frame.pack(fill="x", pady=10)
    
    amount_label = tk.Label(amount_frame, text="Amount Paid:", 
                          font=("Arial", 14), bg="#F8FAFC", fg="#64748B")
    amount_label.pack(side="left")
    
    amount_value = tk.Label(amount_frame, text=f"₹{float(transaction['amount']):.2f}", 
                          font=("Arial", 14, "bold"), bg="#F8FAFC", fg="#0F172A")
    amount_value.pack(side="left", padx=10)
    
    # Divider
    divider3 = tk.Frame(receipt_window, height=2, bg="#CBD5E1")
    divider3.pack(fill="x", padx=20, pady=10)
    
    # Generate QR code for digital verification
    try:
        # Create QR code with transaction details
        qr_data = f"ID:{transaction['transaction_id']}\nSpace:{transaction['space_number']}\nAmount:₹{float(transaction['amount']):.2f}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to temp file and display
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        qr_img.save(temp_file.name)
        
        # Display QR code
        qr_frame = tk.Frame(receipt_window, bg="#F8FAFC")
        qr_frame.pack(pady=10)
        
        # Convert to PhotoImage
        qr_pil = Image.open(temp_file.name)
        qr_pil = qr_pil.resize((120, 120), Image.LANCZOS)
        qr_photo = ImageTk.PhotoImage(qr_pil)
        
        qr_label = tk.Label(qr_frame, image=qr_photo, bg="#F8FAFC")
        qr_label.image = qr_photo  # Keep a reference
        qr_label.pack()
        
        qr_text = tk.Label(qr_frame, text="Scan for digital verification", 
                         font=("Arial", 10), bg="#F8FAFC", fg="#64748B")
        qr_text.pack(pady=5)
        
    except Exception as e:
        # If QR code generation fails, just show a message
        error_msg = tk.Label(receipt_window, text="QR Code unavailable", 
                          font=("Arial", 10, "italic"), bg="#F8FAFC", fg="#64748B")
        error_msg.pack(pady=10)
    
    # Thank you note
    thank_you = tk.Label(receipt_window, text="Thank you for using ParkWatch", 
                       font=("Arial", 12, "bold"), bg="#F8FAFC", fg="#334155")
    thank_you.pack(pady=10)
    
    # Button Frame for Print and Feedback
    button_frame = tk.Frame(receipt_window, bg="#F8FAFC")
    button_frame.pack(pady=10)
    
    # Print button
    def print_receipt():
        messagebox.showinfo("Print", "Sending receipt to printer...")
        # In a real application, implement actual printing functionality here
    
    print_button = tk.Button(button_frame, text="Print Receipt", font=("Arial", 12, "bold"), 
                          bg="#2563EB", fg="white", padx=15, pady=8,
                          activebackground="#1D4ED8", activeforeground="white",
                          command=print_receipt)
    print_button.pack(side="left", padx=10)
    
    # Feedback Button
    def show_feedback():
        # Create a new top-level window for feedback
        feedback_window = tk.Toplevel(receipt_window)
        feedback_window.title("ParkWatch - Feedback")
        feedback_window.geometry("400x450")
        feedback_window.configure(bg="#F8FAFC")
        
        # Header
        feedback_header = tk.Label(feedback_window, text="We Value Your Feedback", 
                                font=("Arial", 16, "bold"), bg="#F8FAFC", fg="#0F172A")
        feedback_header.pack(pady=15)
        
        # Rating frame
        rating_frame = tk.Frame(feedback_window, bg="#F8FAFC")
        rating_frame.pack(pady=10)
        
        rating_label = tk.Label(rating_frame, text="How would you rate your parking experience?", 
                             font=("Arial", 12), bg="#F8FAFC", fg="#334155")
        rating_label.pack(anchor="w", pady=5)
        
        # Variable to store rating
        rating_var = tk.IntVar()
        rating_var.set(0)
        
        # Star rating
        stars_frame = tk.Frame(rating_frame, bg="#F8FAFC")
        stars_frame.pack(pady=5)
        
        for i in range(1, 6):
            star_btn = tk.Radiobutton(stars_frame, text="★", variable=rating_var, value=i,
                                   font=("Arial", 20), bg="#F8FAFC", fg="#FCD34D",
                                   selectcolor="#F8FAFC", indicatoron=0,
                                   activebackground="#F8FAFC", activeforeground="#FBBF24")
            star_btn.pack(side=tk.LEFT, padx=5)
        
        # Comments section
        comments_frame = tk.Frame(feedback_window, bg="#F8FAFC")
        comments_frame.pack(fill="x", padx=20, pady=15)
        
        comments_label = tk.Label(comments_frame, text="Additional Comments:", 
                               font=("Arial", 12), bg="#F8FAFC", fg="#334155")
        comments_label.pack(anchor="w", pady=5)
        
        comments_text = tk.Text(comments_frame, height=6, width=40, font=("Arial", 11),
                              bg="white", fg="#0F172A", wrap=tk.WORD,
                              relief=tk.SOLID, borderwidth=1)
        comments_text.pack(pady=5)
        
        # Contact information (optional)
        contact_frame = tk.Frame(feedback_window, bg="#F8FAFC")
        contact_frame.pack(fill="x", padx=20, pady=10)
        
        contact_label = tk.Label(contact_frame, text="Email (Optional):", 
                              font=("Arial", 12), bg="#F8FAFC", fg="#334155")
        contact_label.pack(anchor="w", pady=5)
        
        email_entry = tk.Entry(contact_frame, width=35, font=("Arial", 11),
                            bg="white", fg="#0F172A", relief=tk.SOLID, borderwidth=1)
        email_entry.pack(pady=5)
        
        # Submit button
        def submit_feedback():
            # In a real application you would save this to a database
            rating = rating_var.get()
            comments = comments_text.get("1.0", tk.END).strip()
            email = email_entry.get().strip()
            
            message = f"Thank you for your feedback!\nRating: {rating}/5"
            if comments:
                # In a real app, save comments to database
                pass
                
            if email:
                # In a real app, save email to database
                message += "\nWe'll follow up if needed."
            
            messagebox.showinfo("Feedback Submitted", message)
            feedback_window.destroy()
        
        submit_btn = tk.Button(feedback_window, text="Submit Feedback", font=("Arial", 12, "bold"),
                            bg="#22C55E", fg="white", padx=15, pady=8,
                            activebackground="#16A34A", activeforeground="white",
                            command=submit_feedback)
        submit_btn.pack(pady=15)
        
        # Position the window relative to the main window
        feedback_window.transient(receipt_window)
        feedback_window.update_idletasks()
        width = feedback_window.winfo_width()
        height = feedback_window.winfo_height()
        x = receipt_window.winfo_x() + (receipt_window.winfo_width() - width) // 2
        y = receipt_window.winfo_y() + (receipt_window.winfo_height() - height) // 2
        feedback_window.geometry(f"+{x}+{y}")
        
        feedback_window.focus_set()
        feedback_window.grab_set()
    
    feedback_button = tk.Button(button_frame, text="Give Feedback", font=("Arial", 12, "bold"),
                             bg="#22C55E", fg="white", padx=15, pady=8,
                             activebackground="#16A34A", activeforeground="white",
                             command=show_feedback)
    feedback_button.pack(side="left", padx=10)
    
    # Footer
    footer = tk.Label(receipt_window, text="© 2025 ParkWatch. All rights reserved.", 
                    font=("Arial", 8), bg="#F8FAFC", fg="#94A3B8")
    footer.pack(side="bottom", pady=10)
    
    receipt_window.mainloop()

if __name__ == "__main__":
    show_receipt()