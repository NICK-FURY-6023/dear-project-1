from django.urls import path
from . import views as v  # Import views with alias 'v'
from django.conf import settings
from django.conf.urls.static import static

# Define URL patterns
urlpatterns = [
    path('report-found/', v.report_found_item, name='report_found'),
    path('view-found/', v.view_found, name='view_found'),
    path('chat_room/', v.chat_room, name='chat_room'),


]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
