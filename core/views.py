from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from trips.models import TripPlan

def home(request):
    """Home page view"""
    context = {
        'user_trip_count': 0,
        'recent_trips': []
    }
    
    if request.user.is_authenticated:
        user_trips = TripPlan.objects.filter(user=request.user)
        context['user_trip_count'] = user_trips.count()
        context['recent_trips'] = user_trips[:3]  # Last 3 trips
    
    return render(request, 'core/home.html', context)

def about(request):
    """About page view"""
    return render(request, 'core/about.html')
