from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
import os
import re
import google.generativeai as genai
from datetime import datetime, timedelta
import logging
from django.conf import settings
import json
from .models import Itinerary

# Create your views here.

# Configure the Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

logger = logging.getLogger(__name__)

@login_required
def home(request):
    itinerary = None
    if request.method == 'POST':
        destination = request.POST.get('destination')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        budget = request.POST.get('budget')
        interests = request.POST.getlist('interests')

        prompt = f"Create a detailed day-by-day travel itinerary for a trip to {destination} from {start_date} to {end_date} with a budget of {budget}. Include activities related to: {', '.join(interests)}. Format each day as 'Day X:' followed by a list of activities."

        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            raw_itinerary = response.text

            # Process the itinerary
            days = re.split(r'Day \d+:', raw_itinerary)[1:]  # Split by 'Day X:' and remove the first empty element
            processed_itinerary = []
            for i, day in enumerate(days, 1):
                activities = [activity.strip() for activity in day.strip().split('\n') if activity.strip()]
                processed_itinerary.append({
                    'day': i,
                    'activities': activities
                })

            itinerary = processed_itinerary
        except Exception as e:
            itinerary = [{'day': 'Error', 'activities': [str(e)]}]

        # Save the itinerary
        Itinerary.objects.create(
            user=request.user,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            interests=', '.join(interests),
            itinerary_data=json.dumps(itinerary)  # Ensure it's JSON serialized
        )

        return render(request, 'itinerary/home.html', {'itinerary': itinerary})
    return render(request, 'itinerary/home.html')

@login_required
def dashboard(request):
    user_itineraries = Itinerary.objects.filter(user=request.user)
    for itinerary in user_itineraries:
        try:
            itinerary.itinerary_data = json.loads(itinerary.itinerary_data)
        except json.JSONDecodeError:
            itinerary.itinerary_data = []  # Set to empty list if JSON is invalid
    return render(request, 'itinerary/dashboard.html', {'itineraries': user_itineraries})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})
