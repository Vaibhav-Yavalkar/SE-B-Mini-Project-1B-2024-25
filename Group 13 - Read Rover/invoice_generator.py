from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

class InvoiceGenerator:
    def __init__(self, invoice_id, user_name, books, total_price, save_path="invoices/"):
        self.invoice_id = invoice_id
        self.user_name = user_name
        self.books = books  # List of tuples: (title, price, quantity)
        self.total_price = total_price
        self.save_path = save_path
        self.invoice_file = f"{save_path}Invoice_{invoice_id}.pdf"

        if not os.path.exists(save_path):
            os.makedirs(save_path)

    def generate_pdf(self):
        c = canvas.Canvas(self.invoice_file, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Header
        c.drawString(30, 750, "Thrift Bookstore - Invoice")
        c.drawString(30, 735, f"Invoice ID: {self.invoice_id}")
        c.drawString(30, 720, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(30, 705, f"Customer: {self.user_name}")

        # Table Headers
        c.drawString(30, 670, "Book Title")
        c.drawString(250, 670, "Price")
        c.drawString(320, 670, "Quantity")
        c.drawString(400, 670, "Total")

        y = 650  # Start position for book details
        for book in self.books:
            title, price, qty = book
            total = price * qty
            c.drawString(30, y, title)
            c.drawString(250, y, f"${price:.2f}")
            c.drawString(320, y, str(qty))
            c.drawString(400, y, f"${total:.2f}")
            y -= 20

        # Total Price
        c.drawString(30, y - 20, f"Grand Total: ${self.total_price:.2f}")

        # Save PDF
        c.save()
        return self.invoice_file

# Example Usage
if __name__ == "__main__":
    books_purchased = [("Python for Beginners", 19.99, 1), ("Data Science Guide", 35.50, 2)]
    total = sum(price * qty for _, price, qty in books_purchased)

    invoice = InvoiceGenerator(invoice_id=101, user_name="John Doe", books=books_purchased, total_price=total)
    pdf_path = invoice.generate_pdf()
    print(f"Invoice saved at: {pdf_path}")
