# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('FARMER', 'Farmer'),
        ('CUSTOMER', 'Customer'),
        ('VISITOR', 'Visitor'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='VISITOR')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"
    
    class Meta:
        # This helps avoid clashes with the default User model
        swappable = 'AUTH_USER_MODEL'
