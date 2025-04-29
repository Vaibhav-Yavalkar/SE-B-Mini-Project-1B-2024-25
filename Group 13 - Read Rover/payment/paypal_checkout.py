import tkinter as tk
from tkinter import ttk, messagebox
import paypalrestsdk

# PayPal API Setup
paypalrestsdk.configure({
    "mode": "sandbox",  # Use "live" for real transactions
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
})

class PayPalPayment:
    def __init__(self, total_amount, on_payment_success):
        self.total_amount = total_amount
        self.on_payment_success = on_payment_success

    def process_payment(self):
        """Process PayPal Payment"""
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:3000/payment_success",
                "cancel_url": "http://localhost:3000/payment_cancel"
            },
            "transactions": [{
                "amount": {
                    "total": f"{self.total_amount:.2f}",
                    "currency": "USD"
                },
                "description": "Book Purchase from Mini Project"
            }]
        })

        if payment.create():
            approval_url = next(link.href for link in payment.links if link.rel == "approval_url")
            messagebox.showinfo("Redirect", f"Please visit this link to complete payment:\n{approval_url}")
        else:
            messagebox.showerror("Payment Error", f"Failed: {payment.error}")

class CheckoutWindow:
    def __init__(self, root, total_amount):
        self.root = root
        self.total_amount = total_amount
        self.window = tk.Toplevel(self.root)
        self.window.title("Checkout")
        self.window.geometry("300x200")

        tk.Label(self.window, text=f"Total: ${self.total_amount:.2f}", font=("Arial", 14)).pack(pady=10)
        
        ttk.Button(self.window, text="Pay with PayPal", command=self.pay_with_paypal).pack(pady=5)
        ttk.Button(self.window, text="Cancel", command=self.window.destroy).pack(pady=5)

    def pay_with_paypal(self):
        """Initiate PayPal Payment"""
        paypal_payment = PayPalPayment(self.total_amount, self.payment_successful)
        paypal_payment.process_payment()

    def payment_successful(self):
        """Handle successful payment actions"""
        messagebox.showinfo("Success", "Payment completed successfully!")
        self.window.destroy()

# Example Usage
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the empty Tkinter window
    CheckoutWindow(root, total_amount=29.99)  # Example total amount
    root.mainloop()
