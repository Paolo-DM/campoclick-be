from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError
from .models import Courts, Schedule, Booking
from .serializer import (
    CourtsSerializer,
    ScheduleSerializer,
    BookingSerializer,
)


# ********** CAMPI SPORTIVI **********


# Recupera tutti i campi sportivi
@api_view(["GET"])
def get_courts(request):
    # Se viene passato un parametro sport (es: "/courts?sport=tennis"), filtra i campi sportivi per court_type
    sport = request.query_params.get("sport", None)
    if sport:
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

    # Recupera i dettagli di un campo sportivo
    if request.method == "GET":
        serializer = CourtsSerializer(court)
        return Response(serializer.data)

    # Aggiorna i dettagli di un campo sportivo
    elif request.method == "PUT":
        serializer = CourtsSerializer(court, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Cancella un campo sportivo
    elif request.method == "DELETE":
        court.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ********** ORARI **********


@api_view(["GET"])
def get_schedules(request):
    court_id = request.query_params.get("court_id", None)
    date = request.query_params.get("date", None)

    schedules = Schedule.objects.all()

    # Filtra le schedules per court_id se specificato
    if court_id:
        schedules = schedules.filter(court_id=court_id)

    if date:
        # Filtra le schedules disponibili per la data specificata
        schedules = [schedule for schedule in schedules if schedule.is_available(date)]

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
        schedule = Schedule.objects.get(pk=pk)  # Recupera una schedule specifica
    except Schedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Recupera i dettagli di una schedule
    if request.method == "GET":
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data)

    # Aggiorna i dettagli di una schedule
    elif request.method == "PUT":
        serializer = ScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Cancella una schedule
    elif request.method == "DELETE":
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ********** PRENOTAZIONI **********


@api_view(["GET"])
def get_bookings(request):
    # Recupera tutte le prenotazioni
    bookings = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny]) # Permette anche a chi non è autenticato di creare una prenotazione
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

    # Recupera i dettagli di una prenotazione
    if request.method == "GET":
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    # Aggiorna i dettagli di una prenotazione
    elif request.method == "PUT":
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Cancella una prenotazione
    elif request.method == "DELETE":
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
