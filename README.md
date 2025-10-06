# 🔍 Lost & Found Management System

A comprehensive Django-based web application for managing lost and found items in educational institutions. This system enables students and staff to report lost items, search for found items, and communicate through real-time chat functionality.

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![WebSocket](https://img.shields.io/badge/WebSocket-Channels-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Architecture](#-project-architecture)
- [Database Schema](#-database-schema)
- [Installation Guide](#-installation-guide)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The **Lost & Found Management System** is designed specifically for educational institutions to streamline the process of reporting and recovering lost items. The platform provides:

- **Email-verified user authentication** (College email required)
- **Item reporting system** with categories and images
- **Real-time chat** between item finders and losers
- **Advanced search and filter** capabilities
- **Responsive design** for mobile and desktop

### Why This Project?

**Problem Statement:**
- Students frequently lose items on campus (phones, wallets, documents, etc.)
- No centralized system to report or claim lost items
- Difficult to connect item finders with losers
- Manual processes are time-consuming and ineffective

**Solution:**
- Digital platform for instant reporting
- Categorized item listing for easy searching
- Real-time communication via WebSocket chat
- Email verification ensures legitimate users
- Image uploads for better item identification

---

## ✨ Features

### 🔐 Authentication & Authorization
- ✅ User registration with college email validation
- ✅ Email verification system using UUID tokens
- ✅ Secure login/logout functionality
- ✅ Session management (2-week persistence)
- ✅ Password validation with Django validators

### 📦 Item Management
- ✅ Report found items with details
- ✅ Upload item images
- ✅ Categorize items (Electronics, Documents, Clothing, Other)
- ✅ Add location and date information
- ✅ Search and filter by category
- ✅ View detailed item information

### 💬 Real-time Communication
- ✅ WebSocket-based chat system
- ✅ One-on-one messaging between users
- ✅ Thread-based conversation management
- ✅ Message history storage
- ✅ Real-time message delivery

### 👤 User Profile
- ✅ User profile management
- ✅ View reported items
- ✅ Chat history
- ✅ Account settings

---

## 🛠 Technology Stack

### Backend
```
├── Django 4.2          → Web Framework
├── Django Channels     → WebSocket Support
├── SQLite3            → Database (Development)
├── MySQL Support      → Database (Production)
└── ASGI               → Async Server Gateway
```

### Frontend
```
├── HTML5 & CSS3       → Structure & Styling
├── JavaScript         → Interactivity
└── Bootstrap          → Responsive Design
```

### Real-time Features
```
├── WebSocket          → Bidirectional Communication
├── Channels           → Django WebSocket Support
└── In-Memory Layer    → Channel Layer (Dev)
```

### Security & Email
```
├── Django Auth        → User Authentication
├── SMTP (Gmail)       → Email Verification
└── CSRF Protection    → Security Middleware
```

---

## 🏗 Project Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Browser    │  │   Mobile     │  │   Tablet     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────┬────────────────────────────────────────────────┘
             │
             │ HTTP/HTTPS & WebSocket
             ▼
┌─────────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Django Templates & Static Files            │  │
│  │  • home.html  • login.html  • register.html          │  │
│  │  • CSS Files  • JavaScript  • Images                 │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │  Accounts  │  │ Found_App  │  │    Chat    │           │
│  │    App     │  │    App     │  │    App     │           │
│  └────────────┘  └────────────┘  └────────────┘           │
│  ┌────────────┐  ┌──────────────────────────────┐         │
│  │   User     │  │      URL Router              │         │
│  │    App     │  │   (lxfpro.urls)              │         │
│  └────────────┘  └──────────────────────────────┘         │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Views     │  │   Consumers  │  │   Managers   │     │
│  │  (HTTP)      │  │  (WebSocket) │  │  (Custom)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATA ACCESS LAYER                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Django ORM (Models)                      │  │
│  │  • User  • Profile  • FoundItem  • Thread  • Message │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   SQLite / MySQL                      │  │
│  │         • auth_user  • found_item                     │  │
│  │         • chat_thread  • chat_message                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Database Schema

```mermaid
erDiagram
    USER ||--o{ FOUND_ITEM : reports
    USER ||--o{ PROFILE : has
    USER ||--o{ MESSAGE : sends
    USER }o--o{ THREAD : participates
    THREAD ||--o{ MESSAGE : contains
    FOUND_ITEM ||--o{ CHAT_MESSAGE : has

    USER {
        int id PK
        string username
        string email
        string password
        boolean is_active
        datetime date_joined
    }

    PROFILE {
        int id PK
        int user_id FK
        string verification_token
    }

    FOUND_ITEM {
        int id PK
        int user_id FK
        string item_name
        text description
        string category
        date date_found
        string location
        image image
    }

    THREAD {
        int id PK
        string name
        string thread_type
        datetime created_at
        datetime updated_at
    }

    MESSAGE {
        int id PK
        int thread_id FK
        int sender_id FK
        text text
        datetime created_at
        datetime updated_at
    }

    CHAT_MESSAGE {
        int id PK
        int item_id FK
        int sender_id FK
        text message
        datetime timestamp
    }
```

### Table Descriptions

#### 1. **User Table** (Django Default)
- Stores user authentication data
- Fields: username, email, password, is_active
- Managed by Django Auth

#### 2. **Profile Table**
- Extends User model
- Stores email verification token
- One-to-One relationship with User

#### 3. **Found_Item Table**
- Stores reported lost/found items
- Categories: Electronics, Documents, Clothing, Other
- Includes image upload capability
- Links to User (reporter)

#### 4. **Thread Table**
- Manages chat conversations
- Types: Personal (1-on-1), Group
- Many-to-Many with Users
- Tracks creation and update times

#### 5. **Message Table**
- Stores chat messages
- Links to Thread and Sender
- Timestamp tracking
- Real-time delivery via WebSocket

#### 6. **Chat_Message Table**
- Item-specific chat messages
- Links Item finder with loser
- Alternative messaging system

---

## 🚀 Installation Guide

### Prerequisites
```bash
- Python 3.8 or higher
- pip (Python package manager)
- Git
- Virtual Environment (recommended)
```

### Step 1: Clone Repository
```bash
git clone https://github.com/NICK-FURY-6023/dear-project-1.git
cd dear-project-1
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install System Dependencies (for Pillow)
```bash
# On Ubuntu/Debian:
sudo apt-get update
sudo apt-get install -y libjpeg-dev zlib1g-dev

# On macOS:
brew install libjpeg zlib

# On Windows:
# Usually not required, Pillow wheels include dependencies
```

### Step 4: Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Requirements.txt Contents:**
```
asgiref==3.7.2      # ASGI support
channels==4.0.0     # WebSocket support
Django==4.2         # Main framework
mysqlclient==2.1.1  # MySQL database driver
Pillow==9.5.0       # Image processing
sqlparse==0.4.4     # SQL parsing
tzdata==2023.3      # Timezone data
```

### Step 5: Configure Database

**For SQLite (Default - Development):**
```python
# Already configured in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**For MySQL (Production):**
```python
# Uncomment in settings.py and configure:
DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'PORT': '3306',
        'HOST': 'localhost',
    }
}
```

### Step 6: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Follow the prompts to create admin account
```

### Step 8: Collect Static Files (Production)
```bash
python manage.py collectstatic
```

### Step 9: Run Development Server
```bash
python manage.py runserver
```

### Step 10: Access Application
```
🌐 Website: http://127.0.0.1:8000/
👨‍💼 Admin Panel: http://127.0.0.1:8000/admin/
```

---

## 💻 Usage

### For Users

#### 1. **Registration**
```
1. Navigate to /register/
2. Enter username, college email, password
3. Email must end with: @vpmrzshah@gmail.com
4. Check email for verification link
5. Click verification link to activate account
```

#### 2. **Login**
```
1. Navigate to /login/
2. Enter username and password
3. Account must be verified to login
4. Session lasts for 2 weeks
```

#### 3. **Report Found Item**
```
1. Login to your account
2. Navigate to report item page
3. Fill in item details:
   - Item name
   - Description
   - Category
   - Location found
   - Date found
   - Upload image (optional)
4. Submit the report
```

#### 4. **Search Items**
```
1. Browse all found items
2. Filter by category
3. Search by keywords
4. View item details
5. Contact item reporter
```

#### 5. **Chat with Users**
```
1. Click on item you're interested in
2. Start chat with reporter
3. Real-time messaging via WebSocket
4. Discuss item details
5. Arrange item return
```

### For Administrators

#### 1. **Admin Panel Access**
```
URL: /admin/
Login with superuser credentials
```

#### 2. **Manage Users**
```
- View all registered users
- Activate/deactivate accounts
- Reset passwords
- Delete spam accounts
```

#### 3. **Manage Items**
```
- View all reported items
- Edit item details
- Delete inappropriate posts
- Monitor item status
```

#### 4. **Monitor Chats**
```
- View chat threads
- Monitor messages
- Handle disputes
```

---

## 📁 Project Structure

```
dear-project-1/
│
├── 📁 accounts/                    # Authentication & User Management
│   ├── __init__.py
│   ├── admin.py                   # Admin configurations
│   ├── apps.py                    # App configuration
│   ├── models.py                  # Profile model
│   ├── urls.py                    # URL routing
│   ├── views.py                   # Login, Register, Verify views
│   ├── 📁 templates/
│   │   ├── home.html              # Homepage
│   │   ├── login.html             # Login page
│   │   └── register.html          # Registration page
│   ├── 📁 static/css/             # Account-specific styles
│   └── 📁 migrations/             # Database migrations
│
├── 📁 chat/                        # Real-time Chat System
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── consumers.py               # WebSocket consumer
│   ├── managers.py                # Custom model managers
│   ├── models.py                  # Thread & Message models
│   ├── urls.py
│   ├── views.py                   # Chat views
│   ├── 📁 templates/chat/
│   └── 📁 migrations/
│
├── 📁 found_app/                   # Lost & Found Item Management
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                  # FoundItem & ChatMessage models
│   ├── urls.py
│   ├── views.py                   # Item CRUD operations
│   ├── 📁 templates/
│   ├── 📁 static/
│   └── 📁 migrations/
│
├── 📁 user/                        # User Profile Management
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── 📁 templates/
│   ├── 📁 static/
│   └── 📁 migrations/
│
├── 📁 lxfpro/                      # Project Configuration
│   ├── __init__.py
│   ├── asgi.py                    # ASGI configuration
│   ├── routing.py                 # WebSocket routing
│   ├── settings.py                # Project settings
│   ├── urls.py                    # Main URL configuration
│   └── wsgi.py                    # WSGI configuration
│
├── 📁 media/                       # User-uploaded files
│   └── lost_items/                # Item images
│
├── 📁 static/                      # Static files (CSS, JS, Images)
│
├── db.sqlite3                     # SQLite database
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── LICENSE                        # MIT License
```

### Key Files Explained

#### **manage.py**
```python
# Django's command-line utility
# Used for:
- Running server: python manage.py runserver
- Migrations: python manage.py migrate
- Creating superuser: python manage.py createsuperuser
```

#### **settings.py**
```python
# Core configurations:
- Installed apps
- Database settings
- Email configuration
- Static/Media file paths
- Security settings
- Channel layers
```

#### **urls.py (Main)**
```python
# URL routing configuration
urlpatterns = [
    path('admin/', admin.site.urls),      # Admin panel
    path('', include('accounts.urls')),    # Auth URLs
    path('', include('found_app.urls')),   # Item URLs
    path('', include('user.urls')),        # Profile URLs
    path('', include('chat.urls')),        # Chat URLs
]
```

#### **routing.py**
```python
# WebSocket routing
# Handles WebSocket connections for real-time chat
```

#### **consumers.py**
```python
# WebSocket consumer
# Handles:
- websocket_connect: Connection establishment
- websocket_receive: Incoming messages
- websocket_message: Message broadcasting
- websocket_disconnect: Connection closing
```

#### **models.py Files**

**accounts/models.py:**
```python
# Profile model
- Extends Django User
- Stores verification token
- One-to-One with User
```

**found_app/models.py:**
```python
# FoundItem model
- Item details (name, description, category)
- Location and date information
- Image upload
- Links to User

# ChatMessage model
- Item-specific messages
- Links sender to item owner
```

**chat/models.py:**
```python
# Thread model
- Chat conversation container
- Personal/Group types
- Many-to-Many with Users

# Message model
- Individual chat messages
- Links to Thread and Sender
- Timestamp tracking
```

---

## 🔌 API Endpoints

### Authentication Endpoints
```
GET  /                    → Home page
GET  /login/              → Login page
POST /login/              → Process login
GET  /register/           → Registration page
POST /register/           → Process registration
GET  /verify/<token>/     → Email verification
GET  /logout/             → Logout user
```

### Item Management Endpoints
```
GET  /items/              → List all items
GET  /items/<id>/         → View item details
GET  /items/add/          → Add item form
POST /items/add/          → Create new item
GET  /items/<id>/edit/    → Edit item form
POST /items/<id>/edit/    → Update item
POST /items/<id>/delete/  → Delete item
GET  /items/search/       → Search items
```

### Chat Endpoints
```
GET  /chat/               → Chat list
GET  /chat/<username>/    → Chat with user
WS   /ws/chat/<username>/ → WebSocket connection
```

### User Profile Endpoints
```
GET  /profile/            → View profile
GET  /profile/edit/       → Edit profile
POST /profile/edit/       → Update profile
GET  /profile/items/      → User's items
```

### Admin Endpoints
```
GET  /admin/              → Admin dashboard
GET  /admin/users/        → Manage users
GET  /admin/items/        → Manage items
GET  /admin/chats/        → View chats
```

---

## 🎨 Application Flow Diagrams

### User Registration Flow
```
┌─────────────┐
│   User      │
│  Visits     │
│  /register/ │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│  Fill Registration Form │
│  - Username             │
│  - College Email        │
│  - Password             │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Email Validation       │
│  Must end with:         │
│  @vpmrzshah@gmail.com   │
└──────┬──────────────────┘
       │
       ├─── ✗ Invalid ──────┐
       │                     │
       │                     ▼
       │            ┌──────────────┐
       │            │ Show Error   │
       │            │ Message      │
       │            └──────────────┘
       │
       ✓ Valid
       │
       ▼
┌─────────────────────────┐
│  Create User Account    │
│  - is_active = False    │
│  - Generate UUID token  │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Send Verification Email│
│  with token link        │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  User Clicks Link       │
│  /verify/<token>/       │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Activate Account       │
│  - is_active = True     │
│  - Clear token          │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Redirect to Login      │
│  Account Ready!         │
└─────────────────────────┘
```

### Item Reporting Flow
```
┌─────────────┐
│ Logged User │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│  Click "Report Item"    │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Fill Item Form         │
│  - Item Name            │
│  - Description          │
│  - Category (Dropdown)  │
│  - Location             │
│  - Date Found           │
│  - Upload Image         │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Validate Form          │
└──────┬──────────────────┘
       │
       ├─── ✗ Invalid ──────┐
       │                     │
       │                     ▼
       │            ┌──────────────┐
       │            │ Show Errors  │
       │            └──────────────┘
       │
       ✓ Valid
       │
       ▼
┌─────────────────────────┐
│  Process Image Upload   │
│  Save to media/         │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Save to Database       │
│  - Create FoundItem     │
│  - Link to User         │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Show Success Message   │
│  Redirect to Item List  │
└─────────────────────────┘
```

### Real-time Chat Flow
```
┌─────────────┐
│   User A    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│  Click Chat with User B │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Establish WebSocket    │
│  Connection             │
│  ws://server/chat/userB │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Server: websocket      │
│  _connect()             │
│  - Get/Create Thread    │
│  - Join room/group      │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Load Message History   │
│  from Thread            │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  User A types message   │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Send via WebSocket     │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Server: websocket      │
│  _receive()             │
│  - Store message in DB  │
│  - Broadcast to group   │
└──────┬──────────────────┘
       │
       ├───────────────────┬──────────────┐
       │                   │              │
       ▼                   ▼              ▼
┌──────────┐      ┌──────────┐   ┌──────────┐
│  User A  │      │  User B  │   │ Database │
│ Receives │      │ Receives │   │  Stores  │
└──────────┘      └──────────┘   └──────────┘
```

---

## 🔒 Security Features

### 1. **Authentication Security**
- Password hashing using Django's PBKDF2
- Session-based authentication
- CSRF protection on all forms
- Email verification required

### 2. **Data Validation**
- Form validation on client and server side
- Email format validation
- File upload validation (size, type)
- SQL injection protection (Django ORM)

### 3. **Session Management**
- Secure session cookies
- 2-week session expiry
- Logout functionality
- Session hijacking prevention

### 4. **File Upload Security**
- Restricted file types (images only)
- File size limitations
- Secure file storage location
- Sanitized file names

---

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test chat
python manage.py test found_app

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 🚀 Deployment

### Production Checklist

1. **Security Settings**
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = 'your-secure-secret-key'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

2. **Database**
```python
# Use PostgreSQL or MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db',
        # ... other settings
    }
}
```

3. **Static Files**
```bash
python manage.py collectstatic
```

4. **Environment Variables**
```bash
# Use .env file for sensitive data
- SECRET_KEY
- DATABASE_URL
- EMAIL_HOST_PASSWORD
```

5. **WebSocket (Redis)**
```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 style guide
- Write meaningful commit messages
- Add comments for complex logic
- Update documentation
- Write tests for new features

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **NICK-FURY-6023** - *Initial work* - [GitHub Profile](https://github.com/NICK-FURY-6023)

---

## 🙏 Acknowledgments

- Django Documentation
- Django Channels Documentation
- Bootstrap Framework
- Stack Overflow Community
- GitHub Community

---

## 📧 Contact & Support

For queries and support:
- **GitHub Issues**: [Create an issue](https://github.com/NICK-FURY-6023/dear-project-1/issues)
- **Email**: lostandfound.vpmrzshah@gmail.com

---

## 📈 Future Enhancements

- [ ] Mobile app (React Native/Flutter)
- [ ] Push notifications
- [ ] Advanced search with AI
- [ ] Item matching algorithm
- [ ] Multi-language support
- [ ] Analytics dashboard
- [ ] Export reports (PDF/Excel)
- [ ] Integration with college ID system
- [ ] QR code for item tracking
- [ ] Reward system for finders

---

## 📊 Statistics

```
Total Lines of Code: ~5000+
Apps: 4 (accounts, chat, found_app, user)
Models: 6
Views: 15+
Templates: 10+
WebSocket Consumers: 1
```

---

**Made with ❤️ for the student community**

*Last Updated: October 6, 2025*