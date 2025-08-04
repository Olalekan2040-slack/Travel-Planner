from django.contrib import admin
from .models import Destination, TripPlan, ItineraryDay, HotelSuggestion, PointOfInterest

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'country', 'average_daily_cost', 'created_at']
    list_filter = ['country', 'created_at']
    search_fields = ['name', 'city', 'country']
    readonly_fields = ['created_at']

class ItineraryDayInline(admin.TabularInline):
    model = ItineraryDay
    extra = 0
    readonly_fields = ['created_at']

class HotelSuggestionInline(admin.TabularInline):
    model = HotelSuggestion
    extra = 0
    readonly_fields = ['created_at']

class PointOfInterestInline(admin.TabularInline):
    model = PointOfInterest
    extra = 0
    readonly_fields = ['created_at']

@admin.register(TripPlan)
class TripPlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'destination', 'start_date', 'end_date', 'days_count', 'total_budget', 'currency', 'status', 'created_at']
    list_filter = ['status', 'currency', 'created_at', 'start_date']
    search_fields = ['title', 'destination', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'daily_budget']
    inlines = [ItineraryDayInline, HotelSuggestionInline, PointOfInterestInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'destination', 'destination_city', 'destination_country')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'days_count')
        }),
        ('Budget', {
            'fields': ('total_budget', 'currency', 'daily_budget')
        }),
        ('Preferences', {
            'fields': ('interests', 'additional_notes')
        }),
        ('Status', {
            'fields': ('status', 'is_public')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(ItineraryDay)
class ItineraryDayAdmin(admin.ModelAdmin):
    list_display = ['trip', 'day_number', 'date', 'title', 'estimated_cost']
    list_filter = ['date', 'created_at']
    search_fields = ['trip__title', 'title']
    readonly_fields = ['created_at']

@admin.register(HotelSuggestion)
class HotelSuggestionAdmin(admin.ModelAdmin):
    list_display = ['name', 'trip', 'rating', 'price_per_night', 'address']
    list_filter = ['rating', 'created_at']
    search_fields = ['name', 'address', 'trip__title']
    readonly_fields = ['created_at']

@admin.register(PointOfInterest)
class PointOfInterestAdmin(admin.ModelAdmin):
    list_display = ['name', 'trip', 'category', 'rating', 'estimated_cost']
    list_filter = ['category', 'rating', 'created_at']
    search_fields = ['name', 'description', 'trip__title']
    readonly_fields = ['created_at']
