from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import uuid  # Importa il modulo uuid per generare ID univoci


# Modello per i campi da gioco
class Courts(models.Model):
    court_id = models.AutoField(primary_key=True)
    court_name = models.CharField(max_length=100)
    court_type = models.CharField(max_length=100)
    court_surface = models.CharField(max_length=100)
    image_url = models.URLField(max_length=255, blank=True, null=True)
    image_credit = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.court_name} ({self.court_type})"


# Modello per gli orari e i prezzi dei campi
class Schedule(models.Model):
    # Definisce le opzioni per gli orari dalle 9:00 alle 18:00
    HOUR_CHOICES = [(i, f"{i:02d}:00") for i in range(9, 19)]

    schedule_id = models.AutoField(primary_key=True)
    court = models.ForeignKey(
        Courts, on_delete=models.CASCADE, related_name="schedules"
    )
    time_slot = models.IntegerField(
        choices=HOUR_CHOICES, validators=[MinValueValidator(9), MaxValueValidator(18)]
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # is_available = models.BooleanField(default=True)

    class Meta:
        # Assicura che non ci siano duplicati di campo e orario
        unique_together = ["court", "time_slot"]

    def __str__(self):
        return f"{self.court.court_name} - {self.get_time_slot_display()} - {self.price}"

    def is_available(self, date):
        return not self.bookings.filter(booking_date=date).exists()


# Modello per le prenotazioni
class Booking(models.Model):
    # Usa UUID come chiave primaria per maggiore sicurezza e unicità
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="bookings") # Relazione con il modello Schedule
    booking_date = models.DateField()
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    booking_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Assicura che non ci siano prenotazioni duplicate per lo stesso campo, data e ora
        unique_together = ["schedule", "booking_date"]

    def __str__(self):
        return f"Booking {self.booking_id.hex[:8]} - {self.name} {self.surname} - {self.schedule.court.court_name} - {self.booking_date} {self.schedule.get_time_slot_display()}"

    def clean(self):
        from django.core.exceptions import ValidationError

        # Verifica se lo slot orario è disponibile per la data selezionata
        if not self.schedule.is_available(self.booking_date): 
            raise ValidationError("Questo slot orario non è disponibile per la data selezionata.")

