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

    def __str__(self):
        return f"{self.item_name} reported by {self.user.username}"

    class Meta:
        db_table="Found_item"


from django.db import models
from django.contrib.auth.models import User
from .models import FoundItem

class ChatMessage(models.Model):
    item = models.ForeignKey(FoundItem, on_delete=models.CASCADE, related_name="chat_messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.item.user.username} at {self.timestamp}"
