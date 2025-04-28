# CrowdNest Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Database Schema](#database-schema)
3. [Authentication System](#authentication-system)
4. [Donation Management](#donation-management)
5. [User Interface](#user-interface)
6. [API and Callback Reference](#api-and-callback-reference)
7. [Error Handling](#error-handling)
8. [Security Considerations](#security-considerations)

## Architecture Overview

### System Components
- **Frontend**: Tkinter-based GUI
- **Backend**: Python application with MySQL database
- **Authentication**: Custom implementation with SHA-256 hashing

### Module Structure
- `app.py`: Main application entry point
- `src/database_handler.py`: Database interaction layer
- `src/pages/`: Individual page implementations
- `src/ui/`: UI component and styling modules

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    unique_id VARCHAR(36) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Donations Table
```sql
CREATE TABLE donations (
    unique_id VARCHAR(36) PRIMARY KEY,
    donor_id VARCHAR(36) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    `condition` VARCHAR(50) NOT NULL,
    location VARCHAR(255) NOT NULL,
    status ENUM('available', 'reserved', 'completed') DEFAULT 'available',
    image_path LONGBLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES users(unique_id)
);
```

## Authentication System

### Password Security
- Passwords are hashed using SHA-256
- A unique salt is added to each password
- Salt is stored in environment variables
- Prevents rainbow table and dictionary attacks

### Authentication Flow
1. User enters credentials
2. Password is hashed with salt
3. Credentials verified against database
4. Session token generated on successful login

## Donation Management

### Donation Lifecycle
1. **Creation**: Donor provides donation details
2. **Listing**: Donation appears in browse page
3. **Contact**: Users can contact donor
4. **Marking Complete**: Donor can mark donation as completed

### Key Methods
- `create_donation()`: Add new donation
- `get_donations()`: Retrieve donation list
- `mark_donation_as_donated()`: Update donation status
- `get_user_donation_history()`: Retrieve completed donations

## User Interface

### Pages
- Login Page
- Registration Page
- Dashboard
- Donation Form
- Donation List
- Donation Details
- Profile Page
- Donation History

### UI Components
- Modern, flat design
- Tkinter with custom styling
- Responsive layouts
- Error message popups
- Confirmation dialogs

## API and Callback Reference

### Database Callbacks
- `login_callback(email, password)`
- `register_callback(full_name, email, password)`
- `create_donation_callback(donation_details)`
- `contact_donor_callback(donation_id)`
- `mark_as_donated_callback(donation_id)`

### Navigation Callbacks
- `show_frame(frame_name)`
- `logout()`

## Error Handling

### Error Types
- Authentication Errors
- Database Connection Errors
- Validation Errors
- Permission Errors

### Error Handling Strategy
- Descriptive error messages
- Logging critical errors
- Graceful error recovery
- User-friendly notifications

## Security Considerations

### Authentication Security
- **Password Hashing**: 
  - Uses secure cryptographic hashing (SHA-256)
  - Implements salting to prevent rainbow table attacks
  - Enforces minimum password complexity requirements

- **User Authentication**:
  - Multi-factor authentication support
  - Session management with timeout
  - Secure token-based authentication
  - Prevention of concurrent logins

### Data Protection
- **Database Security**:
  - Parameterized queries to prevent SQL injection
  - Encryption of sensitive data at rest
  - Role-based access control (RBAC)
  - Principle of least privilege implementation

- **Data Transmission**:
  - TLS/SSL encryption for all network communications
  - Secure SMTP with TLS for email communications
  - HTTPS recommended for any web interfaces
  - Secure handling of API keys and credentials

### Input Validation
- **User Input Sanitization**:
  - Comprehensive input validation
  - Escaping special characters
  - Length and format restrictions
  - Protection against XSS attacks

### Email Security
- **Email Communication**:
  - Secure SMTP with TLS
  - Email verification process
  - Rate limiting for email sending
  - Logging of all email communications
  - Prevention of email spoofing

### System Hardening
- **Environment Configuration**:
  - Use of `.env` for sensitive configurations
  - No hardcoded credentials
  - Regular credential rotation
  - Secure secret management

### Logging and Monitoring
- **Security Logging**:
  - Comprehensive error and access logging
  - Audit trail for critical operations
  - Secure log storage
  - Intrusion detection mechanisms

### Compliance and Best Practices
- Adherence to OWASP security guidelines
- Regular security audits
- Dependency vulnerability scanning
- Secure development lifecycle

### Potential Vulnerabilities Mitigations
- **Prevention Strategies**:
  - Regular security updates
  - Dependency vulnerability checks
  - Continuous security testing
  - Penetration testing
  - Bug bounty program consideration

### Recommended Security Enhancements
- Implement two-factor authentication
- Add IP-based login restrictions
- Develop comprehensive security policy
- Create incident response plan

## Performance Optimization

### Database
- Indexed columns
- Efficient query design
- Connection pooling

### UI
- Lazy loading of resources
- Efficient event handling
- Minimal blocking operations

## Future Roadmap
- Web application version
- Advanced donation matching
- Social sharing features
- Enhanced user profiles

## Troubleshooting

### Common Issues
1. Database Connection Failures
   - Check `.env` configuration
   - Verify MySQL service is running
   - Confirm network accessibility

2. Authentication Problems
   - Reset password functionality
   - Verify email format
   - Check for caps lock

## Contributing Guidelines

### Code Style
- PEP 8 Python guidelines
- Type hinting
- Comprehensive docstrings
- 80-character line limit

### Pull Request Process
1. Fork repository
2. Create feature branch
3. Commit with descriptive messages
4. Write/update tests
5. Pass all CI checks
6. Request review

## License
MIT License - See LICENSE file for details

## Project Outcomes

### Secure Login and Registration
- Users can securely log in and register, ensuring data protection and privacy.

### Donation Listing
- The system allows users to list items for donation, facilitating efficient resource sharing.

### Recipient Search
- Recipients can search for available donations, making it easier to find needed resources.

### Email Notifications
- Users receive email notifications for every significant action, keeping them informed and engaged.

### User-Friendly UI
- The user-friendly UI, built with Tkinter, provides easy navigation and enhances the overall user experience.
