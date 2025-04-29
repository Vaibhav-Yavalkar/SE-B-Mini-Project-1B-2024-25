import tkinter as tk
from tkinter import ttk, messagebox
from sell_book import SellBookWindow  
from buy_book import BuyBookWindow 
from donate_book import DonateBookWindow
from profile import ProfileWindow  
from donated_books import ViewDonatedBooksWindow

class Dashboard:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Dashboard - Read Rover")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#e3f2fd")

        # Frame for UI content
        self.frame = tk.Frame(self.root, bg="#e3f2fd")
        self.frame.pack(fill="both", expand=True)

        # Title Label
        title_label = tk.Label(self.frame, text="📚 Read Rover Dashboard", font=("Helvetica", 18, "bold"), fg="#1e88e5", bg="#e3f2fd")
        title_label.pack(pady=10)

        # Subtitle
        subtitle_label = tk.Label(self.frame, text="Explore your options below", font=("Helvetica", 12), fg="#555", bg="#e3f2fd")
        subtitle_label.pack(pady=5)

        # Add Dark Mode Toggle
        self.dark_mode = False
        self.toggle_button = tk.Button(self.frame, text="🌙 Dark Mode", command=self.toggle_theme, font=("Helvetica", 10, "bold"), bg="#42a5f5", fg="white")
        self.toggle_button.pack(pady=5)

        # Buttons
        self.create_buttons(self.frame)

        # Status Bar
        self.status_label = tk.Label(self.root, text="Ready", font=("Helvetica", 10), bg="#e3f2fd", fg="#555")
        self.status_label.pack(side="bottom", fill="x")

        # Track open windows
        self.open_windows = {}

        # Handle Exit Confirmation
        self.root.protocol("WM_DELETE_WINDOW", self.confirm_exit)

    def create_buttons(self, frame):
        """Creates buttons with a modern UI."""
        button_data = [
            ("📖 Buy Book", BuyBookWindow, "<Control-b>"),
            ("💰 Sell Book", SellBookWindow, "<Control-s>"),
            ("🎁 Donate a Book", DonateBookWindow, "<Control-d>"),
            ("📚 View Donated Books", ViewDonatedBooksWindow, "<Control-v>"),
            ("👤 Profile", ProfileWindow, "<Control-p>"),
        ]

        for text, window_class, shortcut in button_data:
            button = tk.Button(
                frame,
                text=text,
                command=lambda wc=window_class, t=text: self.open_new_window(wc, t),
                font=("Helvetica", 12, "bold"),
                fg="white",
                bg="#42a5f5",
                activebackground="#1e88e5",
                activeforeground="white",
                width=25,
                height=2,
                relief="ridge",
                bd=3,
                cursor="hand2"
            )
            button.pack(pady=10, fill="x", padx=20)
            self.add_hover_effect(button)

            # Bind keyboard shortcuts
            self.root.bind(shortcut, lambda event, wc=window_class, t=text: self.open_new_window(wc, t))

    def add_hover_effect(self, button):
        """Adds hover effect to buttons."""
        def on_enter(event):
            button.config(bg="#1e88e5")

        def on_leave(event):
            button.config(bg="#42a5f5")

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def open_new_window(self, window_class, text=""):
        """Opens a new window and ensures only one instance of each window is open."""
        if window_class in self.open_windows:
            # If window already exists, just focus on it instead of creating a new one
            self.open_windows[window_class].focus_force()
            return

        self.status_label.config(text=f"Opening {text}...")  # Show status

        self.root.withdraw()  # Hide the dashboard
        new_window = tk.Toplevel(self.root)  # Create a new window
        new_window.title(text)  # Set window title
        new_window.geometry("500x600")  # Default size
        
        # Store reference to the window
        self.open_windows[window_class] = new_window  # Track the window

        # Create the window content
        window_instance = window_class(new_window, self.user_id)

        # Ensure when the window is closed, it returns to the dashboard
        new_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close_window(window_class))

    def on_close_window(self, window_class):
        """Handles window close event and returns to the dashboard."""
        if window_class in self.open_windows:
            self.open_windows[window_class].destroy()
            del self.open_windows[window_class]
        self.root.deiconify()
        self.status_label.config(text="Back to Dashboard")

    def toggle_theme(self):
        """Toggles between light and dark mode."""
        self.dark_mode = not self.dark_mode
        bg_color = "#121212" if self.dark_mode else "#e3f2fd"
        fg_color = "white" if self.dark_mode else "#555"
        btn_color = "#333" if self.dark_mode else "#42a5f5"
        title_color = "#90caf9" if self.dark_mode else "#1e88e5"

        # Apply to dashboard
        self.root.configure(bg=bg_color)
        self.frame.configure(bg=bg_color)
        self.status_label.configure(bg=bg_color, fg=fg_color)

        # Apply changes to buttons and labels
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(bg=btn_color, fg="white")
            elif isinstance(widget, tk.Label):
                widget.configure(bg=bg_color)
                if widget.cget("text") == "📚 Read Rover Dashboard":
                    widget.configure(fg=title_color)
                else:
                    widget.configure(fg=fg_color)

        # Update toggle button
        self.toggle_button.config(text="☀ Light Mode" if self.dark_mode else "🌙 Dark Mode")

    def confirm_exit(self):
        """Asks user for confirmation before exiting."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit Read Rover?"):
            self.root.destroy()

# Add the DashboardWindow class that redirects to Dashboard class
class DashboardWindow(Dashboard):
    """
    This class exists as a bridge between other modules and the Dashboard class.
    It inherits all functionality from Dashboard but can be called as DashboardWindow.
    """
    def __init__(self, root, user_id):
        super().__init__(root, user_id)

# Run the application
if __name__ == "__main__":
    user_id = 1  # Replace with actual user ID from the login system
    root = tk.Tk()
    app = Dashboard(root, user_id)
    root.mainloop()