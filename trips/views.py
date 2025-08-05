from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from .models import TripPlan, ItineraryDay, HotelSuggestion, PointOfInterest
import requests
import json

@login_required
def dashboard(request):
    """User dashboard showing all trips"""
    trips = TripPlan.objects.filter(user=request.user)
    
    # Statistics
    total_trips = trips.count()
    completed_trips = trips.filter(status='completed').count()
    ongoing_trips = trips.filter(status='ongoing').count()
    planned_trips = trips.filter(status='planned').count()
    
    context = {
        'trips': trips,
        'total_trips': total_trips,
        'completed_trips': completed_trips,
        'ongoing_trips': ongoing_trips,
        'planned_trips': planned_trips,
    }
    
    return render(request, 'trips/dashboard.html', context)

@login_required
def create_trip(request):
    """Create a new trip"""
    if request.method == 'POST':
        # Get form data
        title = request.POST.get('title', '').strip()
        destination = request.POST.get('destination', '').strip()
        departure_location = request.POST.get('departure_location', '').strip()
        departure_latitude = request.POST.get('departure_latitude', '')
        departure_longitude = request.POST.get('departure_longitude', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        total_budget = request.POST.get('total_budget', '')
        currency = request.POST.get('currency', 'USD')
        interests = request.POST.get('interests', '').strip()
        additional_notes = request.POST.get('additional_notes', '').strip()
        
        # Validation
        errors = []
        
        if not title:
            errors.append('Trip title is required')
        if not destination:
            errors.append('Destination is required')
        if not departure_location:
            errors.append('Departure location is required')
        if not start_date:
            errors.append('Start date is required')
        if not end_date:
            errors.append('End date is required')
        if not total_budget:
            errors.append('Total budget is required')
        if not interests:
            errors.append('Please specify your interests')
        
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            if start_date_obj <= timezone.now().date():
                errors.append('Start date must be in the future')
            if end_date_obj <= start_date_obj:
                errors.append('End date must be after start date')
                
            days_count = (end_date_obj - start_date_obj).days + 1
            
        except ValueError:
            errors.append('Invalid date format')
            start_date_obj = end_date_obj = None
            days_count = 0
        
        try:
            total_budget_float = float(total_budget)
            if total_budget_float <= 0:
                errors.append('Budget must be greater than 0')
        except ValueError:
            errors.append('Invalid budget amount')
            total_budget_float = 0
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'trips/create.html', {
                'form_data': request.POST,
                'currencies': TripPlan.BUDGET_CURRENCIES
            })
        
        try:
            # Create trip
            trip = TripPlan.objects.create(
                user=request.user,
                title=title,
                destination=destination,
                departure_location=departure_location,
                departure_latitude=float(departure_latitude) if departure_latitude else None,
                departure_longitude=float(departure_longitude) if departure_longitude else None,
                start_date=start_date_obj,
                end_date=end_date_obj,
                days_count=days_count,
                total_budget=total_budget_float,
                currency=currency,
                interests=interests,
                additional_notes=additional_notes,
                status='draft'
            )
            
            # Get destination coordinates and process departure location
            get_destination_coordinates(trip)
            process_departure_location(trip)
            
            # Calculate flight costs and allocate budget
            trip.allocate_budget()
            
            # Generate itinerary
            generate_itinerary(trip)
            
            # Get hotel suggestions
            get_hotel_suggestions(trip)
            
            messages.success(request, f'Trip "{title}" created successfully!')
            return redirect('trips:detail', trip_id=trip.id)
            
        except Exception as e:
            messages.error(request, f'Failed to create trip: {str(e)}')
            return render(request, 'trips/create.html', {
                'form_data': request.POST,
                'currencies': TripPlan.BUDGET_CURRENCIES
            })
    
    return render(request, 'trips/create.html', {
        'currencies': TripPlan.BUDGET_CURRENCIES
    })

@login_required
def trip_detail(request, trip_id):
    """View trip details"""
    trip = get_object_or_404(TripPlan, id=trip_id, user=request.user)
    
    # Get itinerary days
    itinerary_days = trip.itinerary_days.all().order_by('day_number')
    
    # Get hotel suggestions
    hotels = trip.hotel_suggestions.all()[:5]  # Top 5 hotels
    
    # Get points of interest
    pois = trip.points_of_interest.all()
    
    context = {
        'trip': trip,
        'itinerary_days': itinerary_days,
        'hotels': hotels,
        'pois': pois,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    
    return render(request, 'trips/detail.html', context)

@login_required
def edit_trip(request, trip_id):
    """Edit an existing trip"""
    trip = get_object_or_404(TripPlan, id=trip_id, user=request.user)
    
    if request.method == 'POST':
        # Similar logic to create_trip but updating existing trip
        # Implementation here...
        pass
    
    return render(request, 'trips/edit.html', {
        'trip': trip,
        'currencies': TripPlan.BUDGET_CURRENCIES
    })

@login_required
def delete_trip(request, trip_id):
    """Delete a trip"""
    trip = get_object_or_404(TripPlan, id=trip_id, user=request.user)
    
    if request.method == 'POST':
        trip_title = trip.title
        trip.delete()
        messages.success(request, f'Trip "{trip_title}" deleted successfully!')
        return redirect('trips:dashboard')
    
    return render(request, 'trips/delete_confirm.html', {'trip': trip})

@login_required
def download_pdf(request, trip_id):
    """Download trip itinerary as PDF"""
    trip = get_object_or_404(TripPlan, id=trip_id, user=request.user)
    
    # This is a placeholder - PDF generation will be implemented later
    messages.info(request, 'PDF download feature will be available soon!')
    return redirect('trips:detail', trip_id=trip_id)

def search_destinations(request):
    """AJAX endpoint for destination search"""
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 3:
        return JsonResponse({'results': []})
    
    # This is a placeholder - will implement with Google Places API
    results = [
        {'name': f'{query} City', 'country': 'Sample Country'},
        {'name': f'New {query}', 'country': 'Another Country'},
    ]
    
    return JsonResponse({'results': results})

def get_destination_coordinates(trip):
    """Get coordinates for destination using Google Geocoding API"""
    if not settings.GOOGLE_MAPS_API_KEY:
        return
    
    try:
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {
            'address': trip.destination,
            'key': settings.GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            location = data['results'][0]['geometry']['location']
            trip.latitude = location['lat']
            trip.longitude = location['lng']
            
            # Extract city and country from address components
            for component in data['results'][0]['address_components']:
                types = component['types']
                if 'locality' in types:
                    trip.destination_city = component['long_name']
                elif 'country' in types:
                    trip.destination_country = component['long_name']
            
            trip.save()
            
    except Exception as e:
        print(f"Failed to get coordinates: {e}")

def process_departure_location(trip):
    """Process departure location and get coordinates if not provided"""
    if not trip.departure_latitude or not trip.departure_longitude:
        # Try to geocode departure location if coordinates not provided
        if settings.GOOGLE_MAPS_API_KEY and trip.departure_location:
            try:
                url = 'https://maps.googleapis.com/maps/api/geocode/json'
                params = {
                    'address': trip.departure_location,
                    'key': settings.GOOGLE_MAPS_API_KEY
                }
                
                response = requests.get(url, params=params)
                data = response.json()
                
                if data['status'] == 'OK' and data['results']:
                    location = data['results'][0]['geometry']['location']
                    trip.departure_latitude = location['lat']
                    trip.departure_longitude = location['lng']
                    
                    # Extract city and country from address components
                    for component in data['results'][0]['address_components']:
                        types = component['types']
                        if 'locality' in types:
                            trip.departure_city = component['long_name']
                        elif 'country' in types:
                            trip.departure_country = component['long_name']
                    
                    trip.save()
                    
            except Exception as e:
                print(f"Failed to geocode departure location: {e}")
    else:
        # If coordinates are provided but no city/country, try reverse geocoding
        if settings.GOOGLE_MAPS_API_KEY and not trip.departure_city:
            try:
                url = 'https://maps.googleapis.com/maps/api/geocode/json'
                params = {
                    'latlng': f'{trip.departure_latitude},{trip.departure_longitude}',
                    'key': settings.GOOGLE_MAPS_API_KEY
                }
                
                response = requests.get(url, params=params)
                data = response.json()
                
                if data['status'] == 'OK' and data['results']:
                    # Extract city and country from address components
                    for component in data['results'][0]['address_components']:
                        types = component['types']
                        if 'locality' in types:
                            trip.departure_city = component['long_name']
                        elif 'country' in types:
                            trip.departure_country = component['long_name']
                    
                    trip.save()
                    
            except Exception as e:
                print(f"Failed to reverse geocode departure coordinates: {e}")

def generate_itinerary(trip):
    """Generate daily itinerary for the trip"""
    # Create basic itinerary days
    current_date = trip.start_date
    
    for day_num in range(1, trip.days_count + 1):
        ItineraryDay.objects.create(
            trip=trip,
            day_number=day_num,
            date=current_date,
            title=f"Day {day_num} in {trip.destination_city or trip.destination}",
            activities=json.dumps([
                {
                    'time': '09:00',
                    'activity': 'Breakfast and hotel check-out' if day_num > 1 else 'Arrival and hotel check-in',
                    'location': 'Hotel',
                    'duration': 60,
                    'cost': trip.daily_budget * 0.1
                },
                {
                    'time': '11:00',
                    'activity': 'Explore local attractions',
                    'location': 'City Center',
                    'duration': 180,
                    'cost': trip.daily_budget * 0.4
                },
                {
                    'time': '14:00',
                    'activity': 'Lunch at local restaurant',
                    'location': 'Downtown',
                    'duration': 90,
                    'cost': trip.daily_budget * 0.2
                },
                {
                    'time': '16:00',
                    'activity': 'Afternoon sightseeing',
                    'location': 'Tourist Area',
                    'duration': 120,
                    'cost': trip.daily_budget * 0.2
                },
                {
                    'time': '19:00',
                    'activity': 'Dinner and evening leisure',
                    'location': 'Restaurant District',
                    'duration': 120,
                    'cost': trip.daily_budget * 0.1
                }
            ]),
            estimated_cost=trip.daily_budget
        )
        
        current_date += timedelta(days=1)

def get_hotel_suggestions(trip):
    """Get hotel suggestions using Google Places API"""
    if not settings.GOOGLE_MAPS_API_KEY or not trip.latitude or not trip.longitude:
        # Create sample hotel suggestions
        sample_hotels = [
            {
                'name': f'Grand Hotel {trip.destination_city or trip.destination}',
                'address': f'123 Main Street, {trip.destination}',
                'rating': 4.5,
                'price_per_night': trip.daily_budget * 0.4,
            },
            {
                'name': f'Budget Inn {trip.destination_city or trip.destination}',
                'address': f'456 Budget Ave, {trip.destination}',
                'rating': 3.8,
                'price_per_night': trip.daily_budget * 0.2,
            },
            {
                'name': f'Luxury Resort {trip.destination_city or trip.destination}',
                'address': f'789 Luxury Blvd, {trip.destination}',
                'rating': 4.8,
                'price_per_night': trip.daily_budget * 0.6,
            }
        ]
        
        for hotel_data in sample_hotels:
            HotelSuggestion.objects.create(
                trip=trip,
                **hotel_data
            )
        return
    
    try:
        # Use Google Places API to find hotels
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        params = {
            'location': f'{trip.latitude},{trip.longitude}',
            'radius': '5000',  # 5km radius
            'type': 'lodging',
            'key': settings.GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK':
            for place in data['results'][:10]:  # Top 10 results
                HotelSuggestion.objects.create(
                    trip=trip,
                    name=place['name'],
                    address=place.get('vicinity', ''),
                    rating=place.get('rating'),
                    latitude=place['geometry']['location']['lat'],
                    longitude=place['geometry']['location']['lng'],
                    google_place_id=place['place_id']
                )
                
    except Exception as e:
        print(f"Failed to get hotel suggestions: {e}")
