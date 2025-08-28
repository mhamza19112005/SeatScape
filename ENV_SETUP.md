# Environment Variables Setup

## Overview
This project uses environment variables to store sensitive information like API keys, database credentials, and other configuration settings. This approach keeps sensitive data out of the codebase and allows for different configurations in development and production environments.

## Setup Instructions

1. Create a `.env` file in the root directory of the project
2. Add the following variables to your `.env` file, replacing the values with your own:

```
# Django Settings
SECRET_KEY=your_django_secret_key
DEBUG=True  # Set to False in production

# Email Configuration
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=your_email@example.com
CONTACT_RECEIVER_EMAIL=your_email@example.com

# Stripe Settings
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret

# Database Settings (if using PostgreSQL)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=your_db_name
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_HOST=localhost
# DB_PORT=5432
```

## Important Notes

1. **Never commit your `.env` file to version control**. It's already added to `.gitignore`.
2. For production deployment, set `DEBUG=False` and ensure all security-related settings are properly configured.
3. Make sure to use strong, unique passwords and API keys.
4. For team development, share a template `.env.example` file with placeholder values.

## Required Packages

This project uses `python-dotenv` to load environment variables. It's included in the `requirements.txt` file, so it will be installed when you run:

```
pip install -r requirements.txt
```