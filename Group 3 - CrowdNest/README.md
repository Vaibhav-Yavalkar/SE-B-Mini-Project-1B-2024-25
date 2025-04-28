# CrowdNest: Collective Resource Gathering System

## Overview
CrowdNest is an innovative platform designed to facilitate resource sharing and community support by connecting donors with those in need. The application provides a seamless, user-friendly interface for donating and requesting items.

## Key Features
- 🎁 Donation Management
- 📬 Email Communication System
- 🔒 Secure User Authentication
- 🖼️ Image Upload and Storage
- 📊 Donation and Request Tracking

## Technical Stack
- **Language**: Python
- **GUI Framework**: Tkinter
- **Database**: MySQL
- **ORM**: mysql-connector-python
- **Email**: SMTP Protocol

## System Requirements
- Python 3.8+
- MySQL 5.7+
- Required Python Packages:
  - mysql-connector-python
  - python-dotenv
  - Pillow
  - tkinter

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/CrowdNest.git
cd CrowdNest
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database
1. Create a MySQL database named `CrowdNest`
2. Update `.env` file with your database credentials
3. Run database setup:
```bash
python database_setup.py
```

### 5. Run the Application
```bash
python app.py
```

## Environment Variables
Create a `.env` file with the following configuration:
```
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=CrowdNest
PASSWORD_SALT=your_salt
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

## Security Features
- Secure password hashing
- Email verification
- SMTP TLS encryption
- User role management

## Database Schema
- **Users**: Stores user profile and authentication details
- **Donations**: Tracks donation items and their status
- **Requests**: Manages community resource requests
- **Email Communications**: Logs email interactions

## Contribution Guidelines
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License.

## Contact
Dhananjay Agarwal
- Email: dhananjay.ag007@gmail.com
- Website: Dhananjay-Agarwal.onrender.com
- LinkedIn: https://www.linkedin.com/in/dhananjay-agarwal-58bb542a1/

## Acknowledgments
- Open-source community
- Contributors and supporters