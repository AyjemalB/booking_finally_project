from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import Listing
from .serializers import ListingSerializer


class ListingList(ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]


class ListingListView(generics.ListAPIView):
    queryset = Listing.objects.filter(is_active=True)
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Поиск
    search_fields = ['title', 'description']

    #Фильтрация
    filterset_fields = {
        'price': ['gte', 'lte'],             # min/max цена
        'location': ['icontains'],           # город/район
        'rooms': ['gte', 'lte'],             # диапазон комнат
        'housing_type': ['exact'],           # тип жилья
        'created_at': ['gte', 'lte'],        # фильтрация по дате
    }

    #Сортировка
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']  # по умолчанию: новые объявления

# Создание объявления (APIView)
class ListingCreateView(generics.CreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'landlord':
            raise PermissionDenied("Только арендодатель может создавать объявления")
        serializer.save(owner=self.request.user)


# Редактирование объявления
class ListingUpdateView(generics.UpdateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        ad = super().get_object()
        if ad.owner != self.request.user:
            raise PermissionDenied("Вы можете редактировать только свои объявления")
        return ad

# Удаление объявления
class ListingDeleteView(generics.DestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        ad = super().get_object()
        if ad.owner != self.request.user:
            raise PermissionDenied("Вы можете удалять только свои объявления")
        return ad

# Переключение доступности
class ToggleListingStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            ad = Listing.objects.get(pk=pk)
            if ad.owner != request.user:
                raise PermissionDenied("Вы можете менять статус только своих объявлений")
            ad.is_active = not ad.is_active
            ad.save()
            return Response({'status': 'updated', 'is_active': ad.is_active})
        except Listing.DoesNotExist:
            return Response({'error': 'Объявление не найдено'}, status=404)


class ListingDetailView(generics.RetrieveAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def retrieve(self, request, *args, **kwargs):
        listing = self.get_object()
        listing.views_count += 1
        listing.save(update_fields=['views_count'])
        return super().retrieve(request, *args, **kwargs)

class PopularListingView(ListAPIView):
    serializer_class = ListingSerializer

    def get_queryset(self):
        return Listing.objects.annotate(review_count=Count('reviews')).order_by('-review_count')