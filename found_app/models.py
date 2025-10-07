from django.db import models
from django.contrib.auth.models import User

class FoundItem(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('documents', 'Documents'),
        ('clothing', 'Clothing'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model
    item_name = models.CharField(max_length=255)  # Name of the lost item
    description = models.TextField()  # Description of the item
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,  # Predefined choices for category
        default='other',  # Default category
    )
    date_found = models.DateField()  # Date when the item was lost
    location = models.CharField(max_length=255)  # Where the item was lost
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)  # Optional image field
    is_claimed = models.BooleanField(default=False)  # Track if item is claimed
    claimed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='claimed_items')  # Who claimed it

    def __str__(self):
        return f"{self.item_name} reported by {self.user.username}"

    class Meta:
        db_table="Found_item"


class ClaimRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    item = models.ForeignKey(FoundItem, on_delete=models.CASCADE, related_name='claim_requests')
    claimant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_claims')
    reason = models.TextField()  # Why they think it's their item
    contact_info = models.CharField(max_length=255)  # Phone or additional contact
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ticket_number = models.CharField(max_length=20, unique=True, null=True, blank=True)  # Unique ticket ID
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Claim #{self.ticket_number or self.id} by {self.claimant.username} for {self.item.item_name}"
    
    def save(self, *args, **kwargs):
        # Generate ticket number if not exists
        if not self.ticket_number:
            import random
            import string
            # Format: CLM-YYYYMMDD-XXXX (CLM-20251007-A3B9)
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            self.ticket_number = f"CLM-{date_str}-{random_str}"
        super().save(*args, **kwargs)


class ChatMessage(models.Model):
    item = models.ForeignKey(FoundItem, on_delete=models.CASCADE, related_name="chat_messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.item.user.username} at {self.timestamp}"
