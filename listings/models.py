from django.db import models
from users.models import User
from django.core.exceptions import ValidationError

class Listing(models.Model):
    HOUSING_TYPES = [
    ('apartment', 'Apartment'),
    ('house', 'House'),
    ('studio', 'Studio'),
    ('villa', 'Villa'),
    ('other', 'Other'),
]
    title = models.CharField(max_length=255)                     # Заголовок
    description = models.TextField()                             # Описание
    location = models.CharField(max_length=255)                  # Местоположение
    price = models.DecimalField(max_digits=10, decimal_places=2) # Цена
    rooms = models.PositiveIntegerField()                        # Количество комнат
    housing_type = models.CharField(max_length=20, choices=HOUSING_TYPES)  # Тип жилья
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')    # Владелец
    created_at = models.DateTimeField(auto_now_add=True)         # Дата создания
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)

    def clean(self):
        """
            Метод для валидации полей модели.
            Проверяет, что цена и количество комнат больше нуля.
            Вызывается перед сохранением модели.
        """
        super().clean()
        if self.price is not None and self.price <= 0:
            raise ValidationError({'price': 'Price must be greater than zero.'})
        if self.rooms is not None and self.rooms <= 0:
            raise ValidationError({'rooms': 'Number of rooms must be greater than zero.'})

    def __str__(self):
        return f"{self.title} in {self.location} ({self.price}€)"
