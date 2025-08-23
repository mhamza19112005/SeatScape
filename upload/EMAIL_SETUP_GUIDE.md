# Email Configuration Guide for SeatScape

## 🔧 **Current Development Setup**

Your project is currently configured to use Django's console email backend, which means:
- Password reset links are printed to the console/terminal
- No actual emails are sent
- Perfect for development and testing

## 📧 **Production Email Setup**

### **Option 1: Gmail SMTP (Recommended for small projects)**

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Update settings.py**:

```python
# Email Configuration for Production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Not your regular password!
```

### **Option 2: SendGrid (Recommended for production)**

1. **Sign up** at [sendgrid.com](https://sendgrid.com)
2. **Create API Key**
3. **Update settings.py**:

```python
# Email Configuration for Production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
```

### **Option 3: Environment Variables (Most Secure)**

Create a `.env` file in your project root:

```bash
# .env file
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Then update `settings.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Email Configuration
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 1025))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'False').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
```

## 🚀 **Testing Email Functionality**

1. **Start your Django server**:
   ```bash
   python manage.py runserver
   ```

2. **Go to forget password page**: `/forget-password/`

3. **Enter a valid email** and submit

4. **Check the result**:
   - **Development**: Link appears in console/terminal
   - **Production**: Email is sent to the address

## 🔒 **Security Features**

- **1-minute expiration**: Reset links expire quickly
- **Secure tokens**: Cryptographically secure reset tokens
- **User validation**: Only valid users can request resets
- **Rate limiting**: Django prevents abuse

## 📱 **Email Template Customization**

The current email template includes:
- Professional greeting
- Clear reset link
- Security warning about expiration
- Branding (SeatScape)

You can customize the email content in `accounts/views.py` around line 90.

## 🎯 **Next Steps**

1. **Test the current setup** (console backend)
2. **Choose an email provider** (Gmail/SendGrid recommended)
3. **Update settings.py** with your email configuration
4. **Test with real email sending**
5. **Deploy to production**

## ❓ **Common Issues**

- **"Authentication failed"**: Check your email/password
- **"Connection refused"**: Check firewall/port settings
- **"SSL/TLS required"**: Make sure `EMAIL_USE_TLS = True`
- **"App password required"**: Gmail needs app-specific passwords

## 🔗 **Useful Links**

- [Django Email Documentation](https://docs.djangoproject.com/en/5.2/topics/email/)
- [Gmail SMTP Setup](https://support.google.com/mail/answer/7126229)
- [SendGrid Documentation](https://sendgrid.com/docs/)
- [Python-dotenv](https://pypi.org/project/python-dotenv/)
