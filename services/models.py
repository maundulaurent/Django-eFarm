# services/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Service(models.Model):
    SERVICE_TYPES = [
        ('COACHING', 'Farming Coaching'),
        ('CONSULTATION', 'Consultation'),
        ('WORKSHOP', 'Workshop'),
        ('TOUR', 'Farm Tour'),
    ]
    
    title = models.CharField(max_length=200)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50)  # e.g., "2 hours", "1 day"
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class ServiceBooking(models.Model):
    # customer = models.ForeignKey(User, on_delete=models.CASCADE) #Don't use this, use the custom model
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.service.title} - {self.customer.username}"