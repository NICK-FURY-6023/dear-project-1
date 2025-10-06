from django.urls import path
from .import views as v

urlpatterns =[
    path('', v.home, name='home'), 
    path('login/', v.login_page, name='login'),  # Login page
    path('register/',v.register_page, name='register'),
    path('verify/<str:token>/',v.verify_email, name='verify_email'),
    path('logout/', v.logout_page, name='logout'),
]