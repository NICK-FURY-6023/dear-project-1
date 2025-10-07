from django.contrib import admin
from .models import Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'verification_token']
    search_fields = ['user__username', 'user__email', 'verification_token']
    list_filter = ['user__is_active']
