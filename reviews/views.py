from django.http import HttpResponse
from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer

def index(request):
    return HttpResponse("Отзывы главная страница")


#Добавление отзыва
class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

# Просмотр отзывов по объявлению
class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        ad_id = self.kwargs['ad_id']
        return Review.objects.filter(ad_id=ad_id).order_by('-created_at')

