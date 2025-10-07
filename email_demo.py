#!/usr/bin/env python
"""
Email Mode Switcher - Console, SMTP, ya DUAL mode ke beech switch karo
"""
import os
import sys

def read_settings():
    with open('lxfpro/settings.py', 'r') as f:
        return f.read()

def write_settings(content):
    with open('lxfpro/settings.py', 'w') as f:
        f.write(content)

def switch_to_dual():
    """DUAL mode - Email bhi bheje AUR console mein bhi print kare (BEST!)"""
    settings = read_settings()
    
    # Find email settings section
    import re
    
    # Replace entire email settings section
    email_section = """# Email settings
# DUAL MODE - Sends emails via Gmail AND prints to console (Best for demo!)
EMAIL_BACKEND = 'lxfpro.email_backend.DualEmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'lostandfound.vpmrzshah@gmail.com'
EMAIL_HOST_PASSWORD = 'olcn hlep cryq bvag'  # Gmail App Password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Other options (agar zaroorat ho to switch kar sakte ho):
# Console Only - EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# SMTP Only - EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'"""
    
    # Replace the email settings section
    pattern = r'# Email settings.*?(?=\n\n# |\n# Password validation)'
    settings = re.sub(pattern, email_section, settings, flags=re.DOTALL)
    
    write_settings(settings)
    print("\n" + "="*70)
    print("✅ DUAL Mode Activated!")
    print("="*70)
    print("\n📧 Email Settings:")
    print("   Mode: DUAL (Email + Console)")
    print("   ✅ Sends real emails via Gmail")
    print("   ✅ Also prints to console/terminal")
    print("\n💡 Benefits:")
    print("   - Users ko email milega")
    print("   - Terminal mein bhi link dikhega")
    print("   - Best of both worlds!")
    print("\n⚠️  Server restart required:")
    print("   pkill -f runserver")
    print("   python manage.py runserver")
    print("\n" + "="*70 + "\n")

def switch_to_smtp():
    """Console se SMTP mode mein switch karo"""
    settings = read_settings()
    
    # Console backend comment karo
    settings = settings.replace(
        "EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'",
        "# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'"
    )
    
    # SMTP backend uncomment karo
    settings = settings.replace(
        "# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'",
        "EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'"
    )
    settings = settings.replace(
        "# EMAIL_HOST = 'smtp.gmail.com'",
        "EMAIL_HOST = 'smtp.gmail.com'"
    )
    settings = settings.replace(
        "# EMAIL_PORT = 587",
        "EMAIL_PORT = 587"
    )
    settings = settings.replace(
        "# EMAIL_USE_TLS = True",
        "EMAIL_USE_TLS = True"
    )
    settings = settings.replace(
        "# EMAIL_HOST_USER = 'lostandfound.vpmrzshah@gmail.com'",
        "EMAIL_HOST_USER = 'lostandfound.vpmrzshah@gmail.com'"
    )
    settings = settings.replace(
        "# EMAIL_HOST_PASSWORD = 'olcn hlep cryq bvag'",
        "EMAIL_HOST_PASSWORD = 'olcn hlep cryq bvag'"
    )
    settings = settings.replace(
        "# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER",
        "DEFAULT_FROM_EMAIL = EMAIL_HOST_USER"
    )
    
    write_settings(settings)
    print("\n" + "="*70)
    print("✅ SMTP Mode Activated!")
    print("="*70)
    print("\n📧 Email Settings:")
    print("   Mode: SMTP (Real emails via Gmail)")
    print("   Host: smtp.gmail.com")
    print("   From: lostandfound.vpmrzshah@gmail.com")
    print("\n⚠️  IMPORTANT:")
    print("   - Gmail App Password already configured")
    print("   - Real emails will be sent now")
    print("   - Server restart required")
    print("\n🔄 Server restart karo:")
    print("   pkill -f runserver")
    print("   python manage.py runserver")
    print("\n" + "="*70 + "\n")

def switch_to_console():
    """SMTP se Console mode mein switch karo"""
    settings = read_settings()
    
    # SMTP backend comment karo
    settings = settings.replace(
        "EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'",
        "# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'"
    )
    settings = settings.replace(
        "EMAIL_HOST = 'smtp.gmail.com'",
        "# EMAIL_HOST = 'smtp.gmail.com'"
    )
    settings = settings.replace(
        "EMAIL_PORT = 587",
        "# EMAIL_PORT = 587"
    )
    settings = settings.replace(
        "EMAIL_USE_TLS = True",
        "# EMAIL_USE_TLS = True"
    )
    settings = settings.replace(
        "EMAIL_HOST_USER = 'lostandfound.vpmrzshah@gmail.com'",
        "# EMAIL_HOST_USER = 'lostandfound.vpmrzshah@gmail.com'"
    )
    settings = settings.replace(
        "EMAIL_HOST_PASSWORD = 'olcn hlep cryq bvag'",
        "# EMAIL_HOST_PASSWORD = 'olcn hlep cryq bvag'"
    )
    settings = settings.replace(
        "DEFAULT_FROM_EMAIL = EMAIL_HOST_USER",
        "# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER"
    )
    
    # Console backend uncomment karo
    settings = settings.replace(
        "# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'",
        "EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'"
    )
    
    write_settings(settings)
    print("\n" + "="*70)
    print("✅ Console Mode Activated!")
    print("="*70)
    print("\n📧 Email Settings:")
    print("   Mode: Console (Prints to terminal)")
    print("   Output: Terminal/Console")
    print("\n💡 Benefits:")
    print("   - No email server needed")
    print("   - Perfect for development/demo")
    print("   - Verification links visible in terminal")
    print("\n🔄 Server restart karo:")
    print("   pkill -f runserver")
    print("   python manage.py runserver")
    print("\n" + "="*70 + "\n")

def show_current_mode():
    """Current email mode dikhaao"""
    settings = read_settings()
    
    print("\n" + "="*70)
    print("📧 CURRENT EMAIL CONFIGURATION")
    print("="*70 + "\n")
    
    if "EMAIL_BACKEND = 'lxfpro.email_backend.DualEmailBackend'" in settings:
        print("✅ Current Mode: DUAL (Email + Console)")
        print("\n📋 What this means:")
        print("   - Real emails sent via Gmail ✅")
        print("   - Also prints to console ✅")
        print("   - Best of both worlds!")
        print("\n💡 Other options:")
        print("   python email_demo.py console  # Console only")
        print("   python email_demo.py smtp     # SMTP only")
    elif "EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'" in settings:
        print("✅ Current Mode: CONSOLE")
        print("\n📋 What this means:")
        print("   - Emails print in terminal (not sent)")
        print("   - Verification links visible in console")
        print("   - Perfect for development/demo")
        print("\n💡 To send real emails:")
        print("   python email_demo.py dual     # Email + Console (Best!)")
        print("   python email_demo.py smtp     # SMTP only")
    else:
        print("✅ Current Mode: SMTP (Gmail)")
        print("\n📋 What this means:")
        print("   - Real emails sent via Gmail")
        print("   - Users receive actual emails")
        print("   - Perfect for production")
        print("\n💡 Other options:")
        print("   python email_demo.py dual     # Email + Console (Best!)")
        print("   python email_demo.py console  # Console only")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n📧 Email Mode Switcher - Usage:\n")
        print("   python email_demo.py dual      # DUAL mode (Email + Console) ⭐ BEST!")
        print("   python email_demo.py console   # Console only (demo ke liye)")
        print("   python email_demo.py smtp      # SMTP only (real emails)")
        print("   python email_demo.py status    # Current mode dekho")
        print()
        show_current_mode()
    elif sys.argv[1] == 'dual':
        switch_to_dual()
    elif sys.argv[1] == 'console':
        switch_to_console()
    elif sys.argv[1] == 'smtp':
        switch_to_smtp()
    elif sys.argv[1] == 'status':
        show_current_mode()
    else:
        print("\n❌ Invalid option. Use: dual, console, smtp, or status\n")
