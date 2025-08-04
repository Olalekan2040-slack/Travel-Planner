<div align="center">

# 🌍 GlobeTrek: Smart Travel Planner

<img src="https://img.shields.io/badge/Django-5.2.4-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap">
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">

**An intelligent Django-based travel planning application that creates personalized itineraries based on your preferences, budget, and interests.**

[🚀 Demo](#demo) • [📋 Features](#features) • [🛠️ Installation](#installation) • [📖 Documentation](#documentation) • [🤝 Contributing](#contributing)

---

</div>

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔐 **User Management**
- ✅ Secure registration & login
- ✅ Email verification with OTP
- ✅ Password reset functionality  
- ✅ User profiles with travel interests
- ✅ Profile picture upload

### 🎨 **Modern UI/UX**
- ✅ Dark theme with Bootstrap 5
- ✅ Responsive design for all devices
- ✅ Beautiful gradient effects
- ✅ Interactive animations
- ✅ Professional dashboard

</td>
<td width="50%">

### ✈️ **Smart Trip Planning**
- ✅ AI-powered itinerary generation
- ✅ Budget management & allocation
- ✅ Interest-based recommendations
- ✅ Multi-day trip planning
- ✅ Hotel suggestions

### 🗺️ **Maps & Integration**
- ✅ Google Maps integration
- ✅ Interactive destination maps
- ✅ Points of interest discovery
- ✅ Real-time location data
- ✅ Route optimization

</td>
</tr>
</table>

---

## 🎯 Demo

<div align="center">

### 🏠 **Home Page**
*Clean, modern interface with dark theme*

### 📊 **Dashboard**
*Comprehensive trip management with statistics*

### 🗓️ **Trip Planning**
*Intelligent itinerary generation based on your preferences*

### 🏨 **Hotel Recommendations**
*Smart suggestions within your budget range*

</div>

---

## 🛠️ Technology Stack

<div align="center">

| Category | Technologies |
|----------|-------------|
| **Backend** | ![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) |
| **Frontend** | ![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=flat&logo=bootstrap&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) |
| **Database** | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white) |
| **APIs** | ![Google Maps](https://img.shields.io/badge/Google_Maps-4285F4?style=flat&logo=google-maps&logoColor=white) ![Gmail](https://img.shields.io/badge/Gmail-D14836?style=flat&logo=gmail&logoColor=white) |
| **Tools** | ![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white) ![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=flat&logo=visual-studio-code&logoColor=white) |

</div>

---

## � Installation

### �📋 Prerequisites

- 🐍 **Python 3.10+**
- 🔑 **Google Maps API Key**
- 📧 **Gmail Account with App Password**

### ⚡ Quick Start

```bash
# 1️⃣ Clone the repository
git clone https://github.com/Olalekan2040-slack/Travel-Planner.git
cd Travel-Planner

# 2️⃣ Create virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Environment setup
cp .env.example .env
# Edit .env with your API keys

# 5️⃣ Database setup
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 6️⃣ Run the server
python manage.py runserver
```

### 🔧 Environment Configuration

Create a `.env` file with your configuration:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Settings
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Google Maps API
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

---

## 🔑 API Setup Guide

### 🗺️ Google Maps Platform

1. Visit [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable these APIs:
   - 🗺️ Maps JavaScript API
   - 📍 Places API
   - 🌐 Geocoding API
   - 🖼️ Maps Embed API
4. Create API credentials
5. Add to your `.env` file

### 📧 Gmail SMTP

1. Go to [Google Account Settings](https://myaccount.google.com/apppasswords)
2. Generate an App Password
3. Use this password (not your regular Gmail password)
4. Add to your `.env` file

---

## 📁 Project Structure

```
Travel-Planner/
├── 🌐 globetrek/           # Main Django project
├── 👤 accounts/            # User authentication
├── ✈️ trips/              # Trip planning functionality
├── 🏠 core/               # Core pages (home, about)
├── 🎨 templates/          # HTML templates
├── 📁 static/             # CSS, JS, images
├── 📷 media/              # User uploads
├── 📋 requirements.txt    # Dependencies
├── ⚙️ .env.example        # Environment template
└── 🚀 manage.py          # Django management
```

---

## 🎨 Screenshots

<div align="center">

### 🌙 Dark Theme Interface

<table>
<tr>
<td width="50%" align="center">
<h4>🏠 Landing Page</h4>
<em>Modern hero section with call-to-action</em>
</td>
<td width="50%" align="center">
<h4>📊 User Dashboard</h4>
<em>Comprehensive trip management</em>
</td>
</tr>
<tr>
<td width="50%" align="center">
<h4>✈️ Trip Creation</h4>
<em>Intuitive trip planning interface</em>
</td>
<td width="50%" align="center">
<h4>🗺️ Trip Details</h4>
<em>Interactive maps and itineraries</em>
</td>
</tr>
</table>

</div>

---

## 📖 Usage

### 👤 User Registration
1. Visit `/accounts/register/`
2. Fill in your details
3. Verify email with OTP
4. Start planning trips!

### ✈️ Creating a Trip
1. Go to "Plan New Trip"
2. Enter destination and dates
3. Set your budget
4. Specify interests
5. Get AI-generated itinerary!

### 🏨 Hotel Recommendations
- Automatic suggestions based on budget
- Ratings and reviews
- Location mapping
- Price comparison

---

## 🚧 Development Status

<div align="center">

### 🎯 Current Version: v1.0

| Feature | Status | Description |
|---------|--------|-------------|
| 🔐 User Auth | ✅ Complete | Registration, login, email verification |
| ✈️ Trip Planning | ✅ Complete | Basic trip creation and management |
| 🎨 UI/UX | ✅ Complete | Dark theme, responsive design |
| 📧 Email System | ✅ Complete | SMTP integration, notifications |
| 🗺️ Maps Integration | 🔄 In Progress | Google Maps API implementation |
| 📄 PDF Export | 📋 Planned | Downloadable itineraries |
| 🤝 Trip Sharing | 📋 Planned | Social features |
| 📱 Mobile App | 📋 Future | React Native implementation |

</div>

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### � Bug Reports
- Use GitHub Issues
- Include detailed steps to reproduce
- Add screenshots if applicable

### 💡 Feature Requests  
- Open a GitHub Issue
- Describe the feature clearly
- Explain the use case

### 🔧 Pull Requests
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### � Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python manage.py test

# Check code style
flake8 .

# Format code
black .
```

---

## �📄 License

<div align="center">

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🆘 Support & Contact

<div align="center">

### 💬 Get Help

[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Olalekan2040-slack/Travel-Planner/issues)
[![Email Support](https://img.shields.io/badge/Email-Support-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:support@globetrek.com)

### 🌟 Show Your Support

If you find this project helpful, please give it a ⭐ on GitHub!

[![GitHub stars](https://img.shields.io/github/stars/Olalekan2040-slack/Travel-Planner?style=social)](https://github.com/Olalekan2040-slack/Travel-Planner/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Olalekan2040-slack/Travel-Planner?style=social)](https://github.com/Olalekan2040-slack/Travel-Planner/network/members)

</div>

---

## 🙏 Acknowledgments

<div align="center">

**Special thanks to:**

- 🐍 **Django Team** - For the amazing framework
- 🎨 **Bootstrap Team** - For the beautiful UI components  
- 🗺️ **Google** - For Maps and Places APIs
- 👥 **Open Source Community** - For inspiration and contributions
- ☕ **Coffee** - For keeping developers awake

---

### 🌟 **Made with ❤️ by developers, for travelers**

**Happy Traveling! ✈️�**

</div>
A web app created with Django that helps users in generating an itinerary plan for a trip based on their destination, start and end date, budget and interests. 
