#!/usr/bin/env python
"""
Pre-Demo Checklist - Verify everything is ready for college presentation
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lxfpro.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile
from django.conf import settings

print("\n" + "="*70)
print("🎓 COLLEGE DEMO - PRE-CHECK VERIFICATION")
print("="*70 + "\n")

# Check 1: User Status
print("1️⃣  Checking User Accounts...")
users = User.objects.all()
active_users = users.filter(is_active=True)
inactive_users = users.filter(is_active=False)

print(f"   📊 Total Users: {users.count()}")
print(f"   ✅ Active Users: {active_users.count()}")
print(f"   ⏳ Inactive Users: {inactive_users.count()}")

if inactive_users.exists():
    print(f"\n   ⚠️  WARNING: {inactive_users.count()} users are still inactive!")
    print(f"   Run: python activate_all_users.py")
else:
    print(f"   ✅ All users are active and ready!")

# Check 2: Profile Status
print(f"\n2️⃣  Checking Verification Status...")
profiles = Profile.objects.all()
pending_profiles = profiles.filter(verification_token__isnull=False)

if pending_profiles.exists():
    print(f"   ⚠️  {pending_profiles.count()} users have pending verifications")
    for p in pending_profiles:
        print(f"      - {p.user.username}")
else:
    print(f"   ✅ All verifications complete!")

# Check 3: Settings
print(f"\n3️⃣  Checking Configuration...")
print(f"   📧 Email Backend: {settings.EMAIL_BACKEND}")
print(f"   🌐 Base URL: {settings.BASE_URL}")
print(f"   🐛 Debug Mode: {settings.DEBUG}")
print(f"   🔒 Secret Key: {'Set ✅' if settings.SECRET_KEY else 'Missing ❌'}")

if 'console' in settings.EMAIL_BACKEND:
    print(f"   ✅ Console email backend - Perfect for demo!")
else:
    print(f"   ℹ️  SMTP email backend - Make sure credentials are correct")

# Check 4: Database
print(f"\n4️⃣  Checking Database...")
from found_app.models import FoundItem
items = FoundItem.objects.all()
print(f"   📦 Found Items: {items.count()}")

# Check 5: Static Files
print(f"\n5️⃣  Checking Static Files...")
static_files = [
    ('static/js/script.js', 'JavaScript'),
    ('static/images/wallet.svg', 'Wallet Icon'),
    ('static/images/bag.svg', 'Bag Icon'),
    ('static/images/idcard.svg', 'ID Card Icon'),
    ('static/images/no-image.svg', 'No Image Placeholder'),
]

for filepath, name in static_files:
    full_path = os.path.join(settings.BASE_DIR, filepath)
    if os.path.exists(full_path):
        print(f"   ✅ {name}")
    else:
        print(f"   ❌ {name} - MISSING!")

# Check 6: Important URLs
print(f"\n6️⃣  Important URLs for Demo...")
base_url = settings.BASE_URL
print(f"   🏠 Home: {base_url}/")
print(f"   🔐 Login: {base_url}/login/")
print(f"   📝 Register: {base_url}/register/")
print(f"   👨‍💼 Admin: {base_url}/admin/")
print(f"   📦 View Items: {base_url}/view-found/")
print(f"   ➕ Report Item: {base_url}/report-found/")

# Final Status
print("\n" + "="*70)

all_active = not inactive_users.exists()
no_pending = not pending_profiles.exists()

if all_active and no_pending:
    print("✅ DEMO READY STATUS: PERFECT! 🎉")
    print()
    print("Your project is 100% ready for the college demo!")
    print()
    print("Next steps:")
    print("1. Start server: python manage.py runserver")
    print("2. Open browser: http://127.0.0.1:8000")
    print("3. Login with any user and demonstrate features")
    print("4. Show registration flow with console verification")
else:
    print("⚠️  DEMO READY STATUS: NEEDS ATTENTION")
    print()
    if inactive_users.exists():
        print(f"❌ Fix inactive users: python activate_all_users.py")
    if pending_profiles.exists():
        print(f"❌ Clear pending verifications: python activate_all_users.py")

print("\n" + "="*70 + "\n")

# User List
print("📋 USER LIST FOR DEMO:")
print("-" * 70)
for user in users:
    status = "✅" if user.is_active else "❌"
    print(f"{status} {user.username:<20} {user.email:<35} {'Active' if user.is_active else 'Inactive'}")

print("\n" + "="*70)
print("Good luck with your presentation! 🎓✨")
print("="*70 + "\n")
