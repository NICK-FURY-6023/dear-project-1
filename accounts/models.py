from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_token = models.CharField(max_length=100, unique=True, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)  # 6-digit OTP
    otp_created_at = models.DateTimeField(null=True, blank=True)  # OTP creation time
    
    def is_otp_valid(self):
        """Check if OTP is still valid (10 minutes expiry)"""
        if self.otp_created_at:
            return timezone.now() < self.otp_created_at + timedelta(minutes=10)
        return False

