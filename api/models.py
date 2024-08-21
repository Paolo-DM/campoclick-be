from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Courts(models.Model):
    # Modello per rappresentare i campi sportivi
    court_id = models.AutoField(primary_key=True)  # ID univoco per ogni campo
    court_name = models.CharField(max_length=100)  # Nome del campo
    court_type = models.CharField(max_length=100)  # Tipo di campo (es. tennis, basket)
    image_url = models.URLField(
        max_length=255, blank=True, null=True
    )  # URL dell'immagine del campo, opzionale

    def __str__(self):
        return f"{self.court_name} ({self.court_type})"


class Schedule(models.Model):
    # Modello per gestire gli orari disponibili per ogni campo
    HOUR_CHOICES = [
        (i, f"{i:02d}:00") for i in range(9, 19)
    ]  # Opzioni per le ore, dalle 9:00 alle 18:00

    schedule_id = models.AutoField(
        primary_key=True
    )  # ID univoco per ogni fascia oraria
    court = models.ForeignKey(
        "Courts", on_delete=models.CASCADE, related_name="schedules"
    )  # Relazione con il campo
    day = models.DateField()  # Giorno della prenotazione
    start_time = models.IntegerField(
        choices=HOUR_CHOICES, validators=[MinValueValidator(9), MaxValueValidator(18)]
    )  # Ora di inizio
    price = models.DecimalField(
        max_digits=6, decimal_places=2
    )  # Prezzo per questa fascia oraria
    is_available = models.BooleanField(
        default=True
    )  # Indica se la fascia oraria è disponibile

    class Meta:
        unique_together = [
            "court",
            "day",
            "start_time",
        ]  # Assicura che non ci siano duplicati

    def __str__(self):
        return f"{self.court.court_name} - {self.day} {self.get_start_time_display()}"


class Booking(models.Model):
    # Modello per gestire le prenotazioni
    booking_id = models.AutoField(primary_key=True)  # ID univoco per ogni prenotazione
    schedule = models.OneToOneField(
        Schedule, on_delete=models.CASCADE
    )  # Relazione uno a uno con Schedule
    name = models.CharField(max_length=100)  # Nome del cliente
    surname = models.CharField(max_length=100)  # Cognome del cliente
    email = models.EmailField()  # Email del cliente
    phone = models.CharField(max_length=20)  # Numero di telefono del cliente
    booking_datetime = models.DateTimeField(
        auto_now_add=True
    )  # Data e ora della prenotazione

    def __str__(self):
        return (
            f"Booking {self.booking_id} - {self.name} {self.surname} - {self.schedule}"
        )

    def save(self, *args, **kwargs):
        # Sovrascrive il metodo save per aggiornare lo stato di disponibilità dello Schedule
        super().save(*args, **kwargs)
        self.schedule.is_available = False  # Imposta lo Schedule come non disponibile
        self.schedule.save()  # Salva le modifiche allo Schedule
