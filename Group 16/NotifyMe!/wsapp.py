import pywhatkit as kit
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


# Function to send the WhatsApp message
def send_whatsapp_message():
    # Get the user input from the GUI
    phone_number = phone_entry.get()
    message = message_text.get("1.0", "end-1c").strip()

    # Check if phone number or message is empty
    if not phone_number or not message:
        messagebox.showwarning("Input Error", "Please enter both phone number and message.")
        return

    # Validate phone number format (e.g., +1234567890)
    if not phone_number.startswith("+"):
        messagebox.showwarning("Input Error", "Phone number must include the country code (e.g., +1 for USA).")
        return

    # Get the current time
    current_time = datetime.now()
    hour = current_time.hour
    minute = current_time.minute + 1  # Add 1 minute to ensure the message sends shortly after

    # Sending the message via PyWhatKit
    try:
        # Send message (time is set to current hour and minute +1)
        kit.sendwhatmsg(phone_number, message, hour, minute)
        messagebox.showinfo("Success", "Message sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Create the Tkinter window
root = tk.Tk()
root.title("WhatsApp Message Sender")
root.geometry("400x350")

# Create the labels and input fields
tk.Label(root, text="Recipient Phone Number (with country code):").pack(pady=5)
phone_entry = tk.Entry(root, width=40)
phone_entry.pack(pady=5)

tk.Label(root, text="Message:").pack(pady=5)
message_text = tk.Text(root, width=40, height=6)
message_text.pack(pady=5)


# Create the send button
send_button = tk.Button(root, text="Send WhatsApp Message", command=send_whatsapp_message, bg="green", fg="white")
send_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
