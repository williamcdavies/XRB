from django.urls import path
from .views import send_otp, verify_otp, register_with_otp

urlpatterns = [
    path('register/', register_with_otp, name='otp-register'),
    path('send/', send_otp, name='otp-send'),
    path('verify/', verify_otp, name='otp-verify'),
]