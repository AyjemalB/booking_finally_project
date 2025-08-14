from django.db import models
from django.conf import settings

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Ожидает подтверждения'),
            ('confirmed', 'Подтверждено'),
            ('cancelled', 'Отменено'),
            ('rejected', 'Отклонено'),
            ('completed', 'Завершено'),
        ],
        default='pending'
    )

    def __str__(self):
        return f"{self.user.username} → {self.listing.title} ({self.start_date} - {self.end_date})"
