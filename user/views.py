from django.shortcuts import render


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from found_app.models import FoundItem


@login_required
def my_found_items(request):
    found_items = FoundItem.objects.filter(user=request.user).order_by("-date_found")
    return render(request, "my_found_items.html", {"found_items": found_items})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from found_app.models import FoundItem

@require_POST  # Ensures only POST requests are allowed
@csrf_protect  # Ensure CSRF protection for this view
def delete_found_item(request, item_id):
    # Retrieve the item and ensure it's associated with the logged-in user
    item = get_object_or_404(FoundItem, id=item_id, user=request.user)
    item.delete()  # Delete the found item
    return JsonResponse({"success": True})  # Send success response

