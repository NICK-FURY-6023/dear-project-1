#!/usr/bin/env python
"""
Show verification links for all pending users
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lxfpro.settings')
django.setup()

from django.conf import settings
from accounts.models import Profile

print("\n" + "="*70)
print("📧 VERIFICATION LINKS FOR PENDING USERS")
print("="*70 + "\n")

pending_profiles = Profile.objects.filter(
    user__is_active=False, 
    verification_token__isnull=False
)

if not pending_profiles.exists():
    print("✅ No pending verifications found!\n")
else:
    print(f"Found {pending_profiles.count()} users waiting for verification:\n")
    
    for i, profile in enumerate(pending_profiles, 1):
        user = profile.user
        verification_link = f"{settings.BASE_URL}/verify/{profile.verification_token}/"
        
        print(f"{i}. User: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Verification Link:")
        print(f"   {verification_link}")
        print(f"   Token: {profile.verification_token}")
        print()

print("="*70)
print("\n💡 Instructions:")
print("   1. Copy any verification link above")
print("   2. Paste it in your browser")
print("   3. The user will be activated automatically")
print("\n" + "="*70 + "\n")
