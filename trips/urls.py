from django.urls import path
from . import views

app_name = 'trips'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_trip, name='create'),
    path('<int:trip_id>/', views.trip_detail, name='detail'),
    path('<int:trip_id>/edit/', views.edit_trip, name='edit'),
    path('<int:trip_id>/delete/', views.delete_trip, name='delete'),
    path('<int:trip_id>/pdf/', views.download_pdf, name='download_pdf'),
    path('search-destinations/', views.search_destinations, name='search_destinations'),
]
