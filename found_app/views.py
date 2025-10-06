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



from django.shortcuts import render
from .models import FoundItem,ChatMessage

def view_found(request):
    items = FoundItem.objects.all().order_by('-date_found')
    return render(request, 'view_found.html', {'items': items})


# views.py
from django.shortcuts import render
from .models import ChatMessage

def chat_room(request, room_name):
    # Get all messages for the given room
    chat_messages = ChatMessage.objects.filter(room__room_name=room_name).order_by('timestamp')
    return render(request, 'chat_room.html', {'chat_messages': chat_messages, 'room_name': room_name})



