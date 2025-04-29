# Constants for the CrowdNest application

# Modern Color scheme
COLORS = {
    'primary': '#0077B6',        # Deep Ocean Blue
    'primary_dark': '#023E8A',   # Darker Blue
    'secondary': '#F77F00',      # Warm Sunset Orange
    'accent': '#00B4D8',         # Vibrant Teal
    'success': '#38A3A5',        # Calming Green
    'warning': '#FFBA08',        # Golden Yellow
    'error': '#D62828',          # Rich Red
    'text': '#1B1B1E',           # Dark Charcoal
    'text_light': '#6C757D',     # Muted Gray
    'background': '#F1F3F5',     # Soft Light Gray
    'card': '#FFFFFF',           # Crisp White
    'border': '#DEE2E6'          # Subtle Border Gray
}

# Item conditions
CONDITIONS = [
    "New", "Like New", "Very Good", "Good", "Acceptable"
]

# Item categories
CATEGORIES = [
    "Clothing", "Electronics", "Books", "Furniture", "Home & Kitchen",
    "Sports & Fitness", "Toys & Games", "School Supplies", "Medical Supplies",
    "Automobiles", "Music Instruments", "Beauty & Personal Care", "Other"
]

# States and Cities
STATES = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool"],
    "Arunachal Pradesh": ["Itanagar", "Naharlagun", "Pasighat", "Tawang", "Ziro"],
    "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur", "Darbhanga"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba", "Durg"],
    "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Gandhinagar"],
    "Haryana": ["Gurgaon", "Faridabad", "Hisar", "Panipat", "Ambala"],
    "Himachal Pradesh": ["Shimla", "Mandi", "Dharamshala", "Solan", "Kullu"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Hazaribagh"],
    "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik"],
    "Manipur": ["Imphal", "Thoubal", "Bishnupur", "Churachandpur", "Senapati"],
    "Meghalaya": ["Shillong", "Tura", "Jowai", "Nongstoin", "Williamnagar"],
    "Mizoram": ["Aizawl", "Lunglei", "Champhai", "Serchhip", "Kolasib"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Tuensang", "Wokha"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur"],
    "Punjab": ["Chandigarh", "Ludhiana", "Amritsar", "Jalandhar", "Patiala"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer"],
    "Sikkim": ["Gangtok", "Namchi", "Gyalshing", "Mangan", "Rangpo"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam"],
    "Tripura": ["Agartala", "Udaipur", "Dharmanagar", "Kailasahar", "Belonia"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Allahabad"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Haldwani", "Rudrapur"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri"]
}

# Major cities by state
CITIES_BY_STATE = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool", "Kakinada"],
    "Arunachal Pradesh": ["Itanagar", "Naharlagun", "Tawang", "Pasighat", "Roing", "Ziro"],
    "Assam": ["Guwahati", "Dibrugarh", "Silchar", "Jorhat", "Tezpur", "Nagaon"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia", "Darbhanga"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba", "Durg", "Rajnandgaon"],
    "Goa": ["Panaji", "Vasco da Gama", "Margao", "Mapusa", "Ponda", "Bicholim"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar"],
    "Haryana": ["Chandigarh", "Faridabad", "Gurugram", "Ambala", "Panipat", "Hisar"],
    "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala", "Solan", "Mandi", "Bilaspur"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Hazaribagh", "Deoghar"],
    "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum", "Gulbarga"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Malappuram", "Kannur"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain", "Sagar"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad"],
    "Manipur": ["Imphal", "Thoubal", "Bishnupur", "Churachandpur", "Senapati", "Ukhrul"],
    "Meghalaya": ["Shillong", "Tura", "Jowai", "Nongstoin", "Baghmara", "Williamnagar"],
    "Mizoram": ["Aizawl", "Lunglei", "Champhai", "Serchhip", "Kolasib", "Saiha"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Tuensang", "Wokha", "Zunheboto"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Sambalpur", "Brahmapur", "Balasore"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Mohali"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Bikaner", "Ajmer"],
    "Sikkim": ["Gangtok", "Namchi", "Gyalshing", "Mangan", "Jorethang", "Rangpo"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli", "Tiruppur"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam", "Ramagundam"],
    "Tripura": ["Agartala", "Udaipur", "Dharmanagar", "Kailashahar", "Ambassa", "Belonia"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra", "Meerut", "Prayagraj"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Rishikesh", "Haldwani", "Nainital", "Rudrapur"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri", "Bardhaman"]
}