from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FoundItem

@login_required
def report_found_item(request):
    """
    View to handle the form submission for reporting a found item.
    """
    if request.method == 'POST':
        # Retrieve form data
        item_name = request.POST.get('item_name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        date_found = request.POST.get('date_found')  # Corrected field name here
        location = request.POST.get('location')
        image = request.FILES.get('image')

        # Validation: Ensure required fields are not empty
        if not item_name or not description or not category or not date_found or not location:
            messages.error(request, "Please fill all required fields!")
            return render(request, 'report_found.html')

        try:
            # Create a new FoundItem object
            found_item = FoundItem(
                user=request.user,  # Assign the current logged-in user
                item_name=item_name,
                description=description,
                category=category,
                date_found=date_found,  # Ensure the correct field is used here
                location=location,
                image=image,
            )

            # Save the item to the database
            found_item.save()

            # Show a success message
            messages.success(request, "Your found item has been reported successfully!")
            return redirect('home')

        except Exception as e:
            # Handle errors (e.g., database save issues)
            print("Error saving item:", e)
            messages.error(request, "An error occurred while saving the found item.")

    return render(request, 'report_found.html')






from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import FoundItem, ChatMessage, ClaimRequest

def view_found(request):
    items = FoundItem.objects.all().order_by('-date_found')
    return render(request, 'view_found.html', {'items': items})


@login_required
def item_detail(request, item_id):
    """Show detailed view of an item"""
    item = get_object_or_404(FoundItem, id=item_id)
    return render(request, 'item_detail.html', {'item': item})


@login_required
def chat_with_user(request, username):
    """Chat page with specific user"""
    chat_user = get_object_or_404(User, username=username)
    return render(request, 'chat_page.html', {'chat_user': chat_user})


@login_required
def claim_item(request, item_id):
    """Handle claim request for an item"""
    item = get_object_or_404(FoundItem, id=item_id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        contact_info = request.POST.get('contact_info')
        
        # Check if user already claimed this item
        existing_claim = ClaimRequest.objects.filter(item=item, claimant=request.user).first()
        if existing_claim:
            messages.warning(request, "You have already submitted a claim for this item!")
            return redirect('view_found')
        
        # Create claim request
        claim = ClaimRequest.objects.create(
            item=item,
            claimant=request.user,
            reason=reason,
            contact_info=contact_info
        )
        
        # Send email to item reporter
        email_subject = f"Claim Request for {item.item_name}"
        email_body = f"""
Hello {item.user.username},

Someone has submitted a claim request for the item you reported: {item.item_name}

Claimant Details:
- Name: {request.user.username}
- Email: {request.user.email}
- Contact: {contact_info}

Reason for Claim:
{reason}

Please log in to your account to review this claim request and chat with the claimant.

Best regards,
Lost & Found Portal Team
"""
        
        try:
            send_mail(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@lostandfound.com',
                [item.user.email],
                fail_silently=False
            )
            print(f"✅ Claim notification sent to {item.user.email}")
        except Exception as e:
            print(f"❌ Email failed: {str(e)}")
        
        messages.success(request, f"✅ Your claim request has been submitted! The item owner will be notified.")
        return redirect('view_found')
    
    return render(request, 'claim_item.html', {'item': item})


# views.py
from django.shortcuts import render
from .models import ChatMessage

def chat_room(request, room_name):
    # Get all messages for the given room
    chat_messages = ChatMessage.objects.filter(room__room_name=room_name).order_by('timestamp')
    return render(request, 'chat_room.html', {'chat_messages': chat_messages, 'room_name': room_name})






