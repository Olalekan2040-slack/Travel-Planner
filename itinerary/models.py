from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    interests = models.CharField(max_length=200)
    itinerary_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s trip to {self.destination}"

    class Meta:
        ordering = ['-created_at']
