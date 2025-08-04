from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, EmailVerificationOTP, PasswordResetRequest

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Unregister the original User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'nationality', 'is_email_verified', 'created_at']
    list_filter = ['is_email_verified', 'nationality', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(EmailVerificationOTP)
class EmailVerificationOTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__username', 'user__email', 'otp']
    readonly_fields = ['created_at']

@admin.register(PasswordResetRequest)
class PasswordResetRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'token']
