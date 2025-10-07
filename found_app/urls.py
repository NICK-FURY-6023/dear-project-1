from django.urls import path
from . import views as v  # Import views with alias 'v'
from django.conf import settings
from django.conf.urls.static import static

# Define URL patterns
urlpatterns = [
    path('report-found/', v.report_found_item, name='report_found'),
    path('view-found/', v.view_found, name='view_found'),
    path('item/<int:item_id>/', v.item_detail, name='item_detail'),
    path('claim/<int:item_id>/', v.claim_item, name='claim_item'),
    path('my-claims/', v.my_claims, name='my_claims'),
    path('claim-requests/', v.claim_requests_received, name='claim_requests_received'),
    path('chat/<str:username>/', v.chat_with_user, name='chat_with_user'),
    path('api/chat-messages/<str:username>/', v.get_chat_messages, name='get_chat_messages'),
    path('chat_room/', v.chat_room, name='chat_room'),


]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)