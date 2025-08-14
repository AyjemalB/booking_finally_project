from django.http import HttpResponse
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Booking
from .serializers import BookingSerializer



# Создание бронирования
class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Просмотр своих бронирований
class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

# Отмена бронирования
class BookingCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        booking = Booking.objects.get(pk=pk, user=request.user)
        if booking.status != 'pending':
            return Response({'error': 'Нельзя отменить подтвержденное или завершенное бронирование.'}, status=400)
        booking.status = 'cancelled'
        booking.save()
        return Response({'status': 'Бронирование отменено'})

# Подтверждение/отклонение арендодателем
class BookingConfirmView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        booking = Booking.objects.get(pk=pk)
        if booking.ad.owner != request.user:
            return Response({'error': 'Вы не владелец этого объявления.'}, status=403)

        action = request.data.get('action')
        if action == 'confirm':
            booking.status = 'confirmed'
        elif action == 'reject':
            booking.status = 'rejected'
        else:
            return Response({'error': 'Неверное действие.'}, status=400)

        booking.save()
        return Response({'status': f'Бронирование {booking.status}'})
