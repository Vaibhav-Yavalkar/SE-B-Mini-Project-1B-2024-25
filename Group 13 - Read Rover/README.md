# Read Rover

A desktop application for buying, selling, and donating books built with Python and Tkinter with MySQL database integration.

## 📚 Overview

Read Rover is a user-friendly desktop application that connects book lovers, allowing them to buy, sell, and donate books. The platform promotes literacy and sustainable reading practices through its intuitive interface with secure user authentication and reliable MySQL database storage.

## ✨ Features

- **Secure Authentication**: Register and login with encrypted password storage and secure session management
- **Buy Books**: Browse and purchase books from other users
- **Sell Books**: List your books for sale with details and pricing
- **Donate Books**: Contribute books to the community for those in need
- **View Donated Books**: Browse and claim donated books
- **User Profiles**: Manage your personal information and track your activities
- **Dark/Light Mode**: Toggle between visual themes for comfortable reading

## 🛠️ Installation

### Prerequisites

- Python 3.6 or higher
- Tkinter (usually comes with Python)
- MySQL Server 5.7+ or MariaDB 10.3+
- mysql-connector-python package

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/read-rover.git
   cd read-rover
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up the MySQL database:

   ```
   mysql -u root -p < database/schema.sql
   ```

4. Configure database connection:

   - Rename `config.example.py` to `config.py`
   - Update the database connection parameters in `config.py`

5. Run the application:
   ```
   python main.py
   ```

## 🧩 Project Structure

```
read-rover/
│
├── login.py                 # User authentication and registration
├── register.py              # New user registration
├── dashboard.py             # Main dashboard interface
├── buy_book.py              # Book purchasing functionality
├── sell_book.py             # Book selling functionality
├── donate_book.py           # Book donation functionality
├── donated_books.py         # View donated books
├── profile.py               # User profile management
└── README.md                # Project documentation
```

## 🔑 Key Components

### Authentication System

Secure login and registration system with password hashing and session management to protect user data and privacy.

### Dashboard

The central hub of the application, providing access to all features through an intuitive interface with modern UI elements.

### Book Management

Specialized windows for buying, selling, and donating books, each with appropriate forms and displays.

### Database Integration

MySQL database integration providing:

- Robust data persistence
- Relational data structure for complex queries
- Transaction support for data integrity
- Multi-user concurrent access
- Efficient data retrieval with indexing

## 💻 Usage

1. **Register**: Create a new account with your email, username, and password
2. **Login**: Securely access your account
3. **Dashboard**: Access all features from the main dashboard
4. **Buy Books**: Browse available books and make purchases
5. **Sell Books**: List your books with details and pricing
6. **Donate Books**: Contribute books to the community
7. **Profile**: Manage your account information
8. **Dark Mode**: Toggle between light and dark themes for comfortable viewing

## 🧠 Technical Details

- **GUI Framework**: Tkinter with ttk for modern UI elements
- **Security**: Password hashing with salt using industry-standard algorithms
- **Database**: MySQL for reliable and efficient data storage
- **Architecture**: Class-based design with separate windows for each feature
- **Data Access**: Parameterized queries to prevent SQL injection
- **UI Design**: Modern interface with hover effects and responsive elements

## 📊 Database Schema

The MySQL database consists of the following core tables:

- `users`: Stores user account information
- `books`: Contains book listings information
- `transactions`: Records book purchases
- `donations`: Tracks donated books
- `categories`: Book categories/genres

## 🚀 Future Enhancements

- Two-factor authentication
- Book recommendation system
- Advanced search and filtering options
- Community forums and discussion boards
- Integration with external book databases for metadata
- Mobile companion application
- Database performance optimizations and caching

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- Simarpreet Kaur (https://github.com/simxrk)

## 🙏 Acknowledgements

- Thanks to all the book lovers who contributed to testing
