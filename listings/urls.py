from django.urls import path
from .views import ListingListView, ListingCreateView, ListingUpdateView, ListingDeleteView, ToggleListingStatusView, ListingDetailView, PopularListingView, ListingList


urlpatterns = [
    path('', ListingListView.as_view(), name='listing-list'), # с фильтрацией
    path('all/', ListingList.as_view(), name='listing-all'),  # все объявления
    path('create/', ListingCreateView.as_view(), name='listing-create'),
    path('<int:pk>/edit/', ListingUpdateView.as_view(), name='listing-edit'),
    path('<int:pk>/delete/', ListingDeleteView.as_view(), name='listing-delete'),
    path('<int:pk>/toggle/', ToggleListingStatusView.as_view(), name='listing-toggle'),
    path('<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),
    path('popular/', PopularListingView.as_view(), name='popular-ads'),
]

