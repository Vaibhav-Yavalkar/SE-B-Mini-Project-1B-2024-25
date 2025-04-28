#
# import os
# import re
# from twilio.rest import Client
# import tkinter as tk
# from tkinter import filedialog, messagebox, scrolledtext
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import smtplib
# import pandas as pd
# from dotenv import load_dotenv
# import pywhatkit as kit
# import pyautogui
# import time
#
# load_dotenv()
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# SENDER_EMAIL = os.getenv("SENDER_EMAIL")
# SENDER_EMAIL_PASSWORD = os.getenv("SENDER_EMAIL_PASSWORD")
# EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#
# def is_valid_email(email):
#     return re.match(EMAIL_REGEX, email) is not None
#
# class SMSNotifier:
#     def __init__(self):
#         self.phone_numbers = []
#         self.email_addresses = []
#
#     def open_file(self):
#         file_path = filedialog.askopenfilename(
#             title="Select file to upload",
#             filetypes=[("Excel files", "*.xlsx;*.xls")]
#         )
#         if file_path:
#             try:
#                 data = pd.read_excel(file_path)
#                 if "Ph_no" in data.columns:
#                     self.phone_numbers = data["Ph_no"].astype(str).tolist()
#                 if "Email" in data.columns:
#                     self.email_addresses = [email for email in data["Email"].astype(str).tolist() if is_valid_email(email)]
#                 messagebox.showinfo("Success",
#                                     f"Loaded all valid phone numbers and emails.")
#             except Exception as e:
#                 messagebox.showerror("Error", f"Error reading the Excel file: {e}")
#
#     def send_sms(self, message):
#         if not self.phone_numbers:
#             messagebox.showerror("Error", "No phone numbers loaded!")
#             return False
#         if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUMBER:
#             messagebox.showerror("Error", "Twilio credentials are missing!")
#             return False
#         try:
#             client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#             for phone_number in self.phone_numbers:
#                 client.messages.create(
#                     body=message,
#                     from_=TWILIO_PHONE_NUMBER,
#                     to=phone_number
#                 )
#             messagebox.showinfo("Success", f"SMS messages sent to {len(self.phone_numbers)} numbers.")
#             return True
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to send SMS messages: {e}")
#             return False
#
# class SMSNotifierGUI:
#     def __init__(self, master, root=None, prev_window=None):
#         if prev_window:
#             prev_window.destroy()
#         self.master = master
#         self.root = root
#         self.master.title("Send Notifications")
#         self.master.state('zoomed')
#         self.master.configure(bg="#1E1E2F")
#         self.sms_notifier = SMSNotifier()
#
#         tk.Label(master, text="Send Bulk Notifications", font=("Roboto", 16, "bold"), bg="#1E1E2F", fg="#E0E0E0").pack(pady=100)
#         self.upload_btn = tk.Button(master, text="Upload Excel", command=self.sms_notifier.open_file, font=("Roboto", 12, "bold"), bg="#00D4FF", fg="#E0E0E0", relief="flat", padx=10, pady=5)
#         self.upload_btn.pack(pady=5)
#
#         button_frame = tk.Frame(master, bg="#1E1E2F")
#         button_frame.pack(expand=True)
#
#         self.whatsapp_img = tk.PhotoImage(file="whatsapp_icon.png")
#         self.email_img = tk.PhotoImage(file="gmail_icon.png")
#         self.sms_img = tk.PhotoImage(file="sms_icon.png")
#
#         self.whatsapp_button = tk.Button(button_frame, image=self.whatsapp_img, compound="left",
#                                          bg="#00D4FF", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5,
#                                          command=self.open_whatsapp_window)
#         self.whatsapp_button.pack(side="left", padx=10)
#
#         self.email_button = tk.Button(button_frame, image=self.email_img, compound="left",
#                                       bg="#00D4FF", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5,
#                                       command=self.open_email_window)
#         self.email_button.pack(side="left", padx=10)
#
#         self.send_btn = tk.Button(button_frame, image=self.sms_img, compound="left",
#                                   font=("Roboto", 12, "bold"), bg="#00D4FF", fg="#E0E0E0", relief="flat", padx=10, pady=5,
#                                   command=self.open_sms_window)
#         self.send_btn.pack(side="left", padx=10)
#
#         self.back_button = tk.Button(master, text="Back", command=lambda: self.back_to_dashboard(),
#                                      bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.back_button.pack(side="bottom", anchor="se", padx=10, pady=10)
#
#     def back_to_dashboard(self):
#         from dashboard import open_dashboard
#         self.master.destroy()
#         open_dashboard(root=self.root, prev_window=self.master)
#
#     def open_sms_window(self):
#         sms_window = tk.Toplevel(self.master)
#         sms_window.title("Send SMS Message")
#         sms_window.geometry("400x400")
#         sms_window.configure(bg="#1E1E2F")
#
#         tk.Label(sms_window, text="Recipient Phone Number (with country code):", font=("Roboto", 12), bg="#1E1E2F", fg="#E0E0E0").pack(pady=5)
#         phone_entry = tk.Entry(sms_window, width=40, font=("Roboto", 12), bg="#2D2D44", fg="#E0E0E0", insertbackground="#00D4FF")
#         phone_entry.pack(pady=5)
#
#         tk.Label(sms_window, text="Message:", font=("Roboto", 12), bg="#1E1E2F", fg="#E0E0E0").pack(pady=5)
#         message_text = tk.Text(sms_window, width=40, height=6, font=("Roboto", 12), bg="#2D2D44", fg="#E0E0E0", insertbackground="#00D4FF")
#         message_text.pack(pady=5)
#
#         def send_sms_message():
#             phone_number = phone_entry.get()
#             message = message_text.get("1.0", "end-1c").strip()
#             if not phone_number or not message:
#                 messagebox.showwarning("Input Error", "Please enter both phone number and message.")
#                 return
#             if not phone_number.startswith("+"):
#                 messagebox.showwarning("Input Error", "Phone number must include the country code (e.g., +1 for USA).")
#                 return
#             try:
#                 client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#                 client.messages.create(
#                     body=message,
#                     from_=TWILIO_PHONE_NUMBER,
#                     to=phone_number
#                 )
#                 messagebox.showinfo("Success", f"SMS message sent to {phone_number}!")
#                 sms_window.destroy()
#             except Exception as e:
#                 messagebox.showerror("Error", f"An error occurred: {e}")
#                 sms_window.destroy()
#
#         def send_sms_to_all():
#             message = message_text.get("1.0", "end-1c").strip()
#             if not message:
#                 messagebox.showwarning("Input Error", "Please enter a message.")
#                 return
#             if not self.sms_notifier.phone_numbers:
#                 messagebox.showwarning("Error", "No phone numbers loaded from Excel. Please upload an Excel file.")
#                 return
#             if self.sms_notifier.send_sms(message):
#                 sms_window.destroy()
#             else:
#                 sms_window.destroy()
#
#         tk.Button(sms_window, text="Send to Single", command=send_sms_message, bg="#39FF14", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(pady=5)
#         tk.Button(sms_window, text="Send to All", command=send_sms_to_all, bg="#00D4FF", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(pady=5)
#
#     def open_whatsapp_window(self):
#         whatsapp_window = tk.Toplevel(self.master)
#         whatsapp_window.title("Send WhatsApp Message")
#         whatsapp_window.geometry("400x400")
#         whatsapp_window.configure(bg="#1E1E2F")
#
#         tk.Label(whatsapp_window, text="Recipient Phone Number (with country code):", font=("Roboto", 12), bg="#1E1E2F", fg="#E0E0E0").pack(pady=5)
#         phone_entry = tk.Entry(whatsapp_window, width=40, font=("Roboto", 12), bg="#2D2D44", fg="#E0E0E0", insertbackground="#00D4FF")
#         phone_entry.pack(pady=5)
#
#         tk.Label(whatsapp_window, text="Message:", font=("Roboto", 12), bg="#1E1E2F", fg="#E0E0E0").pack(pady=5)
#         message_text = tk.Text(whatsapp_window, width=40, height=6, font=("Roboto", 12), bg="#2D2D44", fg="#E0E0E0", insertbackground="#00D4FF")
#         message_text.pack(pady=5)
#
#         def send_whatsapp_message():
#             phone_number = phone_entry.get()
#             message = message_text.get("1.0", "end-1c").strip()
#             if not phone_number or not message:
#                 messagebox.showwarning("Input Error", "Please enter both phone number and message.")
#                 return
#             if not phone_number.startswith("+"):
#                 messagebox.showwarning("Input Error", "Phone number must include the country code (e.g., +1 for USA).")
#                 return
#             try:
#                 kit.sendwhatmsg_instantly(phone_number, message, wait_time=10)
#                 time.sleep(10)
#                 pyautogui.press("enter")
#                 messagebox.showinfo("Success", f"WhatsApp message sent to {phone_number}!")
#                 whatsapp_window.destroy()
#             except Exception as e:
#                 messagebox.showerror("Error", f"An error occurred: {e}")
#                 whatsapp_window.destroy()
#
#         def send_whatsapp_to_all():
#             message = message_text.get("1.0", "end-1c").strip()
#             if not message:
#                 messagebox.showwarning("Input Error", "Please enter a message.")
#                 return
#             if not self.sms_notifier.phone_numbers:
#                 messagebox.showwarning("Error", "No phone numbers loaded from Excel. Please upload an Excel file.")
#                 return
#             success = True
#             for phone_number in self.sms_notifier.phone_numbers:
#                 try:
#                     kit.sendwhatmsg_instantly(phone_number, message, wait_time=10)
#                     time.sleep(10)
#                     pyautogui.press("enter")
#                     time.sleep(5)
#                 except Exception as e:
#                     messagebox.showerror("Error", f"Error sending WhatsApp message to {phone_number}: {e}")
#                     success = False
#             if success:
#                 messagebox.showinfo("Success", "WhatsApp messages sent to all numbers!")
#                 whatsapp_window.destroy()
#             else:
#                 whatsapp_window.destroy()
#
#         tk.Button(whatsapp_window, text="Send to Single", command=send_whatsapp_message, bg="#39FF14", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(pady=5)
#         tk.Button(whatsapp_window, text="Send to All", command=send_whatsapp_to_all, bg="#00D4FF", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(pady=5)
#
#     def open_email_window(self):
#         email_window = tk.Toplevel(self.master)
#         email_window.title("Send Email")
#         email_window.geometry("400x400")
#         email_window.configure(bg="#1E1E2F")
#
#         tk.Label(email_window, text="Recipient Email:", font=("Roboto", 12), bg="#1E1E2F", fg="#E0E0E0").pack(pady=5)
#         receiver_entry = tk.Entry(email_window, width=40, font=("Roboto", 12), bg="#2D2D44", fg="#E0E0E0", insertbackground="#00D4FF")
#         receiver_entry.pack(pady=5)
#
#         tk.Label(email_window, text="Message:", font=("Roboto", 12), bg="#1E1E2F", fg="#E0E0E0").pack(pady=5)
#         message_text = tk.Text(email_window, width=40, height=8, font=("Roboto", 12), bg="#2D2D44", fg="#E0E0E0", insertbackground="#00D4FF")
#         message_text.pack(pady=5)
#
#         predefined_message = """
#            Subject: Important Notification
#
#            Dear [Recipient Name],
#
#            This is to inform you about [your message].
#
#            Regards,
#            Your Company
#            """
#         message_text.insert("1.0", predefined_message)
#
#         def send_email(receiver_email, email_body):
#             if not SENDER_EMAIL or not SENDER_EMAIL_PASSWORD:
#                 messagebox.showerror("Error", "Email credentials are missing!")
#                 return False
#             if not is_valid_email(receiver_email):
#                 messagebox.showerror("Error", "Invalid email address!")
#                 return False
#             msg = MIMEMultipart()
#             msg["From"] = SENDER_EMAIL
#             msg["To"] = receiver_email
#             msg["Subject"] = "Hello from Notify!me"
#             msg.attach(MIMEText(email_body, "plain"))
#             try:
#                 server = smtplib.SMTP("smtp.gmail.com", 587)
#                 server.starttls()
#                 server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
#                 server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
#                 server.quit()
#                 return True
#             except Exception as e:
#                 messagebox.showerror("Error", f"Failed to send email to {receiver_email}:\n{e}")
#                 return False
#
#         def send_single_email():
#             receiver_email = receiver_entry.get().strip()
#             email_body = message_text.get("1.0", tk.END).strip()
#             if not receiver_email or not email_body:
#                 messagebox.showerror("Error", "Please enter recipient email and message.")
#                 return
#             if send_email(receiver_email, email_body):
#                 messagebox.showinfo("Success", "Email sent successfully!")
#                 email_window.destroy()
#             else:
#                 email_window.destroy()
#
#         def send_bulk_email():
#             email_body = message_text.get("1.0", tk.END).strip()
#             if not email_body:
#                 messagebox.showerror("Error", "Please enter a message.")
#                 return
#             if not self.sms_notifier.email_addresses:
#                 messagebox.showerror("Error", "No email contacts loaded.")
#                 return
#             success_count = 0
#             for email in self.sms_notifier.email_addresses:
#                 if send_email(email, email_body):
#                     success_count += 1
#             if success_count == len(self.sms_notifier.email_addresses):
#                 messagebox.showinfo("Success", f"Emails sent successfully to {success_count} recipients!")
#                 email_window.destroy()
#             else:
#                 messagebox.showinfo("Partial Success", f"Emails sent to {success_count} out of {len(self.sms_notifier.email_addresses)} recipients.")
#                 email_window.destroy()
#
#         tk.Button(email_window, text="Send to Single", command=send_single_email, bg="#39FF14", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(pady=5)
#         tk.Button(email_window, text="Send to All", command=send_bulk_email, bg="#00D4FF", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(pady=5)
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.state("zoomed")
#     app = SMSNotifierGUI(root)
#     root.mainloop()




# import os
# import re
# from twilio.rest import Client
# import tkinter as tk
# from tkinter import filedialog, messagebox, scrolledtext
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import smtplib
# import pandas as pd
# from dotenv import load_dotenv
# import pywhatkit as kit
# import pyautogui
# import time
#
# load_dotenv()
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
# SENDER_EMAIL = os.getenv("SENDER_EMAIL")
# SENDER_EMAIL_PASSWORD = os.getenv("SENDER_EMAIL_PASSWORD")
# EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#
# def is_valid_email(email):
#     return re.match(EMAIL_REGEX, email) is not None
#
# class SMSNotifier:
#     def __init__(self):
#         self.phone_numbers = []
#         self.email_addresses = []
#
#     def open_file(self):
#         file_path = filedialog.askopenfilename(
#             title="Select file to upload",
#             filetypes=[("Excel files", "*.xlsx;*.xls")]
#         )
#         if file_path:
#             try:
#                 data = pd.read_excel(file_path)
#                 if "Ph_no" in data.columns:
#                     self.phone_numbers = data["Ph_no"].astype(str).tolist()
#                 if "Email" in data.columns:
#                     self.email_addresses = [email for email in data["Email"].astype(str).tolist() if is_valid_email(email)]
#                 messagebox.showinfo("Success",
#                                     f"Loaded all valid phone numbers and emails.")
#             except Exception as e:
#                 messagebox.showerror("Error", f"Error reading the Excel file: {e}")
#
#     def send_sms(self, message):
#         if not self.phone_numbers:
#             messagebox.showerror("Error", "No phone numbers loaded!")
#             return False
#         if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUMBER:
#             messagebox.showerror("Error", "Twilio credentials are missing!")
#             return False
#         try:
#             client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#             for phone_number in self.phone_numbers:
#                 client.messages.create(
#                     body=message,
#                     from_=TWILIO_PHONE_NUMBER,
#                     to=phone_number
#                 )
#             messagebox.showinfo("Success", f"SMS messages sent to {len(self.phone_numbers)} numbers.")
#             return True
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to send SMS messages: {e}")
#             return False
#
# class SMSNotifierGUI:
#     def __init__(self, master, root=None, prev_window=None):
#         if prev_window:
#             prev_window.destroy()
#         self.master = master
#         self.root = root
#         self.master.title("Send Notifications")
#         self.master.state('zoomed')
#         self.master.configure(bg="#2B2B2B")
#         self.sms_notifier = SMSNotifier()
#
#         tk.Label(master, text="Send Bulk Notifications", font=("Roboto", 16, "bold"), bg="#2B2B2B", fg="#E0E0E0").pack(pady=100)
#         self.upload_btn = tk.Button(master, text="Upload Excel", command=self.sms_notifier.open_file, font=("Roboto", 12, "bold"), bg="#4A90E2", fg="#E0E0E0", relief="flat", padx=10, pady=5)
#         self.upload_btn.pack(pady=5)
#
#         button_frame = tk.Frame(master, bg="#2B2B2B")
#         button_frame.pack(expand=True)
#
#         self.whatsapp_img = tk.PhotoImage(file="whatsapp_icon.png")
#         self.email_img = tk.PhotoImage(file="gmail_icon.png")
#         self.sms_img = tk.PhotoImage(file="sms_icon.png")
#
#         self.whatsapp_button = tk.Button(button_frame, image=self.whatsapp_img, compound="left",
#                                          bg="#4A90E2", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5,
#                                          command=self.open_whatsapp_window)
#         self.whatsapp_button.pack(side="left", padx=10)
#
#         self.email_button = tk.Button(button_frame, image=self.email_img, compound="left",
#                                       bg="#4A90E2", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5,
#                                       command=self.open_email_window)
#         self.email_button.pack(side="left", padx=10)
#
#         self.send_btn = tk.Button(button_frame, image=self.sms_img, compound="left",
#                                   font=("Roboto", 12, "bold"), bg="#4A90E2", fg="#E0E0E0", relief="flat", padx=10, pady=5,
#                                   command=self.open_sms_window)
#         self.send_btn.pack(side="left", padx=10)
#
#         self.back_button = tk.Button(master, text="Back", command=lambda: self.back_to_dashboard(),
#                                      bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5)
#         self.back_button.pack(side="bottom", anchor="se", padx=10, pady=10)
#
#     def back_to_dashboard(self):
#         from dashboard import open_dashboard
#         self.master.destroy()
#         open_dashboard(root=self.root, prev_window=self.master)
#
#     def open_sms_window(self):
#         sms_window = tk.Toplevel(self.master)
#         sms_window.title("Send SMS Message")
#         sms_window.geometry("400x400")
#         sms_window.configure(bg="#2B2B2B")
#
#         tk.Label(sms_window, text="Recipient Phone Number (with country code):", font=("Roboto", 12), bg="#2B2B2B", fg="#E0E0E0").pack(pady=5)
#         phone_entry = tk.Entry(sms_window, width=40, font=("Roboto", 12), bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#         phone_entry.pack(pady=5)
#
#         tk.Label(sms_window, text="Message:", font=("Roboto", 12), bg="#2B2B2B", fg="#E0E0E0").pack(pady=5)
#         message_text = tk.Text(sms_window, width=40, height=6, font=("Roboto", 12), bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#         message_text.pack(pady=5)
#
#         def send_sms_message():
#             phone_number = phone_entry.get()
#             message = message_text.get("1.0", "end-1c").strip()
#             if not phone_number or not message:
#                 messagebox.showwarning("Input Error", "Please enter both phone number and message.")
#                 return
#             if not phone_number.startswith("+"):
#                 messagebox.showwarning("Input Error", "Phone number must include the country code (e.g., +1 for USA).")
#                 return
#             try:
#                 client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#                 client.messages.create(
#                     body=message,
#                     from_=TWILIO_PHONE_NUMBER,
#                     to=phone_number
#                 )
#                 messagebox.showinfo("Success", f"SMS message sent to {phone_number}!")
#                 sms_window.destroy()
#             except Exception as e:
#                 messagebox.showerror("Error", f"An error occurred: {e}")
#                 sms_window.destroy()
#
#         def send_sms_to_all():
#             message = message_text.get("1.0", "end-1c").strip()
#             if not message:
#                 messagebox.showwarning("Input Error", "Please enter a message.")
#                 return
#             if not self.sms_notifier.phone_numbers:
#                 messagebox.showwarning("Error", "No phone numbers loaded from Excel. Please upload an Excel file.")
#                 return
#             if self.sms_notifier.send_sms(message):
#                 sms_window.destroy()
#             else:
#                 sms_window.destroy()
#
#         tk.Button(sms_window, text="Send to Single", command=send_sms_message, bg="#50C878", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(pady=5)
#         tk.Button(sms_window, text="Send to All", command=send_sms_to_all, bg="#4A90E2", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(pady=5)
#
#     def open_whatsapp_window(self):
#         whatsapp_window = tk.Toplevel(self.master)
#         whatsapp_window.title("Send WhatsApp Message")
#         whatsapp_window.geometry("400x400")
#         whatsapp_window.configure(bg="#2B2B2B")
#
#         tk.Label(whatsapp_window, text="Recipient Phone Number (with country code):", font=("Roboto", 12), bg="#2B2B2B", fg="#E0E0E0").pack(pady=5)
#         phone_entry = tk.Entry(whatsapp_window, width=40, font=("Roboto", 12), bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#         phone_entry.pack(pady=5)
#
#         tk.Label(whatsapp_window, text="Message:", font=("Roboto", 12), bg="#2B2B2B", fg="#E0E0E0").pack(pady=5)
#         message_text = tk.Text(whatsapp_window, width=40, height=6, font=("Roboto", 12), bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#         message_text.pack(pady=5)
#
#         def send_whatsapp_message():
#             phone_number = phone_entry.get()
#             message = message_text.get("1.0", "end-1c").strip()
#             if not phone_number or not message:
#                 messagebox.showwarning("Input Error", "Please enter both phone number and message.")
#                 return
#             if not phone_number.startswith("+"):
#                 messagebox.showwarning("Input Error", "Phone number must include the country code (e.g., +1 for USA).")
#                 return
#             try:
#                 kit.sendwhatmsg_instantly(phone_number, message, wait_time=10)
#                 time.sleep(10)
#                 pyautogui.press("enter")
#                 messagebox.showinfo("Success", f"WhatsApp message sent to {phone_number}!")
#                 whatsapp_window.destroy()
#             except Exception as e:
#                 messagebox.showerror("Error", f"An error occurred: {e}")
#                 whatsapp_window.destroy()
#
#         def send_whatsapp_to_all():
#             message = message_text.get("1.0", "end-1c").strip()
#             if not message:
#                 messagebox.showwarning("Input Error", "Please enter a message.")
#                 return
#             if not self.sms_notifier.phone_numbers:
#                 messagebox.showwarning("Error", "No phone numbers loaded from Excel. Please upload an Excel file.")
#                 return
#             try:
#                 for phone_number in self.sms_notifier.phone_numbers:
#                     if not phone_number.startswith("+"):
#                         messagebox.showwarning("Input Error", f"Phone number {phone_number} must include the country code (e.g., +1 for USA).")
#                         continue
#                     kit.sendwhatmsg_instantly(phone_number, message, wait_time=10)
#                     time.sleep(10)
#                     pyautogui.press("enter")
#                 messagebox.showinfo("Success", f"WhatsApp messages sent to {len(self.sms_notifier.phone_numbers)} numbers!")
#                 whatsapp_window.destroy()
#             except Exception as e:
#                 messagebox.showerror("Error", f"An error occurred: {e}")
#                 whatsapp_window.destroy()
#
#         tk.Button(whatsapp_window, text="Send to Single", command=send_whatsapp_message, bg="#50C878", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(pady=5)
#         tk.Button(whatsapp_window, text="Send to All", command=send_whatsapp_to_all, bg="#4A90E2", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(pady=5)
#
#     def open_email_window(self):
#         email_window = tk.Toplevel(self.master)
#         email_window.title("Send Email")
#         email_window.geometry("400x500")
#         email_window.configure(bg="#2B2B2B")
#
#         tk.Label(email_window, text="Recipient Email:", font=("Roboto", 12), bg="#2B2B2B", fg="#E0E0E0").pack(pady=5)
#         email_entry = tk.Entry(email_window, width=40, font=("Roboto", 12), bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#         email_entry.pack(pady=5)
#
#         tk.Label(email_window, text="Subject:", font=("Roboto", 12), bg="#2B2B2B", fg="#E0E0E0").pack(pady=5)
#         subject_entry = tk.Entry(email_window, width=40, font=("Roboto", 12), bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#         subject_entry.pack(pady=5)
#
#         tk.Label(email_window, text="Message:", font=("Roboto", 12), bg="#2B2B2B", fg="#E0E0E0").pack(pady=5)
#         message_text = tk.Text(email_window, width=40, height=6, font=("Roboto", 12), bg="#3A3A3A", fg="#E0E0E0", insertbackground="#4A90E2")
#         message_text.pack(pady=5)
#
#         def send_email_message():
#             recipient_email = email_entry.get()
#             subject = subject_entry.get()
#             message = message_text.get("1.0", "end-1c").strip()
#             if not recipient_email or not subject or not message:
#                 messagebox.showwarning("Input Error", "Please enter recipient email, subject, and message.")
#                 return
#             if not is_valid_email(recipient_email):
#                 messagebox.showwarning("Input Error", "Please enter a valid email address.")
#                 return
#             try:
#                 msg = MIMEMultipart()
#                 msg['From'] = SENDER_EMAIL
#                 msg['To'] = recipient_email
#                 msg['Subject'] = subject
#                 msg.attach(MIMEText(message, 'plain'))
#                 with smtplib.SMTP('smtp.gmail.com', 587) as server:
#                     server.starttls()
#                     server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
#                     server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
#                 messagebox.showinfo("Success", f"Email sent to {recipient_email}!")
#                 email_window.destroy()
#             except Exception as e:
#                 messagebox.showerror("Error", f"An error occurred: {e}")
#                 email_window.destroy()
#
#         def send_email_to_all():
#             subject = subject_entry.get()
#             message = message_text.get("1.0", "end-1c").strip()
#             if not subject or not message:
#                 messagebox.showwarning("Input Error", "Please enter subject and message.")
#                 return
#             if not self.sms_notifier.email_addresses:
#                 messagebox.showwarning("Error", "No email addresses loaded from Excel. Please upload an Excel file.")
#                 return
#             try:
#                 with smtplib.SMTP('smtp.gmail.com', 587) as server:
#                     server.starttls()
#                     server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
#                     for email in self.sms_notifier.email_addresses:
#                         msg = MIMEMultipart()
#                         msg['From'] = SENDER_EMAIL
#                         msg['To'] = email
#                         msg['Subject'] = subject
#                         msg.attach(MIMEText(message, 'plain'))
#                         server.sendmail(SENDER_EMAIL, email, msg.as_string())
#                 messagebox.showinfo("Success", f"Emails sent to {len(self.sms_notifier.email_addresses)} addresses!")
#                 email_window.destroy()
#             except Exception as e:
#                 messagebox.showerror("Error", f"An error occurred: {e}")
#                 email_window.destroy()
#
#         tk.Button(email_window, text="Send to Single", command=send_email_message, bg="#50C878", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(pady=5)
#         tk.Button(email_window, text="Send to All", command=send_email_to_all, bg="#4A90E2", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5).pack(pady=5)
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = SMSNotifierGUI(root)
#     root.mainloop()



import os
import re
from twilio.rest import Client
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import pandas as pd
from dotenv import load_dotenv
import pywhatkit as kit #pywhatmsg_instantly
import pyautogui  #press
import time

# Load environment variables from .env file
load_dotenv()

# Twilio and Email credentials from .env
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_EMAIL_PASSWORD = os.getenv("SENDER_EMAIL_PASSWORD")

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def is_valid_email(email):
    return re.match(EMAIL_REGEX, email) is not None

class SMSNotifier:
    def __init__(self):
        self.phone_numbers = []
        self.email_addresses = []

    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Select file to upload",
            filetypes=[("Excel files", "*.xlsx;*.xls")]
        )
        if file_path:
            try:
                data = pd.read_excel(file_path)
                if "Ph_no" in data.columns:
                    self.phone_numbers = data["Ph_no"].astype(str).tolist()
                if "Email" in data.columns:
                    self.email_addresses = [email for email in data["Email"].astype(str).tolist() if is_valid_email(email)]
                messagebox.showinfo("Success",
                                    f"Loaded {len(self.phone_numbers)} phone numbers and {len(self.email_addresses)} valid emails.")
            except Exception as e:
                messagebox.showerror("Error", f"Error reading the Excel file: {e}")

    def send_sms(self, message):
        if not self.phone_numbers:
            messagebox.showerror("Error", "No phone numbers loaded!")
            return False
        if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUMBER:
            messagebox.showerror("Error", "Twilio credentials are missing!")
            return False
        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            for phone_number in self.phone_numbers:
                client.messages.create(
                    body=message,
                    from_=TWILIO_PHONE_NUMBER,
                    to=phone_number
                )
            messagebox.showinfo("Success", f"SMS messages sent to {len(self.phone_numbers)} numbers.")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send SMS messages: {e}")
            return False

class SMSNotifierGUI:
    def __init__(self, master, root=None, prev_window=None):
        if prev_window:
            prev_window.destroy()
        self.master = master
        self.root = root
        self.master.title("Send Notifications")
        self.master.state('zoomed')
        self.master.configure(bg="#1a1a1a")  # Unified dark theme

        self.sms_notifier = SMSNotifier()

        tk.Label(master, text="Send Bulk Notifications", font=("Roboto", 16, "bold"), bg="#1a1a1a", fg="#69dbc8").pack(pady=100)

        self.upload_btn = tk.Button(master, text="Upload Excel", command=self.sms_notifier.open_file,
                                    font=("Roboto", 12, "bold"), bg="#5192ed", fg="white", relief="flat", padx=10, pady=5,
                                    activebackground="#406fb3")
        self.upload_btn.pack(pady=5)
        self.upload_btn.bind("<Enter>", lambda e: self.upload_btn.config(bg="#406fb3"))
        self.upload_btn.bind("<Leave>", lambda e: self.upload_btn.config(bg="#5192ed"))

        button_frame = tk.Frame(master, bg="#1a1a1a")
        button_frame.pack(expand=True)

        # Load images for buttons
        self.whatsapp_img = tk.PhotoImage(file="whatsapp_icon.png")
        self.email_img = tk.PhotoImage(file="gmail_icon.png")
        self.sms_img = tk.PhotoImage(file="sms_icon.png")

        self.whatsapp_button = tk.Button(button_frame, image=self.whatsapp_img, compound="left",
                                         bg="#41d627", fg="black", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5,
                                         command=self.open_whatsapp_window, activebackground="#33aa1e")
        self.whatsapp_button.pack(side="left", padx=10)
        self.whatsapp_button.bind("<Enter>", lambda e: self.whatsapp_button.config(bg="#33aa1e"))
        self.whatsapp_button.bind("<Leave>", lambda e: self.whatsapp_button.config(bg="#41d627"))

        self.email_button = tk.Button(button_frame, image=self.email_img, compound="left",
                                      bg="#ff0000", fg="white", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5,
                                      command=self.open_email_window, activebackground="#cc0000")
        self.email_button.pack(side="left", padx=10)
        self.email_button.bind("<Enter>", lambda e: self.email_button.config(bg="#cc0000"))
        self.email_button.bind("<Leave>", lambda e: self.email_button.config(bg="#ff0000"))

        self.send_btn = tk.Button(button_frame, image=self.sms_img, compound="left",
                                  font=("Roboto", 12, "bold"), bg="#69dbc8", fg="black", relief="flat", padx=10, pady=5,
                                  command=self.open_sms_window, activebackground="#54b0a0")
        self.send_btn.pack(side="left", padx=10)
        self.send_btn.bind("<Enter>", lambda e: self.send_btn.config(bg="#54b0a0"))
        self.send_btn.bind("<Leave>", lambda e: self.send_btn.config(bg="#69dbc8"))

        self.back_button = tk.Button(master, text="Back", command=lambda: self.back_to_dashboard(),
                                     bg="#FF5555", fg="#E0E0E0", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5,
                                     activebackground="#cc4444")
        self.back_button.pack(side="bottom", anchor="se", padx=10, pady=10)
        self.back_button.bind("<Enter>", lambda e: self.back_button.config(bg="#cc4444"))
        self.back_button.bind("<Leave>", lambda e: self.back_button.config(bg="#FF5555"))

    def back_to_dashboard(self):
        try:
            from dashboard import open_dashboard
            self.master.destroy()
            open_dashboard(root=self.root, prev_window=self.master)
        except ImportError:
            self.master.destroy()

    def open_sms_window(self):
        sms_window = tk.Toplevel(self.master)
        sms_window.title("Send SMS Message")
        sms_window.geometry("400x400")
        sms_window.configure(bg="#1a1a1a")

        tk.Label(sms_window, text="Recipient Phone Number (with country code):", font=("Roboto", 12), bg="#1a1a1a", fg="#ffffff").pack(pady=5)
        phone_entry = tk.Entry(sms_window, width=40, font=("Roboto", 12), bg="#333333", fg="white", insertbackground="#69dbc8")
        phone_entry.pack(pady=5)

        tk.Label(sms_window, text="Message:", font=("Roboto", 12), bg="#1a1a1a", fg="#ffffff").pack(pady=5)
        message_text = tk.Text(sms_window, width=40, height=6, font=("Roboto", 12), bg="#333333", fg="white", insertbackground="#69dbc8")
        message_text.pack(pady=5)

        def send_sms_message():
            phone_number = phone_entry.get()
            message = message_text.get("1.0", "end-1c").strip()
            if not phone_number or not message:
                messagebox.showwarning("Input Error", "Please enter both phone number and message.")
                return
            if not phone_number.startswith("+"):
                messagebox.showwarning("Input Error", "Phone number must include the country code (e.g., +1 for USA).")
                return
            try:
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                client.messages.create(
                    body=message,
                    from_=TWILIO_PHONE_NUMBER,
                    to=phone_number
                )
                messagebox.showinfo("Success", f"SMS message sent to {phone_number}!")
                sms_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                sms_window.destroy()

        def send_sms_to_all():
            message = message_text.get("1.0", "end-1c").strip()
            if not message:
                messagebox.showwarning("Input Error", "Please enter a message.")
                return
            if not self.sms_notifier.phone_numbers:
                messagebox.showwarning("Error", "No phone numbers loaded from Excel. Please upload an Excel file.")
                return
            if self.sms_notifier.send_sms(message):
                sms_window.destroy()
            else:
                sms_window.destroy()

        tk.Button(sms_window, text="Send to Single", command=send_sms_message, bg="#41d627", fg="black", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5,
                  activebackground="#33aa1e").pack(pady=5)
        tk.Button(sms_window, text="Send to All", command=send_sms_to_all, bg="#5192ed", fg="white", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5,
                  activebackground="#406fb3").pack(pady=5)

    def open_whatsapp_window(self):
        whatsapp_window = tk.Toplevel(self.master)
        whatsapp_window.title("Send WhatsApp Message")
        whatsapp_window.geometry("400x400")
        whatsapp_window.configure(bg="#1a1a1a")

        tk.Label(whatsapp_window, text="Recipient Phone Number (with country code):", font=("Roboto", 12), bg="#1a1a1a", fg="#ffffff").pack(pady=5)
        phone_entry = tk.Entry(whatsapp_window, width=40, font=("Roboto", 12), bg="#333333", fg="white", insertbackground="#69dbc8")
        phone_entry.pack(pady=5)

        tk.Label(whatsapp_window, text="Message:", font=("Roboto", 12), bg="#1a1a1a", fg="#ffffff").pack(pady=5)
        message_text = tk.Text(whatsapp_window, width=40, height=6, font=("Roboto", 12), bg="#333333", fg="white", insertbackground="#69dbc8")
        message_text.pack(pady=5)

        def send_whatsapp_message():
            phone_number = phone_entry.get()
            message = message_text.get("1.0", "end-1c").strip()
            if not phone_number or not message:
                messagebox.showwarning("Input Error", "Please enter both phone number and message.")
                return
            if not phone_number.startswith("+"):
                messagebox.showwarning("Input Error", "Phone number must include the country code (e.g., +1 for USA).")
                return
            try:
                kit.sendwhatmsg_instantly(phone_number, message, wait_time=10)
                time.sleep(10)
                pyautogui.press("enter")
                messagebox.showinfo("Success", f"WhatsApp message sent to {phone_number}!")
                whatsapp_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                whatsapp_window.destroy()

        def send_whatsapp_to_all():
            message = message_text.get("1.0", "end-1c").strip()
            if not message:
                messagebox.showwarning("Input Error", "Please enter a message.")
                return
            if not self.sms_notifier.phone_numbers:
                messagebox.showwarning("Error", "No phone numbers loaded from Excel. Please upload an Excel file.")
                return
            success = True
            for phone_number in self.sms_notifier.phone_numbers:
                if not phone_number.startswith("+"):
                    messagebox.showwarning("Input Error", f"Phone number {phone_number} must include the country code (e.g., +1 for USA).")
                    continue
                try:
                    kit.sendwhatmsg_instantly(phone_number, message, wait_time=10)
                    time.sleep(10)
                    pyautogui.press("enter")
                    time.sleep(5)
                except Exception as e:
                    messagebox.showerror("Error", f"Error sending WhatsApp message to {phone_number}: {e}")
                    success = False
            if success:
                messagebox.showinfo("Success", f"WhatsApp messages sent to {len(self.sms_notifier.phone_numbers)} numbers!")
                whatsapp_window.destroy()
            else:
                whatsapp_window.destroy()

        tk.Button(whatsapp_window, text="Send to Single", command=send_whatsapp_message, bg="#41d627", fg="black", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5,
                  activebackground="#33aa1e").pack(pady=5)
        tk.Button(whatsapp_window, text="Send to All", command=send_whatsapp_to_all, bg="#5192ed", fg="white", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5,
                  activebackground="#406fb3").pack(pady=5)

    def open_email_window(self):
        email_window = tk.Toplevel(self.master)
        email_window.title("Send Email")
        email_window.geometry("400x500")
        email_window.configure(bg="#1a1a1a")

        tk.Label(email_window, text="Recipient Email:", font=("Roboto", 12), bg="#1a1a1a", fg="#ffffff").pack(pady=5)
        email_entry = tk.Entry(email_window, width=40, font=("Roboto", 12), bg="#333333", fg="white", insertbackground="#69dbc8")
        email_entry.pack(pady=5)

        tk.Label(email_window, text="Subject:", font=("Roboto", 12), bg="#1a1a1a", fg="#ffffff").pack(pady=5)
        subject_entry = tk.Entry(email_window, width=40, font=("Roboto", 12), bg="#333333", fg="white", insertbackground="#69dbc8")
        subject_entry.pack(pady=5)

        tk.Label(email_window, text="Message:", font=("Roboto", 12), bg="#1a1a1a", fg="#ffffff").pack(pady=5)
        message_text = tk.Text(email_window, width=40, height=8, font=("Roboto", 12), bg="#333333", fg="white", insertbackground="#69dbc8")
        message_text.pack(pady=5)

        predefined_message = """
           Subject: Important Notification

           Dear [Recipient Name],

           This is to inform you about [your message].

           Regards,
           Your Company
           """
        message_text.insert("1.0", predefined_message)

        def send_email(receiver_email, subject, email_body):
            if not SENDER_EMAIL or not SENDER_EMAIL_PASSWORD:
                messagebox.showerror("Error", "Email credentials are missing!")
                return False
            if not is_valid_email(receiver_email):
                messagebox.showerror("Error", "Invalid email address!")
                return False
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL
            msg["To"] = receiver_email
            msg["Subject"] = subject
            msg.attach(MIMEText(email_body, "plain"))
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
                server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
                server.quit()
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send email to {receiver_email}:\n{e}")
                return False

        def send_single_email():
            receiver_email = email_entry.get().strip()
            subject = subject_entry.get().strip()
            email_body = message_text.get("1.0", tk.END).strip()
            if not receiver_email or not subject or not email_body:
                messagebox.showerror("Error", "Please enter recipient email, subject, and message.")
                return
            if send_email(receiver_email, subject, email_body):
                messagebox.showinfo("Success", "Email sent successfully!")
                email_window.destroy()
            else:
                email_window.destroy()

        def send_bulk_email():
            subject = subject_entry.get().strip()
            email_body = message_text.get("1.0", tk.END).strip()
            if not subject or not email_body:
                messagebox.showerror("Error", "Please enter subject and message.")
                return
            if not self.sms_notifier.email_addresses:
                messagebox.showerror("Error", "No email addresses loaded from Excel. Please upload an Excel file.")
                return
            success_count = 0
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
                for email in self.sms_notifier.email_addresses:
                    if send_email(email, subject, email_body):
                        success_count += 1
            if success_count == len(self.sms_notifier.email_addresses):
                messagebox.showinfo("Success", f"Emails sent successfully to {success_count} recipients!")
                email_window.destroy()
            else:
                messagebox.showinfo("Partial Success", f"Emails sent to {success_count} out of {len(self.sms_notifier.email_addresses)} recipients.")
                email_window.destroy()

        tk.Button(email_window, text="Send to Single", command=send_single_email, bg="#41d627", fg="black", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5,
                  activebackground="#33aa1e").pack(pady=5)
        tk.Button(email_window, text="Send to All", command=send_bulk_email, bg="#5192ed", fg="white", font=("Roboto", 12, "bold"), relief="flat", padx=10, pady=5,
                  activebackground="#406fb3").pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = SMSNotifierGUI(root)
    root.mainloop()



