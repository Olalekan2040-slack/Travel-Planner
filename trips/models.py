from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class Destination(models.Model):
    """Pre-populated destinations for better performance"""
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    description = models.TextField(blank=True)
    popular_attractions = models.TextField(help_text="JSON list of popular attractions", blank=True)
    average_daily_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    best_time_to_visit = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name}, {self.country}"
    
    def get_popular_attractions(self):
        """Return popular attractions as a list"""
        if self.popular_attractions:
            try:
                return json.loads(self.popular_attractions)
            except json.JSONDecodeError:
                return []
        return []

class TripPlan(models.Model):
    """Main trip plan model"""
    BUDGET_CURRENCIES = [
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
        ('NGN', 'Nigerian Naira (₦)'),
        ('INR', 'Indian Rupee (₹)'),
        ('CAD', 'Canadian Dollar (C$)'),
        ('AUD', 'Australian Dollar (A$)'),
    ]
    
    TRIP_STATUS = [
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    destination_country = models.CharField(max_length=100, blank=True)
    destination_city = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    start_date = models.DateField()
    end_date = models.DateField()
    days_count = models.IntegerField()
    
    total_budget = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=BUDGET_CURRENCIES, default='USD')
    daily_budget = models.DecimalField(max_digits=10, decimal_places=2)
    
    interests = models.TextField(help_text="Comma-separated interests")
    additional_notes = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=TRIP_STATUS, default='draft')
    is_public = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.destination}"
    
    def get_interests_list(self):
        """Return interests as a list"""
        if self.interests:
            return [interest.strip() for interest in self.interests.split(',')]
        return []
    
    def save(self, *args, **kwargs):
        if self.total_budget and self.days_count:
            self.daily_budget = self.total_budget / self.days_count
        super().save(*args, **kwargs)

class ItineraryDay(models.Model):
    """Daily itinerary for each trip"""
    trip = models.ForeignKey(TripPlan, on_delete=models.CASCADE, related_name='itinerary_days')
    day_number = models.IntegerField()
    date = models.DateField()
    title = models.CharField(max_length=200, default="Day {day_number}")
    activities = models.TextField(help_text="JSON list of activities for the day")
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['day_number']
        unique_together = ['trip', 'day_number']
    
    def __str__(self):
        return f"{self.trip.title} - Day {self.day_number}"
    
    def get_activities(self):
        """Return activities as a list"""
        if self.activities:
            try:
                return json.loads(self.activities)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_activities(self, activities_list):
        """Set activities from a list"""
        self.activities = json.dumps(activities_list)

class HotelSuggestion(models.Model):
    """Hotel suggestions for trips"""
    trip = models.ForeignKey(TripPlan, on_delete=models.CASCADE, related_name='hotel_suggestions')
    name = models.CharField(max_length=200)
    address = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    google_place_id = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    amenities = models.TextField(help_text="JSON list of amenities", blank=True)
    photos = models.TextField(help_text="JSON list of photo references", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-rating', 'price_per_night']
    
    def __str__(self):
        return f"{self.name} - {self.trip.destination}"
    
    def get_amenities(self):
        """Return amenities as a list"""
        if self.amenities:
            try:
                return json.loads(self.amenities)
            except json.JSONDecodeError:
                return []
        return []
    
    def get_photos(self):
        """Return photo references as a list"""
        if self.photos:
            try:
                return json.loads(self.photos)
            except json.JSONDecodeError:
                return []
        return []

class PointOfInterest(models.Model):
    """Points of Interest for trips"""
    CATEGORY_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('tourist_attraction', 'Tourist Attraction'),
        ('museum', 'Museum'),
        ('park', 'Park'),
        ('shopping', 'Shopping'),
        ('entertainment', 'Entertainment'),
        ('nightlife', 'Nightlife'),
        ('cultural', 'Cultural Site'),
        ('adventure', 'Adventure Activity'),
        ('religious', 'Religious Site'),
        ('historical', 'Historical Site'),
        ('nature', 'Nature'),
        ('other', 'Other'),
    ]
    
    trip = models.ForeignKey(TripPlan, on_delete=models.CASCADE, related_name='points_of_interest')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    address = models.TextField()
    description = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    google_place_id = models.CharField(max_length=200, blank=True)
    opening_hours = models.TextField(help_text="JSON format opening hours", blank=True)
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    photos = models.TextField(help_text="JSON list of photo references", blank=True)
    recommended_duration = models.IntegerField(help_text="Recommended visit duration in minutes", null=True, blank=True)
    assigned_day = models.ForeignKey(ItineraryDay, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-rating', 'estimated_cost']
    
    def __str__(self):
        return f"{self.name} - {self.category}"
    
    def get_opening_hours(self):
        """Return opening hours as a dict"""
        if self.opening_hours:
            try:
                return json.loads(self.opening_hours)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def get_photos(self):
        """Return photo references as a list"""
        if self.photos:
            try:
                return json.loads(self.photos)
            except json.JSONDecodeError:
                return []
        return []
