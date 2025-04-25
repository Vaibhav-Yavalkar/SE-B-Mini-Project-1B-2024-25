# GREEN THUMB 🌿 - Nursery Management Solutions

**GREEN THUMB** is a GUI-based desktop application built with Python (Tkinter), offering nursery management features such as plant/pot catalog, ordering, reviews, admin dashboard, and more.

---

## 🚀 Features

- 🌿 Category-wise Plant and Pot Display
- 🛒 Add to Cart & Buy Now functionality
- 💼 Admin Dashboard for order management
- 📱 SMS Notifications via Twilio
- 📅 Customer Reviews & Ratings
- 📖 Plantation Blog Articles
- 🎥 Nursery Tour with Video Player
- 🌍 Dynamic State-City Dropdown via CountryStateCity API
- 💳 Secure Multi-method Payment System

---

## 💻 Tech Stack

| Component     | Technology                  |
| ------------- | --------------------------- |
| Frontend      | Python (Tkinter)            |
| Backend       | SQLite                      |
| APIs          | Twilio, CountryStateCity    |
| Media Support | PIL (Pillow), Tkinter Video |

---

## 📊 Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/maazzshaikh11/GREEN-THUMB---Nursery-Management-Solutions.git
cd green-thumb
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in root:

```env
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE=+1XXXXXXXXXX
CSC_API_KEY=your_countrystatecity_api_key
```

### 5. Setup the Database

```bash
python database_setup.py
```

### 6. Run the Application

```bash
python mini_project.py
```

---

## 📋 Project Structure

```
green-thumb/
├── Images/               # Product & Category Images
├── Videos/               # Nursery Tour Videos
├── mini_project.py       # Main GUI Application
├── database_setup.py     # One-time DB Creation Script
├── requirements.txt      # Python dependencies
├── .env                  # (Not uploaded to GitHub)
├── .gitignore
├── README.md
└── LICENSE
```

---

## 🚧 Security Note

- Do **not** upload `.db` or `.env` files to public repositories.
- Always exclude credentials using `.gitignore`.

---

## 🌐 Live Demo / Executable

*Coming soon: PyInstaller .exe for offline use!*

---

## 🌟 Author

**Maaz Shaikh**
GitHub: [@maazzshaikh11](https://github.com/maazzshaikh11)

---

## 🔖 License

Licensed under the [MIT License](LICENSE).

