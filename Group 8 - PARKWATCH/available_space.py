import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import time
from datetime import datetime
from parking_data import load_parking_data, save_parking_data, update_parking_status

# Update parking status to refresh availability
update_parking_status("shopping_mall")

# Load current parking data
parking_spaces = load_parking_data("shopping_mall")

# Dictionary to store button widgets with shopping mall parking keys
buttons = {}

# Variable to store the currently selected space
selected_space = None

# Mapping of row indices to letters
row_letters = {0: "P", 1: "Q", 2: "R", 3: "S"}

# Function to redirect to time&cost.py with the selected space
def redirect_to_time_cost(selected_space):
    # Save the selected space to pass to the next script
    with open("selected_space.txt", "w") as f:
        f.write(selected_space)
    
    # Save parking type to indicate we're using shopping mall
    with open("parking_type.txt", "w") as f:
        f.write("shopping_mall")
    
    # Close current window
    root.destroy()
    
    # Launch the time&cost.py script
    try:
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        time_cost_path = os.path.join(current_dir, "time&cost.py")
        
        # Check if the file exists
        if os.path.exists(time_cost_path):
            if sys.platform.startswith('win'):
                subprocess.Popen(["python", time_cost_path])
            else:
                subprocess.Popen(["python3", time_cost_path])
        else:
            print(f"Error: Cannot find time&cost.py at {time_cost_path}")
    except Exception as e:
        print(f"Error launching time&cost.py: {e}")

# Function to display parking spaces (with green for available and red for occupied)
def show_parking_spaces():
    global submit_button, status_label

    # Update parking status to refresh availability
    update_parking_status("shopping_mall")

    # Load updated parking data from JSON
    global parking_spaces
    parking_spaces = load_parking_data("shopping_mall")

    # Clear previous widgets
    for widget in location_selection_frame.winfo_children():
        widget.destroy()

    label_location = tk.Label(location_selection_frame, text="SHOPPING MALL PARKING SPACES", font=("Arial", 30, "bold"), bg="#2C3E50", fg="white")
    label_location.pack(pady=30)

    grid_frame = tk.Frame(location_selection_frame, bg="#2C3E50")
    grid_frame.pack(pady=10)
    
    for row_index in range(4):  
        row_letter = row_letters[row_index]
        
        for col_index in range(5):  
            position = f"{row_letter}{col_index+1}"
            space_data = parking_spaces[position]
            
            # Determine the color and status text based on availability
            if isinstance(space_data, dict) and space_data.get("status") == "occupied":
                color = "red"
                remaining_time = space_data["occupied_until"] - time.time()
                remaining_hours = max(0, remaining_time / 3600)
                status_text = f"{position} (Booked)"
            else:
                color = "green"
                status_text = position
            
            space_button = tk.Button(
                grid_frame, 
                text=status_text, 
                width=12, 
                height=3, 
                bg=color, 
                fg="white", 
                relief="raised", 
                font=("Arial", 14), 
                command=lambda pos=position: select_space(pos)
            )
            space_button.grid(row=row_index, column=col_index, padx=8, pady=5)
            
            buttons[position] = space_button

    location_selection_frame.pack(expand=True)

    # Display selected space information
    selection_label = tk.Label(location_selection_frame, text="No Space Selected", font=("Arial", 14), bg="#2C3E50", fg="white")
    selection_label.pack(pady=10)
    # Store reference to update later
    status_label = selection_label

    # Create Back and Submit buttons in the same row (bottom)
    button_frame = tk.Frame(location_selection_frame, bg="#2C3E50")
    button_frame.pack(pady=20)

    back_button = tk.Button(button_frame, text="Back", font=("Arial", 14, "bold"), bg="#E74C3C", fg="white", relief="raised", width=15, height=2, command=back_action)
    back_button.grid(row=0, column=0, padx=20)

    submit_button = tk.Button(button_frame, text="Submit", font=("Arial", 14, "bold"), bg="#2980B9", fg="white", relief="raised", width=15, height=2, command=submit_action, state="disabled")
    submit_button.grid(row=0, column=1, padx=20)

    # Add refresh button
    refresh_button = tk.Button(button_frame, text="Refresh", font=("Arial", 14, "bold"), bg="#27AE60", fg="white", relief="raised", width=15, height=2, command=show_parking_spaces)
    refresh_button.grid(row=0, column=2, padx=20)

# Function to select a parking space
def select_space(position):
    global selected_space, submit_button, status_label
    
    # Get current space data
    space_data = parking_spaces[position]
    
    # Check if the space is available
    if isinstance(space_data, dict) and space_data.get("status") == "occupied":
        # Calculate remaining time
        remaining_time = space_data["occupied_until"] - time.time()
        remaining_hours = max(0, remaining_time / 3600)
        
        # Format time for display
        if remaining_hours > 0:
            hours = int(remaining_hours)
            minutes = int((remaining_hours - hours) * 60)
            time_str = f"{hours}h {minutes}m"
            
            # Show a message that the space is occupied
            messagebox.showwarning("Space Occupied", 
                                  f"Sorry, space {position} is already occupied.\n"
                                  f"It will be available in approximately {time_str}.")
        else:
            # This should not happen as expired spaces should be marked available
            # But just in case, handle it
            messagebox.showinfo("Space Available Soon", 
                               f"Space {position} booking has expired. Refreshing status...")
            update_parking_status("shopping_mall")
            show_parking_spaces()
    else:
        # Reset any previously selected space
        if selected_space:
            # If there was a previously selected space, reset it to green
            buttons[selected_space].config(bg="green")
        
        # Update the selected space
        selected_space = position
        
        # Update the button color to blue (selected)
        buttons[position].config(bg="blue")
        
        # Update the status label
        status_label.config(text=f"Selected Space: {position}")
        
        # Enable the Submit button
        submit_button.config(state="normal")
        
        # Show a selection message
        messagebox.showinfo("Space Selected", f"You have selected space {position}.")

# Back button action to go back to dashboard
def back_action():
    # Close current window
    root.destroy()
    
    # Launch the dashboard script
    try:
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dashboard_path = os.path.join(current_dir, "dashboard.py")
        
        # Check if the file exists
        if os.path.exists(dashboard_path):
            if sys.platform.startswith('win'):
                subprocess.Popen(["python", dashboard_path])
            else:
                subprocess.Popen(["python3", dashboard_path])
        else:
            print(f"Error: Cannot find dashboard.py at {dashboard_path}")
    except Exception as e:
        print(f"Error launching dashboard.py: {e}")

# Submit button action (submitting the parking space reservation and redirecting)
def submit_action():
    global selected_space

    if selected_space:
        # The actual booking will be handled in time&cost.py
        # Just mark the space as temporarily selected here
        redirect_to_time_cost(selected_space)
    else:
        messagebox.showwarning("No Selection", "Please select a parking space first.")

# Auto-refresh function
def auto_refresh():
    # Refresh every 30 seconds
    show_parking_spaces()
    root.after(30000, auto_refresh)  # 30000 ms = 30 seconds

# Create the main window
root = tk.Tk()
root.title("Shopping Mall Parking Manager")

# Set the size of the window and background color
root.geometry("800x600")
root.state('zoomed')
root.configure(bg="#2C3E50")

# Create a frame for the parking spaces page
location_selection_frame = tk.Frame(root, bg="#2C3E50")

# Show the parking spaces when the program starts
show_parking_spaces()

# Set up auto-refresh
auto_refresh()

# Start the Tkinter event loop
root.mainloop()