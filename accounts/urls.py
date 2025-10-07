from django.urls import path
from .import views as v

urlpatterns =[
    path('', v.home, name='home'), 
    path('about/', v.about, name='about'),
    path('contact/', v.contact, name='contact'),
    path('login/', v.login_page, name='login'),  # Login page
    path('register/',v.register_page, name='register'),
    path('verify-otp/<str:username>/', v.verify_otp, name='verify_otp'),  # OTP verification
    path('verify/<str:token>/',v.verify_email, name='verify_email'),  # Old token-based verification
    path('logout/', v.logout_page, name='logout'),
]