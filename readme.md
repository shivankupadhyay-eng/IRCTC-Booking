# IRCTC Railway Booking System API

A Django REST Framework-based API for managing train tickets and bookings. This project provides endpoints for user authentication, train search, booking management, and analytics.

## Project Overview

This is a backend API system that mimics IRCTC (Indian Railways) booking functionality with the following core features:
- User authentication and registration using JWT tokens
- Train data management (CRUD operations)
- Advanced train search with filtering and pagination
- Booking management with seat allocation
- Analytics for top routes
- Activity logging to MongoDB

## Tech Stack

- **Framework**: Django 6.0.2
- **API**: Django REST Framework 3.16.1
- **Authentication**: Django REST Framework Simple JWT 5.5.1
- **Database**: MySQL
- **Logging**: MongoDB integration for search logs
- **Language**: Python 3.x

## Project Structure

```
IRCTCProject/
├── Booking/              # Train booking management app
│   ├── models.py         # BookingData model
│   ├── views.py          # Booking and analytics views
│   ├── serializers.py    # Booking serializers
│   ├── urls.py           # Booking endpoints
│   └── migrations/
│
├── Train/                # Train data management app
│   ├── models.py         # TrainData model
│   ├── views.py          # Train CRUD and search views
│   ├── serializers.py    # Train serializers
│   ├── urls.py           # Train endpoints
│   └── migrations/
│
├── Users/                # User authentication app
│   ├── models.py         # CustomUser (AbstractUser)
│   ├── views.py          # Signup and Login views
│   ├── serializers.py    # User serializers
│   ├── urls.py           # Auth endpoints
│   ├── backends.py       # Custom authentication backends
│   └── migrations/
│
├── IRCTCProject/         # Project settings
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL router
│   ├── wsgi.py           # WSGI config
│   └── asgi.py           # ASGI config
│
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── settings.py           # Django project settings

## Models

### Users App - CustomUser
Custom user model with email-based authentication:
- `id` (UUID, Primary Key)
- `email` (Unique, Indexed)
- `first_name` (Required)
- `last_name` (Optional)
- `created_at` (Auto-set on creation)
- `updated_at` (Auto-updated)
- Uses email as USERNAME_FIELD instead of username

### Train App - TrainData
Train information and availability:
- `id` (UUID, Primary Key)
- `train_number` (Unique, Indexed, Max 5 chars)
- `name` (Max 100 chars)
- `source` (Max 100 chars)
- `destination` (Max 100 chars)
- `departure_time` (DateTime)
- `arrival_time` (DateTime)
- `total_seats` (Integer)
- `available_seats` (Integer, dynamically updated)
- Unique constraint: (train_number, name)

### Booking App - BookingData
User train bookings and reservations:
- `id` (UUID, Primary Key)
- `user` (ForeignKey to CustomUser)
- `train` (ForeignKey to TrainData)
- `booking_date` (Date)
- `seat_requested` (Integer, default: 1)
- Unique constraint: (user, train, booking_date)

## API Endpoints

### Authentication (Users App)

#### Register User
- **Endpoint**: `POST /api/users/register/`
- **Description**: Create a new user account
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```
- **Response**: User details with status 201

#### Login
- **Endpoint**: `POST /api/users/login/`
- **Description**: Authenticate user and get JWT tokens
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
- **Response**:
  ```json
  {
    "refresh": "refresh_token",
    "access": "access_token"
  }
  ```

### Train Management (Train App)

#### List All Trains (Admin Only)
- **Endpoint**: `GET /api/trains/`
- **Permissions**: IsAuthenticated, IsAdminUser
- **Response**: List of all trains

#### Get Train by Number (Admin Only)
- **Endpoint**: `GET /api/trains/<train_number>/`
- **Permissions**: IsAuthenticated, IsAdminUser
- **Response**: Single train details

#### Create/Update Train (Admin Only)
- **Endpoint**: `POST /api/trains/`
- **Permissions**: IsAuthenticated, IsAdminUser
- **Request Body**:
  ```json
  {
    "train_number": "12345",
    "name": "Express Train",
    "source": "Delhi",
    "destination": "Mumbai",
    "departure_time": "2026-02-25T10:00:00Z",
    "arrival_time": "2026-02-26T08:00:00Z",
    "total_seats": 500,
    "available_seats": 500
  }
  ```
- **Response**: Created/updated train data with status 200

#### Search Trains
- **Endpoint**: `GET /api/trains/search/`
- **Permissions**: IsAuthenticated
- **Query Parameters**:
  - `source` (string, required): Origin station
  - `destination` (string, required): Destination station
  - `date` (string, optional): Departure date (YYYY-MM-DD)
  - `limit` (integer, optional, default: 10): Results per page
  - `offset` (integer, optional, default: 0): Pagination offset
- **Response**:
  ```json
  {
    "count": 5,
    "results": [
      {
        "id": "uuid",
        "train_number": "12345",
        "name": "Express",
        "source": "Delhi",
        "destination": "Mumbai",
        "departure_time": "2026-02-25T10:00:00Z",
        "arrival_time": "2026-02-26T08:00:00Z",
        "total_seats": 500,
        "available_seats": 450
      }
    ]
  }
  ```
- **Features**:
  - Case-insensitive search
  - Pagination support
  - Optional date filtering
  - Logs search queries to MongoDB with execution time
  - Tracks user ID and result count for analytics

### Booking Management (Booking App)

#### Get User Bookings
- **Endpoint**: `GET /api/booking/`
- **Permissions**: IsAuthenticated
- **Description**: Retrieve all bookings for the authenticated user
- **Response**: List of user's bookings with related train information

#### Create Booking
- **Endpoint**: `POST /api/booking/create/`
- **Permissions**: IsAuthenticated
- **Description**: Book seats on a train
- **Request Body**:
  ```json
  {
    "train_number": "12345",
    "booking_date": "2026-02-25",
    "seat_requested": 2
  }
  ```
- **Response**: Booking details with status 201
- **Features**:
  - Atomic transactions ensure seat availability
  - Validates sufficient seats available
  - Automatically decrements available seats
  - Prevents duplicate bookings per user, train, and date

#### Analytics - Top Routes
- **Endpoint**: `GET /api/booking/analytics/top-routes/`
- **Permissions**: IsAuthenticated
- **Description**: Get analytics for most booked routes
- **Response**: Sorted list of routes by booking count

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
cd d:\IRCTCProject
```

### 2. Create Virtual Environment
```bash
python -m venv irctcenv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
irctcenv\Scripts\activate
```

**Linux/Mac:**
```bash
source irctcenv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure MySQL Database

Update `settings.py` with your MySQL configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'irctc_db',
        'USER': 'root',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
```

Make sure:
- MySQL server is running
- Database `irctc_db` is created
- MySQL user has appropriate permissions
- `MySQLdb` or `mysql-connector-python` package is installed

### 6. Run Migrations
```bash
python manage.py migrate
```

### 7. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 8. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. Register or login to get access tokens
2. Include the access token in request headers:
   ```
   Authorization: Bearer <access_token>
   ```

## Database Logging

Search queries are logged to MongoDB with the following details:
- Endpoint accessed
- Query parameters (source, destination, date, limit, offset)
- User ID
- Execution time in milliseconds
- Result count
- Timestamp

Requires MongoDB configuration in settings.py.

## Key Features

✅ **Email-based Authentication** - Custom user model with JWT tokens
✅ **Advanced Train Search** - Filter by source, destination, date with pagination
✅ **Atomic Bookings** - Database transactions ensure data consistency
✅ **Seat Management** - Real-time seat availability tracking
✅ **Admin Controls** - Separate permissions for train management
✅ **Analytics** - Track popular routes
✅ **Activity Logging** - MongoDB integration for audit trails
✅ **Error Handling** - Comprehensive validation and error responses

## Future Enhancements

- Payment gateway integration
- Cancellation and refund management
- Real-time seat availability notifications
- Rating and review system
- Email notifications
- Advance booking system
- Multiple booking types (General, First Class, AC)

## Contributing

1. Create a new branch for features/fixes
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please contact the development team.
