# 🌍 GlobeTrek: Smart Travel Planner

GlobeTrek is an intelligent Django-based travel planning application that helps users create personalized itineraries based on their preferences, budget, and interests. The application features a modern dark theme, AI-powered trip planning, and integration with Google Maps and Places API.

## 🚀 Features

- **User Authentication**: Registration, login, email verification with OTP
- **Smart Trip Planning**: AI-powered itinerary generation based on user preferences
- **Budget Management**: Automatic budget allocation and daily spending calculations
- **Interactive Maps**: Google Maps integration for destination visualization
- **Hotel Recommendations**: Smart hotel suggestions within budget range
- **Responsive Design**: Dark theme with Bootstrap 5
- **Profile Management**: User profiles with travel interests and preferences
- **Admin Panel**: Complete Django admin interface for management

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4, Python 3.10+
- **Frontend**: Django Templates, Bootstrap 5, JavaScript
- **Database**: SQLite (development), PostgreSQL (production ready)
- **APIs**: Google Maps, Google Places, Gmail SMTP
- **Styling**: Bootstrap 5 with custom dark theme

## 📋 Prerequisites

- Python 3.10 or higher
- Git
- Google Maps API Key
- Gmail account with App Password (for email features)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Olalekan2040-slack/Travel-Planner.git
   cd Travel-Planner
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Email Settings (Gmail SMTP)
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   
   # Google Maps API
   GOOGLE_MAPS_API_KEY=your-google-maps-api-key
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 🔑 API Keys Setup

### Google Maps Platform API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Maps JavaScript API
   - Places API
   - Geocoding API
   - Maps Embed API
4. Create credentials (API Key)
5. Add the API key to your `.env` file

### Gmail SMTP Setup

1. Go to [Google Account Settings](https://myaccount.google.com/apppasswords)
2. Generate an App Password
3. Use this app password (not your regular Gmail password) in `.env`

## 📁 Project Structure

```
Travel-Planner/
├── globetrek/           # Main Django project
├── accounts/            # User authentication app
├── trips/              # Trip planning app
├── core/               # Core functionality (home, about)
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS, images)
├── media/              # User uploaded files
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── manage.py          # Django management script
```

## 🎨 Features Overview

### User Management
- User registration with email verification
- Secure login/logout
- Profile management with travel interests
- Password reset functionality

### Trip Planning
- Create detailed trip plans
- Set destination, dates, and budget
- Specify travel interests
- Automatic itinerary generation
- Daily budget allocation

### Smart Recommendations
- Hotel suggestions based on budget
- Points of interest based on user interests
- Interactive maps for visualization
- Cost-effective activity planning

## 🚧 Development Status

This is the initial release (v1.0) with core functionality implemented:

✅ **Completed Features:**
- User authentication system
- Basic trip planning
- Dark theme UI
- Database models
- Admin interface
- Email notifications

🔄 **In Progress:**
- Google Maps API integration
- Advanced itinerary generation
- PDF export functionality
- Hotel booking integration

📋 **Planned Features:**
- Weather integration
- Social sharing
- Trip collaboration
- Mobile app
- Advanced analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact: support@globetrek.com

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive UI components
- Google for Maps and Places APIs
- All contributors and testers

---

**Happy Traveling! 🌟**
A web app created with Django that helps users in generating an itinerary plan for a trip based on their destination, start and end date, budget and interests. 
