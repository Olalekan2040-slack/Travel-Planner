from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string

class UserProfile(models.Model):
    """Extended user profile with additional fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    interests = models.TextField(help_text="Comma-separated interests like: food, culture, nature, adventure", blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_interests_list(self):
        """Return interests as a list"""
        if self.interests:
            return [interest.strip() for interest in self.interests.split(',')]
        return []

class EmailVerificationOTP(models.Model):
    """Model to store OTP for email verification"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = self.generate_otp()
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=10)  # 10 minutes expiry
        super().save(*args, **kwargs)
    
    def generate_otp(self):
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))
    
    def is_expired(self):
        """Check if OTP is expired"""
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"OTP for {self.user.username}: {self.otp}"

class PasswordResetRequest(models.Model):
    """Model to handle password reset requests"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(hours=1)  # 1 hour expiry
        super().save(*args, **kwargs)
    
    def generate_token(self):
        """Generate a random token"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    
    def is_expired(self):
        """Check if token is expired"""
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"Password reset for {self.user.username}"
