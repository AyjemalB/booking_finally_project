from django.urls import path
from . views import BookingListView, BookingCreateView

urlpatterns = [
    path('bookings/', BookingListView.as_view(), name='booking-list-api'), # Это вернет JSON
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create-api'),
]