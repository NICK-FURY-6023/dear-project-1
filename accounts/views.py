from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from found_app.models import FoundItem

def home(request):
    # Get 3 most recent found items
    recent_items = FoundItem.objects.all().order_by('-date_found')[:3]
    return render(request,'home.html', {'recent_items': recent_items})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Send email to admin
        email_body = f"""
New Contact Form Submission

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""
        try:
            send_mail(
                f"Contact Form: {subject}",
                email_body,
                settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@lostandfound.com',
                ['lostandfound.vpmrzshah@gmail.com'],
                fail_silently=False
            )
            messages.success(request, "✅ Thank you! Your message has been sent successfully.")
        except Exception as e:
            messages.error(request, f"❌ Failed to send message. Please try again.")
        
        return redirect('contact')
    
    return render(request, 'contact.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Attempting login for: {username}")

        # Check if the user exists
        user = User.objects.filter(username=username).first()
        
        if user:
            if not user.is_active:
                messages.error(request, "Please verify your email before logging in.")
                return redirect('login')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            
            if user:
                login(request, user)
                print(f"Logged in user: {user}")
                return redirect('home')  
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        else:
            messages.error(request, "User not registered. Please register first.")
        
        return redirect('login')

    return render(request, 'login.html')


from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import uuid
import random
from django.utils import timezone
from .models import Profile

# Registration View
def register_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if the email is already used
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email address is already associated with an account.")
            return redirect('register')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        # Create user but set as inactive (until OTP verification)
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False  # Deactivate user until verification
        user.save()

        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))

        # Create Profile and store the OTP with timestamp
        Profile.objects.create(user=user, otp=otp, otp_created_at=timezone.now())

        # Email with OTP
        email_subject = "Your Verification OTP - Lost & Found Portal"
        email_body = f"""
Hello {username},

Thank you for registering with Lost & Found Portal!

Your verification OTP is: {otp}

This OTP is valid for 10 minutes only.

Please enter this OTP on the verification page to activate your account.

If you didn't register for this account, please ignore this email.

Best regards,
Lost & Found Portal Team
"""

        # Try to send email with detailed error handling
        email_sent = False
        error_message = ""
        
        try:
            print("=" * 50)
            print(f"🔧 Attempting to send OTP email...")
            print(f"📧 To: {email}")
            print(f"🔑 OTP: {otp}")
            print(f"📨 From: {settings.EMAIL_HOST_USER}")
            print(f"🌐 SMTP: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
            print("=" * 50)
            
            result = send_mail(
                email_subject, 
                email_body, 
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
            
            if result > 0:
                email_sent = True
                print(f"✅ Email sent successfully! Result: {result}")
            else:
                print(f"⚠️ send_mail returned {result}")
                
        except Exception as e:
            error_message = str(e)
            print(f"❌ Email sending failed!")
            print(f"❌ Error type: {type(e).__name__}")
            print(f"❌ Error message: {error_message}")
            import traceback
            traceback.print_exc()
        
        # Show appropriate message based on email status
        if email_sent:
            print(f"\n{'='*50}")
            print(f"✅ SUCCESS: OTP sent to {email}")
            print(f"🔑 OTP for testing: {otp}")
            print(f"{'='*50}\n")
            messages.success(request, f"✅ OTP sent to your email! Please check your inbox. (OTP: {otp})")
        else:
            # Even if email fails, show OTP in console for development
            print(f"\n{'='*50}")
            print(f"⚠️ EMAIL FAILED but here's your OTP for testing:")
            print(f"🔑 OTP: {otp}")
            print(f"👤 Username: {username}")
            print(f"{'='*50}\n")
            messages.warning(request, f"⚠️ Email delivery issue. For testing, your OTP is: {otp}")
        
        # Always redirect to OTP verification page
        return redirect('verify_otp', username=username)

    return render(request, 'register.html')


# OTP Verification View
def verify_otp(request, username):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        
        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            
            # Check if user is already verified
            if user.is_active:
                messages.info(request, "Your account is already verified. You can log in.")
                return redirect('login')
            
            # Check if OTP is valid (not expired)
            if not profile.is_otp_valid():
                messages.error(request, "❌ OTP has expired. Please register again.")
                user.delete()  # Delete user if OTP expired
                return redirect('register')
            
            # Verify OTP
            if profile.otp == otp_entered:
                user.is_active = True
                user.save()
                
                # Clear OTP after successful verification
                profile.otp = None
                profile.otp_created_at = None
                profile.save()
                
                messages.success(request, "✅ Account verified successfully! You can now log in.")
                return redirect('login')
            else:
                messages.error(request, "❌ Invalid OTP. Please try again.")
                return redirect('verify_otp', username=username)
                
        except User.DoesNotExist:
            messages.error(request, "❌ User not found.")
            return redirect('register')
        except Profile.DoesNotExist:
            messages.error(request, "❌ Profile not found.")
            return redirect('register')
    
    # GET request - show OTP input form
    return render(request, 'verify_otp.html', {'username': username})


# Old token-based verification (kept for backward compatibility)
def verify_email(request, token):
    try:
        profile = Profile.objects.get(verification_token=token)
        user = profile.user

        if user.is_active:
            messages.info(request, "Your email is already verified. You can log in.")
            return redirect('login')

        user.is_active = True
        user.save()

        # Remove the token after verification
        profile.verification_token = None
        profile.save()

        messages.success(request, "✅ Your email has been verified successfully! You can now log in.")
        return redirect('login')

    except Profile.DoesNotExist:
        messages.error(request, "❌ Invalid or expired verification link.")
        return redirect('register')


from django.contrib.auth import logout


def logout_page(request):
    logout(request)
    messages.success(request, "Logout successful. You have been logged out.")
    return redirect('login')