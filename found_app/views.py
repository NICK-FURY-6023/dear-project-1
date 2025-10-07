from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FoundItem
from django.http import JsonResponse
from chat.models import Thread, Message
from django.contrib.auth.models import User

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
def my_claims(request):
    """View user's claim requests (tickets)"""
    claims = ClaimRequest.objects.filter(claimant=request.user).order_by('-created_at')
    return render(request, 'my_claims.html', {'claims': claims})


@login_required
def claim_requests_received(request):
    """View claim requests for items user has reported"""
    my_items = FoundItem.objects.filter(user=request.user)
    claims = ClaimRequest.objects.filter(item__in=my_items).order_by('-created_at')
    return render(request, 'claim_requests_received.html', {'claims': claims})


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
def get_chat_messages(request, username):
    """API endpoint to get previous chat messages"""
    try:
        other_user = User.objects.get(username=username)
        thread = Thread.objects.get_or_create_personal_thread(request.user, other_user)
        
        messages_list = Message.objects.filter(thread=thread).order_by('created_at')
        
        messages_data = [{
            'text': msg.text,
            'username': msg.sender.username,
            'timestamp': msg.created_at.strftime('%H:%M')
        } for msg in messages_list]
        
        return JsonResponse({'messages': messages_data})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def claim_item(request, item_id):
    """Handle claim request for an item"""
    item = get_object_or_404(FoundItem, id=item_id)
    
    # Check if item belongs to current user
    if item.user == request.user:
        messages.error(request, "❌ You cannot claim your own item!")
        return redirect('view_found')
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        contact_info = request.POST.get('contact_info')
        
        # Check if user already claimed this item
        existing_claim = ClaimRequest.objects.filter(item=item, claimant=request.user).first()
        if existing_claim:
            messages.warning(request, f"⚠️ You already submitted a claim! Ticket #: {existing_claim.ticket_number}")
            return redirect('view_found')
        
        # Create claim request (ticket number auto-generated in model)
        claim = ClaimRequest.objects.create(
            item=item,
            claimant=request.user,
            reason=reason,
            contact_info=contact_info
        )
        
        # Email to claimant (person who made the claim)
        claimant_subject = f"Claim Request Submitted - Ticket #{claim.ticket_number}"
        claimant_body = f"""
Hello {request.user.username},

Your claim request has been successfully submitted!

🎫 Ticket Number: {claim.ticket_number}
📦 Item: {item.item_name}
📅 Submitted: {claim.created_at.strftime('%B %d, %Y at %I:%M %p')}
📍 Location Found: {item.location}
📝 Status: Pending Review

Item Details:
- Category: {item.get_category_display()}
- Description: {item.description}
- Found By: {item.user.username}

Your Claim Details:
- Reason: {reason}
- Contact: {contact_info}

What Happens Next?
1. The person who found the item ({item.user.username}) will be notified
2. They will review your claim request
3. You can chat with them to discuss item details
4. If approved, you can arrange to collect the item

Please save your ticket number for reference: {claim.ticket_number}

You can login to check the status of your claim or chat with the finder.

Best regards,
Lost & Found Portal Team
"""
        
        # Email to item reporter (person who found the item)
        reporter_subject = f"🔔 New Claim Request for {item.item_name} - Ticket #{claim.ticket_number}"
        reporter_body = f"""
Hello {item.user.username},

Someone has submitted a claim request for the item you reported!

🎫 Ticket Number: {claim.ticket_number}
📦 Item: {item.item_name}
📅 Claim Date: {claim.created_at.strftime('%B %d, %Y at %I:%M %p')}
👤 Claimant: {request.user.username}

Claimant Details:
- Email: {request.user.email}
- Contact: {contact_info}

Reason for Claim:
"{reason}"

Action Required:
1. Log in to your account: {settings.BASE_URL if hasattr(settings, 'BASE_URL') else 'http://localhost:8000'}
2. Review the claim request (Ticket #{claim.ticket_number})
3. Chat with {request.user.username} to verify ownership
4. Approve or reject the claim based on verification

Tips for Verification:
- Ask specific questions about the item
- Request description of unique features
- Verify through the chat system
- Check contact information

Please respond to this claim request at your earliest convenience.

Best regards,
Lost & Found Portal Team
"""
        
        # Send emails
        emails_sent = {'claimant': False, 'reporter': False}
        
        # Send to claimant
        try:
            result = send_mail(
                claimant_subject,
                claimant_body,
                settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@lostandfound.com',
                [request.user.email],
                fail_silently=False
            )
            if result > 0:
                emails_sent['claimant'] = True
                print(f"✅ Claim confirmation sent to {request.user.email}")
        except Exception as e:
            print(f"⚠️ Email to claimant failed: {str(e)}")
        
        # Send to reporter
        try:
            result = send_mail(
                reporter_subject,
                reporter_body,
                settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@lostandfound.com',
                [item.user.email],
                fail_silently=False
            )
            if result > 0:
                emails_sent['reporter'] = True
                print(f"✅ Claim notification sent to reporter {item.user.email}")
        except Exception as e:
            print(f"⚠️ Email to reporter failed: {str(e)}")
        
        # Show success message with ticket number
        print(f"\n{'='*60}")
        print(f"🎫 NEW CLAIM REQUEST CREATED!")
        print(f"{'='*60}")
        print(f"Ticket Number: {claim.ticket_number}")
        print(f"Item: {item.item_name}")
        print(f"Claimant: {request.user.username}")
        print(f"Reporter: {item.user.username}")
        print(f"Status: Pending")
        print(f"Emails Sent: Claimant={emails_sent['claimant']}, Reporter={emails_sent['reporter']}")
        print(f"{'='*60}\n")
        
        # Success message to user
        success_msg = f"""
        ✅ Claim request submitted successfully!<br>
        🎫 <strong>Your Ticket Number: {claim.ticket_number}</strong><br>
        📧 Confirmation email sent to your inbox.<br>
        👤 The item reporter ({item.user.username}) has been notified.<br>
        💬 You can now chat with them to verify ownership.
        """
        
        messages.success(request, success_msg)
        return redirect('view_found')
    
    return render(request, 'claim_item.html', {'item': item})


# views.py
from django.shortcuts import render
from .models import ChatMessage

def chat_room(request, room_name):
    # Get all messages for the given room
    chat_messages = ChatMessage.objects.filter(room__room_name=room_name).order_by('timestamp')
    return render(request, 'chat_room.html', {'chat_messages': chat_messages, 'room_name': room_name})






