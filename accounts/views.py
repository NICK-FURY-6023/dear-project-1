from django.shortcuts import render

def home(request):
    return render(request,'home.html')


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
from .models import Profile

# Registration View
def register_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Allow only emails ending with @vpmrzshah@gmail.com
        if not email.endswith('vpmrzshah@gmail.com'):
            messages.error(request, "Only emails provided by college are allowed.")
            return redirect('register')
        
           # Validate email format
        email_validator = EmailValidator()
        try:
            email_validator(email)  # This will raise a ValidationError if email is invalid
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return redirect('register')

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

        # Create user but set as inactive (until email verification)
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False  # Deactivate user until verification
        user.save()

        # Generate a verification token
        token = str(uuid.uuid4())

        # Create Profile and store the token
        Profile.objects.create(user=user, verification_token=token)

        # Email verification link
        verification_link = f"{settings.BASE_URL}/verify/{token}/"
        email_body = f"Hello {username},\n\nClick here to verify your email: {verification_link}"

        try:
            send_mail("Verify Your Email", email_body, settings.EMAIL_HOST_USER, [email])
            messages.success(request, "✅ Verification email sent! Please check your inbox.")
        except Exception as e:
            messages.error(request, f"❌ Failed to send email. Error: {str(e)}")

        return redirect('register')  # Redirect to show message properly

    return render(request, 'register.html')


# Email Verification View
def verify_email(request, token):
    try:
        profile = Profile.objects.get(verification_token=token)
        user = profile.user

        if user.is_active:
            messages.info(request, "Your email is already verified. You can log in.")
            return redirect('login')  # Redirect to login if already verified

        user.is_active = True  # Activate user account
        user.save()

        # Remove the token after verification
        profile.verification_token = None
        profile.save()

        messages.success(request, "✅ Your email has been verified successfully! You can now log in.")
        return redirect('login')  # Redirect to login after verification

    except Profile.DoesNotExist:
        messages.error(request, "❌ Invalid or expired verification link.")
        return redirect('register')  # Redirect to register if the token is invalid

from django.contrib.auth import logout


def logout_page(request):
    logout(request)
    messages.success(request, "Logout successful. You have been logged out.")
    return redirect('login')  # Redirect to login page