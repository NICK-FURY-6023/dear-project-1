#!/usr/bin/env python
"""
Manually activate all pending users (bypassing email verification)
Use this ONLY for testing/development or emergency situations
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lxfpro.settings')
django.setup()

from accounts.models import Profile

print("\n" + "="*70)
print("🔓 MANUAL USER ACTIVATION SCRIPT")
print("="*70 + "\n")

pending_profiles = Profile.objects.filter(
    user__is_active=False, 
    verification_token__isnull=False
)

if not pending_profiles.exists():
    print("✅ No pending verifications found!\n")
else:
    print(f"⚠️  Found {pending_profiles.count()} users waiting for verification\n")
    
    for i, profile in enumerate(pending_profiles, 1):
        user = profile.user
        print(f"{i}. Activating: {user.username} ({user.email})")
        
        # Activate user
        user.is_active = True
        user.save()
        
        # Clear token
        profile.verification_token = None
        profile.save()
        
        print(f"   ✅ Activated successfully!")

print("\n" + "="*70)
print("✅ All pending users have been activated!")
print("="*70 + "\n")
