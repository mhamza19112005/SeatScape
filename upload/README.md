# SeatScape - Event Booking System

A modern Django-based event booking platform with advanced seat selection, unified authentication, and beautiful UI design.

## 🌟 Features

### 🎫 **Event Management**
- Browse and view events with detailed information
- Interactive seat selection with SVG-based venue layouts
- Real-time seat availability updates
- Booking confirmation and ticket generation

### 🔐 **Unified Authentication System**
- **Single Page Authentication**: Combined login and signup forms with tab switching
- **Enhanced Security**: CSRF protection, password validation, and secure sessions
- **Password Management**: Forget password and reset functionality
- **Social Login Ready**: Google OAuth integration prepared
- **Modern UI**: Glassmorphism design with smooth animations

### 👤 **User Experience**
- **Profile Dropdown**: User avatar with navigation menu
- **Responsive Design**: Works seamlessly on all devices
- **Error Handling**: Clear, user-friendly error messages
- **Success Feedback**: Visual confirmation for user actions

### 🎨 **Modern Interface**
- **Glassmorphism Design**: Translucent, modern UI elements
- **Smooth Animations**: Hover effects and transitions
- **Mobile Responsive**: Optimized for all screen sizes
- **Icon Integration**: Font Awesome icons throughout

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 5.2+
- SQLite (default) or PostgreSQL

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mhamza19112005/SeatScape.git
   cd SeatScape
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - You'll see the unified authentication page

## 📱 Application Structure

```
SeatScape/
├── accounts/                    # Authentication app
│   ├── templates/
│   │   ├── auth.html           # Unified login/signup page
│   │   ├── home.html           # User dashboard
│   │   ├── forget_password.html # Password reset request
│   │   └── reset_password.html # Password reset form
│   ├── views.py                # Authentication logic
│   └── urls.py                 # Auth URL patterns
├── tickets/                    # Event booking app
│   ├── templates/
│   │   ├── event_list.html     # Events listing
│   │   ├── event_detail.html   # Seat selection
│   │   ├── checkout.html       # Payment process
│   │   └── booking_confirmation.html
│   ├── models.py               # Event, Seat, Ticket models
│   └── views.py                # Booking logic
├── contactus/                  # Contact functionality
├── eventbooking/               # Main project settings
└── requirements.txt            # Dependencies
```

## 🔐 Authentication Features

### Unified Authentication Page
- **Single Interface**: Both login and signup on one page
- **Tab Switching**: Seamless transition between forms
- **Form Validation**: Real-time error checking
- **Auto-redirect**: Logged-in users automatically redirected

### Password Management
- **Forget Password**: Email-based password reset
- **Secure Tokens**: Cryptographically secure reset links
- **Token Validation**: Time-limited reset tokens

### User Profile
- **Avatar Display**: Initial-based user avatars
- **Dropdown Menu**: Quick access to profile options
- **Logout Functionality**: Secure session termination

## 🎫 Booking System

### Event Management
- **Event Listing**: Browse available events
- **Detailed View**: Event information and seat map
- **Seat Selection**: Interactive SVG-based selection
- **Availability**: Real-time seat status updates

### Ticket Processing
- **Checkout Flow**: Streamlined booking process
- **Payment Integration**: Ready for payment gateway
- **Confirmation**: Booking confirmation with details
- **History Tracking**: User booking history

## 🎨 UI/UX Design

### Modern Aesthetics
- **Glassmorphism**: Translucent, layered design
- **Color Scheme**: Gradient backgrounds and glass effects
- **Typography**: Clean, readable fonts
- **Spacing**: Consistent, balanced layout

### Interactive Elements
- **Hover Effects**: Smooth transition animations
- **Button States**: Visual feedback for interactions
- **Form Focus**: Clear input state indicators
- **Loading States**: User feedback during processing

## 🛠️ Technical Details

### Backend
- **Framework**: Django 5.2
- **Database**: SQLite (development), PostgreSQL ready
- **Authentication**: Django built-in auth system
- **Session Management**: Secure session handling

### Frontend
- **CSS Framework**: Custom CSS with Bootstrap components
- **Icons**: Font Awesome 5.15.4
- **Fonts**: Google Fonts (Poppins)
- **JavaScript**: Vanilla JS for interactions

### Security
- **CSRF Protection**: All forms protected
- **Password Validation**: Django validators
- **Session Security**: Secure session configuration
- **Input Sanitization**: Form data validation

## 📋 URL Structure

```
/                    → Unified Authentication Page
/login/             → Redirects to unified auth
/signup/            → Redirects to unified auth
/home/              → User dashboard (auth required)
/logout/            → Logout and redirect
/forget-password/   → Password reset request
/reset-password/    → Password reset form
/tickets/           → Event listing
/tickets/<id>/      → Event detail and booking
/contact/           → Contact form
/admin/             → Django admin panel
```

## 🔧 Configuration

### Settings Highlights
```python
# Authentication
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# Messages Framework
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tickets',
    'contactus',
    'accounts',
]
```

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure production database (PostgreSQL)
- [ ] Set up static files serving
- [ ] Configure email backend
- [ ] Set secure headers
- [ ] Enable HTTPS
- [ ] Configure domain in `ALLOWED_HOSTS`

### Environment Variables
```bash
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/dbname
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Muhammad Hamza**
- GitHub: [@mhamza19112005](https://github.com/mhamza19112005)
- Project: [SeatScape](https://github.com/mhamza19112005/SeatScape)

## 🙏 Acknowledgments

- Django community for the excellent framework
- Font Awesome for the beautiful icons
- Google Fonts for typography
- Bootstrap for UI components

## 📸 Screenshots

### Authentication Page
![Auth Page](screenshots/auth-page.png)
*Unified login and signup interface with glassmorphism design*

### User Dashboard
![Dashboard](screenshots/dashboard.png)
*Modern user dashboard with profile dropdown*

### Event Booking
![Booking](screenshots/event-booking.png)
*Interactive seat selection and booking interface*

## 🔄 Version History

- **v1.0.0** - Initial release with unified authentication
- **v1.1.0** - Enhanced UI/UX with glassmorphism design
- **v1.2.0** - Added password reset functionality
- **v1.3.0** - Improved error handling and user feedback

---

Made with ❤️ by [Muhammad Hamza](https://github.com/mhamza19112005)
