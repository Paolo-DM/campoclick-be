from rest_framework import serializers
from .models import Courts, Schedule, Booking

# Il serializer permette di convertire i dati dei modelli in formato JSON


# Serializer per il modello Courts
class CourtsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courts
        fields = "__all__"  # Indica che il serializer deve includere tutti i campi del modello Courts


# Serializer per il modello Schedule
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"


# Serializer per il modello Bookings
class BookingSerializer(serializers.ModelSerializer):
    court_name = serializers.CharField(source='schedule.court.court_name', read_only=True)
    court_type = serializers.CharField(source='schedule.court.court_type', read_only=True)
    court_image_url = serializers.URLField(source='schedule.court.image_url', read_only=True)
    booking_time = serializers.CharField(source='schedule.time_slot', read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"