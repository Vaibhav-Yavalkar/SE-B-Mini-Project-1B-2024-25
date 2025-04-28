# CrowdNest: Collective Resource Gathering System

## Project Overview
- A platform facilitating community resource sharing
- Connects donors with those in need
- User-friendly interface for donation management

## Technical Stack
- **Backend**: Python with MySQL database
- **Frontend**: Tkinter-based GUI
- **Authentication**: Custom implementation with SHA-256 hashing
- **Email System**: SMTP Protocol

## System Architecture

### Core Components
1. **User Interface Layer**
   - Modern, flat design using Tkinter
   - Responsive layouts
   - Custom styling and components

2. **Application Layer**
   - User authentication and session management
   - Donation and request processing
   - Email communication system

3. **Data Layer**
   - MySQL database
   - Secure data storage
   - Efficient query handling

## Key Features

### 1. User Authentication
- Secure password hashing with SHA-256
- Unique salt for each password
- Session token management
- Email verification

### 2. Donation Management
- Create and track donations
- Image upload capability
- Status tracking (available/reserved/completed)
- Donation history

### 3. Request System
- Create resource requests
- Browse available donations
- Contact donors
- Track request status

### 4. Profile Management
- User profile customization
- Donation history tracking
- Request history viewing

## Database Design

### Users Table
- Unique ID (Primary Key)
- Full Name
- Email (Unique)
- Password Hash
- Creation Timestamp

### Donations Table
- Unique ID (Primary Key)
- Donor ID (Foreign Key)
- Title and Description
- Category and Condition
- Location
- Status
- Image Data
- Timestamps

## Security Implementation

### Password Security
- SHA-256 hashing
- Unique salt per password
- Environment variable configuration

### Data Protection
- Secure database connections
- Input validation
- SQL injection prevention

## Future Enhancements

### Real-time Updates
- Push notifications for new donations
- Request status updates

### Advanced Search
- Geolocation-based search
- Advanced filtering options

### Collaboration
- Collaborative donation management
- Request review processes

## Project Impact

### Community Benefits
- Efficient resource distribution
- Reduced waste
- Stronger community bonds
- Easy access to needed resources

### Environmental Impact
- Promotes reuse
- Reduces landfill waste
- Encourages sustainable practices

## Technical Achievements

### Code Quality
- Modular architecture
- Clean code practices
- Comprehensive documentation
- Efficient error handling

### Performance
- Fast response times
- Optimized database queries
- Efficient resource usage
- Scalable design

## Demonstration

### Key Workflows
1. User Registration
2. Donation Creation
3. Request Management
4. Profile Updates
5. Email Notifications

## Conclusion

### Project Success
- Meets all requirements
- User-friendly interface
- Secure implementation
- Ready for deployment

### Learning Outcomes
- Full-stack development
- Database design
- Security implementation
- UI/UX principles