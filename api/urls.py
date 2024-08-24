from django.urls import path
from .views import (
    get_courts,
    create_court,
    court_detail,
    get_schedules,
    create_schedule,
    schedule_detail,
    get_bookings,
    create_booking,
    booking_detail,
)

urlpatterns = [
    # URL per i campi sportivi
    path("courts/", get_courts, name="get_courts"),
    path("courts/create/", create_court, name="create_court"),
    path("courts/<str:pk>/", court_detail, name="court_detail"),
    # URL per gli orari
    path("schedules/", get_schedules, name="get_schedules"),
    path("schedules/create/", create_schedule, name="create_schedule"),
    path("schedules/<str:pk>/", schedule_detail, name="schedule_detail"),
    # URL per le prenotazioni
    path("bookings/", get_bookings, name="get_bookings"),
    path("bookings/create/", create_booking, name="create_booking"),
    path("bookings/<str:pk>/", booking_detail, name="booking_detail"),
]
