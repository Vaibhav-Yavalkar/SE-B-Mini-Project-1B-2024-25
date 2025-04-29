import json
import os
import time
from datetime import datetime

# File paths for data storage
SHOPPING_MALL_DATA_FILE = "shopping_mall_parking.json"
COLLEGE_DATA_FILE = "college_parking.json"

def initialize_parking_data():
    """Initialize parking data files if they don't exist"""
    # Initialize shopping mall parking data
    if not os.path.exists(SHOPPING_MALL_DATA_FILE):
        shopping_mall_spaces = {
            "P1": "available", "P2": "available", "P3": "available", "P4": "available", "P5": "available",
            "Q1": "available", "Q2": "available", "Q3": "available", "Q4": "available", "Q5": "available",
            "R1": "available", "R2": "available", "R3": "available", "R4": "available", "R5": "available",
            "S1": "available", "S2": "available", "S3": "available", "S4": "available", "S5": "available"
        }
        save_parking_data(shopping_mall_spaces, SHOPPING_MALL_DATA_FILE)
    
    # Initialize college parking data
    if not os.path.exists(COLLEGE_DATA_FILE):
        college_spaces = {
            "A1": "available", "A2": "available", "A3": "available", "A4": "available", "A5": "available",
            "B1": "available", "B2": "available", "B3": "available", "B4": "available", "B5": "available",
            "C1": "available", "C2": "available", "C3": "available", "C4": "available", "C5": "available",
            "D1": "available", "D2": "available", "D3": "available", "D4": "available", "D5": "available"
        }
        save_parking_data(college_spaces, COLLEGE_DATA_FILE)

def load_parking_data(location_type="shopping_mall"):
    """Load parking data from the appropriate JSON file"""
    file_path = SHOPPING_MALL_DATA_FILE if location_type == "shopping_mall" else COLLEGE_DATA_FILE
    
    if not os.path.exists(file_path):
        initialize_parking_data()
    
    try:
        with open(file_path, "r") as f:
            parking_data = json.load(f)
        
        # Update parking spaces based on time expiry
        current_time = time.time()
        updated = False
        
        for space, status in parking_data.items():
            if isinstance(status, dict) and "occupied_until" in status:
                # Check if the booking has expired
                if status["occupied_until"] < current_time:
                    parking_data[space] = "available"
                    updated = True
        
        # Save the updated data if any changes were made
        if updated:
            save_parking_data(parking_data, file_path)
        
        return parking_data
    except Exception as e:
        print(f"Error loading parking data: {e}")
        # Return default data in case of an error
        if location_type == "shopping_mall":
            return {
                "P1": "available", "P2": "available", "P3": "available", "P4": "available", "P5": "available",
                "Q1": "available", "Q2": "available", "Q3": "available", "Q4": "available", "Q5": "available",
                "R1": "available", "R2": "available", "R3": "available", "R4": "available", "R5": "available",
                "S1": "available", "S2": "available", "S3": "available", "S4": "available", "S5": "available"
            }
        else:
            return {
                "A1": "available", "A2": "available", "A3": "available", "A4": "available", "A5": "available",
                "B1": "available", "B2": "available", "B3": "available", "B4": "available", "B5": "available",
                "C1": "available", "C2": "available", "C3": "available", "C4": "available", "C5": "available",
                "D1": "available", "D2": "available", "D3": "available", "D4": "available", "D5": "available"
            }

def save_parking_data(parking_data, file_path=None):
    """Save parking data to the appropriate JSON file"""
    if file_path is None:
        # Determine file path based on space naming convention
        first_key = next(iter(parking_data))
        if first_key.startswith(('P', 'Q', 'R', 'S')):
            file_path = SHOPPING_MALL_DATA_FILE
        else:
            file_path = COLLEGE_DATA_FILE
    
    try:
        with open(file_path, "w") as f:
            json.dump(parking_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving parking data: {e}")
        return False

def update_parking_status(location_type=None):
    """Update parking status based on current time"""
    if location_type is None or location_type == "shopping_mall":
        shopping_data = load_parking_data("shopping_mall")
        save_parking_data(shopping_data, SHOPPING_MALL_DATA_FILE)
    
    if location_type is None or location_type == "college":
        college_data = load_parking_data("college")
        save_parking_data(college_data, COLLEGE_DATA_FILE)

def occupy_space(space, duration_hours, vehicle_number=None):
    """
    Mark a parking space as occupied for a specific duration
    
    Args:
        space (str): The parking space identifier (e.g., 'P1', 'A2')
        duration_hours (float): The duration in hours
        vehicle_number (str, optional): The vehicle number
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Determine location type based on space naming
    location_type = "shopping_mall" if space[0] in ['P', 'Q', 'R', 'S'] else "college"
    
    # Load current parking data
    parking_data = load_parking_data(location_type)
    
    # Calculate expiry time
    expiry_time = time.time() + (duration_hours * 3600)  # Convert hours to seconds
    
    # Update the space status
    parking_data[space] = {
        "status": "occupied",
        "occupied_until": expiry_time,
        "vehicle_number": vehicle_number,
        "booking_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "duration_hours": duration_hours
    }
    
    # Save the updated data
    file_path = SHOPPING_MALL_DATA_FILE if location_type == "shopping_mall" else COLLEGE_DATA_FILE
    return save_parking_data(parking_data, file_path)

# Initialize the parking data when the module is imported
initialize_parking_data()