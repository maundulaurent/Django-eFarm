# livestock/models.py
from django.db import models

class AnimalType(models.Model):
    name = models.CharField(max_length=100)  # Chicken, Goat, Cow, etc.
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Livestock(models.Model):
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE)
    breed = models.CharField(max_length=100)
    tag_number = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    status = models.CharField(max_length=20, choices=[
        ('HEALTHY', 'Healthy'),
        ('SICK', 'Sick'),
        ('SOLD', 'Sold'),
        ('DECEASED', 'Deceased'),
    ], default='HEALTHY')
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to='livestock/', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.breed} - {self.tag_number}"