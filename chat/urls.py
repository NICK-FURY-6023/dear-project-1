from django.urls import path, include
from chat.views import ThreadView
from chat.api_views import (
    get_unread_count, 
    mark_thread_as_read, 
    get_recent_conversations,
    check_new_messages
)

urlpatterns = [
    path('chat/<str:username>/', ThreadView.as_view(), name='chat_thread'),
    
    # API endpoints for notifications
    path('api/unread-count/', get_unread_count, name='api_unread_count'),
    path('api/mark-read/<str:thread_id>/', mark_thread_as_read, name='api_mark_read'),
    path('api/conversations/', get_recent_conversations, name='api_conversations'),
    path('api/check-messages/', check_new_messages, name='api_check_messages'),
]
