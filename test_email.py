#!/usr/bin/env python
"""
Simple email test script for SeatScape
Run this to test if your email configuration is working
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventbooking.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    """Test email sending functionality"""
    print("🧪 Testing Email Configuration...")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'Not set'}")
    
    try:
        # Test email
        subject = '🧪 SeatScape Email Test'
        message = '''
Hello!

This is a test email from your SeatScape application.

If you receive this email, your email configuration is working correctly!

Best regards,
SeatScape Team
        '''
        
        # Send to yourself
        recipient = settings.EMAIL_HOST_USER
        
        print(f"\n📧 Sending test email to: {recipient}")
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [recipient],
            fail_silently=False,
        )
        
        print("✅ Email sent successfully!")
        print("📬 Check your inbox (and spam folder)")
        
    except Exception as e:
        print(f"❌ Email failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check if 2-Factor Authentication is enabled on your Gmail")
        print("2. Verify the app password is correct")
        print("3. Make sure 'Less secure app access' is disabled")
        print("4. Check if your Gmail account allows SMTP access")

if __name__ == "__main__":
    test_email()
