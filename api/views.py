from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import Courts, Schedule, Booking
from .serializer import (
    CourtsSerializer,
    ScheduleSerializer,
    BookingSerializer,
)
from django.core.management.base import BaseCommand
from decimal import Decimal

def populate_schedules():
    courts = Courts.objects.all()
    
    for court in courts:
        for hour in range(9, 19):  # 9 AM to 6 PM
            price = Decimal('20.00')  # Base price
            
            # Adjust price for peak hours (11 AM to 2 PM)
            if 11 <= hour <= 14:
                price = Decimal('25.00')
            
            Schedule.objects.get_or_create(
                court=court,
                time_slot=hour,
                defaults={'price': price, 'is_available': True}
            )
    
    print("Schedules populated successfully!")

# Endpoint per i campi sportivi


# Recupera tutti i campi sportivi
@api_view(["GET"])
def get_courts(request):
    # Se viene passato un parametro sport (es: "/courts?sport=tennis"), filtra i campi sportivi per court_type
    sport = request.query_params.get("sport", None)
    if sport:
        print("SPORT if", sport)
        courts = Courts.objects.filter(
            court_type__iexact=sport
        )  # __iexact per non distinguere tra maiuscole e minuscole
    else:
        courts = Courts.objects.all()
    serializer = CourtsSerializer(courts, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_court(request):
    # Crea un nuovo campo sportivo
    serializer = CourtsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def court_detail(request, pk):
    # Gestisce le operazioni di dettaglio per un singolo campo sportivo
    try:
        court = Courts.objects.get(pk=pk)
    except Courts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = CourtsSerializer(court)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CourtsSerializer(court, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        court.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Endpoint per gli orari


@api_view(["GET"])
def get_schedules(request):
    # Recupera tutti gli orari
    court_id = request.query_params.get("court_id", None)
    if court_id:
        schedules = Schedule.objects.filter(court_id=court_id)
    else:
        schedules = Schedule.objects.all()
    serializer = ScheduleSerializer(schedules, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_schedule(request):
    # Crea un nuovo orario
    serializer = ScheduleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def schedule_detail(request, pk):
    # Gestisce le operazioni di dettaglio per un singolo orario
    try:
        schedule = Schedule.objects.get(pk=pk)
    except Schedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Endpoint per le prenotazioni


@api_view(["GET"])
def get_bookings(request):
    # Recupera tutte le prenotazioni
    bookings = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_booking(request):
    # Crea una nuova prenotazione
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def booking_detail(request, pk):
    # Gestisce le operazioni di dettaglio per una singola prenotazione
    try:
        booking = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
