#!/usr/bin/env python
"""
Email Configuration Test Script for Lost & Found Portal
Tests SMTP email sending functionality
"""

import os
import sys
import django

# Setup Django
sys.path.append('/workspaces/dear-project-1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lxfpro.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
import smtplib

print("=" * 60)
print("📧 EMAIL CONFIGURATION TEST")
print("=" * 60)

# Display current settings
print("\n🔧 Current Email Settings:")
print(f"   Backend: {settings.EMAIL_BACKEND}")
print(f"   Host: {settings.EMAIL_HOST}")
print(f"   Port: {settings.EMAIL_PORT}")
print(f"   TLS: {settings.EMAIL_USE_TLS}")
print(f"   User: {settings.EMAIL_HOST_USER}")
print(f"   Password: {'*' * len(settings.EMAIL_HOST_PASSWORD)}")

# Test 1: Basic SMTP Connection
print("\n" + "=" * 60)
print("TEST 1: Basic SMTP Connection")
print("=" * 60)

try:
    smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    smtp.ehlo()
    print("✅ SMTP connection successful")
    
    smtp.starttls()
    print("✅ TLS encryption enabled")
    
    smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    print("✅ SMTP login successful")
    
    smtp.quit()
    print("✅ SMTP connection closed properly")
    
except smtplib.SMTPAuthenticationError as e:
    print(f"❌ Authentication failed: {e}")
    print("   Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD")
    
except smtplib.SMTPException as e:
    print(f"❌ SMTP error: {e}")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")

# Test 2: Send Test Email
print("\n" + "=" * 60)
print("TEST 2: Send Test Email via Django")
print("=" * 60)

test_email = input("\nEnter email address to receive test OTP (or press Enter to skip): ").strip()

if test_email:
    test_otp = "123456"
    
    email_body = f"""
Hello Test User,

This is a test email from Lost & Found Portal.

Your test OTP is: {test_otp}

If you received this email, the email configuration is working correctly!

Best regards,
Lost & Found Portal Team
"""
    
    try:
        print(f"\n📤 Sending test email to {test_email}...")
        
        result = send_mail(
            "Test OTP - Lost & Found Portal",
            email_body,
            settings.EMAIL_HOST_USER,
            [test_email],
            fail_silently=False
        )
        
        if result > 0:
            print(f"✅ Test email sent successfully!")
            print(f"   Check inbox of {test_email}")
        else:
            print(f"⚠️ send_mail returned {result}")
            
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        import traceback
        traceback.print_exc()
else:
    print("ℹ️ Skipping email send test")

# Test 3: Check Email Backend
print("\n" + "=" * 60)
print("TEST 3: Email Backend Check")
print("=" * 60)

try:
    from lxfpro.email_backend import DualEmailBackend
    print("✅ DualEmailBackend module found")
    
    backend = DualEmailBackend()
    print("✅ DualEmailBackend initialized successfully")
    
except ImportError as e:
    print(f"❌ Cannot import DualEmailBackend: {e}")
except Exception as e:
    print(f"❌ Backend initialization failed: {e}")

# Summary
print("\n" + "=" * 60)
print("📊 TEST SUMMARY")
print("=" * 60)
print("\nIf all tests passed:")
print("✅ Email configuration is correct")
print("✅ OTP emails should be sent successfully")
print("\nIf tests failed:")
print("❌ Check Gmail App Password")
print("❌ Make sure 2-Factor Authentication is enabled on Gmail")
print("❌ Generate a new App Password from Google Account settings")
print("❌ Update EMAIL_HOST_PASSWORD in settings.py")

print("\n" + "=" * 60)
print("💡 TROUBLESHOOTING TIPS")
print("=" * 60)
print("""
1. Gmail App Password Issues:
   - Go to: https://myaccount.google.com/apppasswords
   - Enable 2-Factor Authentication first
   - Create new App Password for 'Mail'
   - Copy the 16-character password (remove spaces)
   - Update settings.py with new password

2. SMTP Connection Issues:
   - Check firewall settings
   - Verify port 587 is not blocked
   - Try port 465 with EMAIL_USE_SSL = True

3. Email Not Receiving:
   - Check spam folder
   - Verify recipient email is correct
   - Check Gmail sending limits (500/day)
   - Try different email provider (not Gmail)

4. DualEmailBackend Issues:
   - Check if lxfpro/email_backend.py exists
   - Switch to: EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   - Or console: EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
""")

print("=" * 60)
print("✅ Test completed!")
print("=" * 60)
