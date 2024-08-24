from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Courts(models.Model):
    court_id = models.AutoField(primary_key=True)
    court_name = models.CharField(max_length=100)
    court_type = models.CharField(max_length=100)
    court_surface = models.CharField(max_length=100)
    image_url = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.court_name} ({self.court_type})"

class Schedule(models.Model):
    HOUR_CHOICES = [(i, f"{i:02d}:00") for i in range(9, 19)]

    schedule_id = models.AutoField(primary_key=True)
    court = models.ForeignKey(Courts, on_delete=models.CASCADE, related_name="schedules")
    time_slot = models.IntegerField(
        choices=HOUR_CHOICES,
        validators=[MinValueValidator(9), MaxValueValidator(18)]
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ['court', 'time_slot']

    def __str__(self):
        return f"{self.court.court_name} - {self.get_time_slot_display()} - {self.price}"

class Booking(models.Model):
    HOUR_CHOICES = [(i, f"{i:02d}:00") for i in range(9, 19)]

    booking_id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.IntegerField(
        choices=HOUR_CHOICES,
        validators=[MinValueValidator(9), MaxValueValidator(18)]
    )
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    booking_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['schedule', 'booking_date', 'booking_time']

    def __str__(self):
        return f"Booking {self.booking_id} - {self.name} {self.surname} - {self.schedule.court.court_name} - {self.booking_date} {self.get_booking_time_display()}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.booking_time != self.schedule.time_slot:
            raise ValidationError("Booking time must match the schedule time slot.")
        if not self.schedule.is_available:
            raise ValidationError("This time slot is not available.")

@receiver(post_save, sender=Booking)
def update_schedule_availability(sender, instance, created, **kwargs):
    if created:
        schedule = instance.schedule
        schedule.is_available = False
        schedule.save()

@receiver(post_delete, sender=Booking)
def restore_schedule_availability(sender, instance, **kwargs):
    schedule = instance.schedule
    schedule.is_available = True
    schedule.save()