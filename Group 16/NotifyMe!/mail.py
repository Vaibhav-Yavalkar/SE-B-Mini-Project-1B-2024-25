import smtplib
import tkinter as tk
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox

SENDER_EMAIL = "sid.surve2005@gmail.com"
PASSWORD = "xuhq nokq olsf qrqi"

def send_email():
    receiver_email = receiver_entry.get()
    email_body = message_text.get("1.0", tk.END).strip()

    if not receiver_email or not email_body:
        messagebox.showerror("Error", "Please enter a recipient email and message.")
        return

    subject = "Hello from Python!"

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(email_body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email:\n{e}")

root = tk.Tk()
root.title("Python Email Sender")
root.geometry("400x350")

tk.Label(root, text="Receiver Email:").pack(pady=5)
receiver_entry = tk.Entry(root, width=40)
receiver_entry.pack(pady=5)

tk.Label(root, text="Message:").pack(pady=5)
message_text = tk.Text(root, width=40, height=8)
message_text.pack(pady=5)

send_button = tk.Button(root, text="Send Email", command=send_email, bg="green", fg="white")
send_button.pack(pady=10)

root.mainloop()
