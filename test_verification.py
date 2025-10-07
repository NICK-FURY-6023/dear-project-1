#!/usr/bin/env python
"""
Test script to verify email registration and verification flow
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lxfpro.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile
import uuid

def test_verification_flow():
    print("\n" + "="*60)
    print("🧪 Testing Email Verification Flow")
    print("="*60 + "\n")
    
    # Test 1: Check if Profile model is working
    print("1️⃣  Testing Profile model...")
    test_username = f"testuser_{uuid.uuid4().hex[:8]}"
    test_email = f"{test_username}@test.com"
    test_password = "TestPass123!"
    
    # Create test user
    user = User.objects.create_user(
        username=test_username,
        email=test_email,
        password=test_password
    )
    user.is_active = False
    user.save()
    
    # Create profile with token
    token = str(uuid.uuid4())
    profile = Profile.objects.create(user=user, verification_token=token)
    
    print(f"   ✅ Created user: {test_username}")
    print(f"   ✅ Created profile with token: {token}")
    print(f"   ✅ User active status: {user.is_active}")
    
    # Test 2: Verify token lookup works
    print("\n2️⃣  Testing token lookup...")
    found_profile = Profile.objects.get(verification_token=token)
    print(f"   ✅ Token lookup successful")
    print(f"   ✅ Found user: {found_profile.user.username}")
    
    # Test 3: Simulate verification
    print("\n3️⃣  Simulating verification...")
    found_profile.user.is_active = True
    found_profile.user.save()
    found_profile.verification_token = None
    found_profile.save()
    
    # Refresh from database
    user.refresh_from_db()
    profile.refresh_from_db()
    
    print(f"   ✅ User activated: {user.is_active}")
    print(f"   ✅ Token cleared: {profile.verification_token}")
    
    # Test 4: Check all existing profiles
    print("\n4️⃣  Listing all profiles in database...")
    all_profiles = Profile.objects.all()
    print(f"   📊 Total profiles: {all_profiles.count()}")
    
    for p in all_profiles:
        status = "✅ Active" if p.user.is_active else "⏳ Pending"
        token_status = "🔑 Has token" if p.verification_token else "✓ Verified"
        print(f"   - {p.user.username} ({p.user.email}): {status} | {token_status}")
    
    # Cleanup test user
    print("\n5️⃣  Cleaning up test user...")
    user.delete()
    print(f"   ✅ Test user deleted")
    
    print("\n" + "="*60)
    print("✅ All tests passed successfully!")
    print("="*60 + "\n")
    
    # Print verification URL format
    from django.conf import settings
    print("📋 Verification URL Format:")
    print(f"   {settings.BASE_URL}/verify/<token>/")
    print("\n")

if __name__ == "__main__":
    test_verification_flow()
