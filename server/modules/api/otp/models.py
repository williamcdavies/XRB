from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
import string

class OTP(models.Model):
    class Meta:
        db_table = 'otp_codes'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    @staticmethod
    def generate_otp():
        return ''.join(random.choices(string.digits, k=6))
    
    def is_valid(self):
        expiry_time = self.created_at + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        return timezone.now() < expiry_time and not self.is_verified
    
    @classmethod
    def create_otp(cls, user):
        # invalidate all previous OTPs for this user
        cls.objects.filter(user=user, is_verified=False).update(is_verified=True)
        
        # create new OTP
        code = cls.generate_otp()
        otp = cls.objects.create(user=user, code=code)
        return otp
        
    def __str__(self):
        return f"{self.user.email} - {self.code}"