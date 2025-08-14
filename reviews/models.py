from django.db import models
from django.conf import settings

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()  # от 1 до 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')  # один отзыв на одно объявление

    def __str__(self):
        return f"{self.user.username} → {self.listing.title}: {self.rating}★"

