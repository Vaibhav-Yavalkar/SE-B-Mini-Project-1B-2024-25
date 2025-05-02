import streamlit as st
import pandas as pd
import random
import time
import google.generativeai as genai
from datetime import datetime
import os
import openpyxl
from openpyxl import Workbook


st.set_page_config(
    page_title="Medimanage - Online Pharmacy",
    page_icon="💊",
    layout="wide"
)


genai.configure(api_key="AIzaSyDkJWlBonIwQiO-azQ4W7a7mDP1SzxMYXw")


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


USERS_DB = "users_db.xlsx"
MEDICINES_DB = "medicines_db.xlsx"
ORDERS_DB = "orders_db.xlsx"


def initialize_excel_databases():

    if not os.path.exists(USERS_DB):
        users_df = pd.DataFrame({
            "username": ["user1", "user2", "admin"],
            "password": ["password1", "password2", "admin123"]
        })
        users_df.to_excel(USERS_DB, index=False)
    

    if not os.path.exists(MEDICINES_DB):
        medicines = pd.DataFrame({
            "id": range(1, 21),
            "name": [
                "Paracetamol", "Aspirin", "Ibuprofen", "Amoxicillin", 
                "Cetirizine", "Omeprazole", "Metformin", "Atorvastatin", 
                "Losartan", "Albuterol", "Levothyroxine", "Amlodipine",
                "Lisinopril", "Simvastatin", "Metoprolol", "Gabapentin",
                "Sertraline", "Montelukast", "Pantoprazole", "Escitalopram"
            ],
            "description": [
                "Pain reliever and fever reducer", "Pain reliever and anti-inflammatory",
                "Non-steroidal anti-inflammatory drug", "Antibiotic for bacterial infections",
                "Antihistamine for allergies", "Proton pump inhibitor for acid reflux",
                "Oral diabetes medication", "Cholesterol-lowering medication",
                "Blood pressure medication", "Bronchodilator for asthma",
                "Thyroid hormone replacement", "Blood pressure medication",
                "ACE inhibitor for blood pressure", "Cholesterol-lowering medication",
                "Beta-blocker for heart conditions", "Anti-seizure and nerve pain medication",
                "Antidepressant (SSRI)", "Asthma and allergy medication",
                "Proton pump inhibitor for ulcers", "Antidepressant (SSRI)"
            ],
            "price": [
                5.99, 4.99, 7.49, 12.99, 8.99, 15.99, 9.99, 22.99, 18.49, 25.99,
                14.99, 16.49, 11.99, 19.99, 13.49, 24.99, 21.99, 28.99, 17.49, 26.99
            ],
            "category": [
                "Pain Relief", "Pain Relief", "Pain Relief", "Antibiotics",
                "Allergy", "Digestive Health", "Diabetes", "Cardiovascular",
                "Cardiovascular", "Respiratory", "Hormones", "Cardiovascular",
                "Cardiovascular", "Cardiovascular", "Cardiovascular", "Neurology",
                "Mental Health", "Respiratory", "Digestive Health", "Mental Health"
            ],
            "stock": [
                random.randint(15, 100) for _ in range(20)
            ],
            "prescription_required": [
                False, False, False, True, False, False, True, True,
                True, True, True, True, True, True, True, True,
                True, True, False, True
            ],
            "image_url": [f"https://picsum.photos/seed/{i}/200/200" for i in range(1, 21)]
        })
        medicines.to_excel(MEDICINES_DB, index=False)
    

    if not os.path.exists(ORDERS_DB):
        orders_df = pd.DataFrame(columns=[
            "order_id", "username", "date", "items", "total", 
            "address", "payment_method", "status"
        ])
        orders_df.to_excel(ORDERS_DB, index=False, engine='openpyxl')

# Database operations
def load_users():
    return pd.read_excel(USERS_DB)

def save_user(username, password):
    users_df = load_users()
    new_user = pd.DataFrame({"username": [username], "password": [password]})
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_excel(USERS_DB, index=False)

def authenticate_user(username, password):
    users_df = load_users()
    user_row = users_df[users_df["username"] == username]
    if not user_row.empty and user_row.iloc[0]["password"] == password:
        return True
    return False

def load_medicines():
    return pd.read_excel(MEDICINES_DB)

def update_medicine_stock(medicine_id, quantity):
    medicines_df = load_medicines()
    idx = medicines_df.index[medicines_df["id"] == medicine_id].tolist()[0]
    medicines_df.at[idx, "stock"] = medicines_df.at[idx, "stock"] - quantity
    medicines_df.to_excel(MEDICINES_DB, index=False)

def load_orders(username=None):
    orders_df = pd.read_excel(ORDERS_DB)
    if username:
        return orders_df[orders_df["username"] == username]
    return orders_df

def save_order(order_data):
    orders_df = load_orders()
    

    items_str = str(order_data["items"])
    
    new_order = pd.DataFrame({
        "order_id": [order_data["order_id"]],
        "username": [order_data["username"]],
        "date": [order_data["date"]],
        "items": [items_str],
        "total": [order_data["total"]],
        "address": [order_data["address"]],
        "payment_method": [order_data["payment_method"]],
        "status": [order_data["status"]]
    })
    
    orders_df = pd.concat([orders_df, new_order], ignore_index=True)
    orders_df.to_excel(ORDERS_DB, index=False)
    

    for item in order_data["items"]:
        medicine_id = item["id"]
        quantity = item["quantity"]
        update_medicine_stock(medicine_id, quantity)


def navigate_to(page):
    st.session_state.current_page = page


def login():
    st.session_state.authenticated = False
    st.session_state.username = ""
    
    with st.form("login_form"):
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if authenticate_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.current_page = "home"
                st.success("Login successful!")
                st.balloons()
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    st.divider()
    st.write("Don't have an account?")
    if st.button("Register"):
        st.session_state.current_page = "register"
        st.rerun()

def register():
    with st.form("register_form"):
        st.subheader("Create an Account")
        new_username = st.text_input("Choose a Username")
        new_password = st.text_input("Choose a Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Register")
        
        if submit:
            users_df = load_users()
            if new_username in users_df["username"].values:
                st.error("Username already exists")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            elif not new_username or not new_password:
                st.error("Username and password cannot be empty")
            else:
                save_user(new_username, new_password)
                st.success("Registration successful! Please login.")
                st.session_state.current_page = "login"
                st.rerun()
    
    st.divider()
    st.write("Already have an account?")
    if st.button("Back to Login"):
        st.session_state.current_page = "login"
        st.rerun()


def add_to_cart(medicine_id, quantity=1):
    medicines_df = load_medicines()
    medicine = medicines_df[medicines_df["id"] == medicine_id].iloc[0]
    
    if medicine_id in st.session_state.cart:
        st.session_state.cart[medicine_id]["quantity"] += quantity
    else:
        st.session_state.cart[medicine_id] = {
            "id": medicine_id,
            "name": medicine["name"],
            "price": medicine["price"],
            "quantity": quantity,
            "prescription_required": medicine["prescription_required"]
        }
    
    st.toast(f"Added {medicine['name']} to cart")

def remove_from_cart(medicine_id):
    if medicine_id in st.session_state.cart:
        medicine_name = st.session_state.cart[medicine_id]["name"]
        del st.session_state.cart[medicine_id]
        st.toast(f"Removed {medicine_name} from cart")

def update_cart_quantity(medicine_id, quantity):
    if medicine_id in st.session_state.cart:
        if quantity <= 0:
            remove_from_cart(medicine_id)
        else:
            st.session_state.cart[medicine_id]["quantity"] = quantity

def calculate_cart_total():
    return sum(item["price"] * item["quantity"] for item in st.session_state.cart.values())

def clear_cart():
    st.session_state.cart = {}

def process_checkout(address, payment_method):
    if not st.session_state.cart:
        st.error("Your cart is empty")
        return False
    

    prescription_items = [item["name"] for item_id, item in st.session_state.cart.items() 
                         if item["prescription_required"]]
    
    if prescription_items and not st.session_state.get("prescription_uploaded", False):
        st.error(f"Please upload prescription for: {', '.join(prescription_items)}")
        return False
    

    order = {
        "order_id": f"ORD-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
        "username": st.session_state.username,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": [{
            "id": int(medicine_id),
            "name": item["name"],
            "quantity": item["quantity"],
            "price": item["price"],
            "subtotal": item["price"] * item["quantity"]
        } for medicine_id, item in st.session_state.cart.items()],
        "total": calculate_cart_total(),
        "address": address,
        "payment_method": payment_method,
        "status": "Processing"
    }
    

    save_order(order)
    
    clear_cart()
    st.session_state.prescription_uploaded = False
    
    return True


def get_gemini_response(question):
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are a helpful medical assistant chatbot that can provide general medical information 
    and advice. The user is asking: {question}
    
    Please provide a helpful and informative response. If it's a serious medical condition, 
    advise seeking professional medical help. Do not prescribe specific medications or make 
    definitive diagnoses. Focus on providing general information and guidance.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}. Please try again later."


def show_header():
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        st.image("https://picsum.photos/seed/logo/100/100", width=80)
    
    with col2:
        st.title("MediManage - Online Pharmacy")
        st.write(f"Welcome, {st.session_state.username}!")
    
    with col3:
        st.button("🛒 Cart", on_click=navigate_to, args=("cart",))
        st.button("📋 Orders", on_click=navigate_to, args=("orders",))
        st.button("💬 Medical Chat", on_click=navigate_to, args=("chat",))
        st.button("🏠 Home", on_click=navigate_to, args=("home",))
        st.button("🚪 Logout", on_click=navigate_to, args=("login",))

def show_categories_sidebar():
    st.sidebar.title("Categories")
    
    medicines_df = load_medicines()
    categories = ["All"] + sorted(list(medicines_df["category"].unique()))
    
    selected_category = st.sidebar.radio("Select Category", categories)
    
    st.sidebar.divider()
    
    min_price = int(medicines_df["price"].min())
    max_price = int(medicines_df["price"].max())
    
    price_range = st.sidebar.slider(
        "Price Range ($)",
        min_price,
        max_price,
        (min_price, max_price)
    )
    
    prescription_filter = st.sidebar.multiselect(
        "Prescription Requirement",
        ["Required", "Not Required"],
        []
    )
    
    st.sidebar.divider()
    search_query = st.sidebar.text_input("Search medicines")
    

    filtered_data = medicines_df.copy()
    
    if selected_category != "All":
        filtered_data = filtered_data[filtered_data["category"] == selected_category]
    
    filtered_data = filtered_data[
        (filtered_data["price"] >= price_range[0]) & 
        (filtered_data["price"] <= price_range[1])
    ]
    
    if "Required" in prescription_filter and "Not Required" not in prescription_filter:
        filtered_data = filtered_data[filtered_data["prescription_required"] == True]
    elif "Not Required" in prescription_filter and "Required" not in prescription_filter:
        filtered_data = filtered_data[filtered_data["prescription_required"] == False]
    
    if search_query:
        filtered_data = filtered_data[
            filtered_data["name"].str.contains(search_query, case=False) |
            filtered_data["description"].str.contains(search_query, case=False) |
            filtered_data["category"].str.contains(search_query, case=False)
        ]
    
    return filtered_data

def show_medicine_listing(filtered_medicines):
    st.header("Available Medicines")
    
    if len(filtered_medicines) == 0:
        st.info("No medicines match your criteria")
        return

    cols_per_row = 3
    for i in range(0, len(filtered_medicines), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(filtered_medicines):
                medicine = filtered_medicines.iloc[i + j]
                with cols[j]:
                    st.image(medicine["image_url"], use_container_width=True)
                    st.subheader(medicine["name"])
                    st.write(f"Category: {medicine['category']}")
                    st.write(medicine["description"])
                    st.write(f"Price: ${medicine['price']:.2f}")
                    st.write(f"In Stock: {medicine['stock']}")
                    
                    if medicine["prescription_required"]:
                        st.warning("⚕️ Prescription Required")
                    
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button(f"Add to Cart", key=f"add_{medicine['id']}"):
                            add_to_cart(medicine["id"])
                    with col2:
                        quantity = st.number_input(
                            "Qty", 
                            min_value=1, 
                            max_value=medicine["stock"], 
                            value=1,
                            key=f"qty_{medicine['id']}"
                        )
                    
                    st.divider()

def show_cart_page():
    st.header("Shopping Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is empty")
        st.button("Continue Shopping", on_click=navigate_to, args=("home",))
        return
    

    for medicine_id, item in st.session_state.cart.items():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(f"**{item['name']}**")
            st.write(f"Price: ${item['price']:.2f}")
            if item["prescription_required"]:
                st.warning("⚕️ Prescription Required")
        
        with col2:
            new_quantity = st.number_input(
                "Quantity", 
                min_value=1, 
                value=item["quantity"],
                key=f"cart_qty_{medicine_id}"
            )
            if new_quantity != item["quantity"]:
                update_cart_quantity(medicine_id, new_quantity)
                st.rerun()
        
        with col3:
            st.write(f"Subtotal: ${item['price'] * item['quantity']:.2f}")
            if st.button("Remove", key=f"remove_{medicine_id}"):
                remove_from_cart(medicine_id)
                st.rerun()
        
        st.divider()
    

    st.subheader("Order Summary")
    st.write(f"Total Items: {sum(item['quantity'] for item in st.session_state.cart.values())}")
    st.write(f"Total Amount: ${calculate_cart_total():.2f}")
    

    prescription_required = any(item["prescription_required"] for item in st.session_state.cart.values())
    
    if prescription_required:
        st.warning("Some items require a valid prescription")
        prescription_file = st.file_uploader("Upload Prescription (PDF/Image)", type=["pdf", "jpg", "jpeg", "png"])
        if prescription_file:
            st.session_state.prescription_uploaded = True
            st.success("Prescription uploaded successfully!")
        else:
            st.session_state.prescription_uploaded = False
    

    st.divider()
    st.subheader("Checkout")
    
    with st.form("checkout_form"):
        st.write("Shipping Information")
        address = st.text_area("Delivery Address")
        
        st.write("Payment Method")
        payment_method = st.radio(
            "Select Payment Method",
            ["Credit Card", "Debit Card", "UPI", "Cash on Delivery"]
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            back_btn = st.form_submit_button("Continue Shopping")
        with col2:
            checkout_btn = st.form_submit_button("Place Order")
        
        if back_btn:
            st.session_state.current_page = "home"
            st.rerun()
        
        if checkout_btn:
            if not address:
                st.error("Please enter a delivery address")
            else:
                success = process_checkout(address, payment_method)
                if success:
                    st.success("Order placed successfully!")
                    st.balloons()
                    st.session_state.current_page = "order_confirmation"
                    st.rerun()

def show_order_confirmation():
    st.header("Order Confirmation")
    

    user_orders = load_orders(st.session_state.username)
    
    if user_orders.empty:
        st.error("No order found!")
        return
    

    order = user_orders.iloc[-1]
    

    items_str = order["items"]
    
    st.success(f"Order Placed Successfully! Order ID: {order['order_id']}")
    st.write(f"Order Date: {order['date']}")
    
    st.subheader("Items")
    st.write(f"Order details: {items_str}")
    
    st.divider()
    st.write(f"Total Amount: ${order['total']:.2f}")
    st.write(f"Shipping Address: {order['address']}")
    st.write(f"Payment Method: {order['payment_method']}")
    st.write(f"Status: {order['status']}")
    
    st.info("You will receive a confirmation email shortly with your order details.")
    
    if st.button("Continue Shopping"):
        st.session_state.current_page = "home"
        st.rerun()

def show_orders_page():
    st.header("Order History")
    
    user_orders = load_orders(st.session_state.username)
    
    if user_orders.empty:
        st.info("You haven't placed any orders yet")
        if st.button("Start Shopping"):
            st.session_state.current_page = "home"
            st.rerun()
        return
    

    for i in range(len(user_orders)-1, -1, -1):
        order = user_orders.iloc[i]
        with st.expander(f"Order #{order['order_id']} - {order['date']}"):
            st.write(f"Status: {order['status']}")
            
            st.subheader("Items")
            st.write(f"Order details: {order['items']}")
            
            st.divider()
            st.write(f"Total Amount: ${order['total']:.2f}")
            st.write(f"Shipping Address: {order['address']}")
            st.write(f"Payment Method: {order['payment_method']}")
            
            
            if st.button("Track Order", key=f"track_{order['order_id']}"):
                st.info("Tracking information: Your order is being processed and will be shipped soon.")

def show_chat_page():
    st.header("Medical Assistant Chat")
    
    st.info("Ask any general medical questions, and our AI assistant will help you with information and guidance.")
    
    
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])
    

    user_input = st.chat_input("Ask a medical question...")
    
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        with st.spinner("Thinking..."):
            response = get_gemini_response(user_input)
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
        st.rerun()
    
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()


def main():
    
    initialize_excel_databases()
    
   
    if st.session_state.current_page == "login":
        login()
    elif st.session_state.current_page == "register":
        register()
    elif not st.session_state.authenticated:
        st.session_state.current_page = "login"
        st.rerun()
    else:
       
        show_header()
        
        if st.session_state.current_page == "home":
            filtered_medicines = show_categories_sidebar()
            show_medicine_listing(filtered_medicines)
        elif st.session_state.current_page == "cart":
            show_cart_page()
        elif st.session_state.current_page == "order_confirmation":
            show_order_confirmation()
        elif st.session_state.current_page == "orders":
            show_orders_page()
        elif st.session_state.current_page == "chat":
            show_chat_page()

if __name__ == "__main__":
    main()