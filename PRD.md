Here’s the **complete project plan and specification** for a **Django-based Travel Planner Web Application** using only Django (without Django REST Framework), focusing on server-rendered HTML, forms, and integrations with external APIs.

---

# 🌍 **Project Title:**

**"GlobeTrek: Smart Travel Planner (Django Edition)"**

---

## 🎯 **Project Goal:**

To build a smart, web-based travel planner using Django that allows users to:

* Create and save trip plans
* Automatically generate itineraries based on the number of days, destination, budget, and interest
* Suggest hotels and attractions
* Display live maps and POIs (Points of Interest)
* Register and login with email verification using Gmail SMTP

---

## 🧱 **Technology Stack**

### 💻 Backend:

* Django (full-stack web framework)
* Python 3.10+

### 🎨 Frontend:

* Django Templates
* Bootstrap 5 (for responsive UI)
* Google Maps Embeds

### 📊 Database:

* SQLite (development)
* PostgreSQL (production)

### 📧 Email:

* Gmail SMTP for sending OTPs, password resets, and notifications

---

## 🔐 **Authentication Features:**

* User registration and login
* Email verification using OTP (sent via Gmail SMTP)
* Password reset via email
* User profile with editable interests

---

## 🧩 **Core Functional Features**

### 1. **User System**

* Registration with name, email, password
* OTP email confirmation using Gmail SMTP
* Login and logout
* Password reset (via link sent to email)
* Profile management (interests, phone, nationality)

---

### 2. **Trip Planning**

Users can:

* Choose destination
* Specify number of days
* Set exact budget (e.g., ₦200,000 or \$1000)
* Select interests (e.g., food, culture, nature)

System will:

* Calculate average daily budget
* Generate daily itinerary with places to visit
* Suggest affordable hotels
* Provide embedded Google Map of destination

---

### 3. **Itinerary Generation Logic**

* Divide budget per day
* Fetch Points of Interest (POIs) using Google Places API based on user interest
* Filter POIs by relevance, rating, and cost (if available)
* Generate structured day-by-day itinerary
* Show live map for each POI
* Offer PDF download of itinerary (optional)

---

### 4. **Hotel Suggestions**

* Use Google Places API to fetch hotels in the destination city
* Filter hotels by budget range
* Display hotel name, rating, address, and Google Maps link

---

### 5. **Live Destination View**

* Integrate Google Maps Embed API to show:

  * Destination city
  * Hotels
  * Attractions
  * Route overview (optional)

---

## 🗃️ **Key Models in the Project**

* **User** (extended from Django default)
* **TripPlan** (stores user trip configurations)
* **ItineraryDay** (details of activities for each day)
* **Destination** (optionally prepopulate some destinations)
* **HotelSuggestion** (cached or fetched from API)

---

## 📄 **Main Pages (Templates)**

| Page           | Description                                 |
| -------------- | ------------------------------------------- |
| Home           | Introduction, call-to-action                |
| Register       | User signup with email                      |
| Verify Email   | OTP input form                              |
| Login          | User login                                  |
| Dashboard      | List of past trip plans, profile management |
| New Trip Plan  | Form to create a trip                       |
| Trip Result    | Itinerary + hotel suggestions + map         |
| Trip Detail    | View saved trip                             |
| Password Reset | Email entry, reset link                     |
| About          | About the platform, contact, etc.           |

---

## 🧪 **Key Features Breakdown**

| Feature                  | Method                                        |
| ------------------------ | --------------------------------------------- |
| OTP generation and email | Use Django's `EmailMessage` and random module |
| Google Maps              | Embed via `<iframe>`                          |
| API integration          | Use `requests` module in views                |
| Budget logic             | Divide by days, match with POI/hotel cost     |
| Session handling         | Django session framework                      |
| Access control           | Django’s built-in login required decorators   |
| Template logic           | Loop through POIs, hotel list, maps           |
| Mobile responsive        | Bootstrap CSS                                 |
| PDF itinerary (optional) | Use `xhtml2pdf` or `WeasyPrint`               |

---

## 🧪 **Admin Panel**

* Django admin will be used to manage:

  * Users
  * Trip plans
  * Saved itineraries
  * Destination data (optional pre-populated)
  * OTP logs (optional)

---

## 🔐 **API Keys Required**

1. **Google Maps Platform API Key**
   Required for:

   * Maps Embed API

   * Places API

   * Geocoding API

   * Directions API (optional)

   > **Get it from**: [https://console.cloud.google.com](https://console.cloud.google.com)

   Enable these services:

   * `Maps JavaScript API`
   * `Places API`
   * `Geocoding API`
   * `Maps Embed API`

2. **Gmail SMTP Configuration (for OTP, reset emails)**

   * SMTP Server: `smtp.gmail.com`
   * Port: `587`
   * TLS: Yes
   * Email: Your Gmail account
   * Password: **App password**, not your normal Gmail password

     > Get app password from [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

---

## 📦 **Optional APIs (Advanced)**

| API                | Purpose                                      | Alternative               |
| ------------------ | -------------------------------------------- | ------------------------- |
| OpenWeatherMap API | Display live weather at destination          | WeatherAPI, Climacell     |
| Booking.com API    | Fetch hotel deals                            | Use Google Places instead |
| OpenAI API         | Smart itinerary suggestion based on interest | Optional                  |
| IPInfo API         | Guess user's country/city                    | Optional                  |

---


---

## 📅 **Development Timeline Suggestion**

| Week | Tasks                                          |
| ---- | ---------------------------------------------- |
| 1    | Project setup, user model, register/login      |
| 2    | Gmail SMTP, OTP verification, password reset   |
| 3    | Trip form, budget logic, itinerary generation  |
| 4    | Integrate Google Maps & Places API             |
| 5    | Show itinerary, hotel results, daily breakdown |
| 6    | User dashboard, save trips                     |
| 7    | Polish UI, testing                             |
| 8    | Deployment to Render/Heroku or VPS             |

---

## 🔚 Summary

You’re building a **smart Django-powered travel assistant** that:

* Understands the user’s trip preferences
* Generates detailed, budget-based itineraries from users location/state/country 
* Embeds rich map experiences
* Relies solely on Django views, forms, and templates (no REST framework)

